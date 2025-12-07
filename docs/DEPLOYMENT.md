# Deployment Guide - bunto-server

**Last Updated:** 2025-12-07  
**Target Server:** bunto-server (Linux MiniPC)

---

## Overview

This guide covers deploying Project Wizard to your bunto-server for 24/7 access via LAN and Tailscale.

### Access Points
- **LAN:** `http://10.69.1.86:8000`
- **Tailscale:** `http://100.68.98.103:8000`
- **Reverse Proxy (future):** `http://10.69.1.86/project-wizard` or `https://wizard.home.local`

---

## Prerequisites

### On bunto-server
- Python 3.11+ installed
- Git installed
- Sufficient disk space (~500MB for venv + data)
- Port 8000 available (or choose alternative)

### On Desktop
- Git repository up to date
- Syncthing configured (optional, for database sync)

---

## Deployment Steps

### 1. Transfer Codebase to Server

**Option A: Git Clone (Recommended)**
```bash
# SSH into bunto-server
ssh user@10.69.1.86

# Clone the repository
cd /srv
git clone https://github.com/dollythedog/project_wizard.git
cd project_wizard
```

**Option B: Syncthing Sync**
```bash
# On bunto-server, set up Syncthing folder
# Folder ID: project_wizard
# Path: /srv/project_wizard
# Sync with: Desktop-Jonathan-01

# Wait for initial sync to complete
```

---

### 2. Python Environment Setup

```bash
# Navigate to project directory
cd /srv/project_wizard

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install in editable mode (if needed for development)
pip install -e .
```

---

### 3. Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit configuration
nano .env
```

**Required `.env` settings:**
```bash
# AI Provider (choose one)
OPENAI_API_KEY=sk-your-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Database location (default is fine)
DATABASE_URL=sqlite:///data/project_wizard.db

# Server configuration
HOST=0.0.0.0  # Listen on all interfaces (LAN + Tailscale)
PORT=8000
```

**Security Note:** Never commit `.env` file to Git. Keep API keys secure.

---

### 4. Database Setup

```bash
# Create data directory if it doesn't exist
mkdir -p data

# The database will be created automatically on first run
# If migrating from desktop, see "Data Migration" section below
```

---

### 5. Test Run

```bash
# Activate virtual environment
source venv/bin/activate

# Run the server
python run_web.py

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test from desktop browser:**
- LAN: `http://10.69.1.86:8000`
- Tailscale: `http://100.68.98.103:8000`

Press `Ctrl+C` to stop the test server.

---

### 6. Systemd Service (Auto-Start)

Create a systemd service file to run Project Wizard automatically:

```bash
sudo nano /etc/systemd/system/project-wizard.service
```

**Service file contents:**
```ini
[Unit]
Description=Project Wizard - AI Document Generation
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/srv/project_wizard
Environment="PATH=/srv/project_wizard/venv/bin"
ExecStart=/srv/project_wizard/venv/bin/python /srv/project_wizard/run_web.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start the service:**
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable project-wizard

# Start service now
sudo systemctl start project-wizard

# Check status
sudo systemctl status project-wizard
```

**Service management commands:**
```bash
sudo systemctl stop project-wizard      # Stop service
sudo systemctl restart project-wizard   # Restart service
sudo systemctl status project-wizard    # Check status
journalctl -u project-wizard -f         # View logs (real-time)
```

---

## Data Migration

### From Desktop to Server

**Option 1: Copy Database File (Simplest)**
```bash
# On desktop (PowerShell)
scp C:\Projects\project_wizard\data\project_wizard.db user@10.69.1.86:/srv/project_wizard/data/

# On server
cd /srv/project_wizard
# Database is now ready to use
```

**Option 2: Syncthing Sync (Continuous)**
- Set up Syncthing folder for `/data` directory only
- Desktop: `C:\Projects\project_wizard\data`
- Server: `/srv/project_wizard/data`
- Both machines will share the same database

**Option 3: Start Fresh**
- No migration needed
- Database created automatically on first run
- Create new projects via web UI

---

## Syncthing Configuration

### Recommended Setup

**Sync entire project folder** (for development):
- **Desktop:** `C:\Projects\project_wizard`
- **Server:** `/srv/project_wizard`
- **Ignore patterns:** `venv/`, `__pycache__/`, `*.pyc`

**OR sync only data** (for production):
- **Desktop:** `C:\Projects\project_wizard\data`
- **Server:** `/srv/project_wizard/data`
- Shares database and generated outputs between machines

**Syncthing Web UI:**
- Desktop: `http://127.0.0.1:8384`
- Server: `http://10.69.1.86:8384`

---

## Reverse Proxy Setup (Optional)

Use Caddy or NGINX to serve multiple applications on bunto-server.

### Option A: Caddy (Recommended - Simpler)

**Install Caddy:**
```bash
sudo apt install -y caddy
```

