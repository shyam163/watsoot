#!/usr/bin/env python3
"""
Configuration Checker
Quick script to check if your WhatsApp API credentials are properly configured
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_config():
    """Check if configuration is properly set up"""
    print("🔧 WhatsApp Bot Configuration Checker")
    print("=" * 50)
    
    # Get environment variables
    token = os.getenv('WHATSAPP_TOKEN')
    phone_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    verify_token = os.getenv('VERIFY_TOKEN')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    issues = []
    
    # Check WhatsApp Token
    if not token or token == 'your_whatsapp_access_token_here' or token.startswith('your_'):
        print("❌ WHATSAPP_TOKEN: Not configured")
        print(f"   Current: {token}")
        issues.append("WhatsApp Access Token")
    else:
        print(f"✅ WHATSAPP_TOKEN: Configured ({token[:10]}...)")
    
    # Check Phone Number ID
    if not phone_id or phone_id == 'your_phone_number_id_here' or phone_id.startswith('your_'):
        print("❌ WHATSAPP_PHONE_NUMBER_ID: Not configured")
        print(f"   Current: {phone_id}")
        issues.append("WhatsApp Phone Number ID")
    else:
        print(f"✅ WHATSAPP_PHONE_NUMBER_ID: Configured ({phone_id})")
    
    # Check Verify Token
    if not verify_token or verify_token == 'your_webhook_verify_token_here' or verify_token.startswith('your_'):
        print("❌ VERIFY_TOKEN: Not configured")
        print(f"   Current: {verify_token}")
        issues.append("Webhook Verify Token")
    else:
        print(f"✅ VERIFY_TOKEN: Configured ({verify_token})")
    
    # Check OpenAI Key
    if not openai_key or openai_key == 'your_openai_api_key_here' or openai_key.startswith('your_'):
        print("❌ OPENAI_API_KEY: Not configured")
        print(f"   Current: {openai_key}")
        issues.append("OpenAI API Key")
    else:
        print(f"✅ OPENAI_API_KEY: Configured ({openai_key[:10]}...)")
    
    print("\n" + "=" * 50)
    
    if issues:
        print("🚨 CONFIGURATION ISSUES FOUND:")
        print()
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue} needs to be configured")
        
        print("\n💡 TO FIX THESE ISSUES:")
        print("1. Open your .env file")
        print("2. Replace the placeholder values with real credentials:")
        print()
        
        if "WhatsApp Access Token" in issues:
            print("   🔑 Get WhatsApp Access Token:")
            print("      - Go to https://developers.facebook.com/apps/")
            print("      - Select your app > WhatsApp > API Setup")
            print("      - Copy the temporary access token")
            print()
        
        if "WhatsApp Phone Number ID" in issues:
            print("   📱 Get Phone Number ID:")
            print("      - In the same WhatsApp API Setup page")
            print("      - Find 'Phone number ID' under your test number")
            print()
        
        if "Webhook Verify Token" in issues:
            print("   🔐 Set Verify Token:")
            print("      - Choose any random string (e.g., 'mybot123')")
            print("      - Use the same value in webhook configuration")
            print()
        
        if "OpenAI API Key" in issues:
            print("   🤖 Get OpenAI API Key:")
            print("      - Go to https://platform.openai.com/api-keys")
            print("      - Create a new API key")
            print()
        
        print("3. Save the .env file")
        print("4. Run this script again to verify")
        
        return False
    else:
        print("🎉 ALL CONFIGURATION LOOKS GOOD!")
        print()
        print("Your bot should be ready to work. You can now:")
        print("1. Run 'python send_test_message.py' to test message sending")
        print("2. Run 'python app.py' to start your bot")
        print("3. Test by sending a message to your WhatsApp bot number")
        
        return True

if __name__ == "__main__":
    check_config()