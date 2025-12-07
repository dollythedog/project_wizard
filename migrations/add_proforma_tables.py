"""
Migration script to add Pro Forma tables to database.

Run this to create the proformas, service_lines, billing_codes, and proforma_snapshots tables.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlmodel import SQLModel, create_engine
from app.models.database import Project, ProjectNote, SupportingFile, DocumentRun, MemoryEntry
from app.models.proforma import ProForma, ServiceLine, BillingCode, ProFormaSnapshot
from app.services.database import get_engine
from app.services.database import engine


def run_migration():
    """Create all Pro Forma tables."""
    print("Creating Pro Forma tables...")
    
    engine = get_engine()
    
    # Create tables (SQLModel automatically creates only missing tables)
    SQLModel.metadata.create_all(engine)
    
    print("✓ Pro Forma tables created successfully!")
    print("\nTables created:")
    print("  - proformas")
    print("  - service_lines")
    print("  - billing_codes")
    print("  - proforma_snapshots")


if __name__ == "__main__":
    run_migration()
