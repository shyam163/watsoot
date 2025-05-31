#!/usr/bin/env python3
"""
Setup script for WhatsApp ChatBot
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False
    return True

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = ["chats", "logs"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("Checking environment configuration...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please copy .env.example to .env and fill in your configuration values.")
        return False
    
    required_vars = [
        'WHATSAPP_TOKEN',
        'WHATSAPP_PHONE_NUMBER_ID',
        'VERIFY_TOKEN',
        'OPENAI_API_KEY',
        'OPENAI_ASSISTANT_ID'
    ]
    
    missing_vars = []
    with open('.env', 'r') as f:
        content = f.read()
        for var in required_vars:
            if f"{var}=your_" in content or f"{var}=" not in content:
                missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing or incomplete environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease update your .env file with the correct values.")
        return False
    
    print("✅ Environment configuration looks good!")
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up WhatsApp ChatBot...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check environment
    env_ok = check_env_file()
    
    print("\n" + "=" * 50)
    print("📋 Setup Summary:")
    print("✅ Requirements installed")
    print("✅ Directories created")
    
    if env_ok:
        print("✅ Environment configured")
        print("\n🎉 Setup complete! You can now run the chatbot with:")
        print("   python app.py")
        print("\nOr for production deployment:")
        print("   gunicorn -w 4 -b 0.0.0.0:5000 app:app")
        print(f"\nWebhook URL for WhatsApp configuration:")
        print("   https://hexawhite.quantumautomata.in/webhook")
    else:
        print("❌ Environment needs configuration")
        print("\n⚠️  Please configure your .env file before running the chatbot.")
    
    print("\n📚 Additional Information:")
    print("- Chat histories will be saved in the 'chats' directory")
    print("- Each phone number gets its own chat file")
    print("- Health check available at: /health")
    print("- Chat history API: /chat-history/<phone_number>")
    print("- Active chats list: /active-chats")
    print("- Deployment domain: hexawhite.quantumautomata.in")

if __name__ == "__main__":
    main()