# Kanban Board Feature Design

**Feature ID:** #1  
**Priority:** High  
**Target Version:** 2.7.0  
**Status:** Design Phase

---

## Overview

Add a visual Kanban board to the Streamlit app for managing issues tracked in ISSUES.md files. This will make issue tracking more actionable and visual, especially when managing multiple projects created by Project Wizard.

## Goals

1. **Visual Issue Management** - See issues at a glance in Kanban columns
2. **Multi-Project Support** - Filter issues by project (project_wizard vs. created projects)
3. **Easy Updates** - Drag-and-drop to change status, inline editing
4. **Sync with ISSUES.md** - Keep markdown files as source of truth
5. **Future GitHub Integration** - Lay groundwork for syncing with GitHub Issues

## User Stories

### US1: View Issues in Kanban Board
**As a** Project Wizard user  
**I want to** see all my issues in a Kanban board view  
**So that** I can quickly understand project status at a glance

**Acceptance Criteria:**
- [ ] New "Issues" tab in main navigation
- [ ] Issues displayed in columns: Backlog, In Progress, Review, Done
- [ ] Each issue card shows: title, priority badge, project tag
- [ ] Issues are color-coded by priority (High=red, Medium=yellow, Low=blue)

### US2: Filter Issues by Project
**As a** user managing multiple projects  
**I want to** filter issues by project  
**So that** I can focus on specific project issues

**Acceptance Criteria:**
- [ ] Dropdown filter: "All Projects", "Project Wizard", [Individual created projects]
- [ ] Filter persists in session state
- [ ] Issue count shown per project in filter dropdown

### US3: Update Issue Status
**As a** user  
**I want to** drag-and-drop issues between columns  
**So that** I can quickly update issue status

**Acceptance Criteria:**
- [ ] Drag-and-drop between columns updates status
- [ ] Changes immediately reflected in ISSUES.md
- [ ] Visual feedback during drag operation
- [ ] Undo option for accidental moves

### US4: Create and Edit Issues
**As a** user  
**I want to** create new issues and edit existing ones  
**So that** I can track work without leaving the app

**Acceptance Criteria:**
- [ ] "New Issue" button opens modal form
- [ ] Form fields: Title, Description, Priority, Project, Component
- [ ] Click issue card to edit inline or in modal
- [ ] Delete issue option with confirmation

---

## Technical Design

### Architecture

```
app/
├── services/
│   └── issue_manager.py        # Core issue management logic
├── models/
│   └── issue.py                # Issue data model
├── ui/
│   └── tabs/
│       └── issues_tab.py       # Kanban board UI
└── parsers/
    └── issues_parser.py        # Parse/write ISSUES.md
```

### Data Model

```python
@dataclass
class Issue:
    id: str                      # Unique identifier (e.g., "PW-001")
    title: str                   # Issue title
    status: IssueStatus          # Backlog, InProgress, Review, Done
    priority: IssuePriority      # High, Medium, Low
    component: str               # UI, Patterns, AI, etc.
    project: str                 # "project_wizard" or project name
    description: str             # Full description
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]

class IssueStatus(Enum):
    BACKLOG = "backlog"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"

class IssuePriority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
```

### ISSUES.md Format

Standardize ISSUES.md format for easier parsing:

```markdown
## 🎯 Active Issues

### High Priority

**#PW-001: Issue Title**  
**Status:** 🟢 In Progress  
**Priority:** High  
**Component:** UI  
**Project:** project_wizard  

**Description:**  
Issue description here...

**Solution:**
- Proposed solution points
```

### Parsing Strategy

1. **Read ISSUES.md** - Use regex to extract issue blocks
2. **Parse metadata** - Extract ID, status, priority, component, project
3. **Create Issue objects** - Populate Issue dataclass instances
4. **Display in UI** - Render in Kanban columns

### Writing Strategy

1. **Update Issue object** - Modify in-memory Issue instance
2. **Regenerate markdown** - Use Jinja2 template to generate ISSUES.md
3. **Write to file** - Atomic write to prevent corruption
4. **Preserve comments** - Keep non-issue content (stats, legends, etc.)

### UI Components

