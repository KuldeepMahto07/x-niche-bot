@echo off
cd /d "%~dp0"
python -m pip install -q -r requirements-studio.txt
start "" http://127.0.0.1:5050
python studio.py
