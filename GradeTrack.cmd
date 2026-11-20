@echo off
"%~dp0.venv\Scripts\python.exe" -B "%~dp0src\gradetrack\main.py"
if errorlevel 1 pause
