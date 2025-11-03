# 📋 PROJECT CHARTER

**Project Title:** Project Wizard  
**Project Sponsor:** Jonathan Ives  
**Department:** Personal Tools / Texas Pulmonary & Critical Care Consultants  
**Date:** November 2025

---

## 1. Project Goal

**Desired Outcome:**  
Create an interactive CLI tool that automates project initiation following formal project management methodology, with seamless OpenProject integration.

**Success Measures:**
- Interactive charter wizard captures all required fields (12+ data points)
- Generates professional PROJECT_CHARTER.md automatically
- Creates standardized repository structure
- Successfully imports projects into OpenProject
- Reduces project setup time from 2+ hours to <15 minutes

---

## 2. Problem / Opportunity Definition

**Problem:**  
Currently, starting a new project requires manually creating:
- Project charter documents
- Repository structure  
- README and documentation
- OpenProject project and work packages
- Git initialization

This manual process is time-consuming, inconsistent, and prone to missing important elements like risk assessment or stakeholder identification.

**Opportunity:**  
Automating this workflow enables consistent, high-quality project documentation while significantly reducing setup time. The tool codifies proven project management methodology.

---

## 3. Proposed Solution

**Solution Overview:**  
Build a Python CLI tool that:
- Guides users through interactive charter creation (Prompts 1 + 2)
- Generates documents from Jinja2 templates
- Creates standardized folder structures
- Syncs with OpenProject via REST API
- Supports multiple project types (software, clinical, infrastructure)

**Why this approach:**
- Interactive CLI is fast and doesn't require web server
- Can be Dockerized for deployment alongside OpenProject
- Reusable across home server and office server
- Python ecosystem provides excellent libraries (Click, Pydantic, Jinja2)

---

## 4. Alignment with Strategic Goals

- **Personal Productivity:** Streamlines project initiation workflow
- **Quality:** Ensures consistent documentation and methodology
- **Knowledge Management:** Codifies project management best practices
- **Scalability:** Can be shared with team for standardization
- **Technology Modernization:** Integrates with OpenProject platform

---

## 5. Selection Criteria

| Criteria | Description |
|---------|-------------|
| **Efficiency** | Reduces project setup from 2+ hours to <15 minutes |
| **Quality** | Ensures no project management elements are missed |
| **Consistency** | Standardizes project structure across all initiatives |
| **Integration** | Works seamlessly with existing OpenProject instance |

---

## 6. Cost / Benefit Analysis

### **Benefits**

**Tangible:**
- 1.75+ hours saved per project setup
- Consistent documentation quality
- Reduced errors and missing elements

**Intangible:**
- Reduced mental overhead for project starts
- Codified organizational knowledge
- Team collaboration enablement

### **Costs**
- Development time: ~16 hours (Phase 1 complete)
- Ongoing maintenance: ~2 hours/month
- Zero infrastructure cost (runs on existing servers)

---

## 7. Scope

**In-Scope:**
- Phase 1: Interactive charter wizard ✅
- Phase 2: Planning wizard with work breakdown
- Phase 3: OpenProject sync (bidirectional)
- Document generation (charter, plan, issues)
- Repository bootstrapping
- Project type templates
- Docker deployment

**Out-of-Scope:**
- Web-based UI (CLI only for MVP)
- Multi-user authentication
- Cloud hosting
- Integration with tools other than OpenProject

---

## 8. Major Deliverables

| **Deliverable** | **Description** | **Status** |
|----------------|----------------|------------|
| **CLI Tool** | Interactive project wizard | ✅ Phase 1 Complete |
| **Charter Wizard** | Captures all Prompt 1 + 2 fields | ✅ Complete |
| **Document Templates** | Jinja2 templates for charter, plan, issues | ✅ Charter done |
| **OpenProject Client** | REST API integration | ⏳ Planned |
| **Docker Deployment** | Container for easy deployment | ⏳ Planned |
| **Documentation** | User guide and technical docs | ✅ Complete |

---

## 9. Major Obstacles

- OpenProject API learning curve (mitigated by patio-drainage POC)
- Ensuring templates work for all project types
- Maintaining backward compatibility as tool evolves
- Windows server deployment differences (Docker on Windows)

---

## 10. Risks & Mitigation

| **Risk** | **Mitigation Strategy** |
|---------|------------------------|
| OpenProject API changes | Use stable v3 API, version pin dependencies |
| Tool adoption resistance | Keep CLI simple, provide clear help text |
| Template inflexibility | Support custom templates via YAML configs |
| Docker deployment issues | Test on both Ubuntu and Windows environments |

---

## 11. Schedule Overview

### **Phase 1: Initiation** ✅ Complete (Nov 3, 2025)
- Charter wizard implementation
- Document generation
- Repository bootstrapping

### **Phase 2: Planning** (Week of Nov 4)
- Work breakdown wizard
- PROJECT_PLAN.md generation
- ISSUES.md template

### **Phase 3: Integration** (Week of Nov 11)
- OpenProject sync implementation
- Project type templates (YAML)
- Bidirectional sync for ISSUES.md

### **Phase 4: Deployment** (Week of Nov 18)
- Docker containerization
- Deploy on home server
- Migrate to office server with OpenProject

**Total Timeline:** 3-4 weeks to full production

---

## 12. Collaboration Needs

| **Collaborator** | **Role** | **Timing** |
|-----------------|---------|-----------|
| Jonathan Ives (self) | Developer, PM, User | Throughout |
| OpenProject Community | API documentation, examples | Ongoing |
| GitHub Community | Open source collaboration (optional) | Post-launch |

---

## ✅ Summary

Project Wizard automates the project initiation phase by capturing charter data interactively and generating professional documentation. Phase 1 (charter wizard) is complete and demonstrates the viability of this approach. The tool will significantly improve project management efficiency and consistency.

**Status:** Phase 1 Complete - Ready for Phase 2 (Planning Wizard)

---

*Generated on 2025-11-03*
