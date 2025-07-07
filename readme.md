# Twilio Real-time OpenAI Voice Assistant

## 🚀 Build a Real-time Voice Assistant with Twilio and OpenAI

This repository showcases how to easily create a **real-time voice assistant** using **Twilio** and **OpenAI**. Whether you're new to AI voice assistants or looking for a scalable solution, this project will guide you through every step.

The assistant leverages OpenAI's **Retrieval-Augmented Generation (RAG)** and integrates with **Twilio** for seamless voice communication.

![Real-time OpenAI Architecture](images/realtime_openai.png)

## ✨ Features

- **Real-time Voice Interaction**: Talk to your assistant and get instant, AI-generated responses.
- **Easy Integration**: Quickly connect Twilio with OpenAI's Realtime API.
- **Scalable**: Use this project as a base to create more sophisticated assistants.
- **Customizable**: Tweak responses, voice prompts, and more to suit your needs.
- **JSON-based Database**: Simulate orders, product inventories, and shipping statuses with a simple JSON database.
- **Dummy Functions**: This version connects to dummy functions, designed for simulation and testing. You are encouraged to modify and extend these functions to connect them to your actual services or documentation. This flexibility allows you to integrate real-world systems like order management, inventory checks, and shipping status updates.

## 💬 What is the OpenAI Realtime API?

The **Realtime API** enables you to build low-latency, multi-modal conversational experiences. It supports both text and audio as input and output, while also enabling tool calling, making it versatile for real-time, interactive applications.

### Key Benefits of the Realtime API

- **Native speech-to-speech**: The API operates without text as an intermediary, reducing latency and delivering more nuanced, natural output.
- **Natural, steerable voices**: The models can produce natural inflections, including features like **laughing and whispering**, while adhering to specific tonal directions.
- **Simultaneous multimodal output**: While text can be useful for moderation or logging, the audio is faster-than-realtime, ensuring stable playback.
  
This API is **websocket-based**, marking the first time OpenAI has published an API capable of sending and receiving audio in real time. It's designed to provide developers with a seamless way to build conversational applications that require instant responses.

### Important Considerations

- **Beta Stage**: The Realtime API is currently in beta and does not offer client-side authentication. For security, audio must be **relayed to a server to authenticate securely**.
- **Network Sensitivity**: Real-time audio experiences can be affected by network conditions, especially when delivering audio reliably to a server. This makes production-scale use challenging in client-side or telephony applications where network conditions may vary.
  
For production use, especially in environments where network reliability is unpredictable, it is recommended to evaluate purpose-built third-party solutions or integrate with trusted partners, as listed by OpenAI.

## 🛠️ Project Structure

- **`dummy_db/`**: Contains JSON files simulating a database of orders, products, and shipping statuses.
- **`helpers/`**: Utility functions for reading files, handling Twilio interactions, and voice prompts.
- **`routers/`**: API routes for the app, such as streaming voice responses.
- **`services/`**: Contains the OpenAI interaction logic.
- **`tools/`**: Specific tools for checking stock, shipping status, and more.
- **`.env`**: Store your environment variables (API keys, secrets, etc.).
- **`app.py`**: The main application file.
- **`requirements.txt`**: Project dependencies.

## 📋 Prerequisites

Before you begin, ensure you have the following:

