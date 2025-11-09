# Project Charter: Hermes - Trading Application

**Project Owner:** Jonathan Ives  
**Project Type:** Software Development  
**Date:** November 9, 2025  
**Status:** Draft

## Business Need

Conducting thorough research for stock trading necessitates significant effort and focus. The extensive workload often discourages potential investors. The checklist for this research typically comprises 50 to 100 questions, presented in a lengthy document.

## Desired Outcomes

Implement AI agents to streamline the investment checklist process, enabling comprehensive research on investments within an organized database. This system will facilitate comparisons of various investment options, track performance in real-time, and identify potential investments. Additionally, it will gather performance data to train the agents over time based on actual stock market outcomes.

## Success Criteria

- A real-time dashboard that retrieves potential investment options and provides recommendations based on the Relative Deal Quality Scale:

| **Score Range** | **Descriptor**        | **Suggested Framing**                                        |
| --------------- | --------------------- | ------------------------------------------------------------ |
| **100%**        | **Absolute Steal**    | Once-in-a-lifetime bargain — exceptional value.              |
| **86 – 99%**    | **Outstanding Deal**  | Hard to beat — clearly below fair market value.              |
| **71 – 85%**    | **Strong Value**      | Definitely favorable — priced well for what you get.         |
| **56 – 70%**    | **Fair Deal**         | Balanced — reasonable trade-off between price and quality.   |
| **46 – 55%**    | **Borderline Value**  | Could go either way — depends on priorities or context.      |
| **31 – 45%**    | **Questionable Deal** | Probably paying a bit too much — value isn’t clear.          |
| **16 – 30%**    | **Poor Deal**         | Overpriced for what’s offered — better options likely exist. |
| **1 – 15%**     | **Bad Deal**          | Clearly not worth it — buyer disadvantage.                   |
| **0%**          | **Rip-Off**           | No redeeming value — avoid at all costs.                     |

## Strategic Alignment

**Financial Stability and Security:** Achieving financial success is a personal goal. I am dedicated to attaining financial stability by actively managing my finances. My priorities include increasing my income, making informed saving decisions, and spending wisely. I aim to create a secure financial future for myself and my family while enjoying a comfortable and fulfilling lifestyle.

## Preferred Solution

I propose developing a lightweight and responsive terminal application (using Streamlit or Flask) with a PostgreSQL database to organize information. This application will employ a Multi-Agent Collaboration strategy to create an Agentic AI Investment Application. The architecture will consist of multiple specialized agents working together on complex tasks, coordinated by a central manager. Given the extensive number of research questions (50-100), parallelization will be utilized to divide this large task into independent segments that can be processed simultaneously by multiple workers. The following outlines the steps and agent roles:

| Step                               | Agent Role                                | Function                                                                                                                                                                                                                                  |
| ---------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1. Complex Task Input**         | _User/System_                             | Input the investment target along with the 50-100 checklist questions, categorized into specialized domains (e.g., "Business Basics").                                                                                                                                  |
| **2. Orchestration & Planning**   | **Coordinator/Manager Agent**             | Receives the complex task and defines specialist roles. The Manager analyzes the input and determines how to divide the large task into independent subtasks (Parallelization). It provides context and assigns tasks to the Research Agents. |
| **3. Execution & Data Gathering** | **Specialized Research Agents** (Workers) | These agents operate in parallel to maximize efficiency (similar to 10 people reading different chapters at the same time). Each worker utilizes external tools, such as web scraping or search APIs, as needed for information or actions. Each worker agent retries until it successfully completes its specific task, collecting the required data for its assigned domain (e.g., "Strengths and Weaknesses"). |
| **4. Synthesis & Recommendation** | **Advisor Agent**                         | This agent serves as the final coordination step, responsible for normalizing and merging results from all Specialized Research Agents. Normalization ensures results are formatted consistently. It simplifies the merged results into a single output, generating the final summary and making specific investment recommendations. |

The benefits of this solution include: 
- **Specialization:** Agents focus on specific investment domains, enhancing clarity and quality.
- **Efficiency:** Parallelization allows simultaneous processing of the extensive checklist (50+ questions), significantly reducing data collection and analysis time.
- **Coordination:** The Manager Agent orchestrates the process, ensuring all outputs are collected and correctly passed to the Advisor Agent.

## Measurable Benefits

Potential metrics to track include investment returns and an analysis of historical accuracy.

## Requirements

- The application must run on my mini-server as a systemd process to ensure continuous operation.
- An easy notification system is needed; I plan to use ntfy.
- A library of prompts will be required.
- An API key is necessary (I currently have one from OpenAI).

## Budget & Timeline

**Budget:** Token charges for the AI agent. When I build a self-hosted AI, the estimated cost is $2,000.  
**Duration:** 6 weeks.

## Risks & Assumptions

- The accuracy of the information fetched is a critical assumption.
- A potential risk includes the possibility of providing poor investment recommendations.

## Approvals

**Sponsor:** ___________________________ Date: ___________  
**Project Owner:** ______________________ Date: ___________  
**Stakeholder:** ________________________ Date: ___________