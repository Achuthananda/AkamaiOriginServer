#!/bin/bash

HOSTNAME=$(hostname)
NGINX_CONF="/etc/nginx/sites-available/flask_app"
NGINX_ENABLED_CONF="/etc/nginx/sites-enabled/flask_app"

# Step 1: Ensure no conflicting Nginx configuration
# Move default configuration to avoid conflicts
if [ -f /etc/nginx/sites-enabled/default ]; then
    sudo mv /etc/nginx/sites-enabled/default /etc/nginx/sites-enabled/default.bak
fi

# Step 2: Create a temporary Nginx configuration for Certbot
cat <<EOF | sudo tee /etc/nginx/sites-available/temp_certbot.conf
server {
    listen 80;
    server_name $HOSTNAME;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

# Enable the temporary configuration
sudo ln -sf /etc/nginx/sites-available/temp_certbot.conf /etc/nginx/sites-enabled/temp_certbot.conf

# Ensure the challenge directory exists and has the correct permissions
sudo mkdir -p /var/www/html/.well-known/acme-challenge
sudo chown -R www-data:www-data /var/www/html/.well-known

# Step 3: Reload Nginx to apply the temporary configuration
sudo nginx -t && sudo systemctl reload nginx

# Install Certbot and obtain the certificate
sudo apt update
sudo apt install --assume-yes certbot python3-certbot-nginx
sudo certbot --nginx --noninteractive --agree-tos -d $HOSTNAME --register-unsafely-without-email

# Step 4: Remove the temporary configuration and restore final Nginx configuration
sudo rm /etc/nginx/sites-enabled/temp_certbot.conf
sudo rm /etc/nginx/sites-available/temp_certbot.conf

# Create the final Nginx configuration
cat <<EOF | sudo tee $NGINX_CONF
server {
    listen 80;
    server_name $HOSTNAME;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

# Enable the final configuration
sudo ln -sf $NGINX_CONF $NGINX_ENABLED_CONF

# Reload Nginx to apply the final configuration
sudo nginx -t && sudo systemctl reload nginx

# Step 5: Install and configure UFW
sudo apt install --assume-yes ufw
sudo systemctl start ufw && sudo systemctl enable ufw
sudo ufw allow http
sudo ufw allow https
echo "y" | sudo ufw enable

# Copy project files
cp -r srcfiles/* /home/flask_app_project/flask_app/

# Restart the application
ps aux | grep gunicorn | awk '{print $2}' | xargs sudo kill -9
sudo systemctl start gunicorn

# Optionally, you can remove the backup of the default configuration
# sudo rm /etc/nginx/sites-enabled/default.bak
