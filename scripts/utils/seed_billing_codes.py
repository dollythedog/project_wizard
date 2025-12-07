"""
Seed the billing codes database with default E/M codes and procedures.

Run this once to populate the BillingCode table with standard rates.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlmodel import Session, select
from app.services.database import get_engine
from app.models.proforma import BillingCode

def seed_billing_codes():
    """Populate BillingCode table with default codes."""
    print("=" * 60)
    print("Seeding Billing Codes")
    print("=" * 60)
    print()
    
    engine = get_engine()
    
    # E/M Codes (Inpatient)
    em_codes = [
        ("99291", "em", "Critical Care", 150.0, "Critical Care"),
        ("99223", "em", "Initial, High (inpatient)", 121.0, "Inpatient E/M"),
        ("99222", "em", "Initial, Moderate (inpatient)", 86.0, "Inpatient E/M"),
        ("99233", "em", "Subsequent, High (inpatient)", 81.0, "Inpatient E/M"),
        ("99232", "em", "Subsequent, Moderate (inpatient)", 54.0, "Inpatient E/M"),
        ("99215", "em", "Established, High (outpatient)", 75.0, "Outpatient E/M"),
        ("99214", "em", "Established, Mod-High (outpatient)", 52.0, "Outpatient E/M"),
        ("99213", "em", "Established, Moderate (outpatient)", 40.0, "Outpatient E/M"),
    ]
    
    # Procedure Codes
    procedure_codes = [
        ("31550", "procedure", "Intubation", 94.0, "Pulmonary"),
        ("36556", "procedure", "Central Line Insertion", 58.0, "Procedures"),
    ]
    
    all_codes = em_codes + procedure_codes
    
    with Session(engine) as session:
        # Check which codes already exist
        existing_codes = session.exec(select(BillingCode.code)).all()
        existing_set = set(existing_codes)
        
        added = 0
        skipped = 0
        
        for code, code_type, description, rate, category in all_codes:
            if code in existing_set:
                print(f"⏭️  Skipping {code} - already exists")
                skipped += 1
                continue
            
            billing_code = BillingCode(
                code=code,
                code_type=code_type,
                description=description,
                rate=rate,
                category=category
            )
            session.add(billing_code)
            print(f"✓ Added {code}: {description} (${rate})")
            added += 1
        
        session.commit()
        
        print()
        print(f"✅ Seeding complete!")
        print(f"   Added: {added}")
        print(f"   Skipped: {skipped}")
        print()
        print("Billing codes are now available for Pro Forma revenue calculations.")

if __name__ == "__main__":
    seed_billing_codes()
