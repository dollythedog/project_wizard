# Project Wizard 🧙‍♂️

**Your Personal Project Management Automation Tool**

An interactive CLI tool that guides you through creating and managing projects following formal project management methodology, with seamless OpenProject integration.

## Features

✨ **Phase 1: Initiation** - Interactive charter creation wizard  
📋 **Automatic Document Generation** - PROJECT_CHARTER.md, README.md, and more  
🗂️ **Standardized Repository Structure** - Consistent folder layout across all projects  
🎮 **RPG-Style Quest Map** - Gamified project progression tracking  
🔄 **OpenProject Integration** - Sync projects and work packages  
📊 **Project Type Templates** - Pre-configured for common project types  
🐳 **Docker Deployment** - Deploy alongside OpenProject

## Quick Start

### Installation

```bash
cd project_wizard
pip install -e .
```

### Create Your First Project

```bash
project-wizard init
```

Follow the interactive prompts to:
1. Define business case and strategic alignment
2. Set measurable success criteria  
3. Document scope and deliverables
4. Identify risks and mitigation strategies
5. Establish timeline and collaboration needs

The wizard will create:
- Complete folder structure (configs/, data/, scripts/, docs/)
- PROJECT_CHARTER.md with all your inputs
- README.md with project overview
- CONTRIBUTING.md with coding standards (PEP-8, commit conventions)
- CODE_OF_CONDUCT.md (Contributor Covenant)
- LICENSE.md (MIT License)
- Standard utility scripts (config_loader, log_utils, etc.)
- Git repository with initial commit

### Plan Your Project

```bash
cd <your-project>
project-wizard plan
```

The planning wizard will:
1. Display your charter summary
2. **Generate a ready-to-use AI prompt** with:
   - Your charter details
   - Formatting requirements
   - Instructions for the AI to ask clarifying questions
3. Wait for you to send the prompt to your AI and get a response
4. Parse the AI's response into structured milestones and tasks
5. Generate PROJECT_PLAN.md and ISSUES.md

**New Workflow:**
- Wizard generates the prompt automatically
- Copy → paste to AI agent (e.g., Warp Agent)
- AI asks questions, answers them, generates plan
- Copy AI response → paste back to wizard
- Done! No guesswork about format or content.

## Commands

```bash
project-wizard init              # Create new project with charter wizard
project-wizard init --type software_mvp   # Use project type template
project-wizard plan              # Create work breakdown (AI-assisted)
project-wizard status            # Show RPG-style quest map
project-wizard status -d         # Show detailed quest map
project-wizard sync              # Sync to OpenProject (coming soon)
```

## Project Types

- `software_mvp` - Software development projects
- `clinical_workflow` - Healthcare/clinical process improvements
- `infrastructure` - Server, network, or infrastructure projects
- `landscaping` - Home or landscaping projects
- `research_analysis` - Data analysis or research projects

## Methodology

Based on formal PM frameworks:
- **Step 1**: Project Owner initiates with business case
- **Step 2**: Project Manager plans with work breakdown
- **Step 3**: Core Team executes with monitoring
- **Step 4**: Stakeholders evaluate and close

See [reference_docs/PROJECT_STEP_BY_STEP.md](reference_docs/PROJECT_STEP_BY_STEP.md) for detailed methodology.

## RPG Framework 🎮⚔️

Project Wizard transforms project management into an epic quest with four chapters:

1. **📜 The Call to Adventure** (Initiation) - Draft your charter
2. **⚙️ The Strategist's Forge** (Planning) - Build your plan
3. **⚔️ The Campaign of Execution** (Execution) - Complete deliverables
4. **📚 The Chronicle of Wisdom** (Closure) - Document lessons learned

Each phase has:
- 🎯 Quest objectives and descriptions
- 📦 Artifacts ("loot") to collect
- 🚪 Gate approvals (RfP, RfE, RfC)
- 📈 Progress tracking

Run `project-wizard status` to see your quest map!

See [docs/RPG_FRAMEWORK_GUIDE.md](docs/RPG_FRAMEWORK_GUIDE.md) for the complete guide.

## Project Structure

This project follows a standardized folder architecture:

