# Deployment Guide - AI Interview System

## Deployment Options

### 1. Local Development
### 2. Streamlit Cloud  
### 3. Docker Container
### 4. Cloud Platforms (AWS, Azure, GCP)
### 5. On-Premise Server

---

## 1. Local Development

**Best for:** Testing and development

### Setup

```bash
# Clone/download project
cd AI

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install system dependencies
# Tesseract OCR
winget install UB-Mannheim.TesseractOCR

# FFmpeg
winget install Gyan.FFmpeg

# Run application
streamlit run app.py
```

### Access
- Local: `http://localhost:8501`
- Network: `http://<your-ip>:8501`

---

## 2. Streamlit Cloud

**Best for:** Quick, free deployment

### Prerequisites
- GitHub account
- Project in GitHub repository
- Streamlit Cloud account (free)

### Steps

#### 1. Prepare Repository

```bash
# Ensure these files exist:
# - app.py
# - requirements.txt
# - modules/
# - README.md
```

#### 2. Update requirements.txt

```txt
# Core
streamlit>=1.28.0
numpy>=1.24.0
opencv-python-headless>=4.8.0  # Use headless for cloud
Pillow>=10.0.0

# OCR (cloud needs apt-packages.txt)
pytesseract>=0.3.10

# Audio
openai-whisper>=20231117

# LLM
langchain>=0.0.350
openai>=1.3.0

# PDF
PyPDF2>=3.0.0
pdfplumber>=0.10.0
reportlab>=4.0.7
markdown>=3.5.1
python-dotenv>=1.0.0
```

#### 3. Create packages.txt

For system-level dependencies:

```txt
# packages.txt
tesseract-ocr
tesseract-ocr-eng
ffmpeg
```

#### 4. Deploy

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Connect GitHub repository
4. Select branch: `main`
5. Main file path: `app.py`
6. Click "Deploy"

#### 5. Configure Secrets

In Streamlit Cloud dashboard:
- Settings → Secrets
- Add:
```toml
OPENAI_API_KEY = "sk-your-key-here"
```

### Limitations
- Free tier: Limited resources
- 1GB memory limit
- Tesseract may need configuration
- Audio processing may be slow

---

## 3. Docker Container

**Best for:** Consistent deployment, production

### Dockerfile

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  ai-interviewer:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data  # For persistent storage
    restart: unless-stopped
```

### .dockerignore

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
.env
.git/
.gitignore
*.md
tests/
examples/
```

### Build and Run

```bash
# Build image
docker build -t ai-interviewer .

# Run container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY="your-key" \
  ai-interviewer

# Or use docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Access
- `http://localhost:8501`

---

## 4. Cloud Platforms

### AWS Deployment

#### Option A: EC2 Instance

```bash
# Launch EC2 (t2.medium recommended)
# Amazon Linux 2 or Ubuntu

# Connect via SSH
ssh -i key.pem ec2-user@<ip-address>

# Update system
sudo yum update -y  # Amazon Linux
# sudo apt update && sudo apt upgrade -y  # Ubuntu

# Install Python
sudo yum install python3 python3-pip -y

# Install system dependencies
sudo yum install tesseract ffmpeg -y

# Clone project
git clone <repository-url>
cd AI

# Install Python packages
pip3 install -r requirements.txt

# Run with screen/tmux for persistence
screen -S interviewer
streamlit run app.py --server.port=8501 --server.address=0.0.0.0

# Detach: Ctrl+A, D
# Reattach: screen -r interviewer
```

#### Security Group
- Inbound: Port 8501 (Custom TCP)
- Source: Your IP or 0.0.0.0/0 (public)

#### Option B: ECS (Docker)

1. Create ECR repository
2. Push Docker image
3. Create ECS cluster
4. Define task with image
5. Create service
6. Configure load balancer

### Azure Deployment

#### Azure Container Instances

