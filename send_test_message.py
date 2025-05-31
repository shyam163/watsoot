#!/usr/bin/env python3
"""
Send Test Message Script
Sends a test message to a specific WhatsApp number to verify the bot is working
"""

import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

# Test phone number
TEST_PHONE_NUMBER = "91986422115"

def send_test_message():
    """Send a test message to the specified phone number"""
    print("🧪 WhatsApp Test Message Sender")
    print("=" * 40)
    print(f"📱 Target Number: {TEST_PHONE_NUMBER}")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check configuration
    if not WHATSAPP_TOKEN or WHATSAPP_TOKEN.startswith('your_'):
        print("❌ WHATSAPP_TOKEN not configured properly")
        print("   Please update your .env file with a valid token")
        return False
    
    if not WHATSAPP_PHONE_NUMBER_ID or WHATSAPP_PHONE_NUMBER_ID.startswith('your_'):
        print("❌ WHATSAPP_PHONE_NUMBER_ID not configured properly")
        print("   Please update your .env file with a valid phone number ID")
        return False
    
    print(f"✅ Using Token: {WHATSAPP_TOKEN[:10]}...")
    print(f"✅ Using Phone ID: {WHATSAPP_PHONE_NUMBER_ID}")
    print(f"📡 API URL: {WHATSAPP_API_URL}")
    print()
    
    # Prepare message
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    test_message = f"""🤖 WhatsApp Bot Test Message

Hello! This is a test message from your WhatsApp bot.

✅ Bot is working correctly
⏰ Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📱 To: {TEST_PHONE_NUMBER}

If you receive this message, your bot's message sending functionality is working properly!"""
    
    data = {
        "messaging_product": "whatsapp",
        "to": TEST_PHONE_NUMBER,
        "type": "text",
        "text": {
            "body": test_message
        }
    }
    
    print("📤 Sending test message...")
    print(f"📦 Message content: {test_message[:50]}...")
    print()
    
    try:
        # Send the message
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=data)
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            response_data = response.json()
            print("✅ TEST MESSAGE SENT SUCCESSFULLY!")
            print(f"📨 Response Data: {json.dumps(response_data, indent=2)}")
            
            if 'messages' in response_data and response_data['messages']:
                message_id = response_data['messages'][0].get('id', 'Unknown')
                print(f"📧 Message ID: {message_id}")
            
            print()
            print("🎉 SUCCESS! Your WhatsApp bot can send messages.")
            print(f"📱 Check WhatsApp on {TEST_PHONE_NUMBER} for the test message.")
            return True
            
        else:
            print("❌ TEST MESSAGE FAILED!")
            print(f"❌ Error Status: {response.status_code}")
            print(f"❌ Error Response: {response.text}")
            
            # Try to parse error details
            try:
                error_data = response.json()
                if 'error' in error_data:
                    error = error_data['error']
                    print(f"❌ Error Code: {error.get('code', 'Unknown')}")
                    print(f"❌ Error Message: {error.get('message', 'Unknown')}")
                    print(f"❌ Error Type: {error.get('type', 'Unknown')}")
                    
                    # Common error solutions
                    if error.get('code') == 190:
                        print("\n💡 Solution: Your access token is invalid or expired")
                        print("   - Get a new token from Meta Developer Console")
                        print("   - Update WHATSAPP_TOKEN in your .env file")
                    elif error.get('code') == 100:
                        print("\n💡 Solution: Invalid phone number or parameter")
                        print("   - Check WHATSAPP_PHONE_NUMBER_ID is correct")
                        print("   - Verify the target phone number format")
                    elif 'phone number' in error.get('message', '').lower():
                        print("\n💡 Solution: Phone number issue")
                        print("   - Ensure the target number has WhatsApp installed")
                        print("   - Check the number format (country code + number)")
                        
            except:
                pass
            
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
        print("\n💡 Solution: Check your internet connection")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def main():
    """Main function"""
    success = send_test_message()
    
    print("\n" + "=" * 40)
    if success:
        print("🎯 TEST RESULT: SUCCESS ✅")
        print()
        print("Your WhatsApp bot is working correctly!")
        print("You can now test the full bot functionality by:")
        print("1. Sending a message to your bot's WhatsApp number")
        print("2. Checking the bot logs for message processing")
        print("3. Verifying you receive a response")
    else:
        print("🎯 TEST RESULT: FAILED ❌")
        print()
        print("Your WhatsApp bot has configuration issues.")
        print("Please:")
        print("1. Check your .env file configuration")
        print("2. Verify your WhatsApp Business API setup")
        print("3. Run 'python debug_whatsapp.py' for detailed diagnosis")
        print("4. Refer to TROUBLESHOOTING.md for help")

if __name__ == "__main__":
    main()