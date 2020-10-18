@echo off
del /q pycfip.exe
pyinstaller -F main.py
move dist\main.exe pycfip.exe
rd /s /q build dist
del /q *.spec
echo ===== Build Finished =====
