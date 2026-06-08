# Construye tu App con IA 🧠⚡

Reto interactivo para el stand de **Ingeniería de Telecomunicaciones - USTA Bucaramanga**. Los participantes diseñan una app tecnológica eligiendo módulos de sensores, procesamiento y acción, y reciben una evaluación con puntaje generada por Inteligencia Artificial.

🌐 **Demo en vivo:** [construye-app-ia-production.up.railway.app](https://construye-app-ia-production.up.railway.app)

---

## ¿Cómo funciona?

1. El participante ingresa el nombre de su equipo y su app
2. Gira la ruleta para descubrir la categoría (Industria, Salud, Agricultura, Financiera, Sustentabilidad)
3. Selecciona 6 módulos tecnológicos: 2 de **Sensores**, 2 de **Piensa** y 2 de **Actúa**
4. Describe con sus propias palabras qué hace la app
5. La IA evalúa la propuesta y entrega un **puntaje del 40 al 100** con fortalezas y sugerencias
6. El resultado aparece en el **ranking general** en tiempo real

---

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| Backend | FastAPI + Python |
| Frontend | HTML + CSS + JavaScript (SPA) |
| IA | Groq API (llama3-8b-8192) |
| Despliegue | Railway |
| Offline (Dell) | Ollama (local) |

---

## Estructura del proyecto

```
construye-app-ia/
├── main.py                  # Backend FastAPI
├── templates/
│   ├── index.html           # App principal (SPA)
│   └── admin.html           # Panel de administración
├── static/
│   ├── escudo5.png          # Escudo USTA
│   ├── Recurso 3santoto.png # Logo Santo Tomás
│   ├── cerebro1.png         # Imagen cerebro
│   ├── icon-192.png         # Ícono PWA
│   ├── icon-512.png         # Ícono PWA grande
│   ├── manifest.json        # Manifiesto PWA
│   └── sw.js               # Service Worker
├── images/                  # Imágenes por categoría
│   ├── industria/
│   ├── salud/
│   ├── agricultura/
│   ├── financiera/
│   └── sustentabilidad/
├── data/
│   └── ranking.json         # Ranking persistente
├── railway.toml             # Configuración Railway
├── requirements.txt
├── start.bat                # Arranque Windows (Dell offline)
└── start.sh                 # Arranque Linux/Mac (Dell offline)
```

---

## Instalación local

```bash
# Clonar el repositorio
git clone https://github.com/chvn00/construye-app-ia.git
cd construye-app-ia

# Instalar dependencias
pip install -r requirements.txt

# Configurar variable de entorno (versión online)
export GROQ_API_KEY=tu_api_key

# Correr la app
uvicorn main:app --host 0.0.0.0 --port 8000
```

Abrir en el navegador: `http://localhost:8000`

---

## Versión offline (Dell)

Para correr sin internet usando **Ollama**:

1. Instalar [Ollama](https://ollama.com) y descargar un modelo (`ollama pull llama3`)
2. Reemplazar en `main.py` la llamada a Groq por la API local de Ollama (`http://localhost:11434`)
3. Ejecutar `start.bat` (Windows) o `start.sh` (Linux/Mac)

---

## Panel de administración

Disponible en `/admin` con contraseña `usta2025`. Permite:
- Ver todas las propuestas enviadas
- Eliminar entradas individuales
- Resetear el ranking completo

---

## PWA

La app es instalable como PWA en cualquier dispositivo:
- **Android (Chrome):** aparece banner automático de instalación
- **iPhone (Safari):** Compartir → Añadir a pantalla de inicio

---

## Easter eggs 🥚

- Equipo `CHVN` → puntaje perfecto 100 🏆
- Equipo `valeriacarioca` → puntaje especial 101 💖

---

## Créditos

Desarrollado para **Facultad de Ingeniería de Telecomunicaciones**  
Universidad Santo Tomás - Bucaramanga  
2025
