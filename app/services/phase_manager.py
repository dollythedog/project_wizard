"""
Phase Manager Service

Manages loading, saving, and updating project phase state.
Handles phase transitions and gate approvals.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..models.charter import CharterData
from ..models.phase_state import PhaseGate, PhaseState, ProjectPhase


class PhaseManager:
    """
    Service for managing project phase state persistence

    Phase state is stored in data/inbox/phase_state.json within the project.
    """

    PHASE_STATE_FILENAME = "phase_state.json"

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize phase manager

        Args:
            project_root: Path to project root. If None, uses current directory.
        """
        project_root = Path.cwd() if project_root is None else Path(project_root)

        self.project_root = project_root
        self.data_inbox = project_root / "data" / "inbox"
        self.phase_state_path = self.data_inbox / self.PHASE_STATE_FILENAME

    def load_state(self) -> Optional[PhaseState]:
        """
        Load phase state from project

        Returns:
            PhaseState if exists, None otherwise
        """
        if not self.phase_state_path.exists():
            return None

        try:
            with open(self.phase_state_path, encoding='utf-8') as f:
                data = json.load(f)
                return PhaseState(**data)
        except Exception as e:
            print(f"Warning: Failed to load phase state: {e}")
            return None

    def save_state(self, state: PhaseState) -> bool:
        """
        Save phase state to project

        Args:
            state: PhaseState to save

        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure data directory exists
            self.data_inbox.mkdir(parents=True, exist_ok=True)

            # Update timestamp
            state.last_updated = datetime.now()

            # Save to JSON
            with open(self.phase_state_path, 'w', encoding='utf-8') as f:
                json.dump(
                    state.model_dump(mode='json'),
                    f,
                    indent=2,
                    default=str
                )
            return True
        except Exception as e:
            print(f"Error: Failed to save phase state: {e}")
            return False

    def init_state(self, charter: CharterData) -> PhaseState:
        """
        Initialize a new phase state from charter

        Args:
            charter: Project charter data

        Returns:
            New PhaseState
        """
        state = PhaseState(
            project_title=charter.project_title,
            project_created_at=datetime.now()
        )

        # Mark initiation as started
        state.initiation.started_at = datetime.now()
        state.initiation.artifacts.append("PROJECT_CHARTER.md")
        state.initiation.artifacts.append("README.md")

        return state

    def advance_phase(self, state: PhaseState, to_phase: ProjectPhase) -> PhaseState:
        """
        Advance project to a new phase

        Args:
            state: Current phase state
            to_phase: Phase to advance to

        Returns:
            Updated phase state
        """
        state.advance_to_phase(to_phase)
        return state

    def approve_gate(self, state: PhaseState, gate: PhaseGate) -> PhaseState:
        """
        Approve a phase gate

        Args:
            state: Current phase state
            gate: Gate to approve

        Returns:
            Updated phase state
        """
        state.approve_gate(gate)
        return state

    def complete_initiation(self, state: PhaseState) -> PhaseState:
        """
        Mark initiation phase as complete and approve RfP gate

        Args:
            state: Current phase state

        Returns:
            Updated phase state
        """
        state.initiation.completed_at = datetime.now()
        state.approve_gate(PhaseGate.RFP)
        return state

    def complete_planning(self, state: PhaseState) -> PhaseState:
        """
        Mark planning phase as complete and approve RfE gate

        Args:
            state: Current phase state

        Returns:
            Updated phase state
        """
        state.planning.completed_at = datetime.now()
        state.planning.artifacts.append("PROJECT_PLAN.md")
        state.planning.artifacts.append("ISSUES.md")
        state.approve_gate(PhaseGate.RFE)
        return state

    def add_artifact(self, state: PhaseState, artifact_name: str,
                    phase: Optional[ProjectPhase] = None) -> PhaseState:
        """
        Add an artifact to a phase

        Args:
            state: Current phase state
            artifact_name: Name of artifact (e.g., "PROJECT_CHARTER.md")
            phase: Phase to add to (defaults to current)

        Returns:
            Updated phase state
        """
        if phase is None:
            phase = state.current_phase

        meta = state.get_phase_metadata(phase)
        if artifact_name not in meta.artifacts:
            meta.artifacts.append(artifact_name)

        return state

    def add_note(self, state: PhaseState, note: str,
                phase: Optional[ProjectPhase] = None) -> PhaseState:
        """
        Add a note to a phase

        Args:
            state: Current phase state
            note: Note text
            phase: Phase to add to (defaults to current)

        Returns:
            Updated phase state
        """
        if phase is None:
            phase = state.current_phase

        meta = state.get_phase_metadata(phase)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        meta.notes += f"\n[{timestamp}] {note}"

        return state

    @staticmethod
    def get_or_create_state(project_root: Optional[Path] = None,
                           charter: Optional[CharterData] = None) -> PhaseState:
        """
        Get existing phase state or create a new one

        Args:
            project_root: Project root directory
            charter: Charter data for new projects

        Returns:
            PhaseState (existing or new)
        """
        manager = PhaseManager(project_root)

        # Try to load existing
        state = manager.load_state()
        if state:
            return state

        # Create new
        if charter:
            state = manager.init_state(charter)
            manager.save_state(state)
            return state

        # Default empty state
        state = PhaseState()
        return state


def load_phase_state(project_root: Optional[Path] = None) -> Optional[PhaseState]:
    """
    Convenience function to load phase state

    Args:
        project_root: Project root directory (defaults to cwd)

    Returns:
        PhaseState if exists, None otherwise
    """
    manager = PhaseManager(project_root)
    return manager.load_state()


def save_phase_state(state: PhaseState, project_root: Optional[Path] = None) -> bool:
    """
    Convenience function to save phase state

    Args:
        state: PhaseState to save
        project_root: Project root directory (defaults to cwd)

    Returns:
        True if successful
    """
    manager = PhaseManager(project_root)
    return manager.save_state(state)
