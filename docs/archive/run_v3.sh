#!/bin/bash
# Project Wizard v3.0 Launcher

echo "Starting Project Wizard v3.0..."
echo "Access at: http://localhost:8503"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run Streamlit
streamlit run app_v3.py --server.port 8503 --server.address 0.0.0.0
