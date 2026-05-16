#!/bin/bash
echo "============================================"
echo " Construye tu App con IA - USTA"
echo " Facultad de Ingenieria de Telecomunicaciones"
echo "============================================"
echo ""

cd "$(dirname "$0")"

echo "Instalando dependencias..."
pip3 install -r requirements.txt -q

echo "Verificando Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "ADVERTENCIA: Ollama no detectado."
else
    echo "Ollama OK"
    ollama pull llama3.2:3b
fi

echo ""
echo "Iniciando servidor en http://localhost:8000"
echo "Admin: http://localhost:8000/admin  (clave: usta2025)"
echo ""

python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
