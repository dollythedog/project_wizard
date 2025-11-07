#!/bin/bash
# Launch AI Project Wizard Web App on LAN

echo "🧙‍♂️ Starting AI Project Wizard Web Interface..."
echo ""
echo "Access at: http://10.69.1.86:8501"
echo ""

cd "$(dirname "$0")"
./venv/bin/streamlit run app_streamlit.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true
