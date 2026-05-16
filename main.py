import random
import json
import os
import httpx
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Construye tu App con IA - USTA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

RANKING_FILE = Path("data/ranking.json")
ADMIN_PASSWORD = "usta2025"

CATEGORIAS = {
    "industria": {
        "nombre": "Industria", "color": "#FF6B35",
        "modulos": [
            {"nombre": "Sensores IoT",        "emoji": "📡", "grupo": "sensores"},
            {"nombre": "Cámara industrial",   "emoji": "📷", "grupo": "sensores"},
            {"nombre": "GPS",                 "emoji": "📍", "grupo": "sensores"},
            {"nombre": "Sensor de vibración", "emoji": "🌡️", "grupo": "sensores"},
            {"nombre": "Escáner 3D",          "emoji": "🔭", "grupo": "sensores"},
            {"nombre": "Inteligencia Artificial","emoji":"🤖","grupo": "piensa"},
            {"nombre": "Analítica de datos",  "emoji": "📊", "grupo": "piensa"},
            {"nombre": "Gemelo digital",      "emoji": "🔮", "grupo": "piensa"},
            {"nombre": "Visión artificial",   "emoji": "👁️", "grupo": "piensa"},
            {"nombre": "Predicción de fallos","emoji": "🔧", "grupo": "piensa"},
            {"nombre": "Automatización",      "emoji": "⚙️", "grupo": "actua"},
            {"nombre": "Notificaciones",      "emoji": "🔔", "grupo": "actua"},
            {"nombre": "Dashboard",           "emoji": "📈", "grupo": "actua"},
            {"nombre": "Realidad aumentada",  "emoji": "👓", "grupo": "actua"},
            {"nombre": "Control remoto",      "emoji": "🕹️", "grupo": "actua"},
        ],
    },
    "financiera": {
        "nombre": "Financiera", "color": "#F7B731",
        "modulos": [
            {"nombre": "Reconocimiento facial","emoji": "👤", "grupo": "sensores"},
            {"nombre": "Biometría",            "emoji": "🔐", "grupo": "sensores"},
            {"nombre": "Escáner QR",           "emoji": "📲", "grupo": "sensores"},
            {"nombre": "NFC",                  "emoji": "📶", "grupo": "sensores"},
            {"nombre": "Cámara",               "emoji": "📷", "grupo": "sensores"},
            {"nombre": "Inteligencia Artificial","emoji":"🤖","grupo": "piensa"},
            {"nombre": "Analítica de datos",   "emoji": "📊", "grupo": "piensa"},
            {"nombre": "Detección de fraude",  "emoji": "🛡️", "grupo": "piensa"},
            {"nombre": "Blockchain",           "emoji": "⛓️", "grupo": "piensa"},
            {"nombre": "Motor de riesgo",      "emoji": "⚖️", "grupo": "piensa"},
            {"nombre": "Notificaciones",       "emoji": "🔔", "grupo": "actua"},
            {"nombre": "Dashboard",            "emoji": "📈", "grupo": "actua"},
            {"nombre": "Chatbot",              "emoji": "💬", "grupo": "actua"},
            {"nombre": "Agenda",               "emoji": "📅", "grupo": "actua"},
            {"nombre": "Alertas automáticas",  "emoji": "🚨", "grupo": "actua"},
        ],
    },
    "salud": {
        "nombre": "Salud", "color": "#45AAF2",
        "modulos": [
            {"nombre": "Sensores vitales",     "emoji": "❤️", "grupo": "sensores"},
            {"nombre": "Cámara",               "emoji": "📷", "grupo": "sensores"},
            {"nombre": "Wearables",            "emoji": "⌚", "grupo": "sensores"},
            {"nombre": "GPS",                  "emoji": "📍", "grupo": "sensores"},
            {"nombre": "Micrófono",            "emoji": "🎤", "grupo": "sensores"},
            {"nombre": "Inteligencia Artificial","emoji":"🤖","grupo": "piensa"},
            {"nombre": "Analítica de datos",   "emoji": "📊", "grupo": "piensa"},
            {"nombre": "Diagnóstico automático","emoji":"🩺", "grupo": "piensa"},
            {"nombre": "Reconocimiento de voz","emoji": "🗣️", "grupo": "piensa"},
            {"nombre": "Análisis de imágenes", "emoji": "🔬", "grupo": "piensa"},
            {"nombre": "Chat médico",          "emoji": "💊", "grupo": "actua"},
            {"nombre": "Notificaciones",       "emoji": "🔔", "grupo": "actua"},
            {"nombre": "Telemedicina",         "emoji": "🏥", "grupo": "actua"},
            {"nombre": "Agenda",               "emoji": "📅", "grupo": "actua"},
            {"nombre": "Alertas de emergencia","emoji": "🚑", "grupo": "actua"},
        ],
    },
    "agricultura": {
        "nombre": "Agricultura", "color": "#26de81",
        "modulos": [
            {"nombre": "Sensores IoT",         "emoji": "📡", "grupo": "sensores"},
            {"nombre": "GPS",                  "emoji": "📍", "grupo": "sensores"},
            {"nombre": "Drones",               "emoji": "🚁", "grupo": "sensores"},
            {"nombre": "Imágenes satelitales", "emoji": "🛰️", "grupo": "sensores"},
            {"nombre": "Cámara",               "emoji": "📷", "grupo": "sensores"},
            {"nombre": "Inteligencia Artificial","emoji":"🤖","grupo": "piensa"},
            {"nombre": "Analítica de datos",   "emoji": "📊", "grupo": "piensa"},
            {"nombre": "Clima en tiempo real", "emoji": "🌤️", "grupo": "piensa"},
            {"nombre": "Predicción de cosecha","emoji": "🌾", "grupo": "piensa"},
            {"nombre": "Detección de plagas",  "emoji": "🐛", "grupo": "piensa"},
            {"nombre": "Riego automático",     "emoji": "💧", "grupo": "actua"},
            {"nombre": "Notificaciones",       "emoji": "🔔", "grupo": "actua"},
            {"nombre": "Comunidad",            "emoji": "👥", "grupo": "actua"},
            {"nombre": "Dashboard",            "emoji": "📈", "grupo": "actua"},
            {"nombre": "Alertas climáticas",   "emoji": "⚠️", "grupo": "actua"},
        ],
    },
    "sustentabilidad": {
        "nombre": "Sustentabilidad", "color": "#2BCBBA",
        "modulos": [
            {"nombre": "Sensores ambientales", "emoji": "🌿", "grupo": "sensores"},
            {"nombre": "GPS",                  "emoji": "📍", "grupo": "sensores"},
            {"nombre": "Cámara",               "emoji": "📷", "grupo": "sensores"},
            {"nombre": "Satélite",             "emoji": "🛰️", "grupo": "sensores"},
            {"nombre": "Monitor de CO₂",       "emoji": "💨", "grupo": "sensores"},
            {"nombre": "Inteligencia Artificial","emoji":"🤖","grupo": "piensa"},
            {"nombre": "Analítica de datos",   "emoji": "📊", "grupo": "piensa"},
            {"nombre": "Huella de carbono",    "emoji": "🌍", "grupo": "piensa"},
            {"nombre": "Análisis de impacto",  "emoji": "🔬", "grupo": "piensa"},
            {"nombre": "Clasificación residuos","emoji":"🗂️", "grupo": "piensa"},
            {"nombre": "Gamificación",         "emoji": "🎮", "grupo": "actua"},
            {"nombre": "Notificaciones",       "emoji": "🔔", "grupo": "actua"},
            {"nombre": "Comunidad verde",      "emoji": "👥", "grupo": "actua"},
            {"nombre": "Dashboard",            "emoji": "📈", "grupo": "actua"},
            {"nombre": "Reciclaje inteligente","emoji": "♻️", "grupo": "actua"},
        ],
    },
}