```
project_wizard/
├── app/                      # Application code
│   ├── wizard/              # Interactive wizard modules
│   ├── services/            # Core services (document_generator, repo_bootstrapper)
│   ├── models/              # Data models
│   ├── templates/           # Document templates
│   └── main.py              # CLI entry point
├── configs/                  # Configuration files
│   ├── .env.example         # Environment variables template
│   └── config.yaml          # Project settings
├── data/                     # Data pipeline stages
│   ├── inbox/               # Input data and specs
│   ├── staging/             # Work in progress
│   ├── archive/             # Completed items
│   └── logs/                # Centralized application logs
├── scripts/                  # Automation scripts
│   └── utils/               # Standard utility modules
│       ├── config_loader.py # Configuration loading
│       ├── db_utils.py      # Database utilities
│       ├── email_utils.py   # Email notifications
│       ├── log_utils.py     # Logging utilities
│       └── time_utils.py    # Timestamp handling
├── docs/                     # Project documentation
│   ├── PROJECT_CHARTER.md
│   ├── PROJECT_PLAN.md
│   ├── ISSUES.md
│   ├── CHANGELOG.md
│   └── DEVELOPMENT_SUMMARY.md
├── tests/                    # Test files
├── venv/                     # Virtual environment
├── Makefile                  # Build automation
├── README.md
├── requirements.txt
├── setup.py
└── .gitignore
```

### Projects Created by the Wizard

Projects created by this wizard will also follow this standard structure:

```
project-name/
├── configs/           # Configuration files
├── data/
│   ├── inbox/        # Input data and specs
│   ├── staging/      # Work in progress
│   ├── archive/      # Completed items
│   └── logs/         # Centralized logging
├── scripts/
│   └── utils/        # Shared utilities
├── docs/
│   ├── PROJECT_CHARTER.md
│   ├── PROJECT_PLAN.md
│   └── ISSUES.md
├── CONTRIBUTING.md    # Contribution guidelines
├── CODE_OF_CONDUCT.md # Code of conduct
├── LICENSE.md         # MIT License
├── README.md
├── pyproject.toml     # Ruff/pytest config
└── .gitignore
```

## Docker Deployment

Deploy alongside OpenProject:

```bash
docker build -t project-wizard .
docker-compose up -d
```

## Known Issues

### Planning Wizard (v0.4.1)

**Data Quality Issues:**
- **Task Formatting:** Tasks run together without line breaks in PROJECT_PLAN.md
- **Duration Parsing:** Parenthetical clarifications incorrectly extracted as task durations
- **Dependencies:** Dependencies may be parsed as tasks instead of separate section

**Workarounds:**
- Manually add line breaks between tasks in generated PROJECT_PLAN.md
- Remove incorrect "Duration" fields from ISSUES.md
- Review Phase 7 tasks and move dependencies to separate section

**Timeline:** Fixes planned for v0.4.2

## Development

### Setup
```bash
# Install in development mode
make install
# or
pip install -e .
```

### Code Quality
```bash
# Check code quality
make lint

# Auto-fix linting issues
make lint-fix

# Run tests (coming soon)
make test
```

### Development Workflow
1. Make your changes
2. Run `make lint` to check code quality
3. Fix any issues or run `make lint-fix` for auto-fixes
4. Test your changes manually or with `make test`
5. Commit with descriptive message: `make git-push MSG="feat: your change"`

## Roadmap

- [x] Phase 1: Charter wizard
- [x] Document generation (PROJECT_CHARTER.md, README.md)
- [x] Repository bootstrapping
- [x] Phase 2: Planning wizard (AI-assisted work breakdown)
- [x] PROJECT_PLAN.md and ISSUES.md generation
- [x] Best practices integration (CONTRIBUTING.md, CODE_OF_CONDUCT.md, LICENSE.md)
- [x] Code quality enforcement (ruff, PEP-8, complexity limits)
- [x] Centralized logging standards (data/logs/)
- [x] **RPG Framework** - Gamified phase tracking and quest map 🎮
- [ ] OpenProject sync (bidirectional)
- [ ] Project type templates (YAML)
- [ ] Built-in AI integration (--ai flag)
- [ ] Phase 3: Execution tracking
- [ ] Phase 4: Closing and lessons learned
- [ ] FastAPI web interface (optional)

## Author

Jonathan Ives  
Texas Pulmonary & Critical Care Consultants

---

*Generated with Project Wizard - Automating project management excellence*
