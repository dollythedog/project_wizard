"""
Phase Navigator - RPG-Style Quest Map Display

Renders the project phase progression as a retro ASCII/emoji quest map
with rich terminal formatting.
"""


from rich.box import HEAVY, ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..models.phase_state import GateStatus, PhaseGate, PhaseState, ProjectPhase

console = Console()


class PhaseNavigator:
    """
    Renders the project's phase progression as a quest map

    Displays:
    - 4 phases with icons and quest descriptions
    - Current location in the journey
    - Gate approval status (RfP, RfE, RfC)
    - Progress indicators
    """

    # Color schemes
    PHASE_COLORS = {
        ProjectPhase.INITIATION: "yellow",
        ProjectPhase.PLANNING: "magenta",
        ProjectPhase.EXECUTION: "cyan",
        ProjectPhase.CLOSURE: "green"
    }

    GATE_COLORS = {
        GateStatus.NOT_REACHED: "dim white",
        GateStatus.PENDING: "yellow",
        GateStatus.APPROVED: "bold green",
        GateStatus.REJECTED: "bold red"
    }

    def __init__(self, phase_state: PhaseState):
        self.state = phase_state

    def render_quest_map(self, show_details: bool = False) -> None:
        """
        Render the complete quest map

        Args:
            show_details: Show extended information for each phase
        """
        console.print()
        console.print(self._build_header())
        console.print()
        console.print(self._build_phase_flow())
        console.print()

        if show_details:
            console.print(self._build_phase_details())
            console.print()

        console.print(self._build_next_steps())
        console.print()

    def _build_header(self) -> Panel:
        """Build the quest map header"""
        progress_pct = self.state.get_progress_percentage()

        title = Text()
        title.append("⚔️  PROJECT QUEST MAP  ⚔️", style="bold cyan")

        content = Text()
        content.append("Project: ", style="bold")
        content.append(f"{self.state.project_title}\n", style="bold white")
        content.append("Progress: ", style="bold")
        content.append(f"{progress_pct}% ", style="bold green")
        content.append(self._progress_bar(progress_pct))

        return Panel(
            content,
            title=title,
            border_style="cyan",
            box=HEAVY,
            padding=(1, 2)
        )

    def _progress_bar(self, pct: int, width: int = 20) -> str:
        """Simple ASCII progress bar"""
        filled = int((pct / 100) * width)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}]"

    def _build_phase_flow(self) -> Panel:
        """Build the main phase flow diagram"""

        flow_lines = []

        # Line 1: Phase names with icons
        flow_lines.append(self._render_phase_line())

        # Line 2: Arrows and current position
        flow_lines.append(self._render_connection_line())

        # Line 3: Gate approvals
        flow_lines.append(self._render_gate_line())

        content = "\n".join(flow_lines)

        return Panel(
            content,
            title="[bold]Quest Progression[/bold]",
            border_style="blue",
            box=ROUNDED,
            padding=(1, 2)
        )

    def _render_phase_line(self) -> str:
        """Render the phase names with icons"""
        phases = [
            (ProjectPhase.INITIATION, "📜", "INITIATION"),
            (ProjectPhase.PLANNING, "⚙️", "PLANNING"),
            (ProjectPhase.EXECUTION, "⚔️", "EXECUTION"),
            (ProjectPhase.CLOSURE, "📚", "CLOSURE")
        ]

        parts = []
        for phase, icon, name in phases:
            is_current = (phase == self.state.current_phase)
            is_complete = self.state.get_phase_metadata(phase).completed_at is not None

            color = self.PHASE_COLORS[phase]

            if is_current:
                # Highlight current phase
                parts.append(f"[bold {color} reverse] {icon} {name} [/]")
            elif is_complete:
                # Completed phase
                parts.append(f"[{color}]✓ {icon} {name}[/]")
            else:
                # Future phase
                parts.append(f"[dim]{icon} {name}[/]")

        return "  ".join(parts)

    def _render_connection_line(self) -> str:
        """Render arrows showing flow and current position"""
        # Position marker
        marker_positions = {
            ProjectPhase.INITIATION: 8,
            ProjectPhase.PLANNING: 32,
            ProjectPhase.EXECUTION: 58,
            ProjectPhase.CLOSURE: 84
        }

        current_pos = marker_positions.get(self.state.current_phase, 8)

        # Build arrow line
        line = " " * 100
        line_parts = list(line)

        # Add arrows between phases
        arrow_positions = [22, 48, 74]
        for pos in arrow_positions:
            if pos < len(line_parts) - 2:
                line_parts[pos:pos+3] = "──→"

        # Add current position marker
        if current_pos < len(line_parts) - 4:
            line_parts[current_pos:current_pos+4] = "[bold yellow]▼ YOU[/]"

        return "".join(line_parts[:95])

    def _render_gate_line(self) -> str:
        """Render gate approval status"""
        gates = [
            ("RfP", self.state.rfp_status, 22),
            ("RfE", self.state.rfe_status, 48),
            ("RfC", self.state.rfc_status, 74),
            ("✓", GateStatus.APPROVED if self.state.project_complete else GateStatus.NOT_REACHED, 95)
        ]

        line = " " * 100
        list(line)

        for _gate_name, status, _pos in gates:
            color = self.GATE_COLORS[status]

            if status == GateStatus.APPROVED or status == GateStatus.PENDING:
                pass
            else:
                pass

            # This is a simplification - Rich markup makes exact positioning tricky
            # In real implementation, you'd need to track visible vs markup length

        # Simplified: just show gates in order
        gate_displays = []
        for gate_name, status, _ in gates:
            color = self.GATE_COLORS[status]
            if status == GateStatus.APPROVED:
                gate_displays.append(f"[{color}]◆ {gate_name}[/]")
            elif status == GateStatus.PENDING:
                gate_displays.append(f"[{color}]◇ {gate_name}[/]")
            else:
                gate_displays.append(f"[{color}]○ {gate_name}[/]")

        return "      " + "        ".join(gate_displays)

    def _build_phase_details(self) -> Table:
        """Build detailed phase information table"""
        table = Table(title="Chapter Details", show_header=True, header_style="bold cyan")

        table.add_column("Chapter", style="bold", width=12)
        table.add_column("Quest", style="", width=50)
        table.add_column("Status", justify="center", width=12)

        for phase in [ProjectPhase.INITIATION, ProjectPhase.PLANNING,
                      ProjectPhase.EXECUTION, ProjectPhase.CLOSURE]:
            meta = self.state.get_phase_metadata(phase)

            # Chapter name
            chapter = f"{meta.icon_emoji} {meta.chapter_title}"

            # Quest description
            quest = meta.quest_description

            # Status
            if meta.completed_at:
                status = "[green]✓ Complete[/]"
            elif meta.started_at:
                status = "[yellow]⚡ Active[/]"
            else:
                status = "[dim]○ Locked[/]"

            table.add_row(chapter, quest, status)

        return table

    def _build_next_steps(self) -> Panel:
        """Build next steps/quest objectives"""
        next_gate = self.state.get_next_gate()
        current_meta = self.state.get_phase_metadata(self.state.current_phase)

        content = Text()
        content.append("🎯 Current Quest:\n", style="bold yellow")
        content.append(f"{current_meta.icon_emoji} {current_meta.chapter_title}\n\n", style="bold")
        content.append(f"{current_meta.quest_description}\n\n", style="")

        if next_gate:
            gate_names = {
                PhaseGate.RFP: "Ready for Planning (RfP)",
                PhaseGate.RFE: "Ready for Execution (RfE)",
                PhaseGate.RFC: "Ready for Closure (RfC)",
                PhaseGate.COMPLETE: "Project Complete"
            }

            content.append("🚩 Next Milestone:\n", style="bold cyan")
            content.append(f"{gate_names[next_gate]} Gate Approval\n", style="")

        if self.state.project_complete:
            content.append("\n🏆 ", style="")
            content.append("Quest Complete! Project successfully delivered.", style="bold green")

        return Panel(
            content,
            title="[bold]Quest Objectives[/bold]",
            border_style="yellow",
            box=ROUNDED,
            padding=(1, 2)
        )

    def render_compact(self) -> None:
        """Render a compact one-line status"""
        progress_pct = self.state.get_progress_percentage()
        current_meta = self.state.get_phase_metadata(self.state.current_phase)

        status = Text()
        status.append(f"{current_meta.icon_emoji} ", style="")
        status.append(f"{self.state.project_title}", style="bold")
        status.append(f" • {current_meta.chapter_title} • ", style="dim")
        status.append(f"{progress_pct}% ", style="green")
        status.append(self._progress_bar(progress_pct, width=10))

        console.print(status)

    def render_phase_badge(self, phase: ProjectPhase) -> str:
        """Render a single phase as a badge string"""
        meta = self.state.get_phase_metadata(phase)
        color = self.PHASE_COLORS[phase]

        if phase == self.state.current_phase:
            return f"[bold {color} reverse] {meta.icon_emoji} {phase.value.upper()} [/]"
        elif meta.completed_at:
            return f"[{color}]✓ {meta.icon_emoji} {phase.value.upper()}[/]"
        else:
            return f"[dim]{meta.icon_emoji} {phase.value.upper()}[/]"


def display_quest_map(phase_state: PhaseState, detailed: bool = True):
    """
    Convenience function to display the quest map

    Args:
        phase_state: Current phase state
        detailed: Show detailed information
    """
    navigator = PhaseNavigator(phase_state)
    navigator.render_quest_map(show_details=detailed)
