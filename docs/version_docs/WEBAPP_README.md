# 🧙‍♂️ AI Project Wizard - Web Interface

**Beautiful Streamlit UI for AI-powered project charter generation**

## 🚀 Quick Start

### Launch the Web App

```bash
cd /home/ivesjl/project_wizard
./run_webapp.sh
```

**Access at:**
- Local: http://localhost:8501
- Network: http://<your-server-ip>:8501

## 🎨 Features

### Tab 1: Draft Charter
- **Input:** Project brief (3-5 sentences)
- **Output:** AI generates all 7 charter sections in ~30 seconds
- **Progress bar:** Shows generation progress

### Tab 2: AI Sections
- **Review & Edit:** All AI-generated sections in expandable panels
- **Interactive editing:** Modify any section before finalizing
- **Save:** Persist all edits to session

### Tab 3: Critique
- **AI Quality Review:** Runs CriticAgent against 6 criteria
- **Overall Score:** Weighted score with pass/fail (75% threshold)
- **Detailed Feedback:** Strengths, weaknesses, improvements per criterion
- **Critical Gaps:** Highlighted issues to address

### Tab 4: Export
- **Preview:** Full charter markdown preview
- **Download:** Export charter as `.md` file
- **Download Critique:** Export critique as JSON

## 🎯 Workflow

1. **Configure** (sidebar):
   - Project title, type, department
   - Budget, duration
   - Sponsor name

2. **Describe** (Tab 1):
   - Brief project description
   - Click "Generate with AI"

3. **Review** (Tab 2):
   - Edit AI drafts as needed
   - Save all sections

4. **Critique** (Tab 3):
   - Run AI quality review
   - See scores and feedback

5. **Export** (Tab 4):
   - Download charter markdown
   - Download critique JSON

## 💰 Cost Per Charter

~$0.002 (less than 1/4 penny) per full charter generation + critique

## 🔧 Configuration

The app uses:
- `.env` - OpenAI API key
- `configs/ai_config.yaml` - Model settings
- `configs/rubric_charter.json` - Quality criteria

## 📦 Tech Stack

- **Frontend:** Streamlit
- **Backend:** CharterAgent, CriticAgent
- **LLM:** OpenAI gpt-4o-mini
- **Cost:** ~$0.002 per charter

## 🐳 Production Deployment

### Option 1: Systemd Service

```bash
sudo nano /etc/systemd/system/project-wizard-web.service
```

```ini
[Unit]
Description=AI Project Wizard Web Interface
After=network.target

[Service]
Type=simple
User=ivesjl
WorkingDirectory=/home/ivesjl/project_wizard
ExecStart=/home/ivesjl/project_wizard/run_webapp.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable project-wizard-web
sudo systemctl start project-wizard-web
```

### Option 2: Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Option 3: Reverse Proxy (Nginx)

```nginx
location /project-wizard/ {
    proxy_pass http://localhost:8501/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}
```

## 🔒 Security

**For production:**
- Add authentication (Streamlit Cloud, OAuth, etc.)
- Use HTTPS (reverse proxy with SSL)
- Restrict network access (firewall rules)
- Set API rate limits

## 🎨 Customization

Edit `app_streamlit.py` to:
- Change branding/colors
- Add more sections
- Customize rubric
- Add export formats (PDF, DOCX)

## 📊 Features vs. CLI

| Feature | Web App | CLI (`project-wizard init`) |
|---------|---------|----------------------------|
| AI Charter Drafting | ✅ | ⏳ (Phase 2) |
| Interactive Editing | ✅ | ❌ |
| Visual Critique | ✅ | ❌ |
| Export MD/JSON | ✅ | ✅ |
| Folder Structure | ❌ | ✅ |
| Git Init | ❌ | ✅ |
| OpenProject Sync | ❌ | ⏳ (Phase 3) |

## 🔮 Future Enhancements

- [ ] Multi-user support (save/load projects)
- [ ] Project history & versioning
- [ ] Export to PDF/DOCX
- [ ] OpenProject integration (create work packages)
- [ ] Team collaboration (comments, approvals)
- [ ] Template library
- [ ] AI-powered work breakdown (Phase 3)

## 🐛 Troubleshooting

**App won't start:**
```bash
# Check if port 8501 is in use
sudo lsof -i :8501

# Try different port
./venv/bin/streamlit run app_streamlit.py --server.port 8502
```

**API errors:**
- Check `.env` has valid `OPENAI_API_KEY`
- Verify billing is enabled on OpenAI account

**Session state issues:**
- Refresh browser
- Clear Streamlit cache (Settings → Clear cache)

## 📚 Documentation

- **Main README:** `README.md`
- **AI Agents:** `AI_AGENTS_README.md`
- **Quick Start:** `QUICKSTART_AI.md`
- **Build Summary:** `AI_BUILD_SUMMARY.txt`

---

**Built by:** Jonathan Ives  
**Organization:** Texas Pulmonary & Critical Care Consultants  
**Date:** November 2025
