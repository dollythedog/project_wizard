#!/usr/bin/env python3
"""
Demo script to test AI agents without full wizard integration.
Run this after OpenAI billing is enabled to verify everything works.
"""

import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.ai_agents import LLMClient, CharterAgent, CriticAgent

console = Console()

def main():
    """Run AI agent demos."""
    load_dotenv()
    
    console.print(Panel.fit(
        "[bold cyan]Project Wizard AI Agents Demo[/bold cyan]\n"
        "Testing charter drafting and critique capabilities",
        title="🧙‍♂️ AI Demo"
    ))
    
    # Test project idea
    project_brief = """
    Create a web dashboard for monitoring clinical productivity metrics.
    Pull data from EHR CSV exports, visualize provider performance,
    and send weekly reports. Target users: clinic managers and medical directors.
    """
    
    context = {
        "department": "Texas Pulmonary & Critical Care Consultants",
        "project_type": "software_mvp",
        "budget": 5000.0
    }
    
    try:
        console.print("\n[yellow]Initializing AI agents...[/yellow]")
        charter_agent = CharterAgent()
        critic_agent = CriticAgent()
        
        # Draft business need
        console.print("\n[green]Step 1:[/green] Drafting Business Need section...")
        business_need = charter_agent.draft_business_need(project_brief, context)
        console.print(Panel(Markdown(business_need), title="Business Need (AI Draft)", border_style="green"))
        
        # Draft success criteria
        console.print("\n[green]Step 2:[/green] Drafting Success Criteria...")
        success_criteria = charter_agent.draft_success_criteria(project_brief, context)
        console.print(Panel(Markdown(success_criteria), title="Success Criteria (AI Draft)", border_style="green"))
        
        # Draft risks
        console.print("\n[green]Step 3:[/green] Drafting Risks & Mitigation...")
        risks = charter_agent.draft_risks_and_mitigation(project_brief, context)
        console.print(Panel(Markdown(risks), title="Risks & Mitigation (AI Draft)", border_style="green"))
        
        # Quick review of business need section
        console.print("\n[blue]Step 4:[/blue] AI Critic reviewing Business Need section...")
        review = critic_agent.quick_review("Business Need", business_need)
        
        console.print(f"\n[bold]Score:[/bold] {review.get('score', 0)}/100")
        if review.get('strengths'):
            console.print("\n[green]Strengths:[/green]")
            for strength in review['strengths']:
                console.print(f"  ✓ {strength}")
        if review.get('improvements'):
            console.print("\n[yellow]Improvements:[/yellow]")
            for improvement in review['improvements']:
                console.print(f"  • {improvement}")
        
        console.print("\n[bold green]✅ Demo completed successfully![/bold green]")
        console.print("\n[dim]The AI agents are working correctly. Ready to integrate with project-wizard init --ai-assist[/dim]")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {e}")
        if "insufficient_quota" in str(e):
            console.print("\n[yellow]⚠️  OpenAI billing not enabled yet.[/yellow]")
            console.print("Please add payment method at: https://platform.openai.com/settings/organization/billing/overview")
        sys.exit(1)

if __name__ == "__main__":
    main()
