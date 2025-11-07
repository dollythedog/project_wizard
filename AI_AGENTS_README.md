# AI Agents for Project Wizard 🤖

**Status:** Infrastructure Complete - Awaiting OpenAI Billing Activation

## Overview

AI-powered enhancements to the Project Wizard that provide:
- **Charter Drafting**: AI generates professional charter sections from brief inputs
- **Quality Critique**: Automated review against PM best practices
- **Iterative Refinement**: Reflection loop for continuous improvement

## Architecture

```
app/services/ai_agents/
├── llm_client.py          # OpenAI wrapper with retry logic
├── charter_agent.py       # Drafts charter sections
└── critic_agent.py        # Reviews and scores charters

configs/
├── ai_config.yaml         # AI feature configuration
└── rubric_charter.json    # Quality scoring rubric
```

## Features

### 1. Charter Agent
Generates professional charter sections:
- Business Need / Opportunity
- Success Criteria (measurable)
- Proposed Solution
- Risks & Mitigation Strategies
- Scope (in/out)
- Deliverables
- Schedule Overview

### 2. Critic Agent
Reviews charter quality:
- Scores against 6 criteria (weighted)
- Identifies gaps and weaknesses
- Suggests specific improvements
- Approval/rejection decision

### 3. Reflection Pattern
- Draft → Critique → Revise loop
- Max 2 iterations (configurable)
- 75% threshold for approval

## Setup

### 1. OpenAI API Key (REQUIRED)

Your API key is already in `.env`, but **billing must be enabled**:

1. Visit: https://platform.openai.com/settings/organization/billing/overview
2. Add payment method (credit/debit card)
3. Set usage limit (recommend $10/month to start)
4. Wait 1-2 minutes for activation

### 2. Test Connection

```bash
cd /home/ivesjl/project_wizard
./venv/bin/python test_openai.py
```

Expected output:
```
✅ SUCCESS! API Response:
   Hello from Project Wizard AI!
📊 Usage: 15 tokens
```

### 3. Run AI Demo

```bash
./venv/bin/python demo_ai_agents.py
```

This demonstrates:
- Drafting business need, success criteria, and risks
- AI critique with scoring
- Beautiful rich console output

## Usage

### Option A: AI-Assisted Mode (Coming Soon)

```bash
project-wizard init --ai-assist
```

Workflow:
1. You provide brief project description (3-5 sentences)
2. AI drafts full charter sections
3. You review and edit each section
4. AI critiques final charter
5. Documents generated as usual

### Option B: Manual Mode (Current)

```bash
project-wizard init
```

Your existing interactive wizard (unchanged).

## Cost Estimate

Using `gpt-4o-mini` (default):

| Operation | Tokens | Cost |
|-----------|--------|------|
| Draft 7 charter sections | ~10k | $0.0015 |
| Critique (2 loops) | ~5k | $0.0008 |
| **Total per charter** | ~15k | **$0.0023** |

**Monthly (20 projects):** ~$0.05 🎉

## Configuration

### AI Settings (`configs/ai_config.yaml`)

```yaml
openai:
  model: gpt-4o-mini      # Fast, cheap, good quality
  temperature: 0.4        # Balance creativity/consistency
  max_tokens: 2000

features:
  ai_assist:
    enabled: true
    auto_critique: true
    max_critique_loops: 2
```

### Quality Rubric (`configs/rubric_charter.json`)

Weighted scoring criteria:
- Clarity of Goal (20%)
- Scope & Deliverables (20%)
- Risks & Mitigations (15%)
- Success Criteria (15%)
- Strategic Alignment (15%)
- Stakeholders & Resources (15%)

**Threshold:** 75% for approval

## Migration to Local LLM (Future)

When you build your local LLM server:

1. **Start Ollama** with OpenAI-compatible API
2. **Update `.env`**:
   ```bash
   OPENAI_BASE_URL=http://llm-server:11434/v1
   OPENAI_MODEL=llama3.1:8b-instruct
   ```
3. **No code changes needed!**

## Development

### File Structure

```
AI Agents Module:
app/services/ai_agents/
├── __init__.py              # Module exports
├── llm_client.py            # OpenAI client (140 lines)
├── charter_agent.py         # Charter drafting (220 lines)
└── critic_agent.py          # Quality review (180 lines)

Configuration:
configs/
├── ai_config.yaml           # Feature flags & settings
└── rubric_charter.json      # Scoring criteria

Demos:
├── test_openai.py           # Quick API test
└── demo_ai_agents.py        # Full agent demo
```

### Key Classes

**LLMClient**
- Wraps OpenAI API
- Retry logic (3 attempts with exponential backoff)
- Environment-based configuration
- Structured completion support

**CharterAgent**
- 7 specialized drafting methods
- Context-aware (department, budget, type)
- Configurable temperature per task
- Enhancement/refinement capability

**CriticAgent**
- Rubric-based scoring
- Weighted criteria evaluation
- JSON-structured feedback
- Improvement suggestion generator

## Next Steps

### Immediate
1. ✅ **Enable OpenAI billing** (5 minutes)
2. ✅ **Run `test_openai.py`** to verify
3. ✅ **Run `demo_ai_agents.py`** to see agents in action

### Phase 2 (This Week)
- [ ] Integrate `--ai-assist` flag into `phase1_initiation.py`
- [ ] Add AI draft preview in wizard prompts
- [ ] Implement auto-critique after charter generation
- [ ] Add `--ai-only` mode for fully automated charters

### Phase 3 (Next Week)
- [ ] Create `planner_agent.py` for work breakdown
- [ ] Integrate with Phase 2 planning wizard
- [ ] Auto-generate PROJECT_PLAN.md with milestones/tasks
- [ ] Add dependency graph generation

## Troubleshooting

### "insufficient_quota" Error

**Cause:** Billing not enabled on OpenAI account

**Fix:** Add payment method at https://platform.openai.com/settings/organization/billing/overview

### Import Errors

**Cause:** Virtual environment not activated or dependencies missing

**Fix:**
```bash
cd /home/ivesjl/project_wizard
./venv/bin/pip install -r requirements.txt
```

### Slow Responses

**Cause:** Using gpt-4o (more powerful but slower/pricier)

**Fix:** Use `gpt-4o-mini` (default in `.env`)

## Credits

**Built by:** Jonathan Ives  
**Organization:** Texas Pulmonary & Critical Care Consultants  
**Date:** November 2025  
**AI Patterns:** Prompt Chaining, Reflection, Tool Use (OpenAI API)

## References

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Project Management Body of Knowledge (PMBOK)](https://www.pmi.org/pmbok-guide-standards)
- [Agentic AI Patterns](https://www.deeplearning.ai/the-batch/) - Reflection, Planning, Tool Use

---

**Status:** Ready for billing activation → immediate use 🚀
