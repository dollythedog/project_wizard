"""
Pro Forma data models for contract financial planning.

Models support both external (expense-only) and internal (full P&L) Pro Formas.
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
import json


class ProForma(SQLModel, table=True):
    """
    Pro Forma financial document for a contract proposal.
    
    Container for service line staffing requirements and financial projections.
    Supports two versions: External (hospital-facing) and Internal (full P&L).
    """
    __tablename__ = "proformas"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id", index=True)
    title: str = Field(max_length=255)  # e.g., "HFW Renegotiation Pro Forma"
    description: Optional[str] = None
    
    # Version tracking
    version: str = Field(default="1.0", max_length=50)
    status: str = Field(default="draft", max_length=50)  # draft, approved, superseded
    
    # Global hourly rates (for billing calculations)
    default_physician_hourly_rate: float = Field(default=175.0)
    default_app_hourly_rate: float = Field(default=90.0)
    
    # Global FTE calculation parameters
    default_shifts_per_physician_per_month: int = Field(default=20)
    default_shifts_per_app_per_month: int = Field(default=22)
    
    # Internal P&L data (optional - only for internal version)
    # Direct costs per FTE
    physician_salary: Optional[float] = Field(default=415000.0)
    physician_benefits_taxes: Optional[float] = Field(default=44631.0)
    physician_malpractice: Optional[float] = Field(default=30000.0)
    
    app_salary: Optional[float] = Field(default=138000.0)
    app_benefits_taxes: Optional[float] = Field(default=20000.0)
    app_malpractice: Optional[float] = Field(default=7200.0)
    
    # Indirect cost percentages (as decimal, e.g., 0.10 = 10%)
    admin_overhead_pct: Optional[float] = Field(default=0.10)
    financial_oversight_pct: Optional[float] = Field(default=0.025)
    office_materials_pct: Optional[float] = Field(default=0.025)
    credentialing_pct: Optional[float] = Field(default=0.015)
    rcm_pct: Optional[float] = Field(default=0.01)
    
    # Calculated totals (stored for quick access)
    total_annual_cost: Optional[float] = None  # Total we bill the hospital
    total_physician_fte: Optional[float] = None
    total_app_fte: Optional[float] = None
    
    # Internal calculations (null for external-only Pro Formas)
    total_projected_revenue: Optional[float] = None
    total_direct_expenses: Optional[float] = None
    total_indirect_expenses: Optional[float] = None
    net_income: Optional[float] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    service_lines: List["ServiceLine"] = Relationship(back_populates="proforma", cascade_delete=True)


class ServiceLine(SQLModel, table=True):
    """
    Individual service line within a Pro Forma (e.g., MICU, CVICU, Code Blue).
    
    Defines staffing requirements, schedules, and optional revenue projections.
    """
    __tablename__ = "service_lines"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    proforma_id: int = Field(foreign_key="proformas.id", index=True)
    
    # Service line identity
    name: str = Field(max_length=100)  # e.g., "CVICU Daytime Coverage"
    description: Optional[str] = None
    order: int = Field(default=0)  # For display ordering
    
    # Staffing requirements
    physician_hours_per_shift: float = Field(default=12.0)  # For physician cost calculation
    app_hours_per_shift: float = Field(default=12.0)  # For APP cost calculation
    physicians_per_day: int = Field(default=0)
    apps_per_day: int = Field(default=0)
    days_per_week: int = Field(default=7)
    
    # Hourly rate overrides (if different from ProForma defaults)
    physician_hourly_rate_override: Optional[float] = None
    app_hourly_rate_override: Optional[float] = None
    
    # Calculated staffing metrics
    annual_physician_shifts: Optional[float] = None
    annual_app_shifts: Optional[float] = None
    physician_fte: Optional[float] = None
    app_fte: Optional[float] = None
    
    # Calculated costs
    annual_physician_cost: Optional[float] = None
    annual_app_cost: Optional[float] = None
    total_annual_cost: Optional[float] = None
    
    # Internal revenue projections (optional)
    avg_daily_census: Optional[float] = None
    weeks_per_year: Optional[int] = Field(default=52)
    
    # E/M billing (stored as JSON for flexibility)
    # Format: {"99233": 0.50, "99291": 0.50} (percentages must sum to 1.0)
    em_billing_profile: Optional[str] = None  # JSON string
    
    # Procedure billing (stored as JSON)
    # Format: {"31500": {"mix": 0.50, "rate": 150.0}, "32550": {"mix": 0.50, "rate": 300.0}}
    procedure_billing_profile: Optional[str] = None  # JSON string
    avg_daily_procedures: Optional[float] = None
    
    # Calculated revenue (internal only)
    annual_em_encounters: Optional[float] = None
    annual_procedure_count: Optional[float] = None
    projected_revenue: Optional[float] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    proforma: Optional["ProForma"] = Relationship(back_populates="service_lines")


class BillingCode(SQLModel, table=True):
    """
    Master list of billing codes and rates for reuse across Pro Formas.
    
    Includes both E/M codes (evaluation/management) and procedure codes (CPT).
    """
    __tablename__ = "billing_codes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(max_length=10, unique=True, index=True)  # e.g., "99233", "31500"
    code_type: str = Field(max_length=50)  # "em" or "procedure"
    description: str = Field(max_length=500)
    rate: float  # Billing rate in dollars
    
    # Metadata
    category: Optional[str] = Field(max_length=100)  # e.g., "Critical Care", "Pulmonary"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ProFormaSnapshot(SQLModel, table=True):
    """
    Archived snapshot of a Pro Forma at a point in time.
    
    Used to track changes and maintain historical versions for proposals.
    """
    __tablename__ = "proforma_snapshots"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    proforma_id: int = Field(foreign_key="proformas.id", index=True)
    version: str = Field(max_length=50)
    snapshot_date: datetime = Field(default_factory=datetime.utcnow)
    
    # Snapshot data (stored as JSON)
    data: str  # JSON dump of ProForma + ServiceLines at this point in time
    notes: Optional[str] = None  # What changed in this version
    
    created_by: Optional[str] = Field(max_length=100)  # User who created snapshot