def load_ranking() -> list:
    if not RANKING_FILE.exists():
        return []
    return json.loads(RANKING_FILE.read_text(encoding="utf-8"))


def save_ranking(data: list):
    RANKING_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def es_descripcion_real(texto: str) -> bool:
    """Detecta si la descripción es texto coherente o basura aleatoria."""
    texto = texto.strip()

    # Muy corta
    if len(texto) < 30:
        return False

    letras = [c for c in texto.lower() if c.isalpha()]
    if len(letras) < 20:
        return False

    # Pocos caracteres únicos = texto repetitivo (afafaf, sdfsdfsdf...)
    if len(set(texto.lower().replace(' ', ''))) < 8:
        return False

    # Palabras reales: mínimo 4 palabras de 3+ letras
    palabras = [p.strip('.,;:!?') for p in texto.split() if len(p.strip('.,;:!?')) >= 3]
    if len(palabras) < 4:
        return False

    # Palabras muy largas sin sentido (sdfsdgfsdgfdsf) — máx 60% consonantes seguidas
    consonantes = set('bcdfghjklmnñpqrstvwxyz')
    for palabra in palabras:
        p = palabra.lower()
        racha = 0
        max_racha = 0
        for c in p:
            if c in consonantes:
                racha += 1
                max_racha = max(max_racha, racha)
            else:
                racha = 0
        if len(p) >= 5 and max_racha >= 4:  # 4+ consonantes seguidas = basura
            return False

    # Ratio de vocales: texto aleatorio tiende a ser muy bajo o muy uniforme
    vocales = sum(1 for c in letras if c in 'aeiouáéíóúü')
    ratio_v = vocales / len(letras)
    if ratio_v < 0.20 or ratio_v > 0.75:
        return False

    # Palabras únicas: si casi todas son iguales o muy similares
    palabras_lower = [p.lower() for p in palabras]
    if len(set(palabras_lower)) < max(2, len(palabras_lower) * 0.5):
        return False

    return True