**Edit Caddyfile:**
```bash
sudo nano /etc/caddy/Caddyfile
```

**Caddyfile contents:**
```caddy
# Serve on LAN IP
10.69.1.86 {
    # Project Wizard
    handle /project-wizard* {
        reverse_proxy localhost:8000
    }
    
    # Other services
    handle /logseq* {
        reverse_proxy localhost:3000
    }
    
    # Add more services as needed
}
```

**Restart Caddy:**
```bash
sudo systemctl restart caddy
```

**Access Project Wizard:**
- `http://10.69.1.86/project-wizard`

---

### Option B: NGINX

**Install NGINX:**
```bash
sudo apt install -y nginx
```

**Create site configuration:**
```bash
sudo nano /etc/nginx/sites-available/project-wizard
```

**Configuration:**
```nginx
server {
    listen 80;
    server_name 10.69.1.86;

    location /project-wizard/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/project-wizard /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

---

## Firewall Configuration

If using UFW (Uncomplicated Firewall):

```bash
# Allow port 8000 from LAN only
sudo ufw allow from 10.69.1.0/24 to any port 8000

# Or allow from anywhere (if using Tailscale)
sudo ufw allow 8000/tcp

# If using reverse proxy, allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Check status
sudo ufw status
```

---

## Monitoring & Logs

### View Application Logs
```bash
# Real-time logs
journalctl -u project-wizard -f

# Last 100 lines
journalctl -u project-wizard -n 100

# Logs from today
journalctl -u project-wizard --since today
```

### Check Server Resources
```bash
# Disk usage
df -h

# Memory usage
free -h

# Running processes
ps aux | grep python
```

---

## Backup Strategy

### Database Backup Script

Create a daily backup script:

```bash
nano /srv/scripts/backup-project-wizard.sh
```

**Script contents:**
```bash
#!/bin/bash
# Backup Project Wizard database

DATE=$(date +%Y-%m-%d)
BACKUP_DIR="/srv/backups/project_wizard"
DB_PATH="/srv/project_wizard/data/project_wizard.db"

mkdir -p $BACKUP_DIR
sqlite3 $DB_PATH ".backup '$BACKUP_DIR/project_wizard_$DATE.db'"

# Keep last 30 days only
find $BACKUP_DIR -name "*.db" -mtime +30 -delete

echo "Backup complete: project_wizard_$DATE.db"
```

**Make executable and schedule:**
```bash
chmod +x /srv/scripts/backup-project-wizard.sh

# Add to crontab (daily at 2 AM)
crontab -e

# Add this line:
0 2 * * * /srv/scripts/backup-project-wizard.sh >> /var/log/project-wizard-backup.log 2>&1
```

---

## Troubleshooting

### Service Won't Start
```bash
# Check logs
journalctl -u project-wizard -n 50

# Common issues:
# - Port 8000 already in use → Change PORT in .env
# - Virtual environment not found → Verify paths in service file
# - Missing API key → Check .env file
```

### Cannot Access from Desktop
```bash
# On server, verify service is running
sudo systemctl status project-wizard

# Check if port is listening
sudo netstat -tulpn | grep 8000

# Check firewall
sudo ufw status

# Test from server itself
curl http://localhost:8000
```

### Database Locked Errors (with Syncthing)
- SQLite doesn't handle concurrent writes well over network sync
- **Solution:** Only run Project Wizard on ONE machine at a time
- OR use separate databases per machine

---

## Upgrading

### Pull Latest Changes from Git
```bash
cd /srv/project_wizard
git pull origin main

# Restart service
sudo systemctl restart project-wizard
```

### Update Dependencies
```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
sudo systemctl restart project-wizard
```

---

## Security Considerations

1. **API Keys:** Never commit `.env` file, use environment variables only
2. **Network Access:** Use firewall to restrict access to LAN/Tailscale only
3. **HTTPS:** Consider using Caddy with automatic TLS for external access
4. **Authentication:** Web UI currently has no authentication (add if needed)
5. **Backups:** Regularly backup database to prevent data loss

---

## Next Steps

1. ✅ Deploy to bunto-server using this guide
2. ✅ Test access from desktop and phone (via Tailscale)
3. ✅ Set up Syncthing for data sync (if desired)
4. ✅ Configure systemd for auto-start
5. ✅ Set up daily database backups
6. ⏭️ Integrate with Logseq (see `docs/LOGSEQ_INTEGRATION.md`)
7. ⏭️ Set up reverse proxy with Caddy (optional)

---

## Related Documentation

- `README.md` - Project overview and quick start
- `PROJECT_PLAN.md` - Architecture and development roadmap
- `docs/LOGSEQ_INTEGRATION.md` - Logseq integration architecture
- `CHANGELOG.md` - Version history

---

**Questions or issues?** Check logs first, then refer to troubleshooting section.
