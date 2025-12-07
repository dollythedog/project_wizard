# Logseq Integration Architecture

**Last Updated:** 2025-12-07  
**Status:** 🎯 Planning / Design Phase

---

## Vision

Transform Project Wizard into a seamless content generator for your Logseq knowledge management system. Generated documents automatically flow into Logseq with proper formatting, tags, and metadata.

### The Integration Flow

```
Project Wizard (AI Document Generation)
    ↓
Markdown Output with Logseq Metadata
    ↓
Logseq Pages/Journals (Auto-detected)
    ↓
Task System Integration
    ↓
Unified Command Center
```

---

## Core Integration Points

### 1. Document Output Integration

**Goal:** Generated documents save directly to Logseq with proper frontmatter and tags.

**Output Locations:**
- **Windows Desktop:** `C:\Users\jonat\Documents\Logseq\pages\`
- **Linux Server:** `/srv/logseq_graph/pages/`
- Synced via Syncthing between desktop and bunto-server

**Document Naming Convention:**
```
📄 [Project Name] - [Document Type] - [Date].md

Examples:
📄 Healthcare Monitoring MVP - Project Charter - 2025-12-07.md
📄 Clinical Workflow Automation - White Paper - 2025-12-07.md
📄 Q4 Productivity Analysis - Data Analysis - 2025-12-07.md
```

---

### 2. Logseq Frontmatter Format

Every generated document should include Logseq-compatible metadata:

```markdown
---
title: Healthcare Monitoring MVP - Project Charter
type:: project-document
document-type:: charter
project:: [[Healthcare Monitoring MVP]]
generated:: 2025-12-07
blueprint:: project_charter
status:: draft
priority:: A
tags:: #work #project #healthcare
---

# Healthcare Monitoring MVP - Project Charter

[Document content here...]
```

**Key Metadata Fields:**
- `title` - Document title
- `type::` - Always "project-document" for discoverability
- `document-type::` - charter, white-paper, proposal, analysis, etc.
- `project::` - Link to project page `[[Project Name]]`
- `generated::` - ISO date (2025-12-07)
- `blueprint::` - Which blueprint was used
- `status::` - draft, final, archived
- `priority::` - A/B/C if applicable
- `tags::` - Role/category tags (#work, #personal, #health)

---

### 3. Project Page Generation

**Goal:** Each project in Project Wizard has a corresponding Logseq page.

**Project Page Template:**

```markdown
# [[Project Name]]

type:: project
status:: active
created:: 2025-12-07
last-updated:: 2025-12-07
role:: #work
priority:: A

## 📋 Project Overview
- **Description:** [Brief description from project]
- **Status:** Active
- **Created:** 2025-12-07

## 📄 Generated Documents
- [[📄 Project Name - Project Charter - 2025-12-07]]
- [[📄 Project Name - Work Plan - 2025-12-08]]
- [[📄 Project Name - White Paper - 2025-12-15]]

## 📝 Notes
- [[Note Title 1]]
- [[Note Title 2]]

## ✅ Tasks
- TODO Review charter with stakeholders #work
  priority:: A
  project:: [[Project Name]]
  SCHEDULED: [[2025-12-10]]

## 🔗 Related
- [[Healthcare]] - Topic
- [[Dr. Smith]] - Stakeholder
```

**Auto-Generated:**
- Project overview section
- Links to all generated documents
- List of notes in the project

**Manually Added:**
- Tasks related to the project
- Related pages/topics/people

---

### 4. Task Extraction from Documents

**Goal:** Automatically extract action items from generated documents into Logseq task system.

**Example Document Section:**
```markdown
## Action Items
1. Schedule kickoff meeting with stakeholders
2. Review budget allocation with finance team
3. Draft initial technical specification
```

**Extracted as Logseq Tasks:**
```markdown
- TODO Schedule kickoff meeting with stakeholders [[Healthcare Monitoring MVP]] #work
  priority:: A
  source:: [[📄 Healthcare Monitoring MVP - Project Charter - 2025-12-07]]
  SCHEDULED: [[2025-12-10]]

- TODO Review budget allocation with finance team [[Healthcare Monitoring MVP]] #work
  priority:: B
  source:: [[📄 Healthcare Monitoring MVP - Project Charter - 2025-12-07]]

- TODO Draft initial technical specification [[Healthcare Monitoring MVP]] #work
  priority:: B
  source:: [[📄 Healthcare Monitoring MVP - Project Charter - 2025-12-07]]
```

**Where Tasks Appear:**
- Today's journal (if scheduled for today)
- Project page
- `[[📊 Master Dashboard]]` (via queries)
- `[[👨‍💻 Code Tasks]]` or `[[🏢 Work Tasks]]` (via role tags)

---

### 5. Session Summary Integration

**Goal:** Automatically post session summaries to Logseq journal for daily reference.

**Current:** `SESSION_SUMMARY.md` in project root  
**Future:** Post to today's journal in Logseq

**Journal Entry Format:**
```markdown
# [[2025-12-07]]

