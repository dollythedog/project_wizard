# Project Wizard 🧙‍♂️

**AI-Powered Project Management Automation Tool**

An intelligent web application that guides you through creating professional project charters following formal project management methodology. Designed to eliminate "setup paralysis" for developers with ADHD by providing structured workflows and AI assistance.

## Current Version: 2.5.1

**Status:** ✅ Production Ready with Visual Project Management

## What's New in v2.5.1

🎨 **Visual Project Gallery** - Browse all your projects with icons in a beautiful card-based layout  
➕ **Guided Project Creation** - Step-by-step wizard with icon selection and automatic folder structure  
📂 **Smart Project Registry** - Persistent tracking of projects with metadata (created date, last accessed, type)  
🔄 **Quick Project Switching** - Recent projects in sidebar for one-click navigation  
🏠 **Welcome Dashboard** - Clear entry point when no project is loaded  
🗂️ **Organized Structure** - Projects stored in `~/Projects/` matching cross-platform conventions

### Previous Features (v2.5.0)
📋 **Pattern-Based Workflow** - Dynamic document generation using reusable patterns  
🤖 **AI Agent Pipeline** - Draft → Edit → Critique orchestration  
📊 **Quality Rubrics** - Document-specific evaluation criteria  
🔄 **Living Charter** - Edit, enhance, and iterate on documents

### Core Features (v2.0+)
✨ **AI Enhancement** - Polish text without fabricating data  
📊 **Quality Critique** - Evaluate charters against PM best practices  
✏️ **Full Manual Control** - Accept, reject, or edit AI suggestions  
💾 **Export Ready** - Professional markdown documents

## Quick Start

### 1. Start the Application

```bash
# Navigate to project directory
cd /home/ivesjl/project_wizard

# Activate virtual environment
source venv/bin/activate

# Run v2.5
./run_v2_5.sh
# or
streamlit run app_v2_5.py
```

### 2. Create Your First Project

When you launch the app, you'll see the Welcome screen:

1. **Click "➕ Create New Project"**
2. **Fill in project details:**
   - Project Name (e.g., "Hermes - Trading Application")
   - Choose an icon (🚀, 💼, ⚡, etc.)
   - Select project type
   - Add optional description
   - Confirm project location (defaults to `~/Projects/`)
3. **Click "🚀 Create Project"**
4. **Start working** - You'll be taken directly to your new project

### 3. Create a Project Charter

Navigate through the 4 main tabs:

1. **📝 Initiation** - Define business need, outcomes, success criteria
2. **💼 Business Case** - Strategic alignment, solution approach, benefits
3. **📋 Charter** - Generate, critique, enhance, and save your charter
4. **🏠 Project Home** - Access LEAN/PM activities (5W1H, SIPOC, etc.)

## Project Management Features

### Visual Project Gallery (📚 My Projects)

Browse all your projects in a visual grid:
- **Project cards** with icons, names, and descriptions
- **Quick actions**: Open project, Remove from list
- **Metadata display**: Project type, created date
- **Sortable** by name, created date, or last accessed

### New Project Wizard (➕ New Project)

Guided project creation with:
- **Icon selection** - Choose from 20 emoji options
- **Project type** - Software Development, Process Improvement, Clinical Initiative, Research, Infrastructure, Other
- **Smart naming** - Automatic folder sanitization (spaces → underscores)
- **Path preview** - See where project will be created before confirming
- **Auto-registration** - Projects automatically tracked in registry

### Recent Projects Sidebar

Quick access to your 5 most recent projects:
- **One-click loading** - Click folder icon to switch projects
- **Smart ordering** - Most recently accessed first
- **Visual indicators** - Project icons and names
- **Current project highlight** - See what you're working on

## Architecture

### v2.5.1 Stack
```
Frontend: Streamlit (Python web framework)
Project Registry: JSON-based persistent storage (~/.project_wizard_projects.json)
AI Engine: OpenAI GPT-4o-mini via API
Pattern System: Fabric-inspired reusable document templates
Backend: Specialized AI agents (Charter, Critic, Draft, Editor)
Storage: Project directories in ~/Projects/
```

