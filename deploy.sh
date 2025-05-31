#!/bin/bash

# WhatsApp ChatBot Deployment Script for Oracle Cloud
# This script helps deploy the chatbot to your Oracle Cloud server

set -e

echo "🚀 WhatsApp ChatBot Deployment Script"
echo "======================================"

# Configuration
APP_NAME="whatsapp-chatbot"
APP_DIR="/opt/$APP_NAME"
SERVICE_NAME="whatsapp-chatbot"
DOMAIN="hexawhite.quantumautomata.in"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

# Function to install system dependencies
install_dependencies() {
    print_status "Installing system dependencies..."
    
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx
    
    print_status "System dependencies installed"
}

# Function to setup application directory
setup_app_directory() {
    print_status "Setting up application directory..."
    
    sudo mkdir -p $APP_DIR
    sudo chown $USER:$USER $APP_DIR
    
    # Copy application files
    cp -r . $APP_DIR/
    cd $APP_DIR
    
    print_status "Application directory setup complete"
}

# Function to setup Python virtual environment
setup_python_env() {
    print_status "Setting up Python virtual environment..."
    
    cd $APP_DIR
    python3 -m venv venv
    . venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    print_status "Python environment setup complete"
}

# Function to create systemd service
create_systemd_service() {
    print_status "Creating systemd service..."
    
    sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null <<EOF
[Unit]
Description=WhatsApp ChatBot
After=network.target

[Service]
Type=exec
User=$USER
Group=$USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable $SERVICE_NAME
    
    print_status "Systemd service created"
}

# Function to configure Nginx
configure_nginx() {
    print_status "Configuring Nginx..."
    
    sudo tee /etc/nginx/sites-available/$DOMAIN > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /webhook {
        proxy_pass http://127.0.0.1:5000/webhook;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }
}
EOF

    # Enable the site
    sudo ln -sf /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default
    
    # Test nginx configuration
    sudo nginx -t
    sudo systemctl restart nginx
    
    print_status "Nginx configured"
}

# Function to setup SSL certificate
setup_ssl() {
    print_status "Setting up SSL certificate..."
    
    sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@quantumautomata.in
    
    print_status "SSL certificate setup complete"
}

# Function to start services
start_services() {
    print_status "Starting services..."
    
    cd $APP_DIR
    sudo systemctl start $SERVICE_NAME
    sudo systemctl restart nginx
    
    print_status "Services started"
}

# Function to check service status
check_status() {
    print_status "Checking service status..."
    
    echo "ChatBot Service Status:"
    sudo systemctl status $SERVICE_NAME --no-pager -l
    
    echo -e "\nNginx Status:"
    sudo systemctl status nginx --no-pager -l
    
    echo -e "\nTesting webhook endpoint:"
    curl -f https://$DOMAIN/health || print_warning "Health check failed"
}

# Function to show deployment summary
show_summary() {
    echo ""
    echo "🎉 Deployment Complete!"
    echo "======================"
    echo ""
    echo "Your WhatsApp ChatBot is now deployed at:"
    echo "  🌐 Domain: https://$DOMAIN"
    echo "  📡 Webhook URL: https://$DOMAIN/webhook"
    echo "  ❤️  Health Check: https://$DOMAIN/health"
    echo "  📱 Configure this webhook URL in Meta Developer Console"
    echo ""
    echo "Next Steps:"
    echo "1. Update your .env file with the correct API keys:"
    echo "   sudo nano $APP_DIR/.env"
    echo ""
    echo "2. Restart the service after updating environment:"
    echo "   sudo systemctl restart $SERVICE_NAME"
    echo ""
    echo "3. Configure your WhatsApp webhook URL in Meta Developer Console:"
    echo "   Webhook URL: https://$DOMAIN/webhook"
    echo ""
    echo "4. Monitor logs:"
    echo "   sudo journalctl -u $SERVICE_NAME -f"
    echo ""
    echo "5. Check chat files:"
    echo "   ls -la $APP_DIR/chats/"
    echo ""
}

# Main deployment process
main() {
    echo "Starting deployment process..."
    echo ""
    
    # Check if .env file exists
    if [[ ! -f ".env" ]]; then
        print_warning ".env file not found. Please create it before deployment."
        print_warning "You can copy from .env.example and fill in your values."
        exit 1
    fi
    
    install_dependencies
    setup_app_directory
    setup_python_env
    create_systemd_service
    configure_nginx
    setup_ssl
    start_services
    check_status
    show_summary
}

# Run main function
main "$@"