```bash
# Login
az login

# Create resource group
az group create --name ai-interviewer-rg --location eastus

# Create container instance
az container create \
  --resource-group ai-interviewer-rg \
  --name ai-interviewer \
  --image <your-dockerhub>/ai-interviewer:latest \
  --dns-name-label ai-interviewer-unique \
  --ports 8501 \
  --environment-variables OPENAI_API_KEY=your-key

# Get URL
az container show \
  --resource-group ai-interviewer-rg \
  --name ai-interviewer \
  --query ipAddress.fqdn
```

#### Azure App Service

1. Create App Service (Python 3.9)
2. Configure deployment from GitHub
3. Set environment variables
4. Deploy

### Google Cloud Platform

#### Cloud Run

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/<project-id>/ai-interviewer

# Deploy to Cloud Run
gcloud run deploy ai-interviewer \
  --image gcr.io/<project-id>/ai-interviewer \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your-key

# Get URL
gcloud run services describe ai-interviewer --region us-central1
```

---

## 5. On-Premise Server

### Linux Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y \
  python3 python3-pip \
  tesseract-ocr \
  ffmpeg \
  nginx

# Create user
sudo useradd -m -s /bin/bash aiinterview
sudo su - aiinterview

# Clone project
git clone <repository-url> /home/aiinterview/app
cd /home/aiinterview/app

# Install Python packages
pip3 install -r requirements.txt

# Create systemd service
sudo nano /etc/systemd/system/ai-interviewer.service
```

### Systemd Service

```ini
[Unit]
Description=AI Interviewer Application
After=network.target

[Service]
Type=simple
User=aiinterview
WorkingDirectory=/home/aiinterview/app
ExecStart=/usr/local/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always
Environment="OPENAI_API_KEY=your-key-here"

[Install]
WantedBy=multi-user.target
```

### Enable Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start service
sudo systemctl start ai-interviewer

# Enable on boot
sudo systemctl enable ai-interviewer

# Check status
sudo systemctl status ai-interviewer

# View logs
sudo journalctl -u ai-interviewer -f
```

### Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/ai-interviewer

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/ai-interviewer /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is automatic
```

---

## Environment Variables

### Required
```bash
# Optional but recommended
OPENAI_API_KEY=sk-your-key

# If Tesseract not in PATH
TESSERACT_CMD=/path/to/tesseract

# If FFmpeg not in PATH
FFMPEG_PATH=/path/to/ffmpeg
```

### Setting Variables

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your-key"
```

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="your-key"
```

**Docker:**
```bash
docker run -e OPENAI_API_KEY="your-key" ...
```

**Systemd:**
```ini
Environment="OPENAI_API_KEY=your-key"
```

---

## Performance Optimization

### 1. Resource Allocation

**Memory:**
- Minimum: 2GB RAM
- Recommended: 4GB RAM
- Optimal: 8GB RAM

**CPU:**
- Minimum: 2 cores
- Recommended: 4 cores

**Storage:**
- 5GB for models and cache

### 2. Caching

Streamlit automatically caches:
- Whisper model loading
- OCR configurations

Ensure cache directory has write permissions.

### 3. Model Selection

**Whisper Models:**
```python
# Fastest (default)
SpeechToText(model_size="tiny")  # ~75MB, fastest

# More accurate
SpeechToText(model_size="base")  # ~150MB, good balance
SpeechToText(model_size="small") # ~500MB, better accuracy
```

Choose based on available resources.

### 4. Load Balancing

For high traffic:

```nginx
upstream ai_interviewer {
    server localhost:8501;
    server localhost:8502;
    server localhost:8503;
}

server {
    location / {
        proxy_pass http://ai_interviewer;
    }
}
```

---

## Monitoring

### Health Checks

```python
# Add to app.py
@st.cache_resource
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Metrics

Monitor:
- Response times
- Memory usage
- Error rates
- Active users
- Request counts

Use tools:
- Prometheus + Grafana
- AWS CloudWatch
- Azure Monitor
- Google Cloud Monitoring

---

## Backup & Recovery

### Data Backup

```bash
# Backup user data
tar -czf backup-$(date +%Y%m%d).tar.gz \
  data/ \
  reports/ \
  logs/

# Automated daily backup
0 2 * * * /path/to/backup-script.sh
```

### Database Backup

If using database:
```bash
# PostgreSQL
pg_dump dbname > backup.sql

