#!/bin/bash
echo "Iniciando Backend TemVagaAi..."
echo ""
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
