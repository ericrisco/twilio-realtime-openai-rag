import asyncio
import json
import logging
import os
import traceback

import aiohttp
from dotenv import load_dotenv
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect

from helpers.twilio import twilio_stream
from helpers.voice_system_prompt import SYSTEM_MESSAGE
from services.openai_functions import (generate_audio_response,
                                       send_session_update, welcome_message)
from tools.execute_tool import execute_tool

stream_router = APIRouter()

load_dotenv()
VOICE = os.getenv("VOICE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@stream_router.api_route("/stream/incoming-call", methods=["GET", "POST"])
async def handle_incoming_call(request: Request):
    logging.info("Stream Incoming call received.")
    host = request.url.hostname
    return twilio_stream(host)

@stream_router.websocket("/stream/websocket")
async def handle_media_stream(twilio_websocket: WebSocket):
    logging.info("Stream WebSocket connection established.")
    await twilio_websocket.accept()

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(
            'wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01',
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "OpenAI-Beta": "realtime=v1"
            }
        ) as openai_ws:

            stream_sid = None

            async def receive_from_twilio():
                nonlocal stream_sid
                try:
                    async for message in twilio_websocket.iter_text():
                        data = json.loads(message)
                        if data['event'] == 'media' and not openai_ws.closed:
                            audio_append = {
                                "type": "input_audio_buffer.append",
                                "audio": data['media']['payload']
                            }
                            await openai_ws.send_json(audio_append)
                        elif data['event'] == 'start':
                            stream_sid = data['start']['streamSid']
                except WebSocketDisconnect:
                    if not openai_ws.closed:
                        await openai_ws.close()

            async def send_to_twilio():
                nonlocal stream_sid
                try:
                    async for openai_message in openai_ws:
                        response = json.loads(openai_message.data)

                        if response['type'] == 'session.created':
                            logging.info(f"OpenAI WSS connection established. => {stream_sid}")
                            await send_session_update(openai_ws, VOICE, SYSTEM_MESSAGE)

                        if response['type'] == 'session.updated': 
                            logging.info(f"OpenAI WSS connection updated. => {stream_sid}: {response}")                       
                            await welcome_message(openai_ws)                            

                        if response['type'] == 'response.function_call_arguments.done':
                            """
                            The LLM has finished providing all the necessary arguments for the requested function call.
                            The application can now proceed to execute the specified function using the provided arguments.
                            """
                            logging.debug(f"Function call arguments received. => {stream_sid}: {response}")
                            result = await execute_tool(response)
                            await generate_audio_response(stream_sid, openai_ws, result['result'])

                        if response['type'] == 'response.audio.delta' and response.get('delta'):
                            audio_delta = {
                                "event": "media",
                                "streamSid": stream_sid,
                                "media": {
                                    "payload": response['delta']
                                }
                            }
                            await twilio_websocket.send_json(audio_delta)

                except Exception as e:
                    logging.error(f"Error in send_to_twilio: {stream_sid} {e} - {traceback.format_exc()}")

            await asyncio.gather(receive_from_twilio(), send_to_twilio())