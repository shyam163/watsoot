import os
import json
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import threading
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_ASSISTANT_ID = os.getenv('OPENAI_ASSISTANT_ID')

# Validate required environment variables
print("🔧 Checking environment configuration...")
required_vars = {
    'WHATSAPP_TOKEN': WHATSAPP_TOKEN,
    'WHATSAPP_PHONE_NUMBER_ID': WHATSAPP_PHONE_NUMBER_ID,
    'VERIFY_TOKEN': VERIFY_TOKEN,
    'OPENAI_API_KEY': OPENAI_API_KEY,
    'OPENAI_ASSISTANT_ID': OPENAI_ASSISTANT_ID
}

missing_vars = []
for var_name, var_value in required_vars.items():
    if not var_value or var_value.startswith('your_'):
        missing_vars.append(var_name)
        print(f"❌ {var_name}: Missing or using placeholder value")
    else:
        # Show partial value for security
        masked_value = var_value[:8] + "..." if len(var_value) > 8 else var_value
        print(f"✅ {var_name}: {masked_value}")

if missing_vars:
    print(f"⚠️  WARNING: {len(missing_vars)} environment variables need to be configured:")
    for var in missing_vars:
        print(f"   - {var}")
    print("   The bot may not function properly until these are set.")

# Initialize OpenAI client with error handling
client = None
try:
    from openai import OpenAI
    if OPENAI_API_KEY:
        client = OpenAI(api_key=OPENAI_API_KEY)
        print("✅ OpenAI client initialized successfully")
    else:
        print("⚠️  OPENAI_API_KEY not found in environment variables")
except Exception as e:
    print(f"❌ Error initializing OpenAI client: {e}")
    print("The app will start but OpenAI features will be disabled")

# WhatsApp API URL
WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

class ChatManager:
    def __init__(self):
        self.active_threads = {}
        self.chat_directory = "chats"
        os.makedirs(self.chat_directory, exist_ok=True)
    
    def get_chat_file_path(self, phone_number):
        """Get the file path for a specific phone number's chat history"""
        safe_number = phone_number.replace('+', '').replace(' ', '')
        return os.path.join(self.chat_directory, f"chat_{safe_number}.txt")
    
    def save_message(self, phone_number, sender, message):
        """Save a message to the chat file"""
        chat_file = self.get_chat_file_path(phone_number)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(chat_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {sender}: {message}\n")
    
    def get_or_create_thread(self, phone_number):
        """Get existing thread or create new one for a phone number"""
        if not client:
            raise Exception("OpenAI client not initialized")
            
        if phone_number not in self.active_threads:
            thread = client.beta.threads.create()
            self.active_threads[phone_number] = thread.id
            print(f"🆕 Created new thread for {phone_number}: {thread.id}")
        return self.active_threads[phone_number]
    
    def get_assistant_response(self, phone_number, user_message):
        """Get response from OpenAI assistant"""
        try:
            thread_id = self.get_or_create_thread(phone_number)
            
            # Add user message to thread
            client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=user_message
            )
            
            # Run the assistant
            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=OPENAI_ASSISTANT_ID
            )
            
            # Wait for completion
            while run.status in ['queued', 'in_progress']:
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
            
            if run.status == 'completed':
                # Get the assistant's response
                messages = client.beta.threads.messages.list(
                    thread_id=thread_id,
                    order="desc",
                    limit=1
                )
                
                if messages.data:
                    response = messages.data[0].content[0].text.value
                    return response
            
            return "I apologize, but I'm having trouble processing your request right now. Please try again."
            
        except Exception as e:
            print(f"Error getting assistant response: {e}")
            return "I'm sorry, I encountered an error while processing your message. Please try again later."

chat_manager = ChatManager()

def send_whatsapp_message(phone_number, message):
    """Send a message via WhatsApp Business API"""
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {
            "body": message
        }
    }
    
    try:
        print(f"📤 Sending message to {phone_number}: {message[:50]}...")
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=data)
        
        # Log detailed response information
        print(f"📊 WhatsApp API Response Status: {response.status_code}")
        print(f"📊 WhatsApp API Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"✅ Message sent successfully: {response_data}")
            return True
        else:
            print(f"❌ WhatsApp API Error: {response.status_code}")
            print(f"❌ Error Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error sending WhatsApp message: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error sending WhatsApp message: {e}")
        return False

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verify webhook for WhatsApp"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge
    else:
        return 'Forbidden', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages"""
    try:
        data = request.get_json()
        print(f"📨 Received webhook data: {json.dumps(data, indent=2)}")
        
        if 'entry' in data:
            for entry in data['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        if 'value' in change and 'messages' in change['value']:
                            for message in change['value']['messages']:
                                phone_number = message['from']
                                message_text = message.get('text', {}).get('body', '')
                                
                                print(f"📱 Incoming message from {phone_number}: {message_text}")
                                
                                if message_text:
                                    # Save incoming message
                                    chat_manager.save_message(phone_number, "User", message_text)
                                    
                                    # Process message in background to avoid timeout
                                    def process_message():
                                        try:
                                            print(f"🔄 Processing message from {phone_number}: {message_text}")
                                            
                                            # Get assistant response
                                            response = chat_manager.get_assistant_response(phone_number, message_text)
                                            print(f"🤖 Assistant response: {response[:100]}...")
                                            
                                            # Save assistant response
                                            chat_manager.save_message(phone_number, "Assistant", response)
                                            
                                            # Send response via WhatsApp
                                            success = send_whatsapp_message(phone_number, response)
                                            if success:
                                                print(f"✅ Successfully sent response to {phone_number}")
                                            else:
                                                print(f"❌ Failed to send response to {phone_number}")
                                                
                                        except Exception as e:
                                            print(f"❌ Error in background message processing: {e}")
                                            import traceback
                                            traceback.print_exc()
                                    
                                    # Run in background thread
                                    thread = threading.Thread(target=process_message)
                                    thread.daemon = True  # Ensure thread doesn't prevent app shutdown
                                    thread.start()
        
        return jsonify({'status': 'success'}), 200
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({'status': 'error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'WhatsApp ChatBot'
    })

@app.route('/chat-history/<phone_number>', methods=['GET'])
def get_chat_history(phone_number):
    """Get chat history for a specific phone number"""
    try:
        chat_file = chat_manager.get_chat_file_path(phone_number)
        if os.path.exists(chat_file):
            with open(chat_file, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({
                'phone_number': phone_number,
                'chat_history': content
            })
        else:
            return jsonify({
                'phone_number': phone_number,
                'chat_history': 'No chat history found'
            }), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/active-chats', methods=['GET'])
def get_active_chats():
    """Get list of all active chat files"""
    try:
        chat_files = []
        if os.path.exists(chat_manager.chat_directory):
            for filename in os.listdir(chat_manager.chat_directory):
                if filename.startswith('chat_') and filename.endswith('.txt'):
                    phone_number = filename.replace('chat_', '').replace('.txt', '')
                    chat_files.append(phone_number)
        
        return jsonify({
            'active_chats': chat_files,
            'total_chats': len(chat_files)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')