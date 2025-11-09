# Project Wizard - Quick Start Guide

## 🚀 Access URLs

- **v1.0 (Production):** http://10.69.1.86:8501
- **v2.0 (MVP - Recommended):** http://10.69.1.86:8502

## 📝 v2.0 Workflow (6 Steps)

### Step 1: Project Initiation Request
Fill in:
- Project Name & Owner
- Business Need (what problem you're solving)
- Desired Outcomes (what you want to achieve)
- Success Criteria (how you'll measure success)
- Initial Risks & Assumptions

**Example:**
> **Business Need:** "The current website for Texas Pulmonary is outdated and difficult to navigate for patients seeking information about our services."

### Step 2: Business Case
Fill in:
- Strategic Alignment (how it connects to organizational goals)
- Potential Solutions Considered (optional)
- Preferred Solution/Approach
- Measurable Benefits
- High-Level Requirements
- Budget & Duration Estimates

### Step 3: AI Enhancement ✨
- Review each section individually
- Click "Enhance" to get AI-polished version
- Choose: Accept / Reject / Edit Manually
- AI will NOT add metrics or data you didn't provide

### Step 4: Generate Charter
- Click "Generate Charter Document"
- Review the generated PROJECT CHARTER
- Download as Markdown file
- Uses YOUR data only (no AI hallucination)

### Step 5: Quality Review 🎯
- Click "Run Quality Critique"
- See scores for 6 PM criteria
- Get actionable feedback
- 75% threshold for passing

### Step 6: Create Project 🚧
- Coming soon: Project scaffolding
- Coming soon: OpenProject integration

---

## 🔧 Service Management

### Check Status
```bash
ps aux | grep streamlit
```

### View Logs
```bash
# v1.0 (systemd service)
sudo journalctl -u project-wizard-web -f

# v2.0 (manual launch)
tail -f /tmp/v2_output.log
```

### Restart Services
```bash
# v1.0
sudo systemctl restart project-wizard-web

# v2.0
pkill -f "streamlit run.*app_streamlit_v2.py"
cd /home/ivesjl/project_wizard
nohup /home/ivesjl/project_wizard/venv/bin/streamlit run app_streamlit_v2.py \
  --server.port 8502 --server.address 0.0.0.0 > /tmp/v2_output.log 2>&1 &
```

---

## 💡 Tips for Best Results

### Writing Business Need
- Be specific about the problem
- Include context (who, what, when, where)
- Only include metrics you actually have
- Don't worry about perfect phrasing - AI will enhance

### Writing Success Criteria
- Make it measurable when possible
- Use concrete indicators
- If you don't have exact numbers, describe qualitative measures

### Using AI Enhancement
1. Write naturally in your own words
2. Let AI restructure for professional clarity
3. Review the enhanced version carefully
4. Edit manually if needed - you have full control

### Dealing with AI Critique
- Scores below 7/10 need attention
- Read feedback carefully - it's actionable
- Overall score <75% means significant revision needed
- Don't stress about perfection - iterate

---

## 📊 What's Different in v2.0?

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Input | Single form | Structured workflow |
| Control | All-or-nothing | Step-by-step review |
| Editing | Limited | Full manual control |
| Hallucination | Possible | Eliminated |
| Methodology | Generic | Formal PM |

---

## 🆘 Troubleshooting

### "AI Enhancement Failed"
- Check `/tmp/v2_output.log` for errors
- Verify OpenAI API key in `configs/ai_config.yaml`
- Ensure internet connectivity

### "Port Already in Use"
```bash
# Find and kill the process
lsof -i :8502
kill <PID>
```

### "Page Not Loading"
- Check firewall: `sudo ufw status`
- Verify service is running: `ps aux | grep streamlit`
- Check logs for errors

---

## 📞 Support

For issues or questions:
1. Check logs first
2. Review `V2_IMPLEMENTATION_COMPLETE.md`
3. Test with simple example project

---

**Current Status:** v2.0 MVP Complete ✅
**Next:** User validation with real projects
