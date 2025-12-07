"""
Setup script for Pro Forma system.

Run this once to create the necessary database tables.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from migrations.add_proforma_tables import run_migration

if __name__ == "__main__":
    print("=" * 60)
    print("Pro Forma System Setup")
    print("=" * 60)
    print()
    
    try:
        run_migration()
        print()
        print("✅ Setup complete!")
        print()
        print("Next steps:")
        print("1. Start the server: python run_web.py")
        print("2. Navigate to your HFW project")
        print("3. Click 'Create Pro Forma'")
        print("4. Add service lines and calculate!")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
