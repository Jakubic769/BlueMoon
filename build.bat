@echo off
title BLUE MOON - Build System
color 0B

echo.
echo  ╔════════════════════════════════════════════════╗
echo  ║       🌙 BLUE MOON SNIPER v1.0 🌙             ║
echo  ║               Build System                     ║
echo  ╚════════════════════════════════════════════════╝
echo.

echo  [1/3] Cleaning old builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"

echo  [2/3] Installing dependencies...
pip install requests urllib3 pyinstaller --quiet --disable-pip-version-check

echo  [3/3] Compiling to EXE...
echo.
pyinstaller --onefile --console --name "BLUE_MOON_Sniper" blue_moon_sniper.py

echo.
echo  ╔════════════════════════════════════════════════╗
echo  ║  ✅ BUILD READY TO USE!                            ║
echo  ║  📂 EXE Location: dist\BLUE_MOON_Sniper.exe   ║
echo  ╚════════════════════════════════════════════════╝
echo.
pause
