# Pattern-Based Document Generation System

**Fabric-Inspired Architecture for Project Management Documents**

## Overview

This system extends Project Wizard from a single-purpose charter generator to a **generalized document generation platform** supporting multiple PM/LEAN methodologies (5W1H, SIPOC, Fishbone, VOC, etc.).

### Design Philosophy

Following **Unix philosophy**: Each component does ONE thing well, and components pipe together:

```
User Input → Draft Agent → Editor Agent → Critic Agent → [Revision Loop] → Format → Output
```

### Key Innovation

**Patterns are self-contained, reusable document templates** - similar to Fabric's 233+ prompt patterns. Each pattern defines:
- AI instructions (`system.md`)
- Input variables (`variables.json`)  
- User context template (`user.md`)
- Quality rubric (`rubric.json`)
- Output format (`template.md.j2`)

## Architecture

### Components

```
patterns/                      # Self-contained document patterns
├── 5w1h_analysis/
│   ├── system.md             # AI behavior instructions
│   ├── user.md               # Context template with {{variables}}
│   ├── variables.json        # UI field definitions
│   ├── rubric.json           # Quality criteria
│   └── template.md.j2        # Output document format
│
└── [future: sipoc, fishbone, voc, etc.]

app/services/
├── pattern_registry.py       # Loads and manages patterns
├── project_context.py        # Injects project documentation
├── pattern_pipeline.py       # Orchestrates agent workflow
│
└── ai_agents/
    ├── draft_agent.py        # Stage 1: Generate initial draft
    ├── editor_agent.py       # Stage 2: Polish for clarity
    └── critic_agent.py       # Stage 3: Evaluate quality
```

### Specialized Agents

Each agent has a **single responsibility**:

1. **DraftAgent**: Creates initial content from pattern + user inputs
   - Temperature: 0.3 (balanced)
   - Focus: Comprehensive first draft

2. **EditorAgent**: Polishes for clarity WITHOUT adding data
   - Temperature: 0.2 (conservative)
   - Focus: Grammar, structure, professional tone
   - **NEVER invents facts**

3. **CriticAgent**: Evaluates against rubric
   - Temperature: 0.2 (consistent scoring)
   - Returns: Scores, strengths, weaknesses, improvements
   - Triggers revision loop if score < threshold

### Project Context Injection

**Critical feature**: All generated documents reference core project docs for consistency:

- `PROJECT_CHARTER.md` - Why does this project exist?
- `README.md` - What is this project?
- `ISSUES.md` - What needs to happen?
- `CHANGELOG.md` - What already happened?

These are injected into `user.md` template so AI maintains alignment.

## Usage

### 1. Test the 5W1H Pattern

```bash
# Activate virtual environment
source venv/bin/activate

# Run test (makes API calls)
python test_5w1h_pipeline.py
```

Expected output:
- Pattern loaded successfully
- Project context injected
- Pipeline stages execute (draft → edit → critique)
- Final document saved to `test_5w1h_output.md`
- Quality score displayed

### 2. Add New Patterns

Create a new directory in `patterns/`:

```bash
mkdir -p patterns/sipoc
cd patterns/sipoc
```

Create the 5 required files:

**system.md**: AI instructions for this methodology
**user.md**: Template with `{{variable_name}}` placeholders
**variables.json**: UI field definitions
**rubric.json**: Quality criteria and weights
**template.md.j2**: Final document format

The PatternRegistry auto-discovers new patterns on startup!

### 3. Programmatic Use

```python
from app.services.pattern_registry import PatternRegistry
from app.services.project_context import ProjectContext
from app.services.pattern_pipeline import PatternPipeline

# Initialize
registry = PatternRegistry()
context = ProjectContext('/path/to/project')
pipeline = PatternPipeline(registry, context)

# Execute
result = pipeline.execute(
    pattern_name='5w1h_analysis',
    user_inputs={
        'problem_statement': '...',
        'what': '...',
        'when': '...',
        # ... other variables
    },
    enable_editing=True,
    enable_critique=True,
    project_path='/path/to/project'
)

# Access results
print(result['document'])        # Formatted output
print(result['final_score'])     # Quality score
print(result['critique'])        # Detailed feedback
```

## Benefits

### 1. Separation of Concerns
- **Patterns** = PM knowledge (portable, versioned)
- **Agents** = AI orchestration (reusable)
- **UI** = Generated dynamically from patterns

### 2. Extensibility
- Add document type: Create pattern folder (no code!)
- Change AI model: Update one config
- A/B test prompts: Version control patterns/

### 3. Quality Control
- Each pattern embeds its own rubric
- Consistent evaluation across document types
- Audit trail via pipeline_log

### 4. ADHD-Friendly
- Guided inputs prevent blank page paralysis
- AI assistance without hallucination risk
- Project context maintains focus

## Next Steps

### Immediate (v2.1)
- [ ] Integrate 5W1H into Streamlit UI
- [ ] Add SIPOC pattern
- [ ] Add Fishbone diagram pattern
- [ ] Build project loader/switcher UI

### Near-term (v2.2)
- [ ] Add 5-10 more LEAN patterns
- [ ] Pattern marketplace/sharing
- [ ] Batch processing
- [ ] Export to slideshow/PDF

### Future (v3.0)
- [ ] Visual diagram generation (Mermaid)
- [ ] Voice input support (Fabric has this!)
- [ ] Multi-project comparative analysis
- [ ] OpenProject bidirectional sync

## Testing

```bash
# Test pattern loading
python -c "from app.services.pattern_registry import PatternRegistry; r = PatternRegistry(); print(r.list_patterns())"

# Test project context
python -c "from app.services.project_context import ProjectContext; from pathlib import Path; c = ProjectContext(Path('.')); print(c.get_summary())"

# Full pipeline test
python test_5w1h_pipeline.py
```

## Files Created

```
patterns/5w1h_analysis/
├── system.md           [5.4 KB] - LEAN expert instructions
├── user.md             [0.9 KB] - Context template
├── variables.json      [2.3 KB] - UI field definitions
├── rubric.json         [1.2 KB] - Quality criteria
└── template.md.j2      [0.8 KB] - Output format

app/services/
├── pattern_registry.py    [6.8 KB] - Pattern loader
├── project_context.py     [3.2 KB] - Context injector
├── pattern_pipeline.py    [7.5 KB] - Agent orchestrator

app/services/ai_agents/
├── draft_agent.py         [2.4 KB] - Initial generation
├── editor_agent.py        [4.1 KB] - Polishing
└── __init__.py            [Updated]  - Module exports

test_5w1h_pipeline.py      [3.9 KB] - Integration test
PATTERN_SYSTEM_README.md   [This file]
```

## References

- **Fabric Project**: https://github.com/danielmiessler/fabric
- **LEAN Six Sigma**: Industry-standard process improvement
- **Unix Philosophy**: Composable, single-purpose tools
- **Prompt Chaining**: Sequential AI task decomposition

---

**Status**: ✅ MVP Complete - 5W1H pattern functional  
**Next**: Integrate into Streamlit UI + add more patterns

*Generated: 2025-11-08*