1. A **Twilio account** (Sign up [here](https://www.twilio.com/login)).
2. An **OpenAI API key** (Get it [here](https://platform.openai.com/)).
3. Python 3.x installed on your machine.
4. Set up a virtual environment for the project.

### Setting up Twilio

1. **Create a Twilio Phone Number**:
   - Log into your Twilio account.
   - Navigate to **Phone Numbers** from the console dashboard.
   - Click on **Buy a Number** and choose a number with voice capabilities.
   - Once purchased, configure this number to route incoming calls to your application.

2. **Modify the Webhook Endpoint**:
   - Go to the **Phone Numbers** section in your Twilio console.
   - Select the number you just purchased.
   - Scroll down to the **Voice & Fax** section.
   - In the **A Call Comes In** field, set the Webhook URL to the endpoint that connects to your service. For example: https://your-domain.com/stream/incoming-call
   - This URL should point to your FastAPI application, specifically the `/stream/incoming-call` route that will handle the incoming Twilio calls.

    ![Real-time OpenAI Architecture](images/webhook_config.png)


### Running Locally

If you want to run the service locally, you will need to create a public endpoint using port forwarding. Here’s how you can do this in **Visual Studio**:

1. Set up the port forwarding in Visual Studio:
   - Open your project in **Visual Studio**.
   - Go to **Project > Properties > Debug**.
   - In the **Web Server Settings**, make sure the **App URL** is set to the port defined in your `.env` file (default is 5000).

2. Create a public port forward:
   - To make your local FastAPI service publicly accessible, you'll need to use a tool like **ngrok** or Visual Studio's **Port Forwarding** feature.
   - You can follow this guide on Youtube to achieve this: [Visual Studio Port Forwarding](https://www.youtube.com/watch?v=FujS16J74Gk).

3. Example `.env` configuration for local development

```bash
VOICE = 'echo'
OPENAI_API_KEY = 'your_openai_key'
PORT=5000
```


## 🛠️ Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/ericrisco/twilio-realtime-openai-rag
   cd repo-name
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your API keys:

   ```bash
    VOICE = 'echo'
    OPENAI_API_KEY = 'your_openai_key'
    PORT=5000
   ```

4. Run the app:

   ```bash
   python app.py
   ```

## 🔧 Usage

1. **Twilio Voice Setup**: To connect your Twilio account to this project:
   - Create a Twilio phone number.
   - Configure the webhook to point to your app's `/stream/incoming-call` route.
   - Set up a Twilio **TwiML** app to handle incoming voice calls.

2. **Making a Call**: Call your Twilio number, and the voice assistant will interact with you using OpenAI's AI model, responding in real-time.

3. **Sample Commands**: You can ask questions like:
   - "What's the status of my order?"
   - "Do you have this Whey Protein in stock?"

## 📂 API Documentation

### Endpoints

| Endpoint               | Description                                        | Method |
| ---------------------- | -------------------------------------------------- | ------ |
| `/stream/incoming-call` | Handles incoming calls from Twilio                 | GET/POST |
| `/stream/websocket`     | Establishes a WebSocket connection for streaming   | WebSocket |

## 🧩 Key Components

### 1. `app.py`

The main entry point for the FastAPI application, handling the configuration of routers and loading environment variables. It utilizes **Uvicorn** to serve the app on a specified port.

### 2. `stream.py`

Handles incoming calls and WebSocket connections for real-time media streaming between Twilio and OpenAI. The connection to OpenAI is established via WebSocket for real-time processing.

### 3. Helpers

- **`read_json_file.py`**: Reads JSON files asynchronously from the `dummy_db` folder to simulate databases.
- **`twilio.py`**: Manages the response for Twilio, directing it to connect via WebSocket to the OpenAI model.
- **`voice_system_prompt.py`**: Contains the system prompt for OpenAI, defining the persona and role of the assistant (in this case, a friendly assistant named "CBum" working at MuscleBoost).

### 4. Services

- **`openai_functions.py`**: Handles interactions with OpenAI, including generating a welcome message, updating the session with the assistant's configuration, and sending responses in audio format.

### 5. Tools

- **`execute_tool.py`**: Maps and executes the appropriate tool based on the user's request, such as searching for a product or checking an order's shipping status.
- **`process_order_tool.py`**: Processes the status of a given order by ID.
- **`search_product_tool.py`**: Searches for a product by name in the simulated product catalog.
- **`check_shipping_status_tool.py`**: Checks the shipping status of an order based on a tracking number.
- **`check_stock_tool.py`**: Verifies the stock availability of a specific product in the catalog.

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
