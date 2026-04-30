# CyberFolio

CyberFolio is a Flask-based cybersecurity portfolio and services website built for an AWS course project. It includes:

- 8 public-facing pages with a fixed top navigation
- A database-backed contact form
- A protected admin/messages page that reads saved submissions from SQLite
- Lightsail deployment notes for a live AWS submission

## Pages

- Home
- About
- Resume
- Certifications
- Projects
- Blog
- Services
- Contact
- Admin Login
- Admin Messages

## Local Setup

1. Install dependencies:

   ```powershell
   python -m pip install -e ".[dev]"
   ```

2. Set environment variables:

   ```powershell
   $env:SECRET_KEY="replace-with-a-secret"
   $env:ADMIN_USERNAME="admin"
   $env:ADMIN_PASSWORD="change-this-password"
   ```

3. Run the application:

   ```powershell
   python run.py
   ```

4. Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Test

```powershell
python -m pytest -q
```

## AWS Deliverables

Before submitting, include:

- The Lightsail public IP or custom URL
- Optional admin demo credentials
- A brief write-up describing the AWS services used and why

Deployment details are in [DEPLOYMENT.md](DEPLOYMENT.md).