## 🧙‍♂️ Project Wizard Session

### Work Completed
- Generated Project Charter for [[Healthcare Monitoring MVP]]
- Refined White Paper on [[Clinical Workflow Automation]]
- Created 3 new project blueprints

### Documents Generated
- [[📄 Healthcare Monitoring MVP - Project Charter - 2025-12-07]]
- [[📄 Clinical Workflow - White Paper - 2025-12-07]]

### Next Actions
- TODO Review charter with stakeholders #work
- TODO Test deployment on [[bunto-server]] #maintenance
```

---

## Implementation Roadmap

### Phase 1: Basic Output Integration (Week 1-2)

#### 1.1 Add Logseq Output Configuration
**File:** `app/config.py`

```python
class Settings(BaseSettings):
    # Existing settings...
    
    # Logseq integration
    LOGSEQ_PAGES_PATH: Optional[Path] = None
    LOGSEQ_JOURNALS_PATH: Optional[Path] = None
    LOGSEQ_INTEGRATION_ENABLED: bool = False
    
    @validator("LOGSEQ_PAGES_PATH", pre=True)
    def validate_logseq_path(cls, v):
        if v and not Path(v).exists():
            logger.warning(f"Logseq pages path does not exist: {v}")
        return v
```

**`.env` additions:**
```bash
# Logseq Integration (optional)
LOGSEQ_INTEGRATION_ENABLED=true
LOGSEQ_PAGES_PATH=C:\Users\jonat\Documents\Logseq\pages
LOGSEQ_JOURNALS_PATH=C:\Users\jonat\Documents\Logseq\journals
```

#### 1.2 Create Logseq Output Service
**New File:** `app/services/logseq_service.py`

```python
from pathlib import Path
from datetime import date
from typing import Optional
import re