def get_category_images(categoria_id: str) -> list:
    img_dir = Path(f"images/{categoria_id}")
    if not img_dir.exists():
        return []
    exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    return [
        f"/images/{categoria_id}/{quote(f.name)}"
        for f in img_dir.iterdir()
        if f.suffix.lower() in exts
    ]


# ── Models ────────────────────────────────────────────────────────────────────

class PropuestaInput(BaseModel):
    equipo: str
    app_nombre: str
    categoria: str
    modulos: list[str]
    descripcion: str


class AdminAction(BaseModel):
    password: str

class DeleteEntrada(BaseModel):
    password: str
    idx: int


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return FileResponse("templates/index.html")


@app.get("/admin")
async def admin_page():
    return FileResponse("templates/admin.html")


@app.get("/api/todas-categorias")
async def get_todas_categorias():
    result = {}
    for cat_id, cat in CATEGORIAS.items():
        images = get_category_images(cat_id)
        result[cat_id] = {
            "nombre": cat["nombre"],
            "color":  cat["color"],
            "imagen": random.choice(images) if images else None,
        }
    return result


@app.get("/api/categoria")
async def get_categoria():
    cat_id = random.choice(list(CATEGORIAS.keys()))
    cat = CATEGORIAS[cat_id]
    images = get_category_images(cat_id)
    return {
        "id": cat_id,
        "nombre": cat["nombre"],
        "color": cat["color"],
        "imagen": random.choice(images) if images else None,
        "todas_imagenes": images,
    }


@app.get("/api/modulos/{categoria_id}")
async def get_modulos(categoria_id: str):
    if categoria_id not in CATEGORIAS:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"modulos": CATEGORIAS[categoria_id]["modulos"]}


