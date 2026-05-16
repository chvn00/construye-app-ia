@echo off
title Construye tu App con IA - USTA
echo ============================================
echo  Construye tu App con IA - USTA
echo  Facultad de Ingenieria de Telecomunicaciones
echo ============================================
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado.
    pause
    exit /b
)

:: Instalar dependencias si es necesario
echo Instalando dependencias...
pip install -r requirements.txt -q

:: Verificar Ollama
echo.
echo Verificando Ollama...
ollama list >nul 2>&1
if errorlevel 1 (
    echo ADVERTENCIA: Ollama no detectado. Instala Ollama en https://ollama.com
) else (
    echo Ollama OK
    echo Descargando modelo llama3.2:3b si no existe...
    ollama pull llama3.2:3b
)

echo.
echo Iniciando servidor en http://localhost:8000
echo Abre el navegador en: http://localhost:8000
echo Admin en: http://localhost:8000/admin  (clave: usta2025)
echo.
echo Presiona Ctrl+C para detener el servidor.
echo.

cd /d "%~dp0"
python -m uvicorn main:app --host 0.0.0.0 --port 8000

pause
