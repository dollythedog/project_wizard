"""Tab UI components."""
from app.ui.tabs.charter_tab import render_charter_tab
from app.ui.tabs.deliverables_tab import render_deliverables_tab
from app.ui.tabs.docs_tab import render_docs_tab
from app.ui.tabs.home_tab import render_home_tab
from app.ui.tabs.issues_tab import render_issues_tab

__all__ = [
    "render_charter_tab",
    "render_deliverables_tab",
    "render_docs_tab",
    "render_home_tab",
    "render_issues_tab",
]
