"""
Phase State Model - RPG-Style Project Progression Tracker

Tracks project progression through the 4-phase journey:
1. Initiation (Call to Adventure) - 📜 Scroll/Quill
2. Planning (Strategist's Forge) - ⚙️ Gear/Blueprint
3. Execution (Campaign of Execution) - ⚔️ Sword/Hammer
4. Closure (Chronicle of Wisdom) - 📚 Tome/Trophy
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ProjectPhase(str, Enum):
    """The four phases of the project lifecycle"""
    INITIATION = "initiation"
    PLANNING = "planning"
    EXECUTION = "execution"
    CLOSURE = "closure"


class GateStatus(str, Enum):
    """Status of phase gate approvals"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NOT_REACHED = "not_reached"


class PhaseGate(str, Enum):
    """Phase gate checkpoints"""
    RFP = "rfp"  # Ready for Planning
    RFE = "rfe"  # Ready for Execution
    RFC = "rfc"  # Ready for Closure
    COMPLETE = "complete"  # Project Complete


class PhaseMetadata(BaseModel):
    """Metadata for a single phase"""
    phase: ProjectPhase
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    artifacts: List[str] = Field(default_factory=list)
    notes: str = ""

    # RPG flavor
    chapter_title: str
    icon_emoji: str
    icon_path: Optional[str] = None
    quest_description: str


class PhaseState(BaseModel):
    """
    Complete state of project's phase progression

    This is the "game state" that tracks where you are in the project journey.
    """
    # Current position
    current_phase: ProjectPhase = ProjectPhase.INITIATION

    # Gate approvals
    rfp_status: GateStatus = GateStatus.NOT_REACHED
    rfp_approved_at: Optional[datetime] = None
    rfe_status: GateStatus = GateStatus.NOT_REACHED
    rfe_approved_at: Optional[datetime] = None
    rfc_status: GateStatus = GateStatus.NOT_REACHED
    rfc_approved_at: Optional[datetime] = None
    project_complete: bool = False
    completed_at: Optional[datetime] = None

    # Phase tracking
    initiation: PhaseMetadata = Field(default_factory=lambda: PhaseMetadata(
        phase=ProjectPhase.INITIATION,
        chapter_title="The Call to Adventure",
        icon_emoji="📜",
        icon_path="docs/images/icon-phase1-quill.png",
        quest_description="Draft your Project Charter — define the quest and win the council's approval"
    ))

    planning: PhaseMetadata = Field(default_factory=lambda: PhaseMetadata(
        phase=ProjectPhase.PLANNING,
        chapter_title="The Strategist's Forge",
        icon_emoji="⚙️",
        icon_path="docs/images/icon-phase2-gear.png",
        quest_description="Forge your project's blueprint — set your scope, assign heroes, and plan the path"
    ))

    execution: PhaseMetadata = Field(default_factory=lambda: PhaseMetadata(
        phase=ProjectPhase.EXECUTION,
        chapter_title="The Campaign of Execution",
        icon_emoji="⚔️",
        icon_path="docs/images/icon-phase3-sword.png",
        quest_description="Embark on your campaign — complete milestones, slay risks, and gather loot"
    ))

    closure: PhaseMetadata = Field(default_factory=lambda: PhaseMetadata(
        phase=ProjectPhase.CLOSURE,
        chapter_title="The Chronicle of Wisdom",
        icon_emoji="📚",
        icon_path="docs/images/icon-phase4-book.png",
        quest_description="Record your saga — lessons learned and victories immortalized"
    ))

    # Project metadata
    project_title: str = ""
    project_created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)

    def get_phase_metadata(self, phase: ProjectPhase) -> PhaseMetadata:
        """Get metadata for a specific phase"""
        return getattr(self, phase.value)

    def advance_to_phase(self, phase: ProjectPhase):
        """Advance to a new phase"""
        old_phase = self.current_phase
        self.current_phase = phase

        # Mark old phase as complete
        old_meta = self.get_phase_metadata(old_phase)
        if not old_meta.completed_at:
            old_meta.completed_at = datetime.now()

        # Mark new phase as started
        new_meta = self.get_phase_metadata(phase)
        if not new_meta.started_at:
            new_meta.started_at = datetime.now()

        self.last_updated = datetime.now()

    def approve_gate(self, gate: PhaseGate):
        """Approve a phase gate"""
        now = datetime.now()

        if gate == PhaseGate.RFP:
            self.rfp_status = GateStatus.APPROVED
            self.rfp_approved_at = now
            # Automatically advance to planning
            self.advance_to_phase(ProjectPhase.PLANNING)
        elif gate == PhaseGate.RFE:
            self.rfe_status = GateStatus.APPROVED
            self.rfe_approved_at = now
            self.advance_to_phase(ProjectPhase.EXECUTION)
        elif gate == PhaseGate.RFC:
            self.rfc_status = GateStatus.APPROVED
            self.rfc_approved_at = now
            self.advance_to_phase(ProjectPhase.CLOSURE)
        elif gate == PhaseGate.COMPLETE:
            self.project_complete = True
            self.completed_at = now
            closure_meta = self.get_phase_metadata(ProjectPhase.CLOSURE)
            closure_meta.completed_at = now

        self.last_updated = now

    def get_next_gate(self) -> Optional[PhaseGate]:
        """Get the next gate that needs approval"""
        if self.current_phase == ProjectPhase.INITIATION:
            return PhaseGate.RFP if self.rfp_status != GateStatus.APPROVED else None
        elif self.current_phase == ProjectPhase.PLANNING:
            return PhaseGate.RFE if self.rfe_status != GateStatus.APPROVED else None
        elif self.current_phase == ProjectPhase.EXECUTION:
            return PhaseGate.RFC if self.rfc_status != GateStatus.APPROVED else None
        elif self.current_phase == ProjectPhase.CLOSURE and not self.project_complete:
            return PhaseGate.COMPLETE
        return None

    def get_progress_percentage(self) -> int:
        """Calculate overall project progress (0-100)"""
        phase_weights = {
            ProjectPhase.INITIATION: 25,
            ProjectPhase.PLANNING: 25,
            ProjectPhase.EXECUTION: 40,
            ProjectPhase.CLOSURE: 10
        }

        progress = 0
        for phase, weight in phase_weights.items():
            meta = self.get_phase_metadata(phase)
            if meta.completed_at:
                progress += weight
            elif meta.started_at:
                # Partial credit for current phase
                progress += weight // 2

        return min(progress, 100)
