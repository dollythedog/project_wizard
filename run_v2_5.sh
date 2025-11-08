#!/bin/bash
# Project Wizard v2.5 Launcher

echo "Starting Project Wizard v2.5 (Integrated)..."
echo "Access at: http://localhost:8504"
echo ""

if [ -d "venv" ]; then
    source venv/bin/activate
fi

streamlit run app_v2_5.py --server.port 8504 --server.address 0.0.0.0