#### Kanban Board Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Issues Tab                                                  │
│                                                               │
│  [Filter: All Projects ▼]  [+ New Issue]                    │
│                                                               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Backlog │  │In Progr.│  │ Review  │  │  Done   │        │
│  │  (3)    │  │  (2)    │  │  (1)    │  │  (4)    │        │
│  ├─────────┤  ├─────────┤  ├─────────┤  ├─────────┤        │
│  │ 🔴 #PW-1│  │ 🟡 #PW-3│  │ 🔵 #PW-6│  │ ✅ #PW-7│        │
│  │ Kanban  │  │ Cleanup │  │ Pattern │  │ Charter │        │
│  │ Board   │  │ Repo    │  │ Library │  │ Fix     │        │
│  │ [PW]    │  │ [PW]    │  │ [PW]    │  │ [PW]    │        │
│  ├─────────┤  ├─────────┤  └─────────┘  ├─────────┤        │
│  │ 🟡 #PW-2│  │ 🔴 #ML-1│              │ ✅ #PW-8│        │
│  │ Entry   │  │ Training│              │ AI Enh. │        │
│  │ Point   │  │ Pipeline│              │ [PW]    │        │
│  │ [PW]    │  │ [ML]    │              └─────────┘        │
│  └─────────┘  └─────────┘                                  │
└─────────────────────────────────────────────────────────────┘
```

#### Issue Card

```python
def render_issue_card(issue: Issue) -> None:
    """Render an issue card in the Kanban board."""
    priority_colors = {
        IssuePriority.HIGH: "🔴",
        IssuePriority.MEDIUM: "🟡",
        IssuePriority.LOW: "🔵"
    }
    
    with st.container():
        st.markdown(f"""
        <div class="issue-card">
            <div class="issue-header">
                {priority_colors[issue.priority]} **{issue.id}**
            </div>
            <div class="issue-title">{issue.title}</div>
            <div class="issue-footer">
                <span class="project-tag">[{issue.project[:2].upper()}]</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
```

### Implementation Plan

#### Phase 1: Core Functionality (v2.7.0)
1. **Issue parser** - Read and parse ISSUES.md
2. **Issue model** - Define Issue dataclass
3. **Issue manager service** - CRUD operations for issues
4. **Basic Kanban UI** - Display issues in columns
5. **Project filter** - Filter by project

#### Phase 2: Interactivity (v2.7.1)
6. **New issue modal** - Form to create issues
7. **Edit issue** - Click to edit inline
8. **Status update** - Button-based status change (drag-and-drop later)
9. **Delete issue** - With confirmation

#### Phase 3: Advanced Features (v2.7.2)
10. **Drag-and-drop** - Move issues between columns
11. **Search/filter** - Search by title, filter by component
12. **Bulk operations** - Select multiple issues
13. **Issue templates** - Quick-create common issue types

#### Phase 4: GitHub Integration (v2.8.0)
14. **GitHub sync** - Two-way sync with GitHub Issues
15. **Label mapping** - Map priorities/components to GitHub labels
16. **Webhook support** - Auto-update on GitHub changes

---

## Alternative Approaches Considered

### 1. Use streamlit-aggrid
**Pros:** Built-in drag-and-drop, sorting, filtering  
**Cons:** Heavy dependency, less customizable UI  
**Decision:** Rejected - too heavy for MVP, prefer lightweight custom solution

### 2. Use external issue tracker (Jira, Linear)
**Pros:** Full-featured, no development needed  
**Cons:** Loses ISSUES.md as source of truth, requires external service  
**Decision:** Rejected - want to keep issues in markdown for portability

### 3. Simple list view (no Kanban)
**Pros:** Easier to implement  
**Cons:** Less visual, harder to see status at a glance  
**Decision:** Rejected - Kanban provides much better UX for issue tracking

---

## Testing Strategy

### Unit Tests
- `test_issue_parser.py` - Test parsing various ISSUES.md formats
- `test_issue_manager.py` - Test CRUD operations
- `test_issue_model.py` - Test Issue dataclass validation

### Integration Tests
- `test_kanban_ui.py` - Test UI rendering with sample data
- `test_issue_workflow.py` - Test create → update → resolve flow

### Manual Testing Scenarios
1. Create new issue and verify it appears in ISSUES.md
2. Move issue between columns and verify markdown updates
3. Filter by project and verify correct issues shown
4. Edit issue inline and verify changes persist
5. Delete issue and verify it's removed from markdown

---

## Performance Considerations

- **Cache parsed issues** - Parse ISSUES.md once per session
- **Lazy load issue details** - Only load full description on click
- **Debounce writes** - Batch multiple updates before writing to file
- **Async file I/O** - Don't block UI while writing ISSUES.md

---

## Future Enhancements

1. **Issue templates** - Pre-defined issue types (bug, feature, task)
2. **Time tracking** - Log time spent on issues
3. **Issue dependencies** - Link related issues
4. **Milestones** - Group issues by milestone/sprint
5. **Activity feed** - Show recent issue updates
6. **Export to CSV/JSON** - Export issues for reporting
7. **Issue comments** - Add discussion threads to issues
8. **Assignees** - Assign issues to team members (multi-user support)

---

## Success Metrics

- **Adoption**: 90% of Project Wizard sessions include visiting Issues tab
- **Issue throughput**: 50% increase in issues resolved per week
- **User satisfaction**: Positive feedback on Kanban UX in user testing
- **Performance**: Issue board loads in <500ms with 100+ issues

---

## Open Questions

1. **How to handle projects created before Kanban feature?**
   - Migration script to parse old ISSUES.md formats?
   - Manual conversion with helper tool?

2. **Should we support custom columns (e.g., "Blocked", "Testing")?**
   - Start with fixed columns, add customization in v2.8.0?

3. **How to preserve manual edits to ISSUES.md?**
   - Warning if file modified externally?
   - Merge strategy for conflicts?

---

**Next Steps:**
1. Review and approve design
2. Create implementation tasks in ISSUES.md
3. Set up development branch: `feature/kanban-board`
4. Begin Phase 1 implementation
