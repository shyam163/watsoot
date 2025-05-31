# WhatsApp ChatBot with OpenAI Assistant

A WhatsApp chatbot that integrates with OpenAI Assistant API to provide intelligent responses to customer queries. The bot saves chat histories for each phone number and is designed to be deployed on Oracle Cloud at hexawhite.quantumautomata.in.

## Features

- 🤖 **OpenAI Assistant Integration**: Uses your custom OpenAI assistant for intelligent responses
- 💬 **WhatsApp Business API**: Receives and sends messages via WhatsApp
- 📁 **Chat History**: Saves conversations from each phone number to individual text files
- 🔄 **Thread Management**: Maintains conversation context using OpenAI threads
- 🌐 **Web API**: RESTful endpoints for monitoring and accessing chat data
- 🚀 **Production Ready**: Configured for deployment on quantumautomata.in

## Prerequisites

1. **WhatsApp Business API Access**
   - WhatsApp Business Account
   - Meta Developer Account
   - Phone Number ID and Access Token

2. **OpenAI Account**
   - OpenAI API Key
   - Created Assistant ID

3. **Server Requirements**
   - Python 3.8+
   - Internet connection
   - HTTPS endpoint (for webhook)

## Quick Setup

1. **Clone and Install**
   ```bash
   git clone <your-repo>
   cd whatsapp-chatbot
   python setup.py
   ```

2. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Fill in your API keys and tokens:
   ```env
   WHATSAPP_TOKEN=your_whatsapp_access_token
   WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
   VERIFY_TOKEN=your_webhook_verify_token
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_ASSISTANT_ID=your_assistant_id
   ```

3. **Run the Application**
   ```bash
   # Development
   python app.py
   
   # Production
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

## Configuration Guide

### WhatsApp Business API Setup

1. **Create Meta Developer App**
   - Go to [Meta for Developers](https://developers.facebook.com/)
   - Create a new app and add WhatsApp Business API

2. **Get Credentials**
   - Phone Number ID: Found in WhatsApp Business API dashboard
   - Access Token: Generate a permanent token
   - Verify Token: Create a custom string for webhook verification

3. **Configure Webhook**
   - URL: `https://hexawhite.quantumautomata.in/webhook`
   - Verify Token: Use the same token from your `.env` file
   - Subscribe to `messages` events

### OpenAI Assistant Setup

1. **Create Assistant**
   - Go to [OpenAI Platform](https://platform.openai.com/)
   - Navigate to Assistants section
   - Create a new assistant with your desired instructions

2. **Get Assistant ID**
   - Copy the Assistant ID from the dashboard
   - Add it to your `.env` file

## API Endpoints

### Webhook Endpoints
- `GET /webhook` - Webhook verification
- `POST /webhook` - Receive WhatsApp messages

### Monitoring Endpoints
- `GET /health` - Health check
- `GET /chat-history/<phone_number>` - Get chat history for specific number
- `GET /active-chats` - List all active chat sessions

## File Structure

```
whatsapp-chatbot/
├── app.py              # Main application
├── setup.py            # Setup script
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── .env.example       # Environment template
├── README.md          # This file
├── chats/             # Chat history files (auto-created)
│   ├── chat_1234567890.txt
│   └── chat_0987654321.txt
└── logs/              # Application logs (auto-created)
```

## Chat History Format

Each phone number gets its own text file in the `chats/` directory:

```
[2025-05-31 15:30:45] User: Hello, I need help with my order
[2025-05-31 15:30:47] Assistant: Hello! I'd be happy to help you with your order. Could you please provide me with your order number?
[2025-05-31 15:31:02] User: My order number is #12345
[2025-05-31 15:31:05] Assistant: Thank you! Let me look up order #12345 for you...
```

## Deployment on Oracle Cloud

### Using Gunicorn (Recommended)

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Configure Reverse Proxy**
   - Set up Nginx or Apache to proxy requests to your Flask app
   - Ensure HTTPS is configured for webhook security
   - Configure DNS for hexawhite.quantumautomata.in subdomain

### Environment Variables for Production

```env
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
```

## Security Considerations

1. **HTTPS Required**: WhatsApp webhooks require HTTPS endpoints
2. **Token Security**: Keep your API tokens secure and never commit them to version control
3. **Webhook Verification**: Always verify incoming webhook requests
4. **Rate Limiting**: Consider implementing rate limiting for production use

## Troubleshooting

### Common Issues

1. **Webhook Verification Failed**
   - Check that your `VERIFY_TOKEN` matches in both Meta dashboard and `.env`
   - Ensure your webhook URL is accessible and returns the challenge

2. **Messages Not Sending**
   - Verify your `WHATSAPP_TOKEN` has the correct permissions
   - Check that your phone number is verified in Meta Business

3. **OpenAI Assistant Not Responding**
   - Verify your `OPENAI_API_KEY` is valid
   - Check that your `OPENAI_ASSISTANT_ID` exists and is accessible

### Logs and Debugging

- Check console output for error messages
- Monitor the `/health` endpoint for service status
- Review chat files in the `chats/` directory

## Support

For issues related to:
- **WhatsApp API**: Check [Meta for Developers Documentation](https://developers.facebook.com/docs/whatsapp)
- **OpenAI Assistant**: Check [OpenAI API Documentation](https://platform.openai.com/docs)
- **This Bot**: Create an issue in the repository

## License

This project is licensed under the MIT License - see the LICENSE file for details.