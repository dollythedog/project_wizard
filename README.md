# Project Wizard 🧙‍♂️

**AI-Powered Project Management Automation Tool**

An intelligent web application that guides you through creating professional project charters following formal project management methodology. Designed to eliminate "setup paralysis" for developers with ADHD by providing structured workflows and AI assistance.

## Current Version: 2.0.0

**Status:** ✅ MVP Complete - Production Ready

## What's New in v2.0

🎯 **Structured PM Methodology** - Step-by-step workflow following formal project initiation → business case → charter process  
✨ **AI Enhancement (No Hallucination)** - Polishes your text for clarity WITHOUT adding fabricated data  
✏️ **Full Manual Control** - Accept, reject, or edit AI suggestions at every step  
📊 **Quality Critique** - AI evaluates your charter against 6 PM best practice criteria  
🚀 **Web Interface** - Clean, intuitive Streamlit app accessible from any browser  
💾 **Export Ready** - Download professional markdown charters for OpenProject integration

## Quick Start

### Access the Web App

**v2.0 (Recommended):** http://10.69.1.86:8502  
**v1.0 (Legacy):** http://10.69.1.86:8501

### Create a Project Charter in 6 Steps

1. **Project Initiation** - Define business need, desired outcomes, success criteria
2. **Business Case** - Strategic alignment, solution approach, benefits, requirements
3. **AI Enhancement** - Optional AI polish (preserves your facts, improves clarity)
4. **Generate Charter** - Professional PROJECT_CHARTER.md from your data
5. **Quality Review** - AI critique with actionable feedback (6 criteria, 75% threshold)
6. **Create Project** - Scaffold structure & OpenProject integration (coming soon)

## Features

### Core Capabilities
- **Guided Data Collection:** Structured forms with helpful prompts and examples
- **AI Text Enhancement:** Improve clarity and professionalism without adding facts
- **Anti-Hallucination Design:** AI only restructures your text, never invents metrics
- **Quality Assurance:** Automated charter review against PM rubric
- **Manual Override:** Full control - edit anything at any point
- **Markdown Export:** Download charters ready for documentation

### Technical Features
- **OpenAI Integration:** GPT-4o-mini for cost-effective AI assistance (~$0.004/charter)
- **Structured Prompts:** JSON-based prompt library prevents AI confabulation
- **Session Persistence:** Form data saved across tabs
- **Real-time Validation:** Field-level error checking
- **Responsive Design:** Works on desktop and tablet

## Architecture

### v2.0 Stack
```
Frontend: Streamlit (Python web framework)
AI Engine: OpenAI GPT-4o-mini via API
Backend: FastAPI agents (CharterAgent, CriticAgent)
Config: YAML + JSON (ai_config.yaml, enhancement_prompts.json, rubric_charter.json)
Storage: Session state + file export
```

### Project Structure
```
project_wizard/
├── app/
│   └── services/
│       └── ai_agents/
│           ├── charter_agent.py      # Enhancement logic
│           ├── critic_agent.py       # Quality review
│           └── llm_client.py         # OpenAI wrapper
├── configs/
│   ├── ai_config.yaml                # AI settings
│   ├── enhancement_prompts.json      # Anti-hallucination prompts
│   └── rubric_charter.json           # Quality criteria
├── app_streamlit_v2.py               # v2.0 web app (6 tabs)
├── app_streamlit.py                  # v1.0 legacy app
├── .env                              # OpenAI API key
└── docs/                             # Documentation
```

## Usage Guide

### Tab 1: Project Initiation Request
Fill in the core problem definition:
- **Project Name & Owner** - Basic identification
- **Business Need** - What problem are you solving? (Be specific, no fabrication)
- **Desired Outcomes** - What success looks like qualitatively
- **Success Criteria** - Measurable indicators (metrics if you have them)
- **Initial Risks** - Known risks and assumptions

**Example:**
> **Business Need:** "The current website for Texas Pulmonary is outdated and difficult to navigate for patients seeking information about our services."

### Tab 2: Business Case
Justify the project:
- **Strategic Alignment** - Connection to organizational goals
- **Potential Solutions** - Alternatives considered (optional)
- **Preferred Solution** - Recommended approach with rationale
- **Measurable Benefits** - Expected value delivery
- **High-Level Requirements** - Technical, functional, compliance needs
- **Budget & Duration** - Resource estimates

### Tab 3: AI Enhancement
Review and polish each section:
1. Click "✨ Enhance" to get AI-improved version
2. Review the enhanced text (NO fabricated data added)
3. Choose: ✅ Accept | ❌ Reject | ✏️ Edit Manually
4. Manual edits are fully supported with save functionality

**Pro Tip:** Write naturally in your own words first. AI will restructure for professional clarity while preserving all your facts.

### Tab 4: Generate Charter
Click "Generate Charter Document" to create:
- Professional markdown structure
- All 9 sections populated with YOUR data
- Date and status headers
- Approval signature lines
- Download button for .md file

### Tab 5: Quality Review
Run AI critique to get:
- **Overall Score** - Percentage based on weighted criteria (75% threshold)
- **6 Detailed Evaluations** - Clarity, Scope, Risks, Success Criteria, Alignment, Stakeholders
- **Strengths & Weaknesses** - Per criterion feedback
- **Improvements** - Specific actionable recommendations
- **Critical Gaps** - Major issues to address
- **Next Steps** - Prioritized action items

