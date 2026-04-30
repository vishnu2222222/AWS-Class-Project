# Lightsail Deployment Guide

This project is designed for a single Ubuntu Lightsail instance with Flask, Gunicorn, Nginx, and SQLite.

## 1. Create the server

1. In AWS Lightsail, create a Linux/Unix instance with Ubuntu.
2. Use the smallest plan that matches your free-trial/credit allowance.
3. Attach a static IP after the instance is running.
4. Open ports `22`, `80`, and `443` in the Lightsail networking tab.

## 2. Install system packages

SSH into the instance and run:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx
```

## 3. Copy the project

Upload the project to the server, for example:

```bash
scp -r cyberfolio ubuntu@YOUR_STATIC_IP:/home/ubuntu/
```

Or clone it from Git if you are using a repository.

## 4. Create a virtual environment

```bash
cd /home/ubuntu/cyberfolio
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## 5. Configure environment variables

Create `/home/ubuntu/cyberfolio/.env.production`:

```bash
SECRET_KEY=replace-with-a-long-random-secret
ADMIN_USERNAME=admin
ADMIN_PASSWORD=replace-with-a-strong-password
DATABASE_PATH=/home/ubuntu/cyberfolio/instance/portfolio.db
```

## 6. Install systemd service

Copy [deploy/cyberfolio.service](deploy/cyberfolio.service) to `/etc/systemd/system/cyberfolio.service`, then update the paths if needed:

```bash
sudo cp deploy/cyberfolio.service /etc/systemd/system/cyberfolio.service
sudo systemctl daemon-reload
sudo systemctl enable cyberfolio
sudo systemctl start cyberfolio
sudo systemctl status cyberfolio
```

## 7. Configure Nginx

Copy [deploy/nginx-cyberfolio.conf](deploy/nginx-cyberfolio.conf) into `/etc/nginx/sites-available/cyberfolio` and enable it:

```bash
sudo cp deploy/nginx-cyberfolio.conf /etc/nginx/sites-available/cyberfolio
sudo ln -s /etc/nginx/sites-available/cyberfolio /etc/nginx/sites-enabled/cyberfolio
sudo nginx -t
sudo systemctl restart nginx
```

At that point the site should be available at `http://YOUR_STATIC_IP`.

## 8. Optional HTTPS

If you add a domain later, install Certbot:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## 9. Final course submission checklist

- Public site loads by IP or domain
- Contact form saves data
- Admin login works
- Admin/messages page shows submissions
- Snapshot the Lightsail instance for backup
- Email the professor your IP/URL and AWS write-up
