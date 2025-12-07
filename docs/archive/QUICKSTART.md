# Quick Start Guide - Project Wizard v3.0 🚀

**Get your AI-powered document generation system running in 5 minutes!**

---

## Prerequisites

- Python 3.11+ installed
- OpenAI API key OR Anthropic API key
- Git (to clone/update the repository)

---

## Step 1: Configure Your API Key (2 minutes)

### Option A: Using OpenAI (GPT-4)

1. Get your API key from https://platform.openai.com/api-keys
2. Copy the example config:
   ```powershell
   cp .env.example .env
   ```
3. Edit `.env` and add your key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   LLM_PROVIDER=openai
   MODEL_NAME=gpt-4o
   ```

### Option B: Using Anthropic (Claude)

1. Get your API key from https://console.anthropic.com/settings/keys
2. Copy the example config:
   ```powershell
   cp .env.example .env
   ```
3. Edit `.env` and add your key:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   LLM_PROVIDER=anthropic
   MODEL_NAME=claude-3-5-sonnet-20241022
   ```

---

## Step 2: Install Dependencies (1 minute)

```powershell
# Make sure you're in the project_wizard directory
cd C:\projects\project_wizard

# Install required packages
pip install -r requirements.txt
```

---

## Step 3: Start the Web Server (30 seconds)

```powershell
python run_web.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Database initialized at data\project_wizard.db
```

---

## Step 4: Test the System (2 minutes)

### Navigate to the Web UI
Open your browser: **http://localhost:8000**

### Create Your First Project

1. Click **"+ New Project"**
2. Fill in:
   - **Title**: Healthcare Monitoring MVP
   - **Type**: software_mvp
   - **Description**: Post-discharge patient monitoring via SMS
3. Click **"Create Project"**

### Add Some Context

Click **"Add Note"** and create 2-3 notes:

**Note 1: System Requirements**
```
- SMS-based patient check-ins
- Weekly CSV patient imports
- HIPAA compliance required
- No PHI in SMS messages
- Twilio for SMS delivery
```

**Note 2: Technical Stack**
```
- Backend: Python FastAPI
- Database: PostgreSQL with encryption
- Frontend: Simple web dashboard
- Hosting: Local MiniPC
```

**Note 3: User Workflow**
```
1. System sends daily SMS check-in
2. Patient responds yes/no
3. System triages responses
4. Alerts sent for concerning responses
5. Weekly CSV updates patient list
```

### Generate Your First Document

1. Click **"📄 Generate Document"**
2. Select **"Project Charter"**
3. Answer the AI-generated questions (5-7 questions)
4. Wait 30-60 seconds for generation
5. **Review your draft!** 🎉

### What You'll Get

- A complete project charter (3-5 pages)
- Context from your notes integrated throughout
- Executive summary
- Token usage stats
- Copy to clipboard or download as `.md`

---

## Step 5: Try More Documents

With the same project, generate:
- **Work Plan** - Detailed implementation roadmap
- **Proposal** - Professional project proposal

Each document uses the same project context but with different perspectives!

---

## Troubleshooting

### "Missing API Key" Error
- Make sure `.env` file exists in the root directory
- Check that your API key starts with `sk-` (OpenAI) or `sk-ant-` (Anthropic)
- Restart the server after adding the key: `Ctrl+C` then `python run_web.py`

### "Module Not Found" Error
```powershell
pip install -r requirements.txt
```

### Database Not Found
The database is created automatically on first run at `data/project_wizard.db`. If you see errors, delete it and restart:
```powershell
rm data/project_wizard.db
python run_web.py
```

### Port 8000 Already in Use
Edit `run_web.py` and change the port:
```python
uvicorn.run(app, host="127.0.0.1", port=8001)  # Change to 8001
```

---

## What's Next?

See `PROJECT_PLAN.md` for:
- **Phase 3 Enhancements**: Verification agent, file uploads, memory system
- **Phase 4 Production**: Docker deployment, authentication, PostgreSQL

For now, enjoy your AI-powered document generator! 🎉

---

## Need Help?

- Read: `README.md` for architecture overview
- Check: `docs/PHASE1_COMPLETION.md` for blueprint system details
- Review: `docs/SPRINT_2.1_COMPLETE.md`, `docs/SPRINT_2.2_COMPLETE.md`, `docs/SPRINT_2.3_COMPLETE.md` for implementation notes