# MySQL
mysqldump dbname > backup.sql
```

### Restore

```bash
# Extract backup
tar -xzf backup-20241206.tar.gz

# Restore database
psql dbname < backup.sql
```

---

## Security

### 1. API Keys

- Never commit keys to Git
- Use environment variables
- Rotate keys regularly
- Use secrets management (AWS Secrets Manager, Azure Key Vault)

### 2. Network Security

```bash
# Firewall
sudo ufw enable
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp # HTTPS
sudo ufw deny 8501/tcp # Block direct Streamlit access
```

### 3. HTTPS Only

- Always use SSL in production
- Redirect HTTP to HTTPS
- Use HSTS headers

### 4. Authentication

Add authentication layer:
```python
import streamlit as st

def check_password():
    def password_entered():
        if st.session_state["password"] == "correct_password":
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("Password incorrect")
        return False
    else:
        return True

if check_password():
    # Main app code
    pass
```

---

## Troubleshooting Deployment

### Issue: Tesseract not found

**Solution:**
```dockerfile
# Dockerfile
RUN apt-get install -y tesseract-ocr tesseract-ocr-eng

# Or set path
ENV TESSERACT_CMD=/usr/bin/tesseract
```

### Issue: FFmpeg not found

**Solution:**
```dockerfile
RUN apt-get install -y ffmpeg
```

### Issue: Out of memory

**Solution:**
- Increase container memory
- Use smaller Whisper model
- Optimize image processing
- Add swap space

### Issue: Slow performance

**Solution:**
- Use faster Whisper model
- Compress images before upload
- Add caching
- Use CDN for static files

---

## Cost Optimization

### Cloud Costs

**AWS EC2:**
- t2.micro (free tier): $0/month
- t2.medium: ~$30/month
- Reserved instance: -40% savings

**Streamlit Cloud:**
- Free tier: $0
- Pro: $20/month per app

**Docker + DO/Linode:**
- 2GB RAM: $12-15/month

### OpenAI API Costs

- GPT-3.5-turbo: $0.002/1K tokens
- Average interview: ~500-1000 tokens
- Cost per interview: ~$0.001-0.002
- 1000 interviews/month: ~$1-2

### Optimization Tips

1. Cache question templates
2. Use fallback for non-critical questions
3. Batch processing
4. Compress uploaded files
5. CDN for static content

---

## Scaling

### Horizontal Scaling

```yaml
# docker-compose-scaled.yml
version: '3.8'

services:
  ai-interviewer:
    image: ai-interviewer:latest
    deploy:
      replicas: 3
    ports:
      - "8501-8503:8501"
```

### Load Balancer

```nginx
upstream ai_backend {
    least_conn;
    server app1:8501 max_fails=3 fail_timeout=30s;
    server app2:8501 max_fails=3 fail_timeout=30s;
    server app3:8501 max_fails=3 fail_timeout=30s;
}
```

### Database for Sessions

For multi-instance deployment:
- Redis for session state
- PostgreSQL for data
- S3/Cloud Storage for files

---

## Maintenance

### Updates

```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart ai-interviewer
```

### Logs Rotation

```bash
# /etc/logrotate.d/ai-interviewer
/var/log/ai-interviewer/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 aiinterview aiinterview
    sharedscripts
    postrotate
        systemctl reload ai-interviewer
    endscript
}
```

---

## Checklist

### Pre-Deployment
- [ ] Test locally
- [ ] Update requirements.txt
- [ ] Set environment variables
- [ ] Configure secrets
- [ ] Test with sample data
- [ ] Check resource requirements

### Deployment
- [ ] Install system dependencies
- [ ] Install Python packages
- [ ] Configure firewall
- [ ] Set up SSL
- [ ] Configure monitoring
- [ ] Set up backups
- [ ] Test application

### Post-Deployment
- [ ] Monitor logs
- [ ] Check performance
- [ ] Verify functionality
- [ ] Load testing
- [ ] Security audit
- [ ] Documentation update

---

**For deployment assistance, refer to platform-specific documentation and the main DOCUMENTATION.md file.**

