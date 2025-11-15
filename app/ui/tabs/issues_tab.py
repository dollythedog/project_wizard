"""
Issues tab with Kanban board view.
"""
import streamlit as st

from app.models.issue import IssueStatus
from app.services.issue_manager import IssueManager


def render_issues_tab(issue_manager: IssueManager):
    """Render the Issues tab with Kanban board."""
    
    st.title("📋 Issues - Kanban Board")
    st.caption("Visual issue tracking for Project Wizard")
    
    # Get all issues
    try:
        all_issues = issue_manager.get_all_issues()
        projects = issue_manager.get_unique_projects()
        issue_counts = issue_manager.get_issue_counts_by_status()
    except Exception as e:
        st.error(f"Error loading issues: {e}")
        return
    
    # Project filter
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Add "All Projects" option
        project_options = ["All Projects"] + projects
        selected_project = st.selectbox(
            "Filter by Project",
            project_options,
            key="issue_project_filter"
        )
    
    with col2:
        st.metric("Total Issues", len(all_issues))
    
    with col3:
        high_priority = sum(1 for i in all_issues if i.priority.value == "high")
        st.metric("High Priority", high_priority, delta=None, delta_color="off")
    
    st.divider()
    
    # Filter issues by selected project
    if selected_project != "All Projects":
        filtered_issues = [i for i in all_issues if i.project == selected_project]
    else:
        filtered_issues = all_issues
    
    # Create Kanban columns
    col_backlog, col_progress, col_review, col_done = st.columns(4)
    
    # Separate issues by status
    backlog_issues = [i for i in filtered_issues if i.status == IssueStatus.BACKLOG]
    progress_issues = [i for i in filtered_issues if i.status == IssueStatus.IN_PROGRESS]
    review_issues = [i for i in filtered_issues if i.status == IssueStatus.REVIEW]
    done_issues = [i for i in filtered_issues if i.status == IssueStatus.DONE]
    
    # Render Backlog column
    with col_backlog:
        st.markdown("### 🔵 Backlog")
        st.caption(f"{len(backlog_issues)} issues")
        st.markdown("---")
        for issue in backlog_issues:
            _render_issue_card(issue)
    
    # Render In Progress column
    with col_progress:
        st.markdown("### 🟢 In Progress")
        st.caption(f"{len(progress_issues)} issues")
        st.markdown("---")
        for issue in progress_issues:
            _render_issue_card(issue)
    
    # Render Review column
    with col_review:
        st.markdown("### 🟡 Review")
        st.caption(f"{len(review_issues)} issues")
        st.markdown("---")
        for issue in review_issues:
            _render_issue_card(issue)
    
    # Render Done column
    with col_done:
        st.markdown("### ✅ Done")
        st.caption(f"{len(done_issues)} issues")
        st.markdown("---")
        for issue in done_issues:
            _render_issue_card(issue)
    
    # Summary at bottom
    st.divider()
    st.caption(f"Showing {len(filtered_issues)} of {len(all_issues)} issues")


def _render_issue_card(issue):
    """Render an individual issue card."""
    
    # Card container
    with st.container():
        # Priority emoji + ID + Title
        st.markdown(
            f"{issue.priority.to_emoji()} **{issue.id}** - {issue.get_short_title(40)}"
        )
        
        # Project tag and component
        tag_col1, tag_col2 = st.columns(2)
        with tag_col1:
            st.caption(f"🏷️ [{issue.get_project_tag()}]")
        with tag_col2:
            st.caption(f"📦 {issue.component}")
        
        # Expander for details
        if issue.description:
            with st.expander("Details", expanded=False):
                st.markdown(issue.description)
                if issue.solution:
                    st.markdown("**Solution:**")
                    st.markdown(issue.solution)
        
        # Spacer
        st.markdown("")
