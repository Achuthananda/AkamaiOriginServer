#[[ -z "$1" ]] && { echo -e "Hostname is empty!!!\nCorrect format to run the script is /bin/bash initialize.sh <hostname>\nExample:/bin/bash initialize.sh 194-177-12-185.ip.linodeusercontent.com" ; exit 1; }
HOSTNAME=$(hostname)
cat <<EOF >nginx.conf
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
mv /etc/nginx/sites-enabled/flask_app /etc/nginx/sites-enabled/flask_app.default
cp nginx.conf /etc/nginx/sites-enabled/flask_app
sudo apt install --assume-yes certbot python-certbot-nginx
sudo certbot --nginx --noninteractive --agree-tos -d $HOSTNAME --register-unsafely-without-email
sudo apt install ufw
sudo systemctl start ufw && sudo systemctl enable ufw
sudo ufw allow http
sudo ufw allow https
echo "y" | sudo ufw enable
cp -r srcfiles/* /home/flask_app_project/flask_app/
ps aux | grep gunicorn | awk '{print $2}' | xargs kill -9
sudo supervisorctl reload