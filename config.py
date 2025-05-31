"""
Configuration module for WhatsApp ChatBot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    
    # WhatsApp Business API Configuration
    WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
    WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://hexawhite.quantumautomata.in/webhook')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_ASSISTANT_ID = os.getenv('OPENAI_ASSISTANT_ID')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    
    # Chat Configuration
    CHAT_DIRECTORY = os.getenv('CHAT_DIRECTORY', 'chats')
    MAX_CHAT_HISTORY = int(os.getenv('MAX_CHAT_HISTORY', 1000))  # Max messages per chat file
    CHAT_BACKUP_ENABLED = os.getenv('CHAT_BACKUP_ENABLED', 'True').lower() == 'true'
    
    # Thread Management
    THREAD_TIMEOUT = int(os.getenv('THREAD_TIMEOUT', 3600))  # 1 hour in seconds
    MAX_ACTIVE_THREADS = int(os.getenv('MAX_ACTIVE_THREADS', 100))
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_MESSAGES = int(os.getenv('RATE_LIMIT_MESSAGES', 10))  # Messages per minute
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', 60))  # Window in seconds
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/chatbot.log')
    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', 10485760))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', 5))
    
    # Security Configuration
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')
    API_KEY_REQUIRED = os.getenv('API_KEY_REQUIRED', 'False').lower() == 'true'
    API_KEY = os.getenv('API_KEY')
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration values"""
        required_vars = [
            'WHATSAPP_TOKEN',
            'WHATSAPP_PHONE_NUMBER_ID',
            'VERIFY_TOKEN',
            'OPENAI_API_KEY',
            'OPENAI_ASSISTANT_ID'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
    
    @classmethod
    def get_whatsapp_api_url(cls):
        """Get WhatsApp API URL"""
        return f"https://graph.facebook.com/v18.0/{cls.WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    @classmethod
    def get_chat_file_path(cls, phone_number):
        """Get chat file path for a phone number"""
        safe_number = phone_number.replace('+', '').replace(' ', '').replace('-', '')
        return os.path.join(cls.CHAT_DIRECTORY, f"chat_{safe_number}.txt")

class DevelopmentConfig(Config):
    """Development configuration"""
    FLASK_DEBUG = True
    FLASK_ENV = 'development'
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    FLASK_DEBUG = False
    FLASK_ENV = 'production'
    LOG_LEVEL = 'INFO'
    RATE_LIMIT_ENABLED = True

class TestingConfig(Config):
    """Testing configuration"""
    FLASK_DEBUG = True
    FLASK_ENV = 'testing'
    CHAT_DIRECTORY = 'test_chats'
    LOG_LEVEL = 'DEBUG'

# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(env_name=None):
    """Get configuration class based on environment"""
    if env_name is None:
        env_name = os.getenv('FLASK_ENV', 'default')
    
    return config_map.get(env_name, DevelopmentConfig)