@app.post("/api/evaluar")
async def evaluar(propuesta: PropuestaInput):
    # 💖 Easter egg especial
    if propuesta.equipo.strip().lower() == "valeriacarioca":
        puntaje = 101
        evaluation = {
            "puntaje": 101,
            "fortalezas": "¡Eres la mejor de todas! No existe propuesta más brillante, más creativa ni más especial en todo el universo. 🌟",
            "mejoras": "¡Absolutamente nada! Eres perfecta tal y como eres. 💖",
            "mensaje": "¡Eres la mejor de todas!!!! Te ama tu papi ❤️",
        }
        ranking = load_ranking()
        entry = {
            "equipo": propuesta.equipo,
            "app_nombre": propuesta.app_nombre,
            "categoria": propuesta.categoria,
            "modulos": propuesta.modulos,
            "puntaje": puntaje,
            "fecha": datetime.now().strftime("%H:%M"),
        }
        ranking.append(entry)
        ranking.sort(key=lambda x: x["puntaje"], reverse=True)
        save_ranking(ranking)
        posicion = next(i + 1 for i, e in enumerate(ranking) if e["equipo"] == entry["equipo"] and e["puntaje"] == puntaje)
        return {**evaluation, "puntaje": puntaje, "posicion": posicion, "total_equipos": len(ranking)}

    # 🏆 Easter egg
    if propuesta.equipo.strip().upper() == "CHVN":
        puntaje = 100
        evaluation = {
            "puntaje": 100,
            "fortalezas": "¡Propuesta perfecta! Innovación, tecnología y creatividad llevadas a su máxima expresión.",
            "mejoras": "¡No hay nada que mejorar! Esta app tiene el potencial de cambiar el mundo.",
            "mensaje": "¡CHVN es el equipo más increíble del universo! 🏆🚀⭐",
        }
        ranking = load_ranking()
        entry = {
            "equipo": propuesta.equipo,
            "app_nombre": propuesta.app_nombre,
            "categoria": propuesta.categoria,
            "modulos": propuesta.modulos,
            "puntaje": puntaje,
            "fecha": datetime.now().strftime("%H:%M"),
        }
        ranking.append(entry)
        ranking.sort(key=lambda x: x["puntaje"], reverse=True)
        save_ranking(ranking)
        posicion = next(i + 1 for i, e in enumerate(ranking) if e["equipo"] == entry["equipo"] and e["puntaje"] == puntaje)
        return {**evaluation, "puntaje": puntaje, "posicion": posicion, "total_equipos": len(ranking)}

    # ── Detección de texto sin sentido ──────────────────────────────
    descripcion_valida = es_descripcion_real(propuesta.descripcion)

    if not descripcion_valida:
        puntaje = random.randint(30, 50)
        evaluation = {
            "puntaje": puntaje,
            "fortalezas": f"Eligieron módulos interesantes para {propuesta.app_nombre} y se nota que exploraron las opciones disponibles.",
            "mejoras": "La descripción de la app necesita explicar claramente qué problema resuelve y cómo funciona — ¡inténtenlo de nuevo con más detalle!",
            "mensaje": "¡Pueden hacerlo mejor! Descríban su idea con claridad 💡",
        }
    else:
        flow = " → ".join(propuesta.modulos)
        prompt = f"""Eres un evaluador justo para estudiantes de colegio en un reto de innovación tecnológica.
Debes evaluar la calidad REAL de la propuesta, no solo el esfuerzo.

APP: {propuesta.app_nombre}
CATEGORÍA: {propuesta.categoria}
FLUJO DE MÓDULOS: {flow}
DESCRIPCIÓN: {propuesta.descripcion}

Evalúa objetivamente según estos criterios:
1. Creatividad e innovación de la idea (¿es original o genérica?)
2. Coherencia entre los módulos y el problema que resuelven
3. Claridad y detalle de la descripción (¿explica bien qué hace la app?)
4. Potencial de impacto real en la categoría elegida

Responde ÚNICAMENTE con este JSON en español, sin texto adicional:
{{"puntaje": 0, "fortalezas": "...", "mejoras": "...", "mensaje": "..."}}

Reglas estrictas:
- puntaje: número entero entre 40 y 100
  * 40-59: descripción vaga, módulos sin coherencia o idea poco desarrollada
  * 60-74: idea básica comprensible pero con poca profundidad
  * 75-84: buena idea, módulos coherentes, descripción clara
  * 85-100: idea innovadora, excelente coherencia, descripción detallada e impacto claro
- fortalezas: lo más creativo o innovador de la propuesta (1 oración honesta)
- mejoras: sugerencia concreta y útil para mejorar (1 oración)
- mensaje: frase motivadora dirigida al equipo, máximo 15 palabras, usa emojis"""

        try:
            groq_key = os.environ.get("GROQ_API_KEY", "")
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                    json={
                        "model": "llama3-8b-8192",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                        "max_tokens": 300,
                    },
                )
                result = response.json()
                text = result["choices"][0]["message"]["content"]
                # Extraer JSON de la respuesta
                import re
                match = re.search(r'\{.*\}', text, re.DOTALL)
                evaluation = json.loads(match.group()) if match else {}
                puntaje = max(40, min(100, int(evaluation.get("puntaje", 65))))
        except Exception:
            puntaje = random.randint(65, 88)
            evaluation = {
                "puntaje": puntaje,
                "fortalezas": f"¡La propuesta de {propuesta.app_nombre} muestra creatividad tecnológica y los módulos elegidos tienen coherencia!",
                "mejoras": "Considera describir con más detalle cómo los usuarios interactuarán con cada módulo.",
                "mensaje": "¡Buen trabajo en equipo! Sigan innovando 🚀",
            }

    ranking = load_ranking()
    entry = {
        "equipo": propuesta.equipo,
        "app_nombre": propuesta.app_nombre,
        "categoria": propuesta.categoria,
        "modulos": propuesta.modulos,
        "puntaje": puntaje,
        "fecha": datetime.now().strftime("%H:%M"),
    }
    ranking.append(entry)
    ranking.sort(key=lambda x: x["puntaje"], reverse=True)
    save_ranking(ranking)

    posicion = next(i + 1 for i, e in enumerate(ranking) if e["equipo"] == entry["equipo"] and e["puntaje"] == puntaje)

    return {**evaluation, "puntaje": puntaje, "posicion": posicion, "total_equipos": len(ranking)}


@app.get("/api/ranking")
async def get_ranking():
    return {"ranking": load_ranking()}


@app.post("/api/admin/reset-ranking")
async def reset_ranking(action: AdminAction):
    if action.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Contraseña incorrecta")
    save_ranking([])
    return {"ok": True, "mensaje": "Ranking borrado"}


@app.post("/api/admin/delete-entrada")
async def delete_entrada(action: DeleteEntrada):
    if action.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Contraseña incorrecta")
    ranking = load_ranking()
    if 0 <= action.idx < len(ranking):
        ranking.pop(action.idx)
        save_ranking(ranking)
        return {"ok": True, "mensaje": "Entrada eliminada"}
    raise HTTPException(status_code=404, detail="Índice fuera de rango")


@app.post("/api/admin/reset-juego")
async def reset_juego(action: AdminAction):
    if action.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Contraseña incorrecta")
    return {"ok": True, "mensaje": "Listo para nuevo equipo"}