### Tab 6: Create Project
*Coming in v2.1:*
- Scaffold complete project folder structure
- Generate README.md, CHANGELOG.md, LICENSE.md
- Initialize git repository
- Create OpenProject tasks via API
- Set up project board with dependencies

## Installation

### Requirements
- Python 3.10+
- OpenAI API key
- Ubuntu/Linux server (Windows/Mac work too)

### Setup

```bash
# Clone repository
cd /home/ivesjl/project_wizard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env

# Run v2.0
streamlit run app_streamlit_v2.py --server.port 8502 --server.address 0.0.0.0
```

### Production Deployment

```bash
# Start v2.0 service (background)
nohup venv/bin/streamlit run app_streamlit_v2.py \
  --server.port 8502 --server.address 0.0.0.0 > /tmp/v2_output.log 2>&1 &

# Check status
ps aux | grep streamlit

# View logs
tail -f /tmp/v2_output.log

# Stop service
pkill -f "streamlit run.*app_streamlit_v2.py"
```

## Configuration

### AI Settings (`configs/ai_config.yaml`)
```yaml
openai:
  model: gpt-4o-mini          # Cost-effective option
  temperature: 0.4            # Balanced creativity
  max_tokens: 2000

features:
  ai_assist:
    enabled: true
    auto_critique: true
    show_drafts: true
```

### Enhancement Prompts (`configs/enhancement_prompts.json`)
Structured prompts with:
- Meta-level constraints (NEVER invent metrics)
- Per-field instructions with examples
- Forbidden actions (no fabricating data)
- Max word limits
- Tone and format specifications

### Quality Rubric (`configs/rubric_charter.json`)
Six weighted criteria:
- Clarity of Goal (20%)
- Scope & Deliverables (20%)
- Risks & Mitigations (15%)
- Success Criteria (15%)
- Strategic Alignment (15%)
- Stakeholders & Resources (15%)

Threshold: 75% for passing

## Cost Analysis

**OpenAI API Usage (gpt-4o-mini):**
- Enhancement (7 fields): ~$0.0021
- Quality critique: ~$0.0020
- **Total per charter: ~$0.004**

**Monthly estimate (20 charters):** ~$0.08

Extremely cost-effective compared to manual PM time.

## Troubleshooting

### "OpenAI API key not found"
Check `.env` file exists with valid key:
```bash
cat .env
# Should show: OPENAI_API_KEY=sk-...
```

### "AI Enhancement Failed"
Check logs: `tail -f /tmp/v2_output.log`  
Verify internet connectivity and API quota.

### "Page Not Loading"
- Verify service running: `ps aux | grep streamlit`
- Check firewall: `sudo ufw status`
- Test locally: `curl http://localhost:8502`

### "Critique Shows 0% Score"
This was fixed in v2.0.0. Clear browser cache or restart service.

## Development Roadmap

### v2.1 (Next)
- [ ] Project scaffolding (Tab 6)
- [ ] OpenProject API integration
- [ ] Automated task creation from charter
- [ ] Project board setup
- [ ] Template library (software, research, clinical, etc.)

### v2.2 (Future)
- [ ] Multi-user support with authentication
- [ ] Charter version history and comparison
- [ ] Custom rubric editor
- [ ] Export to PDF/DOCX
- [ ] Integration with GitHub Projects

### v3.0 (Vision)
- [ ] Phase 2: Project planning (WBS, Gantt charts)
- [ ] Phase 3: Execution tracking
- [ ] Phase 4: Closure and lessons learned
- [ ] Full project lifecycle management

## Design Philosophy

### ADHD-Friendly Principles
1. **Eliminate Setup Paralysis** - Guided workflow removes decision fatigue
2. **Discrete Actionable Steps** - One thing at a time, clear progress
3. **Instant Scaffolding** - Complete structure ready immediately
4. **No Surprises** - Full control, transparent AI actions
5. **Professional Output** - First draft is usable, not embarrassing

### Technical Principles
1. **User Data is Truth** - AI enhances, never invents
2. **Conservative Temperature** - Consistency over creativity (0.3-0.4)
3. **Explicit Constraints** - Meta-prompts prevent hallucination
4. **Template Over Generation** - Structure from data, not AI imagination
5. **Fail Gracefully** - Errors return user's original text

## Contributing

This is a personal project for managing my own projects, but improvements welcome:

```bash
# Fork, create feature branch
git checkout -b feature/your-feature

# Make changes, test thoroughly
streamlit run app_streamlit_v2.py

# Commit with conventional commits format
git commit -m "feat: add custom template support"

# Push and create PR
git push origin feature/your-feature
```

## Documentation

- **QUICK_START.md** - User guide with examples
- **V2_IMPLEMENTATION_COMPLETE.md** - Technical implementation details
- **CRITIQUE_FIX.md** - Data structure fix documentation
- **PROJECT_CHARTER.md** - This project's own charter
- **PROJECT_PLAN.md** - Development roadmap
- **CHANGELOG.md** - Version history
- **ISSUES.md** - Known issues and resolutions

## License

MIT License - Use freely, attribution appreciated

## Author

**dollythedog** - Building tools to tame project chaos, one charter at a time

## Acknowledgments

- OpenAI for accessible AI APIs
- Streamlit for amazing web framework
- The PM community for formal methodology
- My ADHD for forcing me to build this 😅

---

**Need Help?** Check QUICK_START.md or review V2_IMPLEMENTATION_COMPLETE.md for technical details.

**Ready to use:** http://10.69.1.86:8502 🚀
