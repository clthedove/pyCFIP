@echo off
del /q pycfip
set RELEASE_FOLDER=release
set ARCH_NAME=%PROCESSOR_ARCHITECTURE%
for %%i in (a b c d e f g h i j k l m n o p q r s t u v w x y z) do call set ARCH_NAME=%%ARCH_NAME:%%i=%%i%%
set BIN_NAME=%RELEASE_FOLDER%\pycfip-windowsnt-%ARCH_NAME%.exe
rd /s /q %RELEASE_FOLDER%
pyinstaller -F main.py
mkdir %RELEASE_FOLDER%
move dist\main.exe %BIN_NAME%
rd /s /q build dist
del /q *.spec
echo ===== Build Finished =====
mklink pycfip %BIN_NAME%
pause
