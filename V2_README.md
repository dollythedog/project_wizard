# AI Project Wizard v2.0 🧙‍♂️

**Status:** Beta - Ready for Testing  
**Purpose:** ADHD-Friendly Project Execution System  
**Methodology:** Formal 4-Step PM Framework

---

## 🎯 What's Different in v2.0?

### **v1.0 (Current Production)**
- ❌ Single brief input (3-5 sentences)
- ❌ AI "hallucinates" to fill gaps
- ❌ Minimal user control
- ❌ Generic charter output
- ❌ No project scaffolding

### **v2.0 (New Approach)**
- ✅ Structured data collection (12+ fields)
- ✅ Follows formal PM methodology
- ✅ AI enhances (not replaces) user input
- ✅ Personalized, detailed charter
- ✅ Complete project scaffolding (coming)

---

## 📋 The 5-Tab Workflow

### **Tab 1: Project Initiation Request** (Step 1 - Part 1)
Collect foundational data:
- Business Need
- Desired Outcomes
- Success Criteria
- Initial Risks & Assumptions

### **Tab 2: Business Case** (Step 1 - Part 2)
Build formal justification:
- Strategic Alignment
- Potential & Preferred Solutions
- Measurable Benefits
- High-Level Requirements
- Budget & Duration

### **Tab 3: AI Enhancement** (Optional)
AI suggests improvements:
- Review AI suggestions side-by-side with originals
- Accept, reject, or edit each suggestion
- You stay in control

### **Tab 4: Generate Charter**
Create formal charter document:
- Uses YOUR actual inputs (not AI confabulation)
- Preview full charter
- Download as Markdown

### **Tab 5: Create Project** (Coming Soon)
Full project scaffolding:
- Complete folder structure
- All boilerplate documents
- Git repository
- OpenProject workspace
- First 3 discrete tasks

---

## 🧠 ADHD-Friendly Design

**Problem:** Setup paralysis kills projects before they start

**Solution:** Remove ALL friction between idea and execution

**Workflow:**
```
Idea (5 min)
  ↓
Structured Form (10 min)
  ↓
Optional AI Polish (5 min)
  ↓
Click "Create Project" (30 sec)
  ↓
EVERYTHING EXISTS
  ↓
Start Working NOW
```

**Time from idea to execution: ~15 minutes**

---

## 🚀 Testing v2.0

### **Access Both Versions:**

**v1.0 (Production):**
- URL: http://10.69.1.86:8501
- Status: Running as system service
- Use: Quick AI-generated charters

**v2.0 (Test):**
- URL: http://10.69.1.86:8502
- Status: Manual launch for testing
- Use: Structured, personalized charters

### **Launch v2.0 Test Instance:**

```bash
/tmp/test-v2.sh
```

Or manually:
```bash
cd /home/ivesjl/project_wizard
./venv/bin/python app_streamlit_v2.py --server.port 8502
```

---

## 📊 Feature Comparison

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Input Method | 3-5 sentence brief | Structured 12+ field form |
| PM Methodology | Generic | Formal 4-Step Framework |
| AI Role | Generates everything | Enhances user input |
| User Control | Low | High |
| Charter Quality | Generic | Personalized |
| Project Scaffolding | ❌ | ✅ (coming) |
| OpenProject Integration | ❌ | ✅ (coming) |
| ADHD-Friendly | Partial | Full |

---

## 🔜 Coming in Next Update

Tab 5 will be completed to include:

### **Project Structure Creation**
```
project-name/
├── configs/
├── data/
│   ├── inbox/
│   ├── staging/
│   └── archive/
├── scripts/utils/
├── docs/
│   ├── PROJECT_CHARTER.md (✅ filled with your data)
│   ├── PROJECT_PLAN.md (generated from work breakdown)
│   └── ISSUES.md (linked to OpenProject)
├── README.md (project overview)
├── CHANGELOG.md (pre-formatted)
├── LICENSE.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
└── .gitignore
```

### **Git Repository**
- Initialized automatically
- First commit with all boilerplate
- Ready to push to GitHub

### **OpenProject Integration**
- Project created automatically
- Work packages from task breakdown
- Dependencies mapped
- Milestones set
- First 3 tasks highlighted

### **Immediate Next Actions**
```
✅ Project folder created: ~/projects/my-project
✅ Git initialized and committed
✅ OpenProject: http://10.69.1.86:8080/projects/my-project

🎯 Your next 3 tasks:
  1. Review PROJECT_CHARTER.md and update any details
  2. Set up development environment (see README.md)
  3. Create initial project structure (see PROJECT_PLAN.md)

cd ~/projects/my-project && code .
```

---

## 💡 Design Philosophy

**From your PM guidelines:**
> "A project plan's value is not in its perfection at kickoff, but in its power to create clarity, enforce discipline, and guide decisive action under pressure."

**v2.0 implements this by:**
1. ✅ Enforcing proper PM methodology
2. ✅ Collecting structured, quality inputs
3. ✅ Removing setup friction
4. ✅ Creating immediate actionable tasks
5. ✅ Supporting execution (not just planning)

---

## 🎓 Methodology Reference

Based on your formal PM framework:

**Step 1:** Project Owner Initiates (Tabs 1-2)
- Project Initiation Request
- Business Case
- **Output:** Project Charter

**Step 2:** Project Manager Plans (Tab 5 - coming)
- Work Breakdown Structure
- Task Dependencies
- Schedule & Resources
- **Output:** Project Plan + Complete Scaffolding

**Step 3:** Core Team Executes
- Work from discrete tasks in OpenProject
- All docs/structure ready to go

**Step 4:** Stakeholders Evaluate & Close
- Track in OpenProject
- Update CHANGELOG.md

---

## 🐛 Known Limitations (v2.0 Beta)

- ❌ Tab 5 (Create Project) not yet implemented
- ❌ Work breakdown UI not built
- ❌ OpenProject integration pending
- ⚠️ Running on port 8502 for testing (not systemd service yet)

---

## 📝 Feedback & Next Steps

**Test v2.0 and provide feedback on:**
1. Tab 1-2 form fields - are they clear and helpful?
2. AI Enhancement (Tab 3) - does it add value?
3. Charter output (Tab 4) - is it better than v1.0?
4. What else do you need in Tab 5?

**Once validated, we'll:**
1. Complete Tab 5 implementation
2. Replace v1.0 with v2.0 on port 8501
3. Update systemd service
4. Archive v1.0 as legacy

---

**Built:** November 2025  
**Author:** Jonathan Ives + AI Assistant  
**Purpose:** From Idea to Execution in 15 Minutes  
**Methodology:** Formal PM + ADHD-Friendly Design

🚀 **Ready to revolutionize your project initiation process!**
