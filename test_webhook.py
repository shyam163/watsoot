#!/usr/bin/env python3
"""
Test script for WhatsApp ChatBot webhook
This script helps test the webhook functionality locally
"""

import requests
import json
import time
from datetime import datetime

# Test configuration
WEBHOOK_URL = "http://localhost:5000/webhook"
VERIFY_TOKEN = "your_webhook_verify_token_here"

def test_webhook_verification():
    """Test webhook verification endpoint"""
    print("🔍 Testing webhook verification...")
    
    params = {
        'hub.mode': 'subscribe',
        'hub.verify_token': VERIFY_TOKEN,
        'hub.challenge': 'test_challenge_123'
    }
    
    try:
        response = requests.get(WEBHOOK_URL, params=params)
        if response.status_code == 200 and response.text == 'test_challenge_123':
            print("✅ Webhook verification successful")
            return True
        else:
            print(f"❌ Webhook verification failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing webhook verification: {e}")
        return False

def test_message_webhook():
    """Test message webhook endpoint"""
    print("📱 Testing message webhook...")
    
    # Sample WhatsApp webhook payload
    test_payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "15550559999",
                                "phone_number_id": "PHONE_NUMBER_ID"
                            },
                            "contacts": [
                                {
                                    "profile": {
                                        "name": "Test User"
                                    },
                                    "wa_id": "1234567890"
                                }
                            ],
                            "messages": [
                                {
                                    "from": "1234567890",
                                    "id": "wamid.test123",
                                    "timestamp": str(int(time.time())),
                                    "text": {
                                        "body": "Hello, this is a test message!"
                                    },
                                    "type": "text"
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(
            WEBHOOK_URL,
            json=test_payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Message webhook test successful")
            return True
        else:
            print(f"❌ Message webhook test failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing message webhook: {e}")
        return False

def test_health_endpoint():
    """Test health check endpoint"""
    print("❤️  Testing health endpoint...")
    
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check successful: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")
        return False

def test_chat_history_endpoint():
    """Test chat history endpoint"""
    print("📚 Testing chat history endpoint...")
    
    try:
        response = requests.get("http://localhost:5000/chat-history/1234567890")
        if response.status_code in [200, 404]:  # 404 is OK if no chat history exists
            print("✅ Chat history endpoint working")
            return True
        else:
            print(f"❌ Chat history endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing chat history endpoint: {e}")
        return False

def test_active_chats_endpoint():
    """Test active chats endpoint"""
    print("📋 Testing active chats endpoint...")
    
    try:
        response = requests.get("http://localhost:5000/active-chats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Active chats endpoint working: {data['total_chats']} chats found")
            return True
        else:
            print(f"❌ Active chats endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing active chats endpoint: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 WhatsApp ChatBot Webhook Tests")
    print("=" * 40)
    print(f"Testing webhook at: {WEBHOOK_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Webhook Verification", test_webhook_verification),
        ("Message Webhook", test_message_webhook),
        ("Chat History API", test_chat_history_endpoint),
        ("Active Chats API", test_active_chats_endpoint),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        result = test_func()
        results.append((test_name, result))
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Summary:")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your webhook is working correctly.")
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Please check your configuration.")
        print("\nTroubleshooting tips:")
        print("1. Make sure the Flask app is running (python app.py)")
        print("2. Check your .env file configuration")
        print("3. Verify your VERIFY_TOKEN matches")
        print("4. Ensure all required packages are installed")

if __name__ == "__main__":
    main()