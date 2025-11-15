# Project Wizard

**Version:** 2.7.0  
**Status:** ✅ Production Ready - Modular Architecture

An AI-powered project scaffolding and document generation tool designed to help you start projects the right way—with proper structure, documentation, and AI-driven pattern-based deliverables.

## 🎯 What Is This?

Project Wizard is a tool to create well-organized projects with all the boilerplate documentation and structure you need to work effectively with AI agents. It helps you:

- **Bootstrap new projects** with standardized folder structure
- **Generate project charters** with AI assistance
- **Create pattern-based deliverables** (proposals, work plans, 5W1H analyses)
- **Export to OpenProject** with one-click work package creation
- **Maintain project documentation** (README, CHANGELOG, ISSUES)
- **Manage multiple projects** through a visual gallery interface

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
cd ~/project_wizard

# Install dependencies
pip install -r requirements.txt

# Set up your OpenAI API key
echo "OPENAI_API_KEY=your-key-here" > .env

# Run the app
streamlit run app.py
```

### First Use

1. **Create a new project**: Click "Start New Project" in the welcome screen
2. **Generate a charter**: Use the Charter tab to define your project with AI assistance
3. **Create deliverables**: Use the Deliverables tab to generate documents from patterns
4. **Export to OpenProject**: Click the upload button to create work packages automatically
5. **Manage documentation**: Use the Documentation tab to view and edit project files

### OpenProject Integration (Optional)

Project Wizard can export your WORK_PLAN.md files to OpenProject, creating structured projects with work packages:

1. Get your API key from OpenProject (My Account > Access tokens)
2. Add to `.env`:
   ```bash
   OPENPROJECT_URL=http://10.69.1.86:8080
   OPENPROJECT_API_KEY=your-api-key-here
   ```
3. In any project, go to Deliverables → Work Plan → Click "📤 Upload to OpenProject"

See [docs/OPENPROJECT_INTEGRATION.md](docs/OPENPROJECT_INTEGRATION.md) for detailed setup.

## 📁 Project Structure

```
project_wizard/
├── app.py                     # Main Streamlit application (modular)
├── app/                       # Application modules
│   ├── components/            # Reusable UI components
│   │   └── document_editor.py
│   ├── configs/               # Configuration files
│   ├── models/                # Data models
│   │   └── charter.py
│   ├── services/              # Business logic services
│   │   ├── ai_agents/         # AI agent implementations
│   │   │   ├── charter_agent.py
│   │   │   ├── critic_agent.py
│   │   │   ├── draft_agent.py
│   │   │   ├── editor_agent.py
│   │   │   └── llm_client.py
│   │   ├── document_generator.py
│   │   ├── document_registry.py
│   │   ├── openproject_exporter.py  # Export work plans to OpenProject
│   │   ├── pattern_pipeline.py
│   │   ├── pattern_registry.py
│   │   ├── project_context.py
│   │   ├── project_registry.py
│   │   ├── project_scaffolder.py
│   │   └── repo_bootstrapper.py
│   ├── state/                 # Session state management
│   ├── templates/             # Project templates
│   │   └── core_docs/         # README, CHANGELOG, ISSUES templates
│   ├── ui/                    # UI components
│   │   ├── tabs/              # Tab implementations
│   │   │   ├── charter_tab.py
│   │   │   ├── deliverables_tab.py
│   │   │   ├── docs_tab.py
│   │   │   └── home_tab.py
│   │   ├── modals/            # Modal dialogs
│   │   ├── pattern_form.py
│   │   ├── project_selector.py
│   │   └── sidebar.py
│   └── utils/                 # Utility functions
├── patterns/                  # AI pattern definitions
│   ├── project_charter/       # Project charter pattern
│   ├── proposal/              # Project proposal pattern
│   ├── 5w1h_analysis/         # 5W1H analysis pattern
│   └── work_plan/             # Work plan pattern
├── docs/                      # Documentation
│   └── archive/               # Historical documentation
├── scripts/                   # Utility scripts
├── README.md                  # This file
├── CHANGELOG.md               # Version history
├── ISSUES.md                  # Issue tracking
├── PROJECT_PLAN.md            # Implementation roadmap
├── PROJECT_CHARTER.md         # Project charter
├── Makefile                   # Development commands
└── requirements.txt           # Python dependencies
```

## 🎨 Available Patterns

Each pattern includes:
- `system.md` - AI system prompt
- `user.md` - User prompt template
- `template.md.j2` - Jinja2 output template
- `variables.json` - Required variables
- `rubric.json` - Critique rubric

### Current Patterns

1. **Project Charter** - Comprehensive project definition with goals, scope, stakeholders
2. **Proposal** - Formal project proposal with problem statement and solution
3. **5W1H Analysis** - Who, What, When, Where, Why, How analysis
4. **Work Plan** - Detailed implementation roadmap with tasks and milestones

## 🔧 Configuration

### Project Registry
Projects are tracked in `~/.project_wizard_projects.json`:

```json
{
  "projects": [
    {
      "name": "My Project",
      "path": "/home/user/Projects/my_project",
      "created_at": "2025-11-14T10:30:00",
      "last_accessed": "2025-11-14T15:45:00"
    }
  ]
}
```

### AI Configuration
Edit `app/configs/ai_config.yaml` to adjust AI behavior:

```yaml
model: gpt-4o-mini
temperature: 0.3
max_tokens: 2000
```

## 💻 Development Commands

Using Make:

```bash
make help        # Show available commands
make install     # Install dependencies
make run         # Run the Streamlit app
make lint        # Run linter (check only)
make lint-fix    # Run linter and auto-fix
make format      # Format code
make check       # Run all checks
make clean       # Clean cache files
```

## 📚 Features

### ✅ Implemented

- **Modular Architecture**: Clean separation of concerns with tabs, components, services
- **AI-Powered Charter Generation**: GPT-4o-mini generates comprehensive project charters
- **Pattern-Based Deliverable Generation**: Create structured documents from AI patterns
- **Document Enhancement**: AI can improve existing documents in chunks
- **Project Gallery**: Visual interface to browse and manage projects
- **Project Registry**: Track all projects with metadata
- **Project Scaffolding**: Auto-create folder structure and boilerplate files
- **Critique System**: AI evaluates documents against rubrics with KPI scores
- **Session State Management**: Persistent state across Streamlit reruns
- **Large Document Support**: Chunked processing for documents >1000 characters

### 🔜 Planned

- **Kanban Board View**: Display ISSUES.md in Kanban format within the app
- **Project Filtering**: Filter issues by project (project_wizard vs created projects)
- **Session Persistence**: Save/resume work sessions
- **Multi-user Support**: Concurrent project editing
- **GitHub Integration**: Auto-sync ISSUES.md with GitHub Issues
- **Custom Pattern Creation**: UI to define new patterns
- **Version Control Integration**: Git operations from UI

## 🐛 Troubleshooting

### OpenAI API Key Not Found
```bash
# Make sure .env file exists with your key
echo "OPENAI_API_KEY=your-key-here" > .env
```

### Project Registry Not Found
Projects are stored in `~/.project_wizard_projects.json`. If missing, create a new project to initialize.

### Import Errors
```bash
# Ensure you're in the project root and venv is activated
cd ~/project_wizard
source venv/bin/activate  # or your venv path
pip install -r requirements.txt
```

## 📖 Documentation

- [`CHANGELOG.md`](CHANGELOG.md) - Version history and changes
- [`ISSUES.md`](ISSUES.md) - Known issues and resolutions
- [`PROJECT_PLAN.md`](PROJECT_PLAN.md) - Implementation roadmap
- [`PROJECT_CHARTER.md`](PROJECT_CHARTER.md) - Project charter

## 🤝 Contributing

This is a personal project but follows best practices:
- PEP 8 style guide for Python
- Conventional commit messages (feat:, fix:, docs:, etc.)
- Keep documentation updated with code changes
- Run `make check` before committing

## 📄 License

Personal project by dollythedog

---

**Project Wizard v2.6.0** - Build projects the right way, from the start  
Powered by OpenAI GPT-4o-mini
