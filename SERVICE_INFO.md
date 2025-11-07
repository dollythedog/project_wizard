# 🧙‍♂️ AI Project Wizard - Service Information

## 🌐 Access URL

**http://10.69.1.86:8501**

Access from any device on your LAN (10.69.1.x network)

---

## 🔧 Service Management

### View Status
```bash
sudo systemctl status project-wizard-web
```

### Start Service
```bash
sudo systemctl start project-wizard-web
```

### Stop Service
```bash
sudo systemctl stop project-wizard-web
```

### Restart Service
```bash
sudo systemctl restart project-wizard-web
```

### View Logs
```bash
sudo journalctl -u project-wizard-web -f
```

### Disable Auto-Start
```bash
sudo systemctl disable project-wizard-web
```

### Enable Auto-Start
```bash
sudo systemctl enable project-wizard-web
```

---

## 📊 Service Details

- **Service Name:** `project-wizard-web.service`
- **Port:** 8501
- **Network:** 0.0.0.0 (all interfaces)
- **Auto-start:** Enabled (starts on boot)
- **Restart:** Automatic (on failure)
- **User:** ivesjl
- **Working Directory:** /home/ivesjl/project_wizard

---

## 🔗 Related Services on This Server

| Service | URL | Port |
|---------|-----|------|
| **AI Project Wizard** | http://10.69.1.86:8501 | 8501 |
| OpenProject | http://10.69.1.86:8080 | 8080 |
| Meeting Minutes Generator | http://10.69.1.86:8502 | 8502 |

---

## 🐛 Troubleshooting

### Check if Service is Running
```bash
sudo systemctl is-active project-wizard-web
```

### Check Port Availability
```bash
sudo lsof -i :8501
```

### Test from Command Line
```bash
curl http://10.69.1.86:8501/_stcore/health
```
Expected: `ok`

### View Recent Errors
```bash
sudo journalctl -u project-wizard-web -n 50 --no-pager
```

### Restart if Issues
```bash
sudo systemctl restart project-wizard-web
sudo systemctl status project-wizard-web
```

---

## 📝 Configuration Files

- **Service File:** `/etc/systemd/system/project-wizard-web.service`
- **App Code:** `/home/ivesjl/project_wizard/app_streamlit.py`
- **API Key:** `/home/ivesjl/project_wizard/.env`
- **Config:** `/home/ivesjl/project_wizard/configs/ai_config.yaml`

---

## 🔄 After Code Changes

If you modify `app_streamlit.py` or AI agents:

```bash
sudo systemctl restart project-wizard-web
```

No need to reload systemd daemon unless you change the service file itself.

---

## 💾 Backup Important Files

```bash
# Backup configuration
cp /home/ivesjl/project_wizard/.env ~/.backups/
cp /home/ivesjl/project_wizard/configs/ai_config.yaml ~/.backups/

# Backup service file
sudo cp /etc/systemd/system/project-wizard-web.service ~/.backups/
```

---

## 📱 Access from Mobile/Tablet

1. Connect to same network (10.69.1.x)
2. Open browser
3. Navigate to: **http://10.69.1.86:8501**

Works on:
- Windows (Chrome, Edge, Firefox)
- Mac (Safari, Chrome)
- iPhone/iPad (Safari)
- Android (Chrome)
- Linux (any browser)

---

## 🔒 Security Notes

**Current Setup:**
- ✅ LAN-only access (not exposed to internet)
- ✅ Runs as non-root user (ivesjl)
- ✅ API key stored securely in .env (600 permissions)

**For Production Enhancement:**
- Consider adding Nginx reverse proxy with SSL
- Add authentication (HTTP Basic Auth or OAuth)
- Set up firewall rules if needed

---

## 💰 Cost Monitoring

View your OpenAI usage:
https://platform.openai.com/usage

Expected monthly cost with 20 charters: ~$0.05

---

**Service Status:** ✅ Running and accessible at http://10.69.1.86:8501
