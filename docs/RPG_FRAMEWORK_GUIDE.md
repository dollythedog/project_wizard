# RPG Framework Guide 🎮⚔️

**Transform Project Management into an Epic Quest**

## Overview

The Project Wizard uses an RPG (Role-Playing Game) metaphor to make project management more engaging and intuitive. Your project journey is framed as an epic quest with four main chapters, each with its own challenges, artifacts, and boss gates to overcome.

## The Four Chapters

### Chapter 1: The Call to Adventure 📜
**Phase:** Initiation  
**Icon:** Scroll/Quill  
**Primary Role:** Project Owner (The Champion)  
**Quest Description:** Draft your Project Charter — define the quest and win the council's approval

**Your Mission:**
- Identify the problem or opportunity
- Define the business case
- Document strategic alignment
- Set success criteria
- Create the Project Charter

**Artifacts (Loot):**
- 📜 PROJECT_CHARTER.md
- 📖 README.md
- 📋 Business Case documentation

**Boss Gate:** Ready for Planning (RfP)
- The Project Steering Committee reviews your charter
- Approval grants passage to the next chapter

---

### Chapter 2: The Strategist's Forge ⚙️
**Phase:** Planning  
**Icon:** Gear/Blueprint  
**Primary Role:** Project Manager (The Strategist)  
**Quest Description:** Forge your project's blueprint — set your scope, assign heroes, and plan the path

**Your Mission:**
- Break down deliverables into tasks
- Create work breakdown structure
- Estimate effort and costs
- Build project schedule
- Define roles and responsibilities (RACI)
- Set up RAID-C logs

**Artifacts (Loot):**
- ⚙️ PROJECT_PLAN.md (Project Handbook + Work Plan)
- 📊 ISSUES.md (Task tracking)
- 🗺️ Gantt charts and timelines
- 🛡️ RAID-C log (Risk management)

**Boss Gate:** Ready for Execution (RfE)
- Steering Committee reviews the plan
- Resource commitments secured
- Baselined scope, schedule, and budget

---

### Chapter 3: The Campaign of Execution ⚔️
**Phase:** Execution  
**Icon:** Sword/Hammer  
**Primary Role:** Core Team (The Warriors)  
**Quest Description:** Embark on your campaign — complete milestones, slay risks, and gather loot

**Your Mission:**
- Execute the work plan
- Produce deliverables
- Monitor progress (Active Buffs system)
- Manage risks and issues
- Control changes
- Report status to stakeholders

**Artifacts (Loot):**
- 💎 Project Deliverables (the treasure!)
- 📈 Status Reports
- ✅ Completed Tasks
- 🏆 Milestone achievements

**Boss Gate:** Ready for Closure (RfC)
- All deliverables completed
- Quality verified
- Formal acceptance by Project Owner

---

### Chapter 4: The Chronicle of Wisdom 📚
**Phase:** Closure  
**Icon:** Tome/Trophy  
**Primary Role:** Stakeholders (The Council)  
**Quest Description:** Record your saga — lessons learned and victories immortalized

**Your Mission:**
- Conduct project-end review
- Document lessons learned
- Create post-project recommendations
- Archive project documents
- Release resources
- Celebrate success!

**Artifacts (Loot):**
- 📚 PROJECT-END REPORT
- 🏆 Achievement badges
- 📝 Lessons Learned document
- 🎖️ Team recognition

**Final Gate:** Project Complete ✓
- Official sign-off
- Knowledge transfer complete
- Project archived

---

## The Quest Map

When you run `project-wizard status`, you'll see your quest map:

```
⚔️  PROJECT QUEST MAP  ⚔️
┌────────────────────────────────────────┐
│ Project: My Awesome Project            │
│ Progress: 50% [██████████░░░░░░░░░░]   │
└────────────────────────────────────────┘

┌─ Quest Progression ─────────────────────┐
│                                          │
│ ✓ 📜 INITIATION  ⚙️ PLANNING  🗡️ EXECUTION  📚 CLOSURE │
│         ──→            ──→           ──→              │
│         ▼ YOU                                         │
│   ◆ RfP ◆      ◇ RfE ◇      ○ RfC ○      ○ ✓ ○       │
│                                          │
└──────────────────────────────────────────┘

🎯 Current Quest:
⚙️ The Strategist's Forge

Forge your project's blueprint — set your scope, 
assign heroes, and plan the path

🚩 Next Milestone:
Ready for Execution (RfE) Gate Approval
```

## Gate Symbols

- **◆ Approved** (Green diamond) - Gate passed! ✅
- **◇ Pending** (Yellow diamond) - Ready for review
- **○ Not Reached** (Gray circle) - Future checkpoint

## Progress Tracking

Your project progress is tracked with a **weighted system**:
- Initiation: 25%
- Planning: 25%
- Execution: 40% (the longest phase)
- Closure: 10%

Each phase contributes to your overall quest completion percentage.

## Commands & Your Quest

### `project-wizard init`
**Begins your adventure!**
- Starts Chapter 1: The Call to Adventure
- Generates your charter and initial artifacts
- Initializes quest tracking

### `project-wizard plan`
**Advances to Chapter 2**
- Completes Initiation and approves RfP gate
- Unlocks The Strategist's Forge
- Creates your battle plan

### `project-wizard status`
**Views your quest map**
- Shows current chapter
- Displays progress and gates
- Lists next objectives
- Use `-d` flag for detailed info

### `project-wizard sync` (Coming Soon)
**Syncs with OpenProject**
- Integrates with your project management tool
- Creates work packages
- Syncs progress

## The Hero's Journey

This framework is inspired by Joseph Campbell's "Hero's Journey" and formal project management methodologies:

1. **Call to Adventure** → Problem identification & charter
2. **Meeting the Mentor** → Gathering stakeholders & planning
3. **Crossing the Threshold** → RfP Gate approval
4. **Tests, Allies, Enemies** → Execution phase
5. **Approach to the Inmost Cave** → Critical milestones
6. **Ordeal** → Overcoming major risks/issues
7. **Reward** → Deliverables completed
8. **Return with the Elixir** → Project closure & lessons learned

## Tips for Quest Masters

**For Project Owners:**
- Think of yourself as the **quest giver** who defines the mission
- Your charter is the **quest scroll** that motivates the team
- Gate approvals are your **checkpoints** to ensure quality

**For Project Managers:**
- You're the **strategic general** planning the campaign
- Your work breakdown is the **battle strategy**
- RAID-C logs are your **threat assessment**

**For Team Members:**
- You're the **heroes** who do the actual work
- Tasks are your **quests** and **side quests**
- Deliverables are the **treasure** you collect

## Customization

You can customize the RPG experience:

1. **Phase Icons:** Replace PNG images in `docs/images/`
2. **Quest Descriptions:** Edit `phase_state.py` metadata
3. **Colors:** Adjust `phase_navigator.py` color schemes
4. **Achievement System:** (Coming soon) Unlock badges for milestones

## Philosophy

Why use an RPG metaphor for project management?

- **Engagement:** Makes PM activities more enjoyable
- **Clarity:** Visualizes abstract concepts (gates, phases)
- **Motivation:** Progress tracking feels like leveling up
- **Gamification:** Encourages completion and best practices
- **Accessibility:** Reduces PM jargon for non-PM audiences

Project management doesn't have to be boring spreadsheets. It can be an **epic adventure** where you build something meaningful, overcome challenges, and emerge victorious! 

---

*"The brave may not live forever, but the cautious do not live at all." – Project Management Proverb (probably)*
