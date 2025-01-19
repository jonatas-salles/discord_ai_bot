# Discord AI BOT

```
This project is a simple Discord bot that interacts with Groq's API to provide AI-based responses to user queries. The bot is configured to run as an AWS Lambda function, allowing for serverless operation. It listens to interactions from Discord, verifies the request signature, handles different types of commands (like echo and ask), and uses Groq to generate responses for the ask command.
```

## Prerequisites
```
Python 3.x

Required Python packages:

groq - The Groq API client
requests - To make HTTP requests to Discord's API
python-dotenv - For loading environment variables from .env
pynacl - For signature verification
```

## Installation
```
Clone the repository or download the code files.

Install the required packages:

pip install -r requirements.txt

Create a .env file in the root directory with the following content:

PUBLIC_KEY=<your_public_key>
APPLICATION_ID=<your_application_id>
GROQ_API_KEY=<your_groq_api_key>
LLM_MODEL=<your_llm_model>
Replace the placeholders with your actual values.

Environment Variables
PUBLIC_KEY: The public key used for verifying the request signature from Discord.
APPLICATION_ID: Your Discord application's ID.
GROQ_API_KEY: Your API key for accessing Groq.
LLM_MODEL: The model to use in the Groq API for chat completions.
```