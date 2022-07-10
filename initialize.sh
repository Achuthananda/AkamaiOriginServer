sudo apt install certbot python-certbot-nginx
sudo certbot --nginx --noninteractive --agree-tos -d $1 --register-unsafely-without-email
sudo apt install ufw
sudo systemctl start ufw && sudo systemctl enable ufw
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
cp -r !(README.md|LICENSE) /home/flask_app_project/flask_app/
cd /home/flask_app_project/flask_app/
ps aux | grep gunicorn | awk '{print $2}' | xargs kill -9
sudo supervisorctl reload