class LogseqService:
    """Service for outputting documents to Logseq."""
    
    def __init__(self, pages_path: Path, journals_path: Path):
        self.pages_path = Path(pages_path)
        self.journals_path = Path(journals_path)
    
    def save_document(
        self,
        title: str,
        content: str,
        document_type: str,
        project_name: str,
        blueprint: str,
        tags: list[str],
        priority: Optional[str] = None,
        status: str = "draft"
    ) -> Path:
        """Save a generated document to Logseq pages."""
        
        # Generate filename
        today = date.today().isoformat()
        filename = f"📄 {project_name} - {document_type.title()} - {today}.md"
        filepath = self.pages_path / filename
        
        # Build frontmatter
        frontmatter = self._build_frontmatter(
            title=title,
            document_type=document_type,
            project_name=project_name,
            blueprint=blueprint,
            tags=tags,
            priority=priority,
            status=status,
            generated_date=today
        )
        
        # Combine frontmatter + content
        full_content = f"{frontmatter}\n\n{content}"
        
        # Write to file
        filepath.write_text(full_content, encoding='utf-8')
        
        return filepath
    
    def _build_frontmatter(self, **kwargs) -> str:
        """Build YAML frontmatter for Logseq."""
        lines = ["---"]
        lines.append(f"title: {kwargs['title']}")
        lines.append("type:: project-document")
        lines.append(f"document-type:: {kwargs['document_type']}")
        lines.append(f"project:: [[{kwargs['project_name']}]]")
        lines.append(f"generated:: {kwargs['generated_date']}")
        lines.append(f"blueprint:: {kwargs['blueprint']}")
        lines.append(f"status:: {kwargs['status']}")
        
        if kwargs.get('priority'):
            lines.append(f"priority:: {kwargs['priority']}")
        
        if kwargs.get('tags'):
            tags_str = " ".join(kwargs['tags'])
            lines.append(f"tags:: {tags_str}")
        
        lines.append("---")
        return "\n".join(lines)
    
    def create_project_page(
        self,
        project_name: str,
        description: str,
        status: str,
        role_tag: str,
        priority: Optional[str] = None,
        documents: list[str] = None,
        notes: list[str] = None
    ) -> Path:
        """Create or update a project page in Logseq."""
        
        filename = f"{project_name}.md"
        filepath = self.pages_path / filename
        
        # Build project page content
        content = [
            f"# [[{project_name}]]",
            "",
            "type:: project",
            f"status:: {status}",
            f"created:: {date.today().isoformat()}",
            f"last-updated:: {date.today().isoformat()}",
            f"role:: {role_tag}",
        ]
        
        if priority:
            content.append(f"priority:: {priority}")
        
        content.extend([
            "",
            "## 📋 Project Overview",
            f"- **Description:** {description}",
            f"- **Status:** {status.title()}",
            f"- **Created:** {date.today().isoformat()}",
            "",
            "## 📄 Generated Documents"
        ])
        
        if documents:
            for doc in documents:
                content.append(f"- [[{doc}]]")
        else:
            content.append("- _No documents generated yet_")
        
        content.extend([
            "",
            "## 📝 Notes"
        ])
        
        if notes:
            for note in notes:
                content.append(f"- [[{note}]]")
        else:
            content.append("- _No notes yet_")
        
        content.extend([
            "",
            "## ✅ Tasks",
            "_Tasks related to this project will appear here_",
            "",
            "## 🔗 Related",
            "_Add related pages, topics, or people here_"
        ])
        
        filepath.write_text("\n".join(content), encoding='utf-8')
        return filepath
    
    def extract_action_items(self, content: str, project_name: str, source_doc: str) -> list[dict]:
        """Extract action items from document content."""
        
        # Simple regex to find "Action Items" section
        action_section_pattern = r"##\s+Action Items.*?(?=##|\Z)"
        action_match = re.search(action_section_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if not action_match:
            return []
        
        action_section = action_match.group()
        
        # Extract numbered/bulleted items
        item_pattern = r"(?:^\d+\.|^-)\s+(.+?)$"
        items = re.findall(item_pattern, action_section, re.MULTILINE)
        
        # Convert to Logseq task format
        tasks = []
        for item in items:
            task = {
                "description": item.strip(),
                "project": project_name,
                "source": source_doc,
                "priority": None  # User assigns manually
            }
            tasks.append(task)
        
        return tasks
    
    def append_to_journal(self, content: str, journal_date: Optional[date] = None):
        """Append content to a journal entry."""
        
        if journal_date is None:
            journal_date = date.today()
        
        # Logseq journal format: 2025_12_07.md
        journal_filename = journal_date.strftime("%Y_%m_%d.md")
        journal_path = self.journals_path / journal_filename
        
        # Append to existing or create new
        if journal_path.exists():
            existing_content = journal_path.read_text(encoding='utf-8')
            full_content = f"{existing_content}\n\n{content}"
        else:
            full_content = f"# [[{journal_date.isoformat()}]]\n\n{content}"
        
        journal_path.write_text(full_content, encoding='utf-8')
        return journal_path
```

#### 1.3 Update Document Generation Flow
**File:** `web/routes/generate.py`

Modify document generation to optionally save to Logseq:

```python
from app.services.logseq_service import LogseqService
from app.config import settings

@router.post("/project/{project_id}/generate/save")
async def save_to_logseq(
    project_id: int,
    document_run_id: int,
    session: Session = Depends(get_session)
):
    """Save generated document to Logseq."""
    
    if not settings.LOGSEQ_INTEGRATION_ENABLED:
        raise HTTPException(400, "Logseq integration not enabled")
    
    # Fetch document run
    doc_run = session.get(DocumentRun, document_run_id)
    project = session.get(Project, project_id)
    
    # Initialize Logseq service
    logseq = LogseqService(
        settings.LOGSEQ_PAGES_PATH,
        settings.LOGSEQ_JOURNALS_PATH
    )
    
    # Save document
    filepath = logseq.save_document(
        title=doc_run.title,
        content=doc_run.refined_draft or doc_run.initial_draft,
        document_type=doc_run.template_name,
        project_name=project.title,
        blueprint=doc_run.template_name,
        tags=["#work"],  # TODO: Make configurable
        priority="A",
        status="draft"
    )
    
    # Extract and save tasks (optional)
    tasks = logseq.extract_action_items(
        content=doc_run.refined_draft or doc_run.initial_draft,
        project_name=project.title,
        source_doc=filepath.stem
    )
    
    # Append task extraction to journal
    if tasks:
        task_content = "## 🧙‍♂️ Project Wizard - New Tasks Extracted\n"
        for task in tasks:
            task_content += f"- TODO {task['description']} [[{task['project']}]] #work\n"
            task_content += f"  source:: [[{task['source']}]]\n"
        
        logseq.append_to_journal(task_content)
    
    return {"success": True, "filepath": str(filepath), "tasks_extracted": len(tasks)}
```

#### 1.4 Add UI Button
**File:** `web/templates/draft.html`

Add "Save to Logseq" button after document generation:

```html
{% if logseq_enabled %}
<div class="logseq-actions">
    <button hx-post="/project/{{ project.id }}/generate/save" 
            hx-target="#status"
            class="btn-primary">
        💡 Save to Logseq
    </button>
</div>
{% endif %}
```

---

### Phase 2: Project Sync (Week 3-4)

#### 2.1 Automatic Project Page Creation
- When creating a project in Project Wizard, automatically create Logseq project page
- Sync project metadata changes

#### 2.2 Note Sync
- Project notes in Project Wizard → linked from Logseq project page
- Optional: Create separate Logseq pages for each note

---

### Phase 3: Task Automation (Week 5-6)

#### 3.1 Enhanced Task Extraction
- NLP/LLM-based action item detection
- Automatic priority assignment
- Smart scheduling suggestions

#### 3.2 Bi-Directional Sync
- Tasks created in Logseq → sync back to Project Wizard?
- Or keep Logseq as read-only consumer?

---

### Phase 4: Dashboard Integration (Week 7-8)

#### 4.1 Project Wizard Dashboard in Logseq
Create `[[🧙‍♂️ Project Wizard Dashboard]]`:

```markdown
# 🧙‍♂️ Project Wizard Dashboard

## 📄 Recently Generated Documents
{{query (and (property type "project-document") (between -7d today))}}

## 📋 Active Projects
{{query (and (property type "project") (property status "active"))}}

## ✅ Tasks from Generated Documents
{{query (and (task TODO DOING) (property source))}}

## 📊 Document Statistics
- Total documents: 47
- This week: 8
- Pending review: 3
```

#### 4.2 Automation Script (on bunto-server)
- Nightly script to generate Logseq stats page
- Count of projects, documents, tasks extracted
- Recent activity summary

---

## Configuration Examples

### Desktop Development Setup
```bash
# .env on Windows
LOGSEQ_INTEGRATION_ENABLED=true
LOGSEQ_PAGES_PATH=C:\Users\jonat\Documents\Logseq\pages
LOGSEQ_JOURNALS_PATH=C:\Users\jonat\Documents\Logseq\journals
```

### Server Production Setup
```bash
# .env on bunto-server
LOGSEQ_INTEGRATION_ENABLED=true
LOGSEQ_PAGES_PATH=/srv/logseq_graph/pages
LOGSEQ_JOURNALS_PATH=/srv/logseq_graph/journals
```

**Note:** Syncthing syncs `/srv/logseq_graph` ↔ `C:\Users\jonat\Documents\Logseq`, so both machines write to the same Logseq graph.

---

## Usage Workflow

### End-to-End Flow

1. **Create Project in Project Wizard**
   - Add notes, context, supporting information
   - Project page automatically created in Logseq

2. **Generate Document**
   - Choose blueprint (e.g., White Paper)
   - Answer step-back questions
   - Review generated draft

3. **Save to Logseq**
   - Click "Save to Logseq" button
   - Document saved to `pages/` with metadata
   - Action items extracted to today's journal
   - Project page updated with document link

4. **Work in Logseq**
   - Open `[[📊 Master Dashboard]]`
   - See tasks from generated document
   - Prioritize, schedule, complete tasks
   - Reference document page when needed

5. **Iterate**
   - Generate updated versions as project evolves
   - All versions linked from project page
   - Task history preserved

---

## Benefits

### 1. Single Source of Truth
- All project documents accessible from Logseq
- No more hunting through folders

### 2. Automatic Task Capture
- Action items flow directly into your task system
- Nothing falls through the cracks

### 3. Context Preservation
- Every document linked to its project
- Full project history in one place

### 4. Markdown-Native
- Edit documents in Logseq if needed
- Version control via Git (optional)

### 5. Synced Everywhere
- Desktop, server, phone (via Syncthing + Tailscale)
- Work from any device

---

## Future Enhancements

### Voice-to-Document Pipeline
1. Voice recording → Whisper transcription
2. Transcription → Project Wizard input
3. Document generation → Logseq
4. All from phone via Tailscale!

### Template Library
- Frequently used document types
- Pre-filled inputs for common scenarios
- One-click generation

### Analytics Dashboard
- Document generation trends
- Project velocity tracking
- Time-to-completion metrics

### AI-Powered Task Management
- LLM suggests task priorities
- Automatic task dependencies
- Smart deadline predictions

---

## Related Documentation

- `README.md` - Project Wizard overview
- `docs/DEPLOYMENT.md` - Server deployment guide
- `C:\Users\jonat\Documents\Logseq\pages\🚀 Automation Roadmap.md` - Full automation vision
- `C:\Users\jonat\Documents\Logseq\pages\🚀 Task System.md` - Logseq task management

---

## Next Steps

1. ✅ Review this architecture
2. ⏭️ Implement Phase 1.1-1.2 (Logseq output service)
3. ⏭️ Test with one project/document
4. ⏭️ Refine frontmatter and formatting
5. ⏭️ Deploy to server and test sync
6. ⏭️ Build task extraction logic
7. ⏭️ Create Logseq dashboard queries

**Start Date:** After server deployment complete  
**Estimated Time:** 2-3 weeks for Phase 1-2

---

**Questions?** This is a living document - update as implementation evolves!