### Project Structure
```
project_wizard/
├── app/
│   └── services/
│       ├── ai_agents/           # AI service modules
│       ├── project_registry.py  # NEW: Project tracking
│       ├── pattern_registry.py  # Pattern management
│       └── pattern_pipeline.py  # AI orchestration
├── patterns/                    # Document templates
│   ├── 5w1h_analysis/
│   └── project_plan/
├── configs/                     # AI configurations
├── docs/                        # Documentation
│   ├── archive/                # Old docs and backups
│   └── version_docs/           # Version-specific guides
├── app_v2_5.py                 # Main application
├── run_v2_5.sh                 # Startup script
└── README.md                   # This file
```

### User Projects Structure
```
~/Projects/
├── Hermes/
│   ├── PROJECT_CHARTER.md
│   ├── 5W1H_ANALYSIS.md       # Generated via Project Home
│   └── PROJECT_PLAN.md        # Generated via Project Home
└── AnotherProject/
    └── PROJECT_CHARTER.md
```

## Usage Guide

### Managing Projects

#### Opening a Project
1. Click **"📚 My Projects"** in sidebar
2. Browse the project gallery
3. Click **"📂 Open"** on the project you want

OR use **Recent Projects** sidebar for quick access

#### Creating a New Project
1. Click **"➕ New Project"** in sidebar
2. Enter project details and choose icon
3. Optionally change base directory (defaults to `~/Projects/`)
4. Click **"🚀 Create Project"**

#### Switching Between Projects
- Use the **Recent Projects** list in sidebar
- Click the folder icon (📂) next to project name
- Charter automatically loads when switching projects

### Creating Documents

#### Project Charter (Tabs 1-3)

**Tab 1: Initiation**
- Project name, owner, type
- Business need (the problem)
- Desired outcomes (qualitative success)
- Success criteria (measurable indicators)

**Tab 2: Business Case**
- Strategic alignment
- Solution approaches considered
- Preferred solution and rationale
- Measurable benefits
- High-level requirements
- Budget and duration estimates

**Tab 3: Charter**
- **Generate** - Creates professional charter from your data
- **Critique** - AI evaluation against 6 PM criteria
- **Enhance** - AI polish options (wording, tone, simplification)
- **Save** - Writes charter to project directory
- **Download** - Export as markdown file

#### LEAN/PM Activities (Tab 4: Project Home)

Choose from activity menu:
- **📊 Project Plan** - Detailed implementation roadmap
- **❓ 5W1H Analysis** - Who, What, When, Where, Why, How framework
- **🔄 SIPOC** - Supplier, Input, Process, Output, Customer mapping
- **🐟 Fishbone** - Root cause analysis diagram
- **🎤 Voice of Customer** - Customer requirements capture

For each activity:
1. Select from radio menu
2. Click **"✨ Create [Activity]"**
3. Fill in the generated form
4. Click **"✨ Generate"** to create document
5. Download or regenerate as needed

## Configuration

### Project Registry

Location: `~/.project_wizard_projects.json`

Structure:
```json
{
  "/home/user/Projects/MyProject": {
    "name": "My Project",
    "path": "/home/user/Projects/MyProject",
    "description": "Project description",
    "project_type": "Software Development",
    "icon": "🚀",
    "created_date": "2025-11-09T10:00:00",
    "last_modified": "2025-11-09T10:00:00",
    "last_accessed": "2025-11-09T10:30:00"
  }
}
```

### AI Settings

Location: `configs/ai_config.yaml`
- Model: gpt-4o-mini (cost-effective)
- Temperature: 0.3-0.4 (balanced)
- Max tokens: 2000

### Pattern System

Location: `patterns/` directory
- Each pattern has its own folder
- Contains template, variables, and rubric
- Auto-discovered by PatternRegistry

## Installation

### Requirements
- Python 3.10+
- OpenAI API key
- Linux/Ubuntu (Windows/Mac also supported)

