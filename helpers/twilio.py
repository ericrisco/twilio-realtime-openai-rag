
import os
from fastapi.responses import Response

def twilio_stream(host: str):
    response = f"""
    <Response> 
        <Connect>
            <Stream url="wss://{host}/stream/websocket" />
        </Connect>
    </Response>
    """
    return Response(content=response, media_type="application/xml")