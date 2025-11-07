# Quick Start: AI-Enhanced Project Wizard

## ⚡ 3-Step Setup

### 1. Enable OpenAI Billing (5 min)
Visit: https://platform.openai.com/settings/organization/billing/overview
- Add payment method
- Set usage limit: $10/month
- Wait 2 minutes for activation

### 2. Test API Connection
```bash
cd /home/ivesjl/project_wizard
./venv/bin/python test_openai.py
```

Expected: `✅ SUCCESS!`

### 3. Run AI Demo
```bash
./venv/bin/python demo_ai_agents.py
```

You'll see:
- AI drafting charter sections
- Quality critique with scoring
- Real-time generation

## 💰 Cost

**~$0.002 per project charter** (less than 1/4 penny)

20 projects/month = ~$0.04/month 🎉

## 📚 Full Documentation

- **AI_AGENTS_README.md** - Complete guide
- **configs/ai_config.yaml** - Configuration
- **configs/rubric_charter.json** - Quality rubric

## 🚀 What's Next?

Once billing is active:
1. Demo will work immediately
2. Integration with `project-wizard init --ai-assist` (Phase 2)
3. Automated work breakdown (Phase 3)

## ❓ Questions?

See `AI_AGENTS_README.md` or contact Jonathan Ives

---

**Built:** November 2025 | **Status:** Ready for activation