### Setup

```bash
# Clone/navigate to repository
cd /home/ivesjl/project_wizard

# Create virtual environment (if not exists)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure OpenAI API key
echo "OPENAI_API_KEY=your_key_here" > .env

# Run application
./run_v2_5.sh
```

### Production Deployment

```bash
# Start service (background)
nohup ./run_v2_5.sh > logs/app.log 2>&1 &

# Check status
ps aux | grep streamlit

# View logs
tail -f logs/app.log

# Stop service
pkill -f "streamlit run.*app_v2_5.py"
```

## Cost Analysis

**OpenAI API Usage per Charter:**
- Charter generation: $0.002
- Quality critique: $0.002
- Enhancements (3x): $0.006
- **Total: ~$0.01 per charter**

**Monthly estimate (50 charters):** ~$0.50

Minimal cost compared to manual PM time.

## Troubleshooting

### Projects Not Showing
- Check `~/.project_wizard_projects.json` exists
- Verify project directory paths are correct
- Click "My Projects" to refresh gallery

### Charter Not Loading
- Ensure `PROJECT_CHARTER.md` exists in project directory
- Check file permissions
- Try clicking "Open" again from gallery

### Cannot Create Project
- Verify write permissions to `~/Projects/`
- Check disk space
- Ensure project name doesn't contain special characters

### AI Enhancement Failed
- Check `.env` file has valid OpenAI API key
- Verify internet connectivity
- Check OpenAI API quota: https://platform.openai.com/usage

## Development Roadmap

### v2.6 (Next)
- [ ] Project templates (software, research, clinical)
- [ ] Project archiving
- [ ] Bulk project operations
- [ ] Project search and filtering

### v2.7 (Future)
- [ ] Project scaffolding (complete folder structure)
- [ ] README/CHANGELOG auto-generation
- [ ] Git integration
- [ ] OpenProject API integration

### v3.0 (Vision)
- [ ] Multi-user support
- [ ] Project sharing and collaboration
- [ ] Version control for charters
- [ ] Export to PDF/DOCX
- [ ] Full project lifecycle (planning → execution → closure)

## Design Philosophy

### ADHD-Friendly Principles
1. **Visual Organization** - See all projects at a glance with icons
2. **Eliminate Setup Paralysis** - Guided workflow, one step at a time
3. **Quick Switching** - Recent projects always accessible
4. **Clear Context** - Always know which project you're in
5. **Instant Scaffolding** - Project structure created automatically

### Technical Principles
1. **User Data is Truth** - AI enhances, never invents
2. **Persistent State** - Projects tracked across sessions
3. **Graceful Degradation** - App works without projects loaded
4. **Clean Organization** - Separate project data from app code
5. **Cross-Platform** - `~/Projects` structure works on Windows/Linux/Mac

## Documentation

- **README.md** - This file (overview and usage)
- **CHANGELOG.md** - Detailed version history
- **ISSUES.md** - Known issues and resolutions
- **PROJECT_PLAN.md** - Development roadmap
- **PROJECT_CHARTER.md** - This project's charter
- **SESSION_SUMMARY.md** - Development session notes
- **PROJECT_MANAGEMENT_UPGRADE.md** - v2.5.1 implementation details
- **docs/QUICK_START.md** - Detailed user guide
- **docs/version_docs/** - Version-specific documentation

## Contributing

Improvements welcome! This is a personal tool but open for collaboration.

```bash
# Fork and create feature branch
git checkout -b feature/your-feature

# Make changes and test
./run_v2_5.sh

# Commit with conventional commits
git commit -m "feat: add project templates"

# Push and create PR
git push origin feature/your-feature
```

## License

MIT License - Use freely, attribution appreciated

## Author

**dollythedog** - Building ADHD-friendly PM tools

## Acknowledgments

- OpenAI for accessible AI APIs
- Streamlit for excellent web framework
- PM community for formal methodology
- Fabric AI pattern system for inspiration

---

**Get Started:** `./run_v2_5.sh` 🚀
