ps aux | grep gunicorn | awk '{print $2}' | xargs kill -9
sudo supervisorctl stop all
sudo supervisorctl start all
