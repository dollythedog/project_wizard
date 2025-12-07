"""
Reset Pro Forma tables (drop and recreate with new schema).

WARNING: This will delete any existing Pro Forma data!
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlmodel import SQLModel
from app.services.database import get_engine
from app.models.database import Project  # Need this for foreign key
from app.models.proforma import ProForma, ServiceLine, BillingCode, ProFormaSnapshot

def reset_proforma_tables():
    """Drop and recreate Pro Forma tables."""
    print("=" * 60)
    print("Resetting Pro Forma Tables")
    print("=" * 60)
    print()
    print("⚠️  WARNING: This will delete all existing Pro Forma data!")
    print()
    
    engine = get_engine()
    
    # Drop tables
    print("Dropping old tables...")
    ProFormaSnapshot.__table__.drop(engine, checkfirst=True)
    ServiceLine.__table__.drop(engine, checkfirst=True)
    BillingCode.__table__.drop(engine, checkfirst=True)
    ProForma.__table__.drop(engine, checkfirst=True)
    print("✓ Old tables dropped")
    
    # Recreate tables with new schema (use metadata to handle dependencies)
    print("\nCreating new tables with updated schema...")
    SQLModel.metadata.create_all(engine)
    print("✓ New tables created")
    
    print()
    print("✅ Reset complete!")
    print()
    print("Next steps:")
    print("1. Start the server: python run_web.py")
    print("2. Navigate to your HFW project")
    print("3. Click 'Create Pro Forma'")

if __name__ == "__main__":
    reset_proforma_tables()
