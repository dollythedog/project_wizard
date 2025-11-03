# Project Wizard 🧙‍♂️

**Your Personal Project Management Automation Tool**

An interactive CLI tool that guides you through creating and managing projects following formal project management methodology, with seamless OpenProject integration.

## Features

✨ **Phase 1: Initiation** - Interactive charter creation wizard  
📋 **Automatic Document Generation** - PROJECT_CHARTER.md, README.md, and more  
🗂️ **Standardized Repository Structure** - Consistent folder layout across all projects  
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
- Git repository with initial commit

## Commands

```bash
project-wizard init              # Create new project with charter wizard
project-wizard init --type software_mvp   # Use project type template
project-wizard plan              # Create work breakdown (coming soon)
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
│   └── logs/                # Application logs
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
│   └── archive/      # Completed items
├── scripts/
│   └── utils/        # Shared utilities
├── docs/
│   ├── PROJECT_CHARTER.md
│   ├── PROJECT_PLAN.md
│   └── ISSUES.md
├── README.md
└── .gitignore
```

## Docker Deployment

Deploy alongside OpenProject:

```bash
docker build -t project-wizard .
docker-compose up -d
```

## Development

```bash
# Install in development mode
pip install -e .

# Run tests
pytest

# Run linter
ruff check app/
```

## Roadmap

- [x] Phase 1: Charter wizard
- [x] Document generation (PROJECT_CHARTER.md, README.md)
- [x] Repository bootstrapping
- [ ] Phase 2: Planning wizard (work breakdown)
- [ ] OpenProject sync (bidirectional)
- [ ] Project type templates (YAML)
- [ ] Phase 3: Execution tracking
- [ ] Phase 4: Closing and lessons learned
- [ ] FastAPI web interface (optional)

## Author

Jonathan Ives  
Texas Pulmonary & Critical Care Consultants

---

*Generated with Project Wizard - Automating project management excellence*
