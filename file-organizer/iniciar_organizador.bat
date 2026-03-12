@echo off
echo ========================================
echo  Organizador Automatico de Archivos
echo ========================================
echo.
echo Iniciando el organizador automatico...
echo Presiona Ctrl+C para detener el servicio.
echo.

cd /d "%~dp0"
python organizar_auto.py

pause

