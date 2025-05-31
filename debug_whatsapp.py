#!/usr/bin/env python3
"""
WhatsApp API Debug Script
This script helps diagnose issues with WhatsApp message sending
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

def check_configuration():
    """Check if all required configuration is present"""
    print("🔧 Checking WhatsApp API Configuration...")
    print("=" * 50)
    
    config_items = [
        ("WHATSAPP_TOKEN", WHATSAPP_TOKEN),
        ("WHATSAPP_PHONE_NUMBER_ID", WHATSAPP_PHONE_NUMBER_ID),
    ]
    
    all_good = True
    for name, value in config_items:
        if not value or value.startswith('your_'):
            print(f"❌ {name}: Missing or placeholder value")
            all_good = False
        else:
            masked = value[:8] + "..." if len(value) > 8 else value
            print(f"✅ {name}: {masked}")
    
    print(f"📡 API URL: {WHATSAPP_API_URL}")
    return all_good

def test_whatsapp_api_access():
    """Test if we can access the WhatsApp API"""
    print("\n🌐 Testing WhatsApp API Access...")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # Test with a simple GET request to check token validity
    try:
        # Try to get phone number info
        info_url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}"
        response = requests.get(info_url, headers=headers)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Access Successful")
            print(f"📱 Phone Number Info: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"❌ API Access Failed")
            print(f"❌ Error Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API access: {e}")
        return False

def test_send_message(test_phone_number):
    """Test sending a message to a specific phone number"""
    print(f"\n📤 Testing Message Send to {test_phone_number}...")
    print("=" * 50)
    
    headers = {
        'Authorization': f'Bearer {WHATSAPP_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": test_phone_number,
        "type": "text",
        "text": {
            "body": "🧪 Test message from WhatsApp bot debug script"
        }
    }
    
    try:
        print(f"📡 Sending to: {WHATSAPP_API_URL}")
        print(f"📦 Payload: {json.dumps(data, indent=2)}")
        
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=data)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"✅ Message Sent Successfully!")
            print(f"📨 Response: {json.dumps(response_data, indent=2)}")
            return True
        else:
            print(f"❌ Message Send Failed")
            print(f"❌ Error Response: {response.text}")
            
            # Try to parse error details
            try:
                error_data = response.json()
                if 'error' in error_data:
                    error = error_data['error']
                    print(f"❌ Error Code: {error.get('code', 'Unknown')}")
                    print(f"❌ Error Message: {error.get('message', 'Unknown')}")
                    print(f"❌ Error Type: {error.get('type', 'Unknown')}")
            except:
                pass
            
            return False
            
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print("🔍 WhatsApp API Diagnostic Tool")
    print("=" * 50)
    
    # Check configuration
    if not check_configuration():
        print("\n⚠️  Configuration issues found. Please update your .env file.")
        return
    
    # Test API access
    if not test_whatsapp_api_access():
        print("\n⚠️  API access failed. Check your token and phone number ID.")
        return
    
    # Ask for test phone number
    print("\n📱 To test message sending, please provide a phone number.")
    print("   Format: Country code + number (e.g., 1234567890)")
    print("   Note: This number must be registered with WhatsApp")
    
    test_phone = input("\nEnter test phone number (or press Enter to skip): ").strip()
    
    if test_phone:
        test_send_message(test_phone)
    else:
        print("⏭️  Skipping message send test")
    
    print("\n🎯 Diagnostic Summary:")
    print("=" * 50)
    print("1. If configuration is OK but API access fails:")
    print("   - Check your WHATSAPP_TOKEN is valid and not expired")
    print("   - Verify WHATSAPP_PHONE_NUMBER_ID is correct")
    print("   - Ensure your WhatsApp Business account is active")
    print()
    print("2. If API access works but message sending fails:")
    print("   - Check the recipient phone number format")
    print("   - Ensure the recipient has WhatsApp installed")
    print("   - Verify your WhatsApp Business account has messaging permissions")
    print()
    print("3. If everything works here but not in your bot:")
    print("   - Check your webhook URL is accessible")
    print("   - Verify webhook verification token")
    print("   - Check server logs for errors")

if __name__ == "__main__":
    main()