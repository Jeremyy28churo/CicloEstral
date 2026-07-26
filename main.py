import streamlit as st
st.set_page_config(page_title="Ciclo Estral", layout="wide")
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import json
from evaluacion import renderizar_evaluacion, BANCO_PREGUNTAS

# FUNCIONES UNIVERSALES DE SINCRONIZACIÓN DE ESTADO
def sync_state(temp_key, real_key):
  st.session_state[real_key] = st.session_state[temp_key]

def aplicar_tema_dinamico(especie):
    # Diccionario Avanzado: Hex, RGB y Color de Contraste (Texto)
    temas = {
        "Bovino":  {"hex": "#00B4D8", "rgb": "0, 180, 216",  "text": "#121212"}, # Cian
        "Porcino": {"hex": "#F4A261", "rgb": "244, 162, 97", "text": "#121212"}, # Naranja
        "Ovino":   {"hex": "#E9C46A", "rgb": "233, 196, 106","text": "#121212"}, # Dorado
        "Caprino": {"hex": "#558B2F", "rgb": "85, 139, 47",  "text": "#FFFFFF"}, # Verde Oliva
        "Equino":  {"hex": "#7B2CBF", "rgb": "123, 44, 191", "text": "#FFFFFF"}, # Púrpura Elegante
        "Ave":     {"hex": "#D32F2F", "rgb": "211, 47, 47",  "text": "#FFFFFF"}  # Rojo
    }
    
    # Fallback de seguridad
    tema_activo = temas.get(especie, temas["Bovino"])
    c_hex = tema_activo["hex"]
    c_rgb = tema_activo["rgb"]
    c_txt = tema_activo["text"]
    
    st.markdown(f"""
    <style>
        /* =========================================
           ROOT VARIABLES & GLOBAL BACKGROUND
           ========================================= */
        :root {{
            --color-hex: {c_hex} !important;
            --color-rgb: {c_rgb} !important;
            --color-text-contrast: {c_txt} !important;
            --background-color: #121212 !important;
            --text-color: #FFFFFF !important;
        }}

        [data-testid="stAppViewContainer"], [data-testid="stHeader"], html, body {{
            background-color: #121212 !important;
            color: #FFFFFF !important;
        }}

        /* =========================================
           CONTENEDORES TINTADOS (TINTED CARDS)
           ========================================= */
        /* Interceptamos los contenedores que envuelvas con .tinted-card */
        .tinted-card {{
            background-color: rgba(var(--color-rgb), 0.15) !important;
            border: 2px solid var(--color-hex) !important;
            border-radius: 12px !important;
            padding: 22px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 8px 24px rgba(var(--color-rgb), 0.2) !important;
            transition: all 0.3s ease;
        }}
        .tinted-card:hover {{
            background-color: rgba(var(--color-rgb), 0.25) !important;
            box-shadow: 0 12px 30px rgba(var(--color-rgb), 0.35) !important;
            transform: translateY(-2px);
        }}

        /* =========================================
           TÍTULOS IMPACTANTES (GRADIENTS)
           ========================================= */
        .tinted-card h1, .tinted-card h2, .tinted-card h3, .gradient-title {{
            background: linear-gradient(90deg, var(--color-hex) 0%, #FFFFFF 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 900 !important;
            letter-spacing: 0.5px !important;
            margin-top: 0 !important;
        }}

        /* =========================================
           ETIQUETAS SÓLIDAS (AGRO-BADGES)
           ========================================= */
        .agro-badge {{
            background-color: var(--color-hex) !important;
            color: var(--color-text-contrast) !important;
            padding: 5px 12px !important;
            border-radius: 6px !important;
            font-weight: 900 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
            font-size: 0.8rem !important;
            display: inline-block !important;
            margin-bottom: 8px !important;
            box-shadow: 0 4px 10px rgba(var(--color-rgb), 0.4) !important;
        }}

        /* =========================================
           BOTONES MASIVOS (NATIVOS DE STREAMLIT)
           ========================================= */
        div.stButton > button {{
            background-color: var(--color-hex) !important;
            color: var(--color-text-contrast) !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 20px 24px !important;
            font-weight: 900 !important;
            font-size: 1.15rem !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 6px 15px rgba(var(--color-rgb), 0.4) !important;
            width: 100% !important;
        }}
        div.stButton > button p {{
            color: var(--color-text-contrast) !important;
            font-weight: 900 !important;
            font-size: 1.15rem !important;
        }}
        div.stButton > button:hover {{
            background-color: #FFFFFF !important;
            color: #121212 !important; /* Fuerza contraste oscuro en hover */
            box-shadow: 0 0 25px rgba(var(--color-rgb), 0.7) !important;
            transform: translateY(-3px) !important;
        }}
        div.stButton > button:hover p {{
            color: #121212 !important;
        }}

        /* =========================================
           NAVEGACIÓN PRINCIPAL (LOS 3 CUADROS MÁGICOS)
           ========================================= */
        @keyframes cyberPulse {{
            0% {{ box-shadow: 0 0 0 0 rgba(var(--color-rgb), 0.6); }}
            70% {{ box-shadow: 0 0 0 15px rgba(var(--color-rgb), 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(var(--color-rgb), 0); }}
        }}

        /* Elevamos la especificidad agregando div.stButton > para vencer al botón por defecto */
        div.stButton > button[aria-label="FASES DEL CICLO ESTRAL"],
        div.stButton > button[aria-label="CHECKLIST DE CELO E IA"],
        div.stButton > button[aria-label="LABORATORIO DE SIMULACION"],
        div.stButton > button[aria-label="FASES DEL CICLO ESTRAL "] /* Fallback por si hay espacios */ {{
            background: linear-gradient(145deg, rgba(20,20,25,0.9) 0%, rgba(35,35,45,0.95) 100%) !important;
            border: 1px solid rgba(var(--color-rgb), 0.3) !important;
            border-left: 8px solid var(--color-hex) !important;
            border-radius: 14px !important;
            padding: 24px !important;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.6) !important;
            animation: cyberPulse 2.5s infinite !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }}
        
        div.stButton > button[aria-label="FASES DEL CICLO ESTRAL"] p,
        div.stButton > button[aria-label="CHECKLIST DE CELO E IA"] p,
        div.stButton > button[aria-label="LABORATORIO DE SIMULACION"] p {{
            color: #FFFFFF !important;
            font-weight: 900 !important;
            font-size: 1.15rem !important;
            letter-spacing: 2px !important;
            text-shadow: 0 2px 10px rgba(0,0,0,0.8) !important;
            text-transform: uppercase !important;
        }}

        div.stButton > button[aria-label="FASES DEL CICLO ESTRAL"]:hover,
        div.stButton > button[aria-label="CHECKLIST DE CELO E IA"]:hover,
        div.stButton > button[aria-label="LABORATORIO DE SIMULACION"]:hover {{
            background: linear-gradient(135deg, var(--color-hex) 0%, rgba(var(--color-rgb), 0.8) 100%) !important;
            border-color: #FFFFFF !important;
            border-left: 8px solid #FFFFFF !important;
            transform: scale(1.04) translateY(-5px) !important;
            box-shadow: 0 20px 40px rgba(var(--color-rgb), 0.7) !important;
            animation: none !important;
        }}
        
        div.stButton > button[aria-label="FASES DEL CICLO ESTRAL"]:hover p,
        div.stButton > button[aria-label="CHECKLIST DE CELO E IA"]:hover p,
        div.stButton > button[aria-label="LABORATORIO DE SIMULACION"]:hover p {{
            color: var(--color-text-contrast) !important;
            text-shadow: none !important;
        }}

        /* Forzar Color en Sliders y Radios Nativos */
        div[data-baseweb="radio"] div[data-checked="true"] > div,
        .stCheckbox div[data-checked="true"] > div,
        .stSlider div[data-baseweb="slider"] div[data-testid="stTickBar"] > div {{
            background-color: var(--color-hex) !important;
            border-color: var(--color-hex) !important;
        }}
    </style>
    """, unsafe_allow_html=True)

# INICIALIZACIÓN GLOBAL DE ESTADO (Para evitar State Loss)
if 'etapa_actual' not in st.session_state:
  st.session_state.etapa_actual = 'portada'
if 'especie_seleccionada' not in st.session_state:
  st.session_state.especie_seleccionada = None
if 'seccion_activa' not in st.session_state:
  st.session_state.seccion_activa = 'Fases del Ciclo Estral'

# Configuración de página
st.set_page_config(page_title="Granja Digital - Fisiología Reproductiva", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS (GLASSMORPHISM PRO THEME) ---
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
  
  /* Ocultar UI base de Streamlit */
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
  header {visibility: hidden;}

  /* Ocultar boton toggle del sidebar */
  [data-testid="collapsedControl"] {display: none !important;}
  [data-testid="stSidebar"] {display: none !important;}
  
  /* Variables y Base - NUEVO FONDO OSCURO */
  [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #121212 !important;
  }
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #121212;
    color: #FFFFFF;
  }
  
  /* Animaciones Generales */
  @keyframes fadeInUpRecurrent {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
  }

  /* Animación principal para los contenedores (pestañas) evitando romper la estructura global */
  div[data-testid="stTabView"] > div[role="tabpanel"] {
      animation: fadeInUpRecurrent 0.4s ease-out forwards;
  }

  /* Retraso escalonado para re-renderizar elementos de texto al cambiar de vista */
  div[data-testid="stTabView"] > div[role="tabpanel"] h1, .stMarkdown h1 {
      opacity: 0; animation: fadeInUpRecurrent 0.4s ease-out forwards; animation-delay: 0.1s;
  }

  div[data-testid="stTabView"] > div[role="tabpanel"] h2, .stMarkdown h2 {
      opacity: 0; animation: fadeInUpRecurrent 0.4s ease-out forwards; animation-delay: 0.2s;
  }

  div[data-testid="stTabView"] > div[role="tabpanel"] h3, .stMarkdown h3 {
      opacity: 0; animation: fadeInUpRecurrent 0.4s ease-out forwards; animation-delay: 0.3s;
  }

  div[data-testid="stTabView"] > div[role="tabpanel"] p,
  div[data-testid="stTabView"] > div[role="tabpanel"] li, .stMarkdown p {
      opacity: 0; animation: fadeInUpRecurrent 0.4s ease-out forwards; animation-delay: 0.4s;
  }

  /* =========================================
     TIPOGRAFÍA PREMIUM Y RESALTES (SIMULADOR)
     ========================================= */
  
  /* Etiquetas de Radio Buttons (Opciones) */
  .stRadio label[data-baseweb="radio"] div {
      font-size: 1.05rem !important;
      font-weight: 600 !important;
      color: #E2E8F0 !important;
  }
  
  /* Títulos de los selectores (ej. Seleccione Patología:) */
  .stRadio > label, .stSelectbox > label {
      font-size: 1.15rem !important;
      font-weight: 900 !important;
      color: var(--color-hex) !important;
      letter-spacing: 0.5px !important;
      margin-bottom: 8px !important;
      text-transform: uppercase !important;
  }
  
  /* Textos generales dentro de markdown */
  .stMarkdown p, .stMarkdown li {
      font-size: 1.1rem !important;
      color: #F1F5F9 !important;
      line-height: 1.6 !important;
  }
  
  /* Negritas impactantes que toman el color del animal */
  .stMarkdown b, .stMarkdown strong {
      color: var(--color-hex) !important;
      font-weight: 900 !important;
      letter-spacing: 0.3px !important;
  }
  
  /* Encabezados de Expanders (Diagnóstico Económico...) */
  [data-testid="stExpander"] summary p {
      font-size: 1.15rem !important;
      font-weight: 800 !important;
      color: #FFFFFF !important;
  }
  
  /* Contenedor del Expander */
  [data-testid="stExpander"] {
      border: 1px solid rgba(var(--color-rgb), 0.4) !important;
      border-radius: 8px !important;
      background-color: rgba(26,28,35,0.7) !important;
      transition: all 0.3s ease;
  }
  [data-testid="stExpander"]:hover {
      box-shadow: 0 4px 15px rgba(var(--color-rgb), 0.2) !important;
      border-color: var(--color-hex) !important;
  }
  
  /* Alertas de Streamlit (Notas Clínicas, etc.) */
  div[data-testid="stAlert"] {
      background-color: rgba(var(--color-rgb), 0.15) !important;
      border: 1px solid rgba(var(--color-rgb), 0.5) !important;
      border-left: 6px solid var(--color-hex) !important;
      color: #FFFFFF !important;
      box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
  }
  div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
      color: #FFFFFF !important;
      font-weight: 600 !important;
      font-size: 1.1rem !important;
  }

  @keyframes cinematicReveal {
    0% {
      opacity: 0 !important;
      filter: blur(10px) saturate(0.5) !important;
      transform: scale(0.975) translateY(16px) !important;
    }
    55% {
      filter: blur(2px) saturate(0.85) !important;
    }
    100% {
      opacity: 1 !important;
      filter: blur(0px) saturate(1) !important;
      transform: scale(1) translateY(0px) !important;
    }
  }

  @keyframes cinematicRevealSidebar {
    0% {
      opacity: 0 !important;
      filter: blur(8px) !important;
      transform: translateX(-22px) !important;
    }
    100% {
      opacity: 1 !important;
      filter: blur(0px) !important;
      transform: translateX(0) !important;
    }
  }

  /* Nodo raiz estatico */
  [data-testid="stAppViewContainer"] {
    animation: cinematicReveal 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0ms both !important;
    will-change: transform, filter, opacity !important;
    transform-origin: center top !important;
  }

  [data-testid="stSidebar"] {
    animation: cinematicRevealSidebar 0.85s cubic-bezier(0.16, 1, 0.3, 1) 120ms both !important;
    will-change: transform, filter, opacity !important;
  }

  [data-testid="stHeader"] {
    animation: cinematicReveal 0.7s cubic-bezier(0.16, 1, 0.3, 1) 0ms both !important;
  }

  .animate-fade-in {
    animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
  }
  
  /* Glassmorphism Containers - FONDO DE TARJETAS GRIS OSCURO */
  .glass-card {
    background: #1E1E1E;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
  }
  .glass-card:hover {
    transform: translateY(-4px);
    border-color: rgba(255, 255, 255, 0.15);
    box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.7);
  }
  
  /* Variantes de color para Glass Cards (Bordes Superiores) */
  .glass-cyan { border-top: 3px solid #00E676; }
  .glass-emerald { border-top: 3px solid #00E676; }
  .glass-orange { border-top: 3px solid #FF9933; }
  .glass-purple { border-top: 3px solid #9c27b0; }
  .glass-red { border-top: 3px solid #FF3366; }
  
  /* Tipografía Premium - BLANCOS Y ACENTOS ESMERALDA */
  .title-gradient {
    font-size: clamp(3rem, 5vw, 5rem) !important;
    font-weight: 900 !important;
    line-height: 1.1 !important;
    color: #00E676 !important;
    background: none !important;
    -webkit-text-fill-color: initial !important;
    text-shadow: 0 0 15px rgba(0, 230, 118, 0.3) !important;
    letter-spacing: -1px !important;
    margin-bottom: 10px !important;
    text-align: center;
  }
  .subtitle-elegant {
    font-size: clamp(1.1rem, 2vw, 1.5rem) !important;
    color: #B0B3B8 !important;
    font-weight: 400 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 30px !important;
  }
  
  .texto-lectura-grande {
    font-size: 16px !important;
    line-height: 1.7 !important;
    color: #FFFFFF !important;
  }
  
  /* Botones Pro - VERDE VIBRANTE */
  .btn-primary-custom {
    background: #00E676;
    color: #121212 !important;
    padding: 16px 32px;
    border-radius: 12px;
    font-weight: 800;
    font-size: 1.2rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    border: none;
    cursor: pointer;
    display: inline-block;
    text-align: center;
    transition: all 0.3s ease;
    text-shadow: none !important;
    text-decoration: none;
  }
  .btn-primary-custom:hover {
    transform: scale(1.05);
    background: #00C853;
    color: #121212 !important;
    text-decoration: none;
  }
  
  /* Tarjetas de Patologías (Laboratorio) */
  .pathology-card {
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 15px;
    border: 1px solid rgba(255,255,255,0.1);
  }
  .path-ben { background: linear-gradient(145deg, rgba(239, 83, 80, 0.1), rgba(0,0,0,0.4)); border-left: 4px solid #EF5350; }
  .path-cl { background: linear-gradient(145deg, rgba(186, 104, 200, 0.1), rgba(0,0,0,0.4)); border-left: 4px solid #BA68C8; }
  .path-heat { background: linear-gradient(145deg, rgba(212, 175, 55, 0.1), rgba(0,0,0,0.4)); border-left: 4px solid #D4AF37; }
  
  /* Ajustes Nativos de Streamlit */
  [data-testid="stMetric"] {
    background: #1E1E1E;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    transition: transform 0.2s ease;
  }
  [data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    background: rgba(42, 45, 52, 0.9);
  }
  
  /* Checkbox y Radio */
  [data-testid="stCheckbox"], [data-testid="stRadio"] {
    padding: 8px;
    border-radius: 8px;
    transition: background-color 0.2s ease;
  }
  [data-testid="stCheckbox"]:hover, [data-testid="stRadio"]:hover {
    background-color: rgba(255, 255, 255, 0.05);
  }

  /* ====== BOTONES DE NAVEGACION GLOBAL ====== */
  /* ==========================================================
     REDISEÑO DE BOTONES DE MENÚ PRINCIPAL (DASHBOARD PREMIUM)
     ========================================================== */

  /* Interceptar los botones nativos de Streamlit */
  div.stButton > button {
    width: 100% !important;
    background-color: #1E1E1E !important;
    background-image: none !important;
    padding: 20px 24px !important;
    
    /* Bordes: Izquierdo grueso y vibrante, los demás invisibles */
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-left: 5px solid #00E676 !important;
    border-radius: 6px !important;
    
    /* Transición suave para el toque mágico */
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4) !important;
    display: flex !important;
    justify-content: flex-start !important;
  }
  
  /* Tipografía Contundente */
  div.stButton > button, 
  div.stButton > button p {
    color: #FFFFFF !important;
    text-transform: uppercase !important;
    font-size: 1.15rem !important;
    font-weight: 800 !important;
    letter-spacing: 1px !important;
  }

  /* Animación y Hover (El Toque Mágico) */
  div.stButton > button:hover {
    background-color: #2A2A2A !important;
    border-left: 5px solid #00E676 !important;
    border-color: rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 0 20px rgba(0, 230, 118, 0.25), 0 8px 16px rgba(0, 0, 0, 0.5) !important;
    transform: translateX(4px) !important;
  }

  /* Efecto al hacer clic */
  div.stButton > button:active {
    background-color: #1A1A1A !important;
    transform: translateX(0px) scale(0.99) !important;
    box-shadow: 0 0 10px rgba(0, 230, 118, 0.2) !important;
  }
  
  /* Resetear estilos específicos de secciones */
  button[aria-label="FASES DEL CICLO ESTRAL"],
  button[aria-label="CHECKLIST DE CELO E IA"],
  button[aria-label="LABORATORIO DE SIMULACION"] {
      background: #1E1E1E !important;
      border: 1px solid rgba(255, 255, 255, 0.05) !important;
      border-left: 5px solid #00E676 !important;
  }
  button[aria-label="FASES DEL CICLO ESTRAL"]:hover,
  button[aria-label="CHECKLIST DE CELO E IA"]:hover,
  button[aria-label="LABORATORIO DE SIMULACION"]:hover {
      background: #2A2A2A !important;
      border-left: 5px solid #00E676 !important;
  }

  /* Boton secundario en sidebar (Cambiar Especie / Volver) */
  [data-testid="stSidebar"] .stButton > button {
    background-color: transparent !important;
    background: transparent !important;
    border: 1px solid rgba(0, 230, 118, 0.5) !important;
    border-left: 1px solid rgba(0, 230, 118, 0.5) !important; /* Sobreescribir el grueso */
    color: #00E676 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    padding: 10px 15px !important;
    justify-content: center !important;
  }
  [data-testid="stSidebar"] .stButton > button p {
    color: #00E676 !important;
    font-size: 13px !important;
  }
  [data-testid="stSidebar"] .stButton > button:hover {
    background-color: rgba(0, 230, 118, 0.12) !important;
    background: rgba(0, 230, 118, 0.12) !important;
    border-color: #00E676 !important;
    border-left: 1px solid #00E676 !important;
    color: #00E676 !important;
    box-shadow: none !important;
    transform: none !important;
  }

  /* RESPONSIVE DESIGN */
  @media (max-width: 768px) {
    [data-testid="stAppViewContainer"] > section > div { padding-left: 12px !important; padding-right: 12px !important; }
    [data-testid="block-container"] { padding: 1rem 0.75rem !important; }
    .title-gradient { font-size: clamp(2rem, 8vw, 3rem) !important; letter-spacing: -0.5px !important; margin-bottom: 6px !important; }
    .subtitle-elegant { font-size: clamp(0.75rem, 3.5vw, 1rem) !important; letter-spacing: 1px !important; margin-bottom: 16px !important; }
    .texto-lectura-grande { font-size: 14px !important; line-height: 1.6 !important; }
    .glass-card { padding: 16px !important; border-radius: 12px !important; margin-bottom: 14px !important; transform: none !important; }
    .glass-card:hover { transform: none !important; }
    .pathology-card { padding: 14px !important; }
    div.stButton > button:first-child { font-size: 12px !important; letter-spacing: 1px !important; padding: 12px 14px !important; min-height: 44px !important; transform: none !important; }
    div.stButton > button:first-child p { font-size: 12px !important; letter-spacing: 1px !important; }
    div.stButton > button:first-child:hover { transform: none !important; }
    button[aria-label="FASES DEL CICLO ESTRAL"], button[aria-label="CHECKLIST DE CELO E IA"], button[aria-label="LABORATORIO DE SIMULACION"] { font-size: 11px !important; letter-spacing: 0.5px !important; padding: 10px 8px !important; }
    .btn-primary-custom { padding: 12px 20px !important; font-size: 1rem !important; letter-spacing: 0.5px !important; border-radius: 10px !important; }
    [data-testid="stMetric"] { padding: 10px !important; }
    [data-testid="stMetric"]:hover { transform: none !important; }
    [data-testid="stRadio"] label { padding: 10px 8px !important; min-height: 44px !important; display: flex !important; align-items: center !important; }
    [data-testid="stCheckbox"] label { min-height: 44px !important; display: flex !important; align-items: center !important; }
    [data-testid="stSidebar"] > div:first-child { padding: 1rem 0.75rem !important; }
    [data-testid="stSidebar"] .stButton > button:first-child { font-size: 12px !important; padding: 10px 12px !important; min-height: 44px !important; }
    div[style*="font-size:0.82rem"] { font-size: 0.75rem !important; }
    hr { margin: 12px 0 !important; }
  }

  @media (max-width: 480px) {
    .title-gradient { font-size: clamp(1.6rem, 9vw, 2.4rem) !important; }
    .subtitle-elegant { font-size: clamp(0.65rem, 3vw, 0.85rem) !important; letter-spacing: 0.5px !important; }
    .glass-card { padding: 12px !important; border-radius: 10px !important; }
    div.stButton > button:first-child { font-size: 11px !important; letter-spacing: 0.5px !important; padding: 11px 10px !important; }
    button[aria-label="FASES DEL CICLO ESTRAL"], button[aria-label="CHECKLIST DE CELO E IA"], button[aria-label="LABORATORIO DE SIMULACION"] { font-size: 10px !important; letter-spacing: 0 !important; padding: 9px 6px !important; white-space: normal !important; word-break: break-word !important; }
    .texto-lectura-grande { font-size: 13px !important; }
    [data-testid="stMetric"] { padding: 8px !important; }
    [data-testid="stMetricLabel"] { font-size: 11px !important; }
    [data-testid="stMetricValue"] { font-size: 1.2rem !important; }
  }

  /* =========================================
     REDISENO VISUAL EXTREMO - UI/UX
     ========================================= */

  @keyframes critical-pulse {
    0% { opacity: 1; text-shadow: 0 0 10px rgba(255, 51, 102, 0.8); color: #FF3366; }
    50% { opacity: 0.7; text-shadow: 0 0 20px rgba(255, 51, 102, 1); color: #FF6688; }
    100% { opacity: 1; text-shadow: 0 0 10px rgba(255, 51, 102, 0.8); color: #FF3366; }
  }

  @keyframes optimum-pulse {
    0% { opacity: 1; text-shadow: 0 0 10px rgba(0, 230, 118, 0.8); color: #00E676; }
    50% { opacity: 0.8; text-shadow: 0 0 25px rgba(0, 230, 118, 1); color: #69F0AE; }
    100% { opacity: 1; text-shadow: 0 0 10px rgba(0, 230, 118, 0.8); color: #00E676; }
  }

  .text-heavy { font-size: 1.4rem !important; font-weight: 800 !important; color: #FFFFFF !important; letter-spacing: 0.5px; }
  .text-neon-green { color: #00E676 !important; font-weight: 800 !important; }
  .text-neon-orange { color: #FF9933 !important; font-weight: 800 !important; }
  .alert-critical-pulse { animation: critical-pulse 1.8s infinite ease-in-out; font-weight: 900 !important; font-size: 1.2rem !important; }
  .alert-optimum-pulse { animation: optimum-pulse 2s infinite ease-in-out; font-weight: 900 !important; font-size: 1.2rem !important; }

  /* ENCUADRES OSCUROS CON RELIEVE */
  .ui-encuadre {
    background: linear-gradient(145deg, rgba(42, 45, 52, 0.9), rgba(24, 24, 27, 0.95));
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6);
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease, border-color 0.3s ease;
  }
  .ui-encuadre:hover {
    transform: scale(1.02);
    box-shadow: 0 15px 45px 0 rgba(0, 0, 0, 0.8);
    border-color: rgba(255, 255, 255, 0.2);
  }

  .encuadre-proestro { border-left: 6px solid #FF3366 !important; }
  .encuadre-proestro:hover { box-shadow: -10px 0 30px -10px rgba(255, 51, 102, 0.5), 0 15px 45px 0 rgba(0, 0, 0, 0.8); }

  .encuadre-estro { border-left: 6px solid #00E676 !important; }
  .encuadre-estro:hover { box-shadow: -10px 0 30px -10px rgba(0, 230, 118, 0.5), 0 15px 45px 0 rgba(0, 0, 0, 0.8); }

  .encuadre-metaestro { border-left: 6px solid #FF9933 !important; }
  .encuadre-metaestro:hover { box-shadow: -10px 0 30px -10px rgba(255, 153, 51, 0.5), 0 15px 45px 0 rgba(0, 0, 0, 0.8); }

  .encuadre-diestro { border-left: 6px solid #3399FF !important; }
  .encuadre-diestro:hover { box-shadow: -10px 0 30px -10px rgba(51, 153, 255, 0.5), 0 15px 45px 0 rgba(0, 0, 0, 0.8); }
  
  .encuadre-alerta {
    border: 2px solid #FF3366;
    background: rgba(30, 10, 15, 0.9);
  }

  /* ==========================================================
     SISTEMA DE DISEÑO DINÁMICO POR ESPECIE (AGRO-TECH)
     ========================================================== */

  /* 1. Tematización Dinámica (Master Classes y Variables CSS) */
  .tema-bovino {
    --color-especie: #00B4D8; /* Azul Tecnológico / Cian Profundo */
    --color-especie-glow: rgba(0, 180, 216, 0.4);
  }

  .tema-porcino {
    --color-especie: #F4A261; /* Ámbar / Naranja Terracota */
    --color-especie-glow: rgba(244, 162, 97, 0.4);
  }

  .tema-ovino {
    --color-especie: #E9C46A; /* Dorado Suave / Tierra */
    --color-especie-glow: rgba(233, 196, 106, 0.4);
  }

  .tema-equino {
    --color-especie: #7B2CBF; /* Púrpura Elegante / Índigo */
    --color-especie-glow: rgba(123, 44, 191, 0.4);
  }
  
  .tema-caprino {
    --color-especie: #E76F51; /* Coral/Rojo Suave */
    --color-especie-glow: rgba(231, 111, 81, 0.4);
  }
  
  .tema-ave {
    --color-especie: #2A9D8F; /* Verde Menta / Esmeralda Suave */
    --color-especie-glow: rgba(42, 157, 143, 0.4);
  }

  /* 2. Zonas Interactivas y Glassmorphism */
  .panel-interactivo {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid var(--color-especie, #FFFFFF); /* Fino borde dinámico */
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  /* Hover del panel interactivo (Efecto levante y glow) */
  .panel-interactivo:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4), 0 0 15px var(--color-especie-glow);
  }

  /* Efecto Focus en Controles y Sliders dentro del panel interactivo */
  .panel-interactivo [data-baseweb="input"]:focus-within,
  .panel-interactivo [data-baseweb="textarea"]:focus-within,
  .panel-interactivo [data-testid="stRadio"] label:hover,
  .panel-interactivo [data-testid="stCheckbox"] label:hover {
    box-shadow: 0 0 10px var(--color-especie) !important;
    border-color: var(--color-especie) !important;
    transition: all 0.3s ease;
  }

  /* 3. Tipografía y Jerarquía Académica */
  .panel-interactivo .texto-destacado {
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
  }

  .panel-interactivo .metrica-economica,
  .panel-interactivo .diagnostico-fisiologico {
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    color: var(--color-especie) !important;
    background: rgba(0, 0, 0, 0.2);
    padding: 10px 18px;
    border-radius: 8px;
    display: inline-block;
    margin: 10px 0;
    text-shadow: 0 0 8px var(--color-especie-glow);
    border-left: 4px solid var(--color-especie);
  }

  .panel-interactivo .texto-relleno {
    font-size: 1rem !important;
    font-weight: 400 !important;
    color: #B0B3B8 !important;
    line-height: 1.6;
  }
</style>
""", unsafe_allow_html=True)

# --- DATOS BIOLÓGICOS DEL PDF ---
SPECIES_DATA = {
  "Bovino": {
    "cycle_duration": 21,
    "estrus_days": [0, 0.75],
    "lh_peak": 0,
    "ovulation_timing": "10-14 h post-fin del estro",
    "maternal_recognition": "IFN-τ",
    "phases": [{"name": "Estro", "range": (0, 0.75), "color": "#FF3366"},
          {"name": "Metaestro", "range": (0.75, 4.75), "color": "#3399FF"},
          {"name": "Diestro", "range": (4.75, 18), "color": "#00CC99"},
          {"name": "Proestro", "range": (18, 21.01), "color": "#FF9933"}],
    "checklist": [
      "Monta aceptada (signo primario)",
      "Moco cervical transparente/filante",
      "Aumento de actividad locomotora (200-400%)",
      "Cabeceo sobre la grupa",
      "Caída del 5-10% de producción láctea",
      "Alza de temperatura vaginal (0.3-0.5°C)"
    ],
    "ia_window": [
      "**Regla AM/PM:** Celo AM -> IA esa tarde; Celo PM -> IA mañana siguiente.",
      "**Ventana:** 6-16h post-inicio del celo.",
      "**Fundamento:** La ovulación es 10-14h post-fin de estro y los espermatozoides requieren 6-8h de capacitación."
    ]
  },
  "Porcino": {
    "cycle_duration": 21,
    "estrus_days": [0, 2.5],
    "lh_peak": 1,
    "ovulation_timing": "36-44 h post-inicio del estro (poliovulatorio: 15-25)",
    "maternal_recognition": "Estrógenos embrionarios",
    "phases": [{"name": "Estro", "range": (0, 2.5), "color": "#FF3366"},
          {"name": "Metaestro", "range": (2.5, 6), "color": "#3399FF"},
          {"name": "Diestro", "range": (6, 18), "color": "#00CC99"},
          {"name": "Proestro", "range": (18, 21.01), "color": "#FF9933"}],
    "checklist": [
      "Reflejo de inmovilidad ante presión dorsal (sensibilidad >90% con verraco)",
      "Orejas rígidas/erectas",
      "Vulva inflamada y enrojecida",
      "Disminución de consumo de alimento"
    ],
    "ia_window": [
      "**Frecuencia:** Inseminar 2-3 veces durante el estro largo (cada 12-24h).",
      "**Dosis:** 80-100 mL con 3-4x10^9 espermatozoides."
    ]
  },
  "Ovino": {
    "cycle_duration": 17,
    "estrus_days": [0, 1.25],
    "lh_peak": 0,
    "ovulation_timing": "~24 h post-inicio",
    "maternal_recognition": "IFN-τ",
    "phases": [{"name": "Estro", "range": (0, 1.25), "color": "#FF3366"},
          {"name": "Metaestro", "range": (1.25, 4), "color": "#3399FF"},
          {"name": "Diestro", "range": (4, 15), "color": "#00CC99"},
          {"name": "Proestro", "range": (15, 17.01), "color": "#FF9933"}],
    "checklist": [
      "Dificultad para detección directa",
      "Uso de machos marcadores con arnés y crayón (marcan la grupa de color)",
      "Efecto Macho (introducción súbita tras >3 semanas de separación)"
    ],
    "ia_window": [
      "**Efecto Macho:** Induce pulsos de LH y ovulación sincronizada.",
      "**Estacionalidad:** Poliéstrica estacional de días cortos (otoño, regulado por melatonina)."
    ]
  },
  "Caprino": {
    "cycle_duration": 21,
    "estrus_days": [0, 1.5],
    "lh_peak": 0,
    "ovulation_timing": "~30 h post-inicio",
    "maternal_recognition": "IFN-τ",
    "phases": [{"name": "Estro", "range": (0, 1.5), "color": "#FF3366"},
          {"name": "Metaestro", "range": (1.5, 4), "color": "#3399FF"},
          {"name": "Diestro", "range": (4, 18), "color": "#00CC99"},
          {"name": "Proestro", "range": (18, 21.01), "color": "#FF9933"}],
    "checklist": [
      "Dificultad para detección directa",
      "Uso de machos marcadores con arnés y crayón (marcan la grupa de color)",
      "Efecto Macho (introducción súbita tras >3 semanas de separación para inducir pulsos de LH)"
    ],
    "ia_window": [
      "**Ventana:** Inseminar a las 24 horas del inicio del estro.",
      "**Estacionalidad:** Poliéstrica estacional (leve, continua en trópico)."
    ]
  },
  "Equino": {
    "cycle_duration": 21, 
    "estrus_days": [0, 5],
    "lh_peak": 4, 
    "ovulation_timing": "24-48 h ANTES del fin del estro",
    "maternal_recognition": "?",
    "phases": [{"name": "Estro", "range": (0, 5), "color": "#FF3366"},
          {"name": "Metaestro", "range": (5, 8), "color": "#3399FF"},
          {"name": "Diestro", "range": (8, 19), "color": "#00CC99"},
          {"name": "Proestro", "range": (19, 21.01), "color": "#FF9933"}],
    "checklist": [
      "Cola levantada",
      "Micción frecuente",
      "Vulva relajada",
      "'Guiño' vulvar rítmico ante el semental"
    ],
    "ia_window": [
      "**Regla Clínica:** IA/Monta DURANTE el estro (cada 48 h mientras esté en celo y se detecte folículo >35 mm).",
      "**Estacionalidad:** Poliéstrica estacional de días largos."
    ]
  },
  "Ave": {
    "cycle_duration": 26,
    "cycle_unit": "horas",
    "estrus_days": None,
    "lh_peak": 6,
    "ovulation_timing": "6-8 h post-oviposición anterior",
    "maternal_recognition": "N/A",
    "phases": [{"name": "Post-oviposición", "range": (0, 2), "color": "#FF9933"},
          {"name": "Pico LH / Ovulación", "range": (2, 8), "color": "#FF3366"},
          {"name": "Formación del huevo", "range": (8, 24), "color": "#3399FF"},
          {"name": "Oviposición", "range": (24, 26.01), "color": "#00CC99"}],
    "checklist": [
      "Programa de luz 16L:8O activo y estable",
      "Postura en serie de 5-7 días consecutivos + 1 día de pausa",
      "Jerarquía folicular intacta (F1→F2→F3→F4→F5)",
      "Calidad de cáscara y consistencia del huevo normales",
      "Consumo de alimento y agua sin alteración"
    ],
    "ia_window": [
      "**Almacenamiento espermático:** Espermatozoides almacenados en túbulos SST (unión útero-vaginal) durante 10-14 días post-cópula.",
      "**Sin regla AM/PM:** La gallina no tiene ciclo estral ni celo detectable.",
      "**Estrategia reproductiva:** Una sola inseminación o cópula cada 7-10 días es suficiente gracias al almacenamiento en SST."
    ]
  }
}

TIMELINE_DATA = {
  "Bovino": {
    "proestro": {"dur": "2-3 días", "icon": "", "title": "Folículo en crecimiento", "text": "Crecimiento del folículo dominante (4mm a 12-18mm). El Estradiol (E2) aumenta causando moco cervical transparente/filante, edema vulvar y relajación cervical."},
    "estro": {"dur": "12-18 horas (Holstein alta prod.: <10h)", "icon": "", "title": "Receptividad sexual", "text": "Período de receptividad sexual activa. Monta aceptada es el signo primario debido a E2 alto. Surge preovulatorio de LH."},
    "metaestro": {"dur": "3-4 días", "icon": "️", "title": "CL en formación", "text": "Ovulación ocurre 10-14h post-fin del estro. Luteinización del folículo ovulado para formar el Cuerpo Lúteo (CL) e inicio de secreción de P4. Posible sangrado metéstrico vaginal (24-48h post-ovulación)."},
    "diestro": {"dur": "12-14 días", "icon": "", "title": "CL Maduro", "text": "Fase más larga (CL maduro con P4 máxima). Sin reconocimiento materno (días 17-18), la PGF2α endometrial destruye el CL (luteólisis) para reiniciar el ciclo. Si hay preñez, el embrión libera IFN-τ."}
  },
  "Porcino": {
    "proestro": {"dur": "2-3 días", "icon": "", "title": "Crecimiento Múltiple", "text": "Fase folicular rápida. Crecimiento de múltiples folículos simultáneos (poliovulatorio)."},
    "estro": {"dur": "24-72 horas", "icon": "", "title": "Receptividad prolongada", "text": "Receptividad sexual prolongada. Signo clave: Reflejo de inmovilidad (lordosis con orejas rígidas) ante presión dorsal y feromonas del verraco."},
    "metaestro": {"dur": "2-3 días", "icon": "️", "title": "Formación de CLs", "text": "Ovulación de 15-25 folículos entre las 36-44h post-inicio del estro. Formación de múltiples cuerpos lúteos e inicio de la secreción de Progesterona (P4)."},
    "diestro": {"dur": "11-13 días", "icon": "", "title": "Dominio de P4", "text": "Producción masiva de P4. Para evitar la luteólisis, se requiere el reconocimiento materno mediado por los estrógenos de mínimo 4 embriones."}
  },
  "Ovino": {
    "proestro": {"dur": "1-2 días", "icon": "", "title": "Desarrollo Rápido", "text": "Crecimiento folicular rápido. Ciclicidad poliéstrica estacional de días cortos (otoño) estimulada por melatonina."},
    "estro": {"dur": "24-36 horas", "icon": "", "title": "Celo Discreto", "text": "Signos conductuales muy discretos. Búsqueda activa del macho. Ovulación de 1-3 folículos hacia el final de esta fase."},
    "metaestro": {"dur": "2-3 días", "icon": "️", "title": "CL Temprano", "text": "Formación del cuerpo lúteo joven y transición rápida hacia la secreción de progesterona (P4)."},
    "diestro": {"dur": "10-12 días", "icon": "", "title": "Fase Lútea Acortada", "text": "Fase lútea acortada en comparación con bovinos. Dominio de P4. Reconocimiento materno embrionario mediado por IFN-τ en el útero."}
  },
  "Caprino": {
    "proestro": {"dur": "2-3 días", "icon": "", "title": "Reclutamiento", "text": "Fase de reclutamiento y dominancia de 1-3 folículos. Poliéstrica estacional (con menor estacionalidad en regiones tropicales)."},
    "estro": {"dur": "24-48 horas", "icon": "", "title": "Celo Evidente", "text": "Signos de celo evidentes por vocalización y movimiento continuo de cola. Inducción de la ciclicidad por el 'Efecto Macho'."},
    "metaestro": {"dur": "2-3 días", "icon": "️", "title": "Luteinización", "text": "Ovulación ocurre unas 30 horas post-inicio de estro. Organización de 1-3 cuerpos lúteos en los ovarios."},
    "diestro": {"dur": "13-15 días", "icon": "", "title": "Dominio Lúteo", "text": "Dominio lúteo clásico de P4. Sin gestación, la PGF2α induce la luteólisis. Si hay preñez, el reconocimiento embrionario se realiza por IFN-τ."}
  },
  "Equino": {
    "proestro": {"dur": "2-3 días", "icon": "", "title": "Transición Inicial", "text": "Fase folicular inicial bajo influencia del fotoperíodo (poliéstrica estacional de días largos / primavera)."},
    "estro": {"dur": "4-7 días", "icon": "", "title": "Celo Muy Prolongado", "text": "Signos severos ante el semental (postura de monta, cola levantada, micción y 'guiño' de vulva rítmico)."},
    "metaestro": {"dur": "2-3 días", "icon": "️", "title": "Ovulación Especial", "text": "¡Particularidad única!: La ovulación ocurre 24-48h ANTES de terminar el estro. Inicio del desarrollo lúteo. La IA se debe programar DURANTE el celo."},
    "diestro": {"dur": "10-12 días", "icon": "", "title": "Reinicio Rápido", "text": "Dominio estricto de P4. Si no hay gestación, la hembra equina regresa al proestro rápidamente debido a la luteólisis fisiológica."}
  },
  "Ave": {
    "proestro": {"dur": "~2 horas", "icon": "", "title": "Fin del Ciclo Anterior", "text": "La oviposición del huevo anterior desencadena una señal neuroendocrina que inicia un nuevo ciclo ovulatorio de 25-27 horas."},
    "estro": {"dur": "~6 horas", "icon": "", "title": "Pico de LH y Ovulación", "text": "Pico preovulatorio de LH 6-8 horas post-oviposición. El folículo F1 (más maduro de la jerarquía F1→F5) ovula y es capturado por el infundíbulo."},
    "metaestro": {"dur": "~16 horas", "icon": "", "title": "Formación del Huevo", "text": "Tránsito oviductal completo: magnum (albúmina, ~3h), istmo (membranas, ~1.5h) y útero/glándula cascarígena (cáscara, ~20h). Calcificación activa."},
    "diestro": {"dur": "~2 horas", "icon": "", "title": "Oviposición", "text": "Expulsión del huevo completo. La postura ocurre en serie de 5-7 días consecutivos seguida de 1 día de pausa (retraso acumulado de ~1h/día)."}
  }
}

@st.cache_data
def generate_hormone_data(species, complication="Normal", pregnancy=False):
  data = SPECIES_DATA[species]
  days = data["cycle_duration"]
  t = np.linspace(0, days, 500)
  lh_peak = data["lh_peak"]

  # ========== RAMA EXCLUSIVA PARA AVE (ciclo ovulatorio de 26 horas) ==========
  if species == "Ave":
    # LH: Pico agudo 6-8h post-oviposición
    lh = 5 + 90 * np.exp(-((t - 6) ** 2) / 1.0)

    # FSH: Elevación basal con pico moderado pre-ovulatorio
    fsh = 15 + 25 * np.exp(-((t - 4) ** 2) / 3.0) + 10 * np.sin(t / days * 4 * np.pi)

    # Estradiol (E2): Elevación progresiva durante maduración del F1, pico pre-ovulatorio
    e2 = 10 + 70 * np.exp(-((t - 5) ** 2) / 4.0)

    # Progesterona (P4): Pico breve pre-ovulatorio (sin CL funcional prolongado)
    p4 = 5 + 50 * np.exp(-((t - 5.5) ** 2) / 1.5)

    # PGF2α y Señal Materna: No aplican en aves
    pgf2a = np.full_like(t, 2.0)
    senal_materna = np.full_like(t, 0.0)

    # Patologías aviares
    if complication == "Estrés por Calor":
      lh = lh * 0.3 + 3
      e2 = e2 * 0.35 + 2
      fsh = fsh * 0.5
      p4 = p4 * 0.4 + 2
    elif complication == "Fotoperíodo Inadecuado (<14h luz)":
      lh = np.full_like(t, 4.0)
      fsh = 8 + 4 * np.sin(t / days * 4 * np.pi)
      e2 = np.full_like(t, 5.0)
      p4 = np.full_like(t, 3.0)
    elif complication == "Agotamiento Ovárico / Muda":
      lh = np.full_like(t, 3.0)
      fsh = np.full_like(t, 5.0)
      e2 = np.full_like(t, 3.0)
      p4 = np.full_like(t, 2.0)

    return pd.DataFrame({
      "Día": t,
      "LH": np.clip(lh, 0, 100),
      "FSH": np.clip(fsh, 0, 100),
      "Estradiol (E2)": np.clip(e2, 0, 100),
      "Progesterona (P4)": np.clip(p4, 0, 100),
      "PGF2α": np.clip(pgf2a, 0, 100),
      "Señal Materna": np.clip(senal_materna, 0, 100)
    })

  # ========== LÓGICA ORIGINAL PARA MAMÍFEROS (sin modificar) ==========
  # Estradiol (E2)
  if species == "Equino":
    e_peak = lh_peak - 1
    e2 = 15 + 85 * np.exp(-((t - e_peak) ** 2) / 5.0)
  else:
    e2 = 10 + 85 * np.exp(-((t - lh_peak) ** 2) / 1.5)
    if lh_peak == 0:
      e2 += 85 * np.exp(-((t - days) ** 2) / 1.5)
      
  # LH
  if species == "Equino":
    lh = 10 + 80 * np.exp(-((t - lh_peak) ** 2) / 4.0)
  else:
    lh = 5 + 95 * np.exp(-((t - lh_peak) ** 2) / 0.05)
    if lh_peak == 0:
      lh += 95 * np.exp(-((t - days) ** 2) / 0.05)
      
  # FSH
  fsh = 15 + 15 * np.sin(t / days * 6 * np.pi) + 35 * np.exp(-((t - lh_peak) ** 2) / 0.5)
  if lh_peak == 0:
     fsh += 35 * np.exp(-((t - days) ** 2) / 0.5)
     
  # Progesterona (P4)
  metaestro_phase = next(p for p in data["phases"] if p["name"] == "Metaestro")
  diestro_phase = next(p for p in data["phases"] if p["name"] == "Diestro")
  m_start, m_end = metaestro_phase["range"]
  d_start, d_end = diestro_phase["range"]
  
  # Sigmoide de crecimiento (durante el Metaestro)
  rise_center = m_start + (m_end - m_start) * 0.4
  p4_rise = 90 / (1 + np.exp(-5.0 * (t - rise_center)))
  
  # Sigmoide de caída (al final del Diestro por PGF2a)
  fall_center = d_end
  p4_fall = 1 - (1 / (1 + np.exp(-3.0 * (t - fall_center))))
  
  # Por defecto, P4 cae al final (Ciclo Vacío)
  p4 = 5 + p4_rise * p4_fall
  
  # Factor Luteolítico y Señal Materna Dinámica
  pgf2a_peak_day = d_end
  pgf2a = 5 + 90 * np.exp(-((t - pgf2a_peak_day) ** 2) / 0.8)
  
  senal_materna = np.full_like(t, 0.0)
  
  if pregnancy:
    senal_start = d_end - 3
    senal_materna = 100 / (1 + np.exp(-3.0 * (t - senal_start)))
    pgf2a = np.full_like(t, 0.0) # Señal embrionaria bloquea/desvía PGF2a
    p4 = 5 + p4_rise # P4 se mantiene en el tope sin la curva de caída
  
  # Complicaciones (Modificadores Fisiopatológicos)
  if complication == "Balance Energético Negativo (BEN)":
    lh = np.full_like(t, 5.0)
    fsh = 10 + 5 * np.sin(t / days * 6 * np.pi)
    e2 = np.full_like(t, 5.0)
    p4 = np.full_like(t, 5.0)
    pgf2a = np.full_like(t, 0.0)
  elif complication == "Cuerpo Lúteo Persistente":
    p4 = 5 + p4_rise # Se mantiene alta sin caer, idéntico a Gestación
    lh = np.full_like(t, 5.0)
    fsh = 15 + 5 * np.sin(t / days * 6 * np.pi)
    e2 = np.full_like(t, 10.0)
    pgf2a = np.full_like(t, 0.0) # Falla uterina en liberar PGF2a
  elif complication == "Estrés Calórico":
    e2 = e2 * 0.4 + 2
    lh = lh * 0.3 + 5
    fsh = fsh * 0.8
  
  return pd.DataFrame({
    "Día": t,
    "LH": np.clip(lh, 0, 100),
    "FSH": np.clip(fsh, 0, 100),
    "Estradiol (E2)": np.clip(e2, 0, 100),
    "Progesterona (P4)": np.clip(p4, 0, 100),
    "PGF2α": np.clip(pgf2a, 0, 100),
    "Señal Materna": np.clip(senal_materna, 0, 100)
  })

def get_current_phase(day, phases):
  for p in phases:
    if p["range"][0] <= day < p["range"][1]:
      return p
  return phases[-1]

def get_hud_diagnosis(day, phase_name, complication, pregnancy=False, species="Bovino"):
  # ========== RAMA EXCLUSIVA PARA AVE ==========
  if species == "Ave":
    unit_label = f"Hora {day:.1f}"
    # Patologías aviares
    if complication == "Estrés por Calor":
      return f"{unit_label} - Estrés por Calor: Supresión de GnRH, caída del pico de LH. Postura reducida un 15-30%. Calidad de cáscara comprometida.", "error"
    elif complication == "Fotoperíodo Inadecuado (<14h luz)":
      return f"{unit_label} - Fotoperíodo Inadecuado: Melatonina elevada suprime eje HHG. Cese de postura. Jerarquía folicular F1-F5 detenida.", "error"
    elif complication == "Agotamiento Ovárico / Muda":
      return f"{unit_label} - Agotamiento Ovárico / Muda: Detención total de la jerarquía folicular. Fase de reposo reproductivo forzado.", "error"
    # Fases normales del ciclo ovulatorio
    if phase_name == "Post-oviposición":
      return f"{unit_label} - Normal: Oviposición del huevo anterior completada. Señal neuroendocrina inicia nuevo ciclo ovulatorio.", "info"
    elif phase_name == "Pico LH / Ovulación":
      return f"{unit_label} - Normal: Pico preovulatorio de LH activo. Ovulación del folículo F1 y captura por el infundíbulo.", "success"
    elif phase_name == "Formación del huevo":
      return f"{unit_label} - Normal: Tránsito oviductal — magnum (albúmina), istmo (membranas) y útero (cáscara). Calcificación en curso.", "info"
    elif phase_name == "Oviposición":
      return f"{unit_label} - Normal: Oviposición inminente. Contracciones del útero para expulsión del huevo.", "success"
    return f"{unit_label} - Ciclo ovulatorio aviar en curso.", "info"

  # ========== LÓGICA ORIGINAL PARA MAMÍFEROS ==========
  if pregnancy:
    if species in ["Bovino", "Ovino", "Caprino"]:
      return f"Día {day:.1f} - GESTACIÓN ACTIVA: Reconocimiento materno (IFN-τ) exitoso. PGF2α bloqueada, CL mantenido.", "success"
    elif species == "Porcino":
      return f"Día {day:.1f} - GESTACIÓN ACTIVA: Estrógenos embrionarios desvían PGF2α a luz uterina. Luteólisis evitada, CL mantenido.", "success"
    elif species == "Equino":
      return f"Día {day:.1f} - GESTACIÓN ACTIVA: Movilidad del concepto frena liberación de PGF2α. CL mantenido.", "success"
  if complication == "Balance Energético Negativo (BEN)":
    return f"Día {day:.1f} - BEN: Alerta de anestro por déficit energético. Eje HHG apagado, ovarios inactivos.", "error"
  elif complication == "Cuerpo Lúteo Persistente":
    return f"Día {day:.1f} - CL Persistente: Bloqueo en fase lútea. Falla en la liberación uterina de PGF2α.", "error"
  elif complication == "Estrés Calórico":
    if phase_name == "Estro":
      return f"Día {day:.1f} - Estrés Calórico: Celo Silencioso detectado. Pico de E2 deprimido, alta probabilidad de celos perdidos.", "warning"
    else:
      return f"Día {day:.1f} - Estrés Calórico: Calidad ovocitaria y desarrollo folicular comprometidos.", "warning"
      
  if phase_name == "Estro":
    return f"Día {day:.1f} - Normal (Estro): Fase de estro activa. Máxima receptividad sexual. Verificar ventana óptima de IA.", "success"
  elif phase_name == "Proestro":
    return f"Día {day:.1f} - Normal (Proestro): Crecimiento folicular rápido. Incremento de E2 acercándose al umbral crítico.", "info"
  elif phase_name == "Metaestro":
    return f"Día {day:.1f} - Normal (Metaestro): Luteinización en curso. Inicio de producción de Progesterona (P4).", "info"
  elif phase_name == "Diestro":
    return f"Día {day:.1f} - Normal (Diestro): Dominancia de P4 máxima. Útero preparado para posible gestación.", "info"

# --- GESTIÓN DE ESTADOS (FLUJO DE PANTALLAS) ---

def renderizar_simulador():

  # Callbacks para la navegacion interna (sin HTTP reload)
  def _ir_fases():
    st.session_state.seccion_activa = "Fases del Ciclo Estral"
  def _ir_checklist():
    st.session_state.seccion_activa = "Checklist de Celo e IA"
  def _ir_simulador():
    st.session_state.seccion_activa = "Laboratorio de Simulacion"

  # CSS para los botones de navegacion
  btn_css = """
  <style>
  /* Estilo base para botones de navegacion de seccion */
  .nav-btn-container button {
    width: 100% !important;
    padding: 14px 20px !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    border-radius: 10px !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.25s ease-in-out !important;
    margin-bottom: 8px !important;
  }
  /* Resaltar botón activo */
  div[data-testid="stVerticalBlock"] button[kind="secondary"] {
    opacity: 0.65;
  }
  </style>
  """
  st.markdown(btn_css, unsafe_allow_html=True)

  # --- INTERFAZ DE USUARIO (CABECERA) ---
  st.markdown("<br>", unsafe_allow_html=True)
  col_nav1, col_nav2 = st.columns([1.5, 1])

  with col_nav1:
    st.markdown('<h1 class="title-gradient" style="font-size: 3rem !important; text-align: left;">CICLO ESTRAL</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-elegant" style="text-align: left; margin-bottom: 20px !important; font-size: 1rem !important;">Fisiología Reproductiva Comparada</p>', unsafe_allow_html=True)

  with col_nav2:
    act_sec = st.session_state.seccion_activa

    # ==========================================
    # MAGIA CSS PARA LOS BOTONES DE NAVEGACIÓN
    # ==========================================
    # Determinamos qué botón está activo
    es_fases = (act_sec == "Fases del Ciclo Estral")
    es_check = (act_sec == "Checklist de Celo e IA")
    es_simul = (act_sec == "Laboratorio de Simulacion")
    
    css_magico = f"""
    <style>
    /* ========================================================
       ESTILO PARA BOTONES INACTIVOS EN LA COLUMNA DE NAVEGACIÓN
       ======================================================== */
    /* Cubrimos todas las versiones de Streamlit (column y stColumn) */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button[kind="secondary"],
    div[data-testid="stColumn"]:nth-of-type(2) div.stButton > button[kind="secondary"] {{
        background: linear-gradient(145deg, rgba(20,20,25,0.8) 0%, rgba(30,30,40,0.9) 100%) !important;
        border: 1px solid rgba(var(--color-rgb), 0.3) !important;
        border-left: 6px solid rgba(var(--color-rgb), 0.5) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
        opacity: 0.7 !important;
        transform: scale(0.98) !important;
    }}
    
    div[data-testid="column"]:nth-of-type(2) div.stButton > button[kind="secondary"]:hover,
    div[data-testid="stColumn"]:nth-of-type(2) div.stButton > button[kind="secondary"]:hover {{
        opacity: 0.9 !important;
        transform: scale(1) translateX(5px) !important;
        border-left: 6px solid var(--color-hex) !important;
        box-shadow: 0 8px 20px rgba(var(--color-rgb), 0.4) !important;
        background: linear-gradient(145deg, rgba(30,30,35,0.9) 0%, rgba(var(--color-rgb), 0.2) 100%) !important;
    }}

    /* ========================================================
       EL BOTÓN ACTIVO (MAGIA PURA) -> TARGETEADO VÍA kind="primary"
       ======================================================== */
    @keyframes pulseMagico {{
        0% {{ box-shadow: 0 0 0 0 rgba(var(--color-rgb), 0.7); }}
        70% {{ box-shadow: 0 0 0 15px rgba(var(--color-rgb), 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(var(--color-rgb), 0); }}
    }}
    
    /* El único botón primario será el que esté activo! */
    div.stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, var(--color-hex) 0%, rgba(var(--color-rgb), 0.7) 100%) !important;
        border: 2px solid #FFFFFF !important;
        border-left: 10px solid #FFFFFF !important;
        border-radius: 12px !important;
        padding: 20px !important;
        opacity: 1 !important;
        transform: scale(1.03) !important;
        box-shadow: 0 15px 35px rgba(var(--color-rgb), 0.8) !important;
        animation: pulseMagico 2.5s infinite !important;
        z-index: 10 !important;
    }}
    
    div.stButton > button[kind="primary"] p {{
        color: var(--color-text-contrast) !important;
        font-weight: 900 !important;
        text-shadow: none !important;
        letter-spacing: 2.5px !important;
    }}
    
    /* Forzar textos para inactivos */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button[kind="secondary"] p,
    div[data-testid="stColumn"]:nth-of-type(2) div.stButton > button[kind="secondary"] p {{
        color: #FFFFFF !important;
        font-weight: 900 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
    }}
    </style>
    """
    st.markdown(css_magico, unsafe_allow_html=True)

    if st.button("FASES DEL CICLO ESTRAL", key="btn_nav_fases", type="primary" if es_fases else "secondary", on_click=_ir_fases, use_container_width=True):
      pass

    if st.button("CHECKLIST DE CELO E IA", key="btn_nav_checklist", type="primary" if es_check else "secondary", on_click=_ir_checklist, use_container_width=True):
      pass

    if st.button("LABORATORIO DE SIMULACION", key="btn_nav_simul", type="primary" if es_simul else "secondary", on_click=_ir_simulador, use_container_width=True):
      pass

  # --- PARAMETROS FISIOLOGICOS — lectura directa desde session_state ---
  # La especie es establecida por st_clickable_images en la pantalla de
  # seleccion y persiste en st.session_state.especie_seleccionada.
  # Este bloque NO solicita al usuario que elija especie nuevamente.

  # Fallback de seguridad: si session_state llegara vacio por recarga directa
  _especies_validas = ["Bovino", "Porcino", "Ovino", "Caprino", "Equino", "Ave"]
  if st.session_state.especie_seleccionada not in _especies_validas:
    st.session_state.especie_seleccionada = "Bovino"

  species = st.session_state.especie_seleccionada
  aplicar_tema_dinamico(species)
  data = SPECIES_DATA[species]

  # Tarjetas de parametros en tres columnas responsivas (se apilan en movil)
  with st.expander("Parametros Fisiologicos — " + species, expanded=False):
    pf_col1, pf_col2, pf_col3 = st.columns(3)

    with pf_col1:
      st.markdown(f"""
      <div style='background: rgba(76,175,80,0.08); border-left: 3px solid #4CAF50;
                  padding: 14px 16px; border-radius: 0 10px 10px 0;'>
        <p style='margin:0 0 4px 0; font-size:0.75rem; color:#90A4AE;
                  text-transform:uppercase; letter-spacing:1px; font-weight:600;'>
          Duracion del Ciclo
        </p>
        <p style='margin:0; font-size:1.25rem; font-weight:800; color:#4CAF50;'>
          {data['cycle_duration']} dias
        </p>
      </div>
      """, unsafe_allow_html=True)

    with pf_col2:
      st.markdown(f"""
      <div style='background: rgba(0,188,212,0.08); border-left: 3px solid #00BCD4;
                  padding: 14px 16px; border-radius: 0 10px 10px 0;'>
        <p style='margin:0 0 4px 0; font-size:0.75rem; color:#90A4AE;
                  text-transform:uppercase; letter-spacing:1px; font-weight:600;'>
          Momento de Ovulacion
        </p>
        <p style='margin:0; font-size:0.95rem; font-weight:600; color:#E8F5E9;
                  line-height:1.4;'>
          {data['ovulation_timing']}
        </p>
      </div>
      """, unsafe_allow_html=True)

    with pf_col3:
      rec_mat = data['maternal_recognition']
      color_rec = "#FF9933" if rec_mat and rec_mat != "?" else "#546E7A"
      texto_rec = rec_mat if rec_mat and rec_mat != "?" else "No determinado"
      st.markdown(f"""
      <div style='background: rgba(255,153,51,0.08); border-left: 3px solid {color_rec};
                  padding: 14px 16px; border-radius: 0 10px 10px 0;'>
        <p style='margin:0 0 4px 0; font-size:0.75rem; color:#90A4AE;
                  text-transform:uppercase; letter-spacing:1px; font-weight:600;'>
          Reconocimiento Materno
        </p>
        <p style='margin:0; font-size:1.05rem; font-weight:700; color:{color_rec};'>
          {texto_rec}
        </p>
      </div>
      """, unsafe_allow_html=True)

  st.markdown("<br>", unsafe_allow_html=True)

  
  # --- SECCIÓN 1: FASES DEL CICLO DINÁMICAS ---
  if st.session_state.seccion_activa == "Fases del Ciclo Estral":
    st.markdown(f"""
    <style>
      .section-header-jump {{
          background: linear-gradient(135deg, rgba(var(--color-rgb), 0.15) 0%, rgba(26,28,35,0.95) 100%);
          border-left: 8px solid var(--color-hex);
          border-radius: 12px;
          padding: 25px 30px;
          box-shadow: 0 4px 15px rgba(0,0,0,0.4);
          transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
          margin-bottom: 25px;
          position: relative;
          overflow: hidden;
      }}
      .section-header-jump::before {{
          content: ""; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
          background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
          transform: skewX(-20deg); transition: all 0.7s ease;
      }}
      .section-header-jump:hover::before {{
          left: 200%;
      }}
      .section-header-jump:hover {{
          transform: translateY(-8px) scale(1.01);
          box-shadow: 0 15px 35px rgba(var(--color-rgb), 0.5);
          border-left-color: #FFF;
      }}
      .section-header-jump h3 {{
          margin-top: 0; color: var(--color-hex); font-weight: 900; 
          font-size: 1.8rem; text-transform: uppercase; letter-spacing: 1.5px;
          text-shadow: 0 2px 10px rgba(var(--color-rgb), 0.4);
          margin-bottom: 8px;
      }}
      .section-header-jump p {{
          margin-bottom: 0; color: #E0E4E8; font-size: 1.15rem; font-weight: 500;
          line-height: 1.5;
      }}
      .section-header-jump p b {{
          color: #FFF; background-color: var(--color-hex); padding: 2px 8px; 
          border-radius: 4px; font-weight: 900; text-transform: uppercase;
      }}
    </style>
    <div class='section-header-jump animate-fade-in'>
      <h3>⏱️ Línea de Tiempo Fisiológica: {species}</h3>
      <p>Dinámica hormonal y biológica ajustada específicamente para el modelo <b>{species}</b>.</p>
    </div>
    """, unsafe_allow_html=True)
  
    # Base de datos interactiva para la Línea de Tiempo (movida a nivel de módulo por rendimiento)
    sd = TIMELINE_DATA[species]

    # Headers dinámicos: mamíferos usan nombres estral, Ave usa nombres ovulatorios
    if species == "Ave":
      phase_headers = [
        ("Post-oviposición", "#FF9933", "🟠"),
        ("Pico LH / Ovulación", "#FF3366", "🔴"),
        ("Formación del Huevo", "#3399FF", "🔵"),
        ("Oviposición", "#00CC99", "🟢")
      ]
    else:
      phase_headers = [
        ("Proestro", "#FF3366", "🔴"),
        ("Estro", "#4CAF50", "🟢"),
        ("Metaestro", "#F8961E", "🟡"),
        ("Diestro", "#00CC99", "🟢")
      ]

    phase_keys = ["proestro", "estro", "metaestro", "diestro"]
    glass_styles = ["glass-red", "glass-cyan", "glass-orange", "glass-emerald"]
    bg_colors = ["rgba(255, 51, 102, 0.05)", "rgba(0, 242, 254, 0.05)", "rgba(248, 150, 30, 0.05)", "rgba(82, 183, 136, 0.05)"]
    border_rgbas = ["rgba(255,51,102,0.2)", "rgba(0,242,254,0.2)", "rgba(248,150,30,0.2)", "rgba(0,204,153,0.2)"]
  
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(4)
  
    for i, col in enumerate(cols):
      with col:
        h_name, h_color, h_icon = phase_headers[i]
        key = phase_keys[i]
        st.markdown(f"""
        <div class="ui-encuadre encuadre-{key} animate-fade-in" style="height: 100%;">
          <h3 style="color: {h_color}; margin-top:0; border-bottom: 1px solid {border_rgbas[i]}; padding-bottom: 10px;">{h_icon} {h_name}</h3>
          <p style="font-size: 0.85rem; color:#A0AAB5; margin-top: 10px;"><i>️ {sd[key]['dur']}</i></p>
          <p class="text-heavy text-neon-orange" style="font-size: 1.2rem !important; margin-bottom: 5px;">{sd[key]['icon']} {sd[key]['title']}</p>
          <p class="text-heavy" style="font-weight: 500 !important; font-size: 1.1rem !important;">{sd[key]['text']}</p>
        </div>
        """, unsafe_allow_html=True)

  
  # --- SECCIÓN 2: CALCULADORA DE DIAGNÓSTICO E IA ---
  if st.session_state.seccion_activa == "Checklist de Celo e IA":
    st.markdown("""
    <div class='section-header-jump animate-fade-in'>
      <h3>🩺 Calculadora Diagnóstica y Decisiones Clínicas</h3>
      <p>Evaluación interactiva del paciente y análisis de impacto <b>Económico en Finca</b>.</p>
    </div>
    """, unsafe_allow_html=True)
  
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.2, 1])
  
    with c1:
      with st.container(border=False):
        score_label = "Score de Postura" if species == "Ave" else "Score de Celo"
        st.markdown(f"""
        <div class='tinted-card' style='padding: 15px 20px !important;'>
          <h4 class='gradient-title' style='margin:0; font-size: 1.3rem;'>📋 {score_label} ({species})</h4>
        </div>
        """, unsafe_allow_html=True)
        score = 0
      
        # El primer signo de la lista siempre lo consideramos el Primario (100 pts)
        for i, signo in enumerate(data["checklist"]):
          temp_k = f"temp_chk_{species}_{i}"
          real_k = f"chk_{species}_{i}"
          if temp_k not in st.session_state:
            st.session_state[temp_k] = st.session_state.get(real_k, False)
          st.checkbox(signo, key=temp_k, on_change=sync_state, args=(temp_k, real_k))
          is_checked = st.session_state.get(real_k, False)
          if is_checked:
            if i == 0:
              score += 100
            else:
              score += 25
      
        st.markdown("---")
        if species == "Ave":
          if score >= 100:
            st.success(" **¡POSTURA ÓPTIMA CONFIRMADA!** Programa de luz 16L:8O activo. Jerarquía folicular F1-F5 funcional.")
          elif score > 0 and score < 75:
            st.warning("️ **ALERTA DE POSTURA.** Revisar fotoperíodo, consumo de alimento y calidad de cáscara.")
          elif score >= 75 and score < 100:
            st.warning("️ **POSTURA PROBABLE.** Verificar continuidad de la serie de postura y estado de la jerarquía folicular.")
          else:
            st.markdown("<div style='padding:1rem; background:rgba(22,27,34,0.6); border-radius:12px; border:1px solid rgba(255,255,255,0.1); color:#8B949E;'>ℹ️ Marque los indicadores de postura observados para generar el diagnóstico reproductivo automático.</div>", unsafe_allow_html=True)
        else:
          if score >= 100:
            st.success(" **¡CELO CONFIRMADÍSIMO!** Proceder al protocolo de Inseminación Artificial o Monta Dirigida.")
          elif score > 0 and score < 75:
            st.warning("️ **SOSPECHA DE CELO (ESTRO INCOMPLETO).** No inseminar aún; se recomienda monitorear activamente.")
          elif score >= 75 and score < 100:
            st.warning("️ **ALTA PROBABILIDAD DE CELO.** Signos secundarios evidentes. Observar de cerca para conformación primaria.")
          else:
            st.markdown("<div style='padding:1rem; background:rgba(22,27,34,0.6); border-radius:12px; border:1px solid rgba(255,255,255,0.1); color:#8B949E;'>ℹ️ Marque los signos clínicos observados en el hato para generar el diagnóstico reproductivo automático.</div>", unsafe_allow_html=True)
  
    with c2:
      with st.container(border=False):
        ia_label = "Manejo Reproductivo" if species == "Ave" else "Decisiones de IA"
        st.markdown(f"""
        <div class='tinted-card' style='padding: 15px 20px !important;'>
          <h4 class='gradient-title' style='margin:0; font-size: 1.3rem;'>🎯 {ia_label} ({species})</h4>
        </div>
        """, unsafe_allow_html=True)
      
        if species == "Bovino":
          st.markdown("**Simulador Interactivo de Regla AM/PM:**")
          if "temp_hora_celo_radio" not in st.session_state:
            st.session_state.temp_hora_celo_radio = st.session_state.get("hora_celo_radio", "Celo Detectado en la Mañana (AM - ej. 07:00 AM)")
          st.radio(
            "¿A qué hora del día detectó el inicio del celo activo?",
            ["Celo Detectado en la Mañana (AM - ej. 07:00 AM)", "Celo Detectado en la Tarde/Noche (PM - ej. 05:00 PM)"],
            key="temp_hora_celo_radio",
            on_change=sync_state,
            args=("temp_hora_celo_radio", "hora_celo_radio")
          )
          hora_celo = st.session_state.get("hora_celo_radio", "Celo Detectado en la Mañana (AM - ej. 07:00 AM)")
          st.markdown("<br>", unsafe_allow_html=True)
          if "AM" in hora_celo:
            st.markdown(f"""
            <div class="tinted-card">
                <div class="agro-badge">REGLA AM/PM</div>
                <h3 class="gradient-title">🎯 Ventana Óptima de IA</h3>
                <p style="font-size: 1.1rem; color: #E0E0E0; line-height: 1.6;">
                    Inseminar hoy por la tarde (estimado 3:00 PM - 5:00 PM).<br>
                    <strong>Ovulación estimada:</strong> 7:00 PM (12 horas post-celo).
                </p>
            </div>
            """, unsafe_allow_html=True)
          else:
            st.markdown(f"""
            <div class="tinted-card">
                <div class="agro-badge">REGLA AM/PM</div>
                <h3 class="gradient-title">🎯 Ventana Óptima de IA</h3>
                <p style="font-size: 1.1rem; color: #E0E0E0; line-height: 1.6;">
                    Inseminar mañana por la mañana a primera hora (estimado 7:00 AM).<br>
                    <strong>Ovulación estimada:</strong> 5:00 AM del día siguiente.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
          for regla in data["ia_window"]:
            st.markdown(f"- {regla}")
          
      with st.container(border=False):
        st.markdown("""
        <div class='tinted-card' style='padding: 15px 20px !important;'>
          <h4 class='gradient-title' style='margin:0; font-size: 1.3rem;'>💰 Retorno de Inversión (ROI)</h4>
        </div>
        """, unsafe_allow_html=True)

        # Diccionario de ROI dinámico por especie
        ROI_DATA = {
          "Bovino": {
            "select_label": "Estrategia de Detección de Celo en Finca:",
            "opciones": ["Observación Visual Tradicional (~40% de éxito)", "Collares de Precisión o Monitoreo Automatizado (~90% de éxito)"],
            "obs_msg": " **Pérdida anual silenciosa de $150-200 USD por vaca.** El 60-70% de las montas de celo ocurren de noche cuando no hay personal vigilando.",
            "tech_msg": " **Sincronización de datos en tiempo real.** ROI tecnológico estimado en menos de 6 meses al reducir días abiertos."
          },
          "Porcino": {
            "select_label": "Estrategia de Detección de Celo en Granja Porcina:",
            "opciones": ["Observación Visual sin Verraco (~50% de éxito)", "Detección con Verraco Marcador + Sensores (~90% de éxito)"],
            "obs_msg": " **Pérdida por retraso post-destete: $50-80 USD por cerda/ciclo.** Sin verraco marcador, el reflejo de inmovilidad es difícil de confirmar.",
            "tech_msg": " **Detección automatizada con sensores + IATF post-destete.** ROI en 2-3 ciclos productivos al sincronizar lotes completos."
          },
          "Ovino": {
            "select_label": "Estrategia Reproductiva en Rebaño Ovino:",
            "opciones": ["Detección Visual sin Macho Marcador (~30% de éxito)", "Efecto Macho + Implantes de Melatonina (~80% de éxito)"],
            "obs_msg": " **Celos discretos, TDC <30% sin machos marcadores.** Pérdida estimada: $30-50 USD por oveja/temporada reproductiva.",
            "tech_msg": " **Efecto macho + implantes de melatonina (Melovine).** Recuperación de inversión en 1 temporada reproductiva."
          },
          "Caprino": {
            "select_label": "Estrategia Reproductiva en Hato Caprino:",
            "opciones": ["Detección Visual sin Macho Marcador (~35% de éxito)", "Efecto Macho Programado + Esponjas/CIDR (~85% de éxito)"],
            "obs_msg": " **TDC <35% sin efecto macho.** Pérdida estimada: $25-45 USD por cabra/temporada por celos no detectados.",
            "tech_msg": " **Efecto macho programado + esponjas/CIDR.** ROI en la primera temporada reproductiva del hato."
          },
          "Equino": {
            "select_label": "Estrategia Reproductiva en Manejo Equino:",
            "opciones": ["Observación Conductual sin Ecografía (~45% de éxito)", "Ecografía Folicular Seriada + IA Dirigida (~90% de éxito)"],
            "obs_msg": " **Estro prolongado (4-7 días) dificulta el timing de IA.** Pérdida estimada: $200-500 USD por ciclo fallido en la hembra equina.",
            "tech_msg": " **Ecografía folicular seriada + IA durante el estro.** ROI en 1-2 ciclos reproductivos al optimizar el momento de inseminación."
          },
          "Ave": {
            "select_label": "Estrategia de Manejo de Postura en Lote Avícola:",
            "opciones": ["Fotoperíodo Natural sin Control (~60% postura)", "Programa de Luz 16L:8O Automatizado (~85-90% postura)"],
            "obs_msg": " **Fotoperíodo inadecuado → caída del 15-30% en postura.** Pérdida estimada: $0.10-0.15 USD por ave/día en huevos no producidos.",
            "tech_msg": " **Programa 16L:8O con temporizador automatizado.** ROI en 30-60 días por lote al maximizar la jerarquía folicular activa."
          }
        }

        roi = ROI_DATA.get(species, ROI_DATA["Bovino"])
        if "temp_estrategia_deteccion_select" not in st.session_state:
          st.session_state.temp_estrategia_deteccion_select = st.session_state.get("estrategia_deteccion_select", roi["opciones"][0])
        # Reset si la opción actual no pertenece a la especie actual
        if st.session_state.temp_estrategia_deteccion_select not in roi["opciones"]:
          st.session_state.temp_estrategia_deteccion_select = roi["opciones"][0]
          st.session_state.estrategia_deteccion_select = roi["opciones"][0]
        st.selectbox(roi["select_label"], roi["opciones"], key="temp_estrategia_deteccion_select", on_change=sync_state, args=("temp_estrategia_deteccion_select", "estrategia_deteccion_select"))
        tech = st.session_state.get("estrategia_deteccion_select", roi["opciones"][0])
      
        if tech == roi["opciones"][0]:
          obs_text = roi["obs_msg"].replace("**", "")
          parts = obs_text.split(". ", 1)
          alert_part = parts[0] + "." if len(parts) > 1 else obs_text
          text_part = parts[1] if len(parts) > 1 else ""
          st.markdown(f"""
          <div class="tinted-card">
              <span class="agro-badge" style="background-color: #FF3366 !important; color: white !important;">ALERTA ECONÓMICA</span>
              <h2 class="gradient-title">⚠️ {alert_part}</h2>
              <p style="font-size: 1rem; color: #B0B3B8;">
                  {text_part}
              </p>
          </div>
          """, unsafe_allow_html=True)
        else:
          tech_text = roi["tech_msg"].replace("**", "")
          parts = tech_text.split(". ", 1)
          alert_part = parts[0] + "." if len(parts) > 1 else tech_text
          text_part = parts[1] if len(parts) > 1 else ""
          st.markdown(f"""
          <div class="tinted-card">
              <span class="agro-badge">ROI POSITIVO</span>
              <h2 class="gradient-title">🚀 {alert_part}</h2>
              <p style="font-size: 1rem; color: #B0B3B8;">
                  {text_part}
              </p>
          </div>
          """, unsafe_allow_html=True)
  
  # --- SECCIÓN 3: LABORATORIO DE SIMULACIÓN Y COMPLICACIONES ---
  if st.session_state.seccion_activa == "Laboratorio de Simulacion":
  
    # 1. Modificadores de Salud Condicionales
    st.markdown("""
    <div class='section-header-jump animate-fade-in'>
      <h3>🧬 Modificadores de Salud y Estado de Gestación</h3>
      <p>Configura las variables patológicas para simular el <b>Comportamiento Endocrino</b>.</p>
    </div>
    """, unsafe_allow_html=True)
  
    # Inicializar session_state si no existe
    if 'escenario_radio' not in st.session_state:
      st.session_state.escenario_radio = "Ciclo Vacío (Sin Embrión - Actúa PGF2α)"
    if 'patologia_radio' not in st.session_state:
      st.session_state.patologia_radio = "Normal"
  
    # Definir opciones base para patología (condicional por especie)
    if species == "Ave":
      opciones_clinicas = ["Normal", "Estrés por Calor", "Fotoperíodo Inadecuado (<14h luz)", "Agotamiento Ovárico / Muda"]
    else:
      opciones_clinicas = ["Normal", "Balance Energético Negativo (BEN)", "Estrés Calórico"]
      if species in ["Bovino", "Caprino", "Equino"]:
        opciones_clinicas.insert(2, "Cuerpo Lúteo Persistente")
  
    # Regla: Si "Gestación Activa" está seleccionada, bloquear BEN y CL Persistente (solo mamíferos)
    if species != "Ave" and st.session_state.escenario_radio == "Gestación Activa (Con Embrión - Reconocimiento Materno)":
      opciones_clinicas = [op for op in opciones_clinicas if op not in ["Balance Energético Negativo (BEN)", "Cuerpo Lúteo Persistente"]]
  
    # Si la patología actual ya no es válida por el filtro, resetear a Normal
    if st.session_state.patologia_radio not in opciones_clinicas:
      st.session_state.patologia_radio = "Normal"
  
    c_mod1, c_mod2 = st.columns(2)
    with c_mod1:
      if "temp_patologia_radio" not in st.session_state:
        st.session_state.temp_patologia_radio = st.session_state.get("patologia_radio", "Normal")
      # Forzar actualización si la opción ya no está disponible
      if st.session_state.temp_patologia_radio not in opciones_clinicas:
        st.session_state.temp_patologia_radio = "Normal"
      
      st.radio(
        "Seleccione Patología:",
        opciones_clinicas,
        horizontal=True,
        key='temp_patologia_radio',
        on_change=sync_state,
        args=("temp_patologia_radio", "patologia_radio")
      )
      complication = st.session_state.get("patologia_radio", "Normal")
    
    # Regla: Si "BEN" o "CL Persistente", forzar Ciclo Vacío y deshabilitar Escenario
    patologias_bloqueantes = ["Balance Energético Negativo (BEN)", "Cuerpo Lúteo Persistente"]
    deshabilitar_gestacion = complication in patologias_bloqueantes or species == "Ave"
  
    if deshabilitar_gestacion:
      # Forzar estado sin gestación
      st.session_state.escenario_radio = "Ciclo Vacío (Sin Embrión - Actúa PGF2α)"
  
    with c_mod2:
      if species == "Ave":
        st.markdown("**Escenario Reproductivo:**")
        st.info("ℹ️ **Nota:** La gallina no tiene gestación uterina. El ciclo ovulatorio es continuo bajo fotoperíodo adecuado.")
        pregnancy = False
      else:
        st.markdown("**Escenario Reproductivo:**")
        if "temp_escenario_radio" not in st.session_state:
          st.session_state.temp_escenario_radio = st.session_state.get("escenario_radio", "Ciclo Vacío (Sin Embrión - Actúa PGF2α)")
        st.radio(
          "Seleccione Escenario:",
          ["Ciclo Vacío (Sin Embrión - Actúa PGF2α)", "Gestación Activa (Con Embrión - Reconocimiento Materno)"],
          label_visibility="collapsed",
          key='temp_escenario_radio',
          on_change=sync_state,
          args=("temp_escenario_radio", "escenario_radio"),
          disabled=deshabilitar_gestacion
        )
        escenario = st.session_state.get("escenario_radio", "Ciclo Vacío (Sin Embrión - Actúa PGF2α)")
        pregnancy = "Gestación" in escenario
    
        if deshabilitar_gestacion:
          st.info("ℹ️ **Nota:** Gestación deshabilitada para esta patología.")
      
    # Caso Especial: Estrés Calórico + Gestación Activa (solo mamíferos)
    if species != "Ave" and complication == "Estrés Calórico" and pregnancy:
      st.error("**️ Alerta de Impacto Económico (Mortalidad Embrionaria Temprana):** El estrés por calor severo en zonas tropicales incrementa la temperatura uterina, deprime la viabilidad del embrión y bloquea su señal de reconocimiento antes del día 15. Esto genera una reabsorción embrionaria silenciosa, provocando el retorno de la hembra al celo. Pérdidas directas de $3.00 USD por día abierto adicional por animal.")
      
    # Mensaje informativo si se omite CL Persistente (solo mamíferos no-bovinos relevantes)
    if species in ["Porcino", "Ovino"]:
      st.info(f"ℹ️ **Nota Clínica:** El 'Cuerpo Lúteo Persistente' no es una patología comúnmente diagnosticada ni representativa en {species.lower()}s. Ha sido deshabilitada para esta especie.")
    
    # ========== PANELES AGROPECUARIOS DINÁMICOS DE PATOLOGÍAS ==========
    if species == "Ave":
      # --- Paneles exclusivos para Ave ---
      if complication == "Normal":
        with st.expander(" Diagnóstico Productivo - Postura Normal", expanded=True):
          st.info("** Diagnóstico Técnico:** Ciclo ovulatorio fisiológico óptimo. Jerarquía folicular F1-F5 activa.")
          st.markdown("""
          <div class='texto-lectura-grande'>
            <ul>
              <li class='item-lista-grande'><b>Métricas de Control:</b> Tasa de postura objetivo: 85-90%. Programa de luz 16L:8O estable. Serie de postura: 5-7 huevos consecutivos + 1 día de pausa.</li>
              <li class='item-lista-grande'><b>Acción Zootécnica:</b> Mantener fotoperíodo constante (16L:8O). Monitorear consumo de calcio para calcificación de cáscara. Registrar producción diaria por lote.</li>
            </ul>
          </div>
          """, unsafe_allow_html=True)
      elif complication == "Estrés por Calor":
        with st.expander(" Diagnóstico Productivo - Estrés por Calor (Ave)", expanded=True):
          st.markdown("""
          <div class="pathology-card path-heat">
            <h4 style="color: #D4AF37; margin-top: 0px; font-size: 20px;"> Estrés por Calor en Aves</h4>
            <ul class="texto-lectura-grande">
              <li class='item-lista-grande'><b>Diagnóstico Económico:</b> Caída del 15-30% en postura diaria. Pérdida estimada de $0.10-0.15 USD por ave/día en huevos no producidos. En un lote de 1,000 aves: $100-150 USD/día.</li>
              <li class='item-lista-grande'><b>Fisiología Productiva:</b> El calor suprime la secreción de GnRH, deprime el pico preovulatorio de LH y altera la calcificación en la glándula cascarígena. Cáscaras delgadas y huevos deformes son signos frecuentes.</li>
              <li class='item-lista-grande'><b>Soluciones Técnicas de Gestión:</b> Instalar ventiladores y nebulizadores en el galpón. Suplementar electrolitos y vitamina C en el agua. Reducir la densidad de aves por metro cuadrado. Ajustar la alimentación a las horas más frescas del día.</li>
            </ul>
          </div>
          """, unsafe_allow_html=True)
      elif complication == "Fotoperíodo Inadecuado (<14h luz)":
        with st.expander(" Diagnóstico Productivo - Fotoperíodo Inadecuado (Ave)", expanded=True):
          st.markdown("""
          <div class="pathology-card path-cl">
            <h4 style="color: #BA68C8; margin-top: 0px; font-size: 20px;"> Fotoperíodo Inadecuado (&lt;14h luz)</h4>
            <ul class="texto-lectura-grande">
              <li class='item-lista-grande'><b>Diagnóstico Económico:</b> Cese parcial o total de la postura. Pérdida directa del 100% de la producción de huevos durante el período de supresión. Activación de muda de plumas forzada.</li>
              <li class='item-lista-grande'><b>Fisiología Productiva:</b> Con menos de 14 horas de luz, la melatonina se eleva y suprime el eje HHG (Hipotálamo-Hipófisis-Gónada). La jerarquía folicular F1-F5 se detiene progresivamente. La gallina entra en un estado de reposo reproductivo.</li>
              <li class='item-lista-grande'><b>Soluciones Técnicas de Gestión:</b> Implementar programa de luz artificial con temporizador automatizado (16L:8O). Verificar la intensidad lumínica ≥20 lux a nivel de comedero. Evitar cortes de luz imprevistos que rompan la continuidad del fotoperíodo.</li>
            </ul>
          </div>
          """, unsafe_allow_html=True)
      elif complication == "Agotamiento Ovárico / Muda":
        with st.expander(" Diagnóstico Productivo - Agotamiento Ovárico / Muda (Ave)", expanded=True):
          st.markdown("""
          <div class="pathology-card path-ben">
            <h4 style="color: #EF5350; margin-top: 0px; font-size: 20px;"> Agotamiento Ovárico / Muda Forzada</h4>
            <ul class="texto-lectura-grande">
              <li class='item-lista-grande'><b>Diagnóstico Económico:</b> Cese de postura durante 6-8 semanas. Pérdida total de producción en el período de muda. Sin embargo, la muda controlada puede extender la vida productiva del lote en un segundo ciclo de postura.</li>
              <li class='item-lista-grande'><b>Fisiología Productiva:</b> Tras 60-80 semanas de postura continua, la calidad de la cáscara y el tamaño del huevo decaen progresivamente. La jerarquía folicular F1-F5 se detiene completamente. El ovario entra en regresión y las plumas se renuevan.</li>
              <li class='item-lista-grande'><b>Soluciones Técnicas de Gestión:</b> Programar muda controlada al final del primer ciclo de postura (semana 72-80). Reducir el fotoperíodo a 8L:16O durante 7-10 días para inducir la regresión ovárica. Tras la muda, restablecer el programa 16L:8O para iniciar el segundo ciclo con un 80-85% de postura.</li>
            </ul>
          </div>
          """, unsafe_allow_html=True)
    else:
      # --- Paneles originales para mamíferos (sin modificar) ---
      if complication == "Normal":
        with st.expander(" Diagnóstico Económico y Gestión - Normal", expanded=True):
          st.info("** Diagnóstico Técnico:** Ciclicidad fisiológica óptima.")
          st.markdown("""
          <div class='texto-lectura-grande'>
            <ul>
              <li class='item-lista-grande'><b>Métricas de Control:</b> Intervalo entre partos proyectado en 12-13 meses. Tasa de Detección de Celo (TDC) objetivo >80%.</li>
              <li class='item-lista-grande'><b>Acción Agropecuaria:</b> Continuar con el registro zootécnico riguroso y monitoreo automatizado diario para inseminación programada.</li>
            </ul>
          </div>
          """, unsafe_allow_html=True)
      elif complication == "Balance Energético Negativo (BEN)":
        with st.expander(" Diagnóstico Económico y Gestión - BEN", expanded=True):
          st.markdown("""
          <div class="tarjeta-ben">
            <h4 style="color: #EF5350; margin-top: 0px; font-size: 20px;">️ Balance Energético Negativo (BEN)</h4>
            <ul class="texto-lectura-grande">
              <li class='item-lista-grande'><b>Diagnóstico Económico:</b> Incremento drástico de "Días Abiertos". Cada día extra por encima de los 85 días post-parto le cuesta al hato $3 USD en alimentación de mantenimiento y leche no producida. En un hato de 100 vacas, 30 días de BEN representan $9,000 USD de pérdida evitable al año.</li>
              <li class='item-lista-grande'><b>Fisiología Productiva:</b> La alta producción de leche supera el consumo de materia seca. El cerebro detecta el déficit de energía y apaga el eje reproductivo (FSH/LH) para priorizar la supervivencia y la lactancia.</li>
              <li class='item-lista-grande'><b>Soluciones Técnicas de Gestión:</b> Balancear raciones aumentando la densidad energética en el tercio inicial de lactancia (grasas sobrepasantes, carbohidratos fermentables). En cerdas lactantes, planificar el "Destete Sincronizado" del lote para agrupar el retorno al celo.</li>
            </ul>
          </div>
          """, unsafe_allow_html=True)
      elif complication == "Cuerpo Lúteo Persistente":
        with st.expander(" Diagnóstico Económico y Gestión - CL Persistente", expanded=True):
          st.markdown("""
          <div class="tarjeta-cl">
            <h4 style="color: #BA68C8; margin-top: 0px; font-size: 20px;"> Cuerpo Lúteo Persistente</h4>
            <ul class="texto-lectura-grande">
              <li class='item-lista-grande'><b>Diagnóstico Económico:</b> Provoca anestro prolongado (falsa preñez) que eleva los días abiertos y disminuye el índice de partos por año del hato.</li>
              <li class='item-lista-grande'><b>Fisiología Productiva:</b> Inflamaciones o infecciones uterinas subclínicas bloquean físicamente la liberación de prostaglandina (PGF2α). El CL se mantiene intacto y la progesterona bloquea el ciclo.</li>
              <li class='item-lista-grande'><b>Soluciones Técnicas de Gestión:</b> Reemplazar la observación visual ineficiente con protocolos de Inseminación Artificial a Tiempo Fijo (IATF, ej. Ovsynch o CIDR/DIB con progesterona) para inducir la ovulación y preñar el 100% de las hembras sincronizadas. Realizar ecografías post-parto preventivas a los 30 días.</li>
            </ul>
          </div>
          """, unsafe_allow_html=True)
      elif complication == "Estrés Calórico":
        with st.expander(" Diagnóstico Económico y Gestión - Estrés Calórico", expanded=True):
          st.markdown("""
          <div class="tarjeta-estres">
            <h4 style="color: #D4AF37; margin-top: 0px; font-size: 20px;"> Estrés Calórico</h4>
            <ul class="texto-lectura-grande">
              <li class='item-lista-grande'><b>Diagnóstico Económico:</b> Ganaderías tropicales (ej. provincia de El Oro) sufren una caída crítica en la Tasa de Detección de Celo (TDC) visual a un 30-40%, provocando pérdidas de hasta $200 USD anuales por vaca.</li>
              <li class='item-lista-grande'><b>Fisiología Productiva:</b> Las hembras suprimen el comportamiento de monta para no generar calor corporal. El 60-70% de los celos ocurren de forma nocturna en la fresca madrugada. Además, se altera drásticamente la calidad ovocitaria y la viabilidad del embrión.</li>
              <li class='item-lista-grande'><b>Soluciones Técnicas de Gestión:</b> Inversión en collares de actividad con acelerómetro 3D para registrar celos silenciosos nocturnos. Instalar infraestructura de enfriamiento activo (sombras, aspersores, ventiladores) en áreas de espera y comederos para disminuir el ITH.</li>
            </ul>
          </div>
          """, unsafe_allow_html=True)
  
    # Data generation
    df = generate_hormone_data(species, complication, pregnancy)
    max_days = data['cycle_duration']
  
    # 2. Control Slider en Streamlit
    st.markdown("---")
    st.markdown("""
    <div class='glass-card glass-cyan' style='margin-bottom:10px; padding: 15px 20px;'>
      <h3 style='margin:0; color:#4CAF50;'>️ Simulador Endocrino en Tiempo Real</h3>
    </div>
    """, unsafe_allow_html=True)
    
    sim_hash = f"{species}_{complication}_{pregnancy}"
    if "is_playing" not in st.session_state:
        st.session_state.is_playing = False
    if "current_time" not in st.session_state:
        st.session_state.current_time = 0.0
    if "sim_hash" not in st.session_state or st.session_state.sim_hash != sim_hash:
        st.session_state.current_time = 0.0
        st.session_state.sim_hash = sim_hash
        st.session_state.is_playing = False
        st.session_state.base_fig = None

    # ── JS: Preservar posición de scroll en cada fragment-rerun ──────────────
    import streamlit.components.v1 as components
    components.html("""
    <script>
    (function() {
        var KEY = 'st_sim_scroll';
        var p = window.parent;
        var saved = sessionStorage.getItem(KEY);
        if (saved !== null) { p.scrollTo(0, parseInt(saved, 10)); }
        p.addEventListener('scroll', function() {
            sessionStorage.setItem(KEY, p.scrollY);
        }, { passive: true });
    })();
    </script>
    """, height=0, scrolling=False)

    # No static plotly layout needed for Altair

    col_play, col_slider = st.columns([1.2, 4])
    with col_play:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.session_state.get('is_playing', False):
            if st.button("⏸️ Pausar", use_container_width=True):
                st.session_state.is_playing = False
                st.rerun()
        else:
            if st.button("▶️ Reproducir", use_container_width=True):
                st.session_state.is_playing = True
                st.rerun()

    with col_slider:
        slider_label = f"Desliza para avanzar {'la Hora' if species == 'Ave' else 'el Día'} del Ciclo manualmente:"
        
        # Omitting the key prevents the UI state from forcing a reset when pausing
        new_time = st.slider(
            slider_label, 
            min_value=0.0, 
            max_value=float(max_days), 
            value=float(st.session_state.get('current_time', 0.0)), 
            step=0.1
        )
        
        if not st.session_state.get('is_playing', False):
            st.session_state.current_time = new_time

    _interval = 0.066 if st.session_state.get('is_playing', False) else None



    @st.fragment(run_every=_interval)
    def renderizar_tiempo_real():
        import time
        import copy
        import numpy as np
        
        t = st.session_state.get('current_time', 0.0)
        
        if st.session_state.get('is_playing', False):
            paso = max_days / 300.0
            t = min(t + paso, max_days)
            
            if t >= max_days:
                st.session_state.is_playing = False
                st.session_state.current_time = float(max_days)
                st.rerun(scope="app")
            else:
                st.session_state.current_time = t

        idx = (df["Día"] - t).abs().idxmin()
        row = df.iloc[idx]

        c_phase = get_current_phase(row["Día"], data["phases"])
        diag_txt, diag_typ = get_hud_diagnosis(row["Día"], c_phase["name"], complication, pregnancy, species)

        if diag_typ == "success": st.success(diag_txt)
        elif diag_typ == "error": st.error(diag_txt)
        elif diag_typ == "warning": st.warning(diag_txt)
        else: st.info(diag_txt)
            
        matLabel = "🟠 PGF2α (%)"
        matKey   = "PGF2α"
        if pregnancy:
            if species == "Porcino":  matLabel = " Estrógenos Emb. (%)"
            elif species == "Equino": matLabel = " Movilidad Emb. (%)"
            else:                     matLabel = " IFN-τ (%)"
            matKey = "Señal Materna"
            
        kpi_html = f'''
        <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 20px; background: rgba(22, 27, 34, 0.6); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.08);">
            <div style="flex: 1; text-align: center; min-width: 100px;"><span style="font-size: 14px; color: #8b949e; display: block; margin-bottom: 8px;">🟣 FSH (%)</span><span style="font-size: 28px; font-weight: 800; color: #BC8BFF;">{row['FSH']:.1f}%</span></div>
            <div style="flex: 1; text-align: center; min-width: 100px;"><span style="font-size: 14px; color: #8b949e; display: block; margin-bottom: 8px;"> LH (%)</span><span style="font-size: 28px; font-weight: 800; color: #FF3366;">{row['LH']:.1f}%</span></div>
            <div style="flex: 1; text-align: center; min-width: 100px;"><span style="font-size: 14px; color: #8b949e; display: block; margin-bottom: 8px;"> E2 (%)</span><span style="font-size: 28px; font-weight: 800; color: #58A6FF;">{row['Estradiol (E2)']:.1f}%</span></div>
            <div style="flex: 1; text-align: center; min-width: 100px;"><span style="font-size: 14px; color: #8b949e; display: block; margin-bottom: 8px;">🟢 P4 (%)</span><span style="font-size: 28px; font-weight: 800; color: #00CC99;">{row['Progesterona (P4)']:.1f}%</span></div>
            <div style="flex: 1; text-align: center; min-width: 100px;"><span style="font-size: 14px; color: #8b949e; display: block; margin-bottom: 8px;">{matLabel}</span><span style="font-size: 28px; font-weight: 800; color: #FF9933;">{row[matKey]:.1f}%</span></div>
        </div>
        '''
        st.markdown(kpi_html, unsafe_allow_html=True)

        import altair as alt
        
        mask = df["Día"].values <= t
        df_plot = df[mask]
        
        # Preparar dataframe para Altair
        df_melt = df_plot.melt(id_vars=["Día"], value_vars=["FSH", "LH", "Estradiol (E2)", "Progesterona (P4)", matKey], var_name="Hormona", value_name="Concentración (%)")
        
        color_scale = alt.Scale(
            domain=["FSH", "LH", "Estradiol (E2)", "Progesterona (P4)", matKey],
            range=['#BC8BFF', '#FF3366', '#58A6FF', '#00CC99', '#FF9933']
        )
        
        dayLabel = 'HORA' if species == 'Ave' else 'DÍA'
        xAxisTitle = 'Horas del Ciclo Ovulatorio' if species == 'Ave' else 'Días del Ciclo'
        
        # Gráfico Base
        base = alt.Chart(df_melt).encode(
            x=alt.X('Día:Q', scale=alt.Scale(domain=[0, max_days]), title=xAxisTitle, axis=alt.Axis(gridColor='rgba(255,255,255,0.05)', grid=True, titleFontSize=14, labelFontSize=12)),
            y=alt.Y('Concentración (%):Q', scale=alt.Scale(domain=[0, 105]), axis=alt.Axis(gridColor='rgba(255,255,255,0.05)', grid=True, titleFontSize=14, labelFontSize=12)),
            color=alt.Color('Hormona:N', scale=color_scale, legend=alt.Legend(orient='bottom', title=None, labelFontSize=13, symbolType='circle'))
        )
        
        # Líneas de las curvas
        lines = base.mark_line(strokeWidth=3.5)
        
        # Línea de tiempo (cursor vertical)
        vline = alt.Chart(pd.DataFrame({'Día': [t]})).mark_rule(color='#FFF', strokeWidth=3).encode(x='Día:Q')
        
        # Etiqueta de texto de la línea de tiempo
        text = alt.Chart(pd.DataFrame({'x': [max_days*0.02], 'y': [100], 'text': [f"{dayLabel} {t:.1f}"]})).mark_text(
            align='left', baseline='top', color='#FFF', fontSize=20, fontStyle='bold', dy=-15
        ).encode(x='x:Q', y='y:Q', text='text:N')
        
        # Ensamblar gráfico
        final_chart = (lines + vline + text).properties(height=400, background='transparent').configure_view(strokeWidth=0)
        
        st.altair_chart(final_chart, use_container_width=True)

    # Iniciar Fragmento
    renderizar_tiempo_real()

if st.session_state.etapa_actual == "portada":
  st.markdown("<br><br><br><br>", unsafe_allow_html=True)
  st.markdown("""
  <div style="text-align: center;" class="animate-fade-in">
    <h1 class="title-gradient">CICLO ESTRAL</h1>
    <h3 class="subtitle-elegant">Fisiología Reproductiva Comparada</h3>
    <style>
    @keyframes pulseGlow {
      0% { box-shadow: 0 15px 35px rgba(0,0,0,0.5), 0 0 15px rgba(76, 175, 80, 0.1); border-top-color: #4CAF50; }
      50% { box-shadow: 0 15px 35px rgba(0,0,0,0.5), 0 0 25px rgba(76, 175, 80, 0.4); border-top-color: #4facfe; }
      100% { box-shadow: 0 15px 35px rgba(0,0,0,0.5), 0 0 15px rgba(76, 175, 80, 0.1); border-top-color: #4CAF50; }
    }
    .sazon-card {
      background: linear-gradient(145deg, rgba(22, 33, 25, 0.85) 0%, rgba(12, 22, 16, 0.95) 100%);
      padding: 45px 55px;
      border-radius: 16px;
      border: 1px solid rgba(76, 175, 80, 0.2);
      border-top: 4px solid #4CAF50;
      text-align: left;
      margin: 40px auto;
      max-width: 850px;
      backdrop-filter: blur(16px);
      position: relative;
      overflow: hidden;
      animation: pulseGlow 4s infinite alternate ease-in-out;
      transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .sazon-card:hover {
      transform: translateY(-5px);
      border: 1px solid rgba(76, 175, 80, 0.4);
      border-top: 4px solid #4facfe;
    }
    </style>
    <div class="sazon-card">
      <p style='font-size: 1.18rem; font-weight: 300; line-height: 1.7; color: #E8F5E9; margin: 0; letter-spacing: 0.4px; position: relative; z-index: 1;'>
        <b style="color: #4CAF50; font-weight: 600; text-shadow: 0 0 10px rgba(76, 175, 80, 0.2);">La monitorización precisa</b> del ciclo estral y el manejo de los parámetros endocrinos son pilares fundamentales en la ingeniería agropecuaria. La optimización de la tasa de detección de celo y la comprensión del reconocimiento materno impactan directamente en el intervalo entre partos y la rentabilidad de la unidad productiva.
      </p>
    </div>
  </div>
  """, unsafe_allow_html=True)

  col1, col2, col3 = st.columns([1, 1.2, 1])
  with col2:
    st.markdown("""
    <style>
    /* ========================================================
       BOTÓN GIGANTE INICIAR SIMULACIÓN (PRIMARY)
       ======================================================== */
    div.stButton > button[kind="primary"] {
      background: linear-gradient(135deg, #00E676 0%, #1DE9B6 100%) !important;
      color: #000000 !important;
      padding: 22px 45px !important;
      border-radius: 16px !important;
      border: 3px solid #FFFFFF !important;
      box-shadow: 0 10px 35px rgba(0, 230, 118, 0.6), inset 0 0 20px rgba(255,255,255,0.4) !important;
      transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
      animation: pulseGlowSim 2.5s infinite;
      width: 100% !important;
    }
    @keyframes pulseGlowSim {
      0% { box-shadow: 0 10px 30px rgba(0, 230, 118, 0.5); }
      50% { box-shadow: 0 15px 50px rgba(29, 233, 182, 0.9), 0 0 20px rgba(255,255,255,0.8); transform: translateY(-4px) scale(1.02); }
      100% { box-shadow: 0 10px 30px rgba(0, 230, 118, 0.5); }
    }
    div.stButton > button[kind="primary"]:hover {
      background: linear-gradient(135deg, #FFFFFF 0%, #B2FF59 100%) !important;
      transform: scale(1.06) translateY(-6px) !important;
      border-color: #00E676 !important;
      box-shadow: 0 20px 50px rgba(29, 233, 182, 0.8) !important;
    }
    div.stButton > button[kind="primary"] p {
      font-size: 1.45rem !important;
      font-weight: 900 !important;
      text-transform: uppercase !important;
      letter-spacing: 4px !important;
      color: #000000 !important;
      margin: 0 !important;
      text-shadow: 0 2px 4px rgba(255,255,255,0.8) !important;
    }

    /* ========================================================
       BOTONES SECUNDARIOS (PRÁCTICA Y EVALUACIÓN)
       ======================================================== */
    div.stButton > button[kind="secondary"] {
      background: linear-gradient(145deg, rgba(30,35,45, 0.9) 0%, rgba(15,20,25, 0.95) 100%) !important;
      border: 1px solid rgba(255,255,255,0.2) !important;
      border-radius: 12px !important;
      color: #FFFFFF !important;
      padding: 16px !important;
      box-shadow: 0 6px 20px rgba(0,0,0,0.5) !important;
      transition: all 0.3s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
      background: linear-gradient(145deg, rgba(50,55,70, 0.9) 0%, rgba(30,35,45, 0.95) 100%) !important;
      border-color: #FFFFFF !important;
      transform: translateY(-3px) !important;
      box-shadow: 0 10px 25px rgba(255,255,255,0.1) !important;
    }
    div.stButton > button[kind="secondary"] p {
      color: #FFFFFF !important;
      font-weight: 800 !important;
      letter-spacing: 1.5px !important;
      font-size: 1rem !important;
      text-transform: uppercase !important;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button("INICIAR SIMULACION", use_container_width=True, key="btn_iniciar_sim", type="primary"):
      st.session_state.etapa_actual = "seleccion"
      st.rerun()

  st.markdown("<br>", unsafe_allow_html=True)

  # ── Dos botones de ruta directa al módulo de preguntas ───────────────────────
  col_b1, col_b2, col_b3 = st.columns([1, 1.2, 1])
  with col_b2:
    st.markdown(
      "<div style='display:flex;gap:20px;margin-bottom:20px;'>"

      "<div style='flex:1;background:linear-gradient(145deg, rgba(76,175,80,0.1) 0%, rgba(20,40,25,0.85) 100%);padding:22px 18px;"
      "border-radius:16px;border:1px solid rgba(76,175,80,0.4);border-top:5px solid #00E676;text-align:center;box-shadow:0 8px 30px rgba(0,0,0,0.6);'>"
      "<p style='margin:0 0 10px 0;color:#00E676;font-weight:900;font-size:1.05rem;"
      "letter-spacing:2px;text-transform:uppercase;text-shadow:0 2px 8px rgba(0,230,118,0.4);'>Banco de Práctica</p>"
      "<p style='margin:0;color:#E0E0E0;font-size:0.85rem;line-height:1.6;'>"
      "<b>50 preguntas interactivas.</b><br>Acceso libre. Sin contraseña.</p></div>"

      "<div style='flex:1;background:linear-gradient(145deg, rgba(156,39,176,0.1) 0%, rgba(40,20,45,0.85) 100%);padding:22px 18px;"
      "border-radius:16px;border:1px solid rgba(156,39,176,0.4);border-top:5px solid #E040FB;text-align:center;box-shadow:0 8px 30px rgba(0,0,0,0.6);'>"
      "<p style='margin:0 0 10px 0;color:#E040FB;font-weight:900;font-size:1.05rem;"
      "letter-spacing:2px;text-transform:uppercase;text-shadow:0 2px 8px rgba(224,64,251,0.4);'>Evaluación Formal</p>"
      "<p style='margin:0;color:#E0E0E0;font-size:0.85rem;line-height:1.6;'>"
      "<b>20 aleatorias. Contraseña.</b><br>Umbral de aprobación: 80%.</p></div>"

      "</div>",
      unsafe_allow_html=True
    )
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
      if st.button("Banco de Practica", use_container_width=True, key="btn_ir_practica_home"):
        st.session_state.etapa_actual = "evaluacion"
        st.session_state.eval_vista = "practica"
        st.session_state.practica_respuestas = {}
        st.rerun()
    with col_btn2:
      if st.button("Evaluacion Formal", use_container_width=True, key="btn_ir_examen_home"):
        st.session_state.etapa_actual = "evaluacion"
        st.session_state.eval_vista = "examen"
        st.session_state.examen_desbloqueado = False
        st.rerun()

elif st.session_state.etapa_actual == "seleccion":
  st.markdown("<br>", unsafe_allow_html=True)

  col_back, _ = st.columns([1, 4])
  with col_back:
    if st.button(" Volver al Inicio", key="btn_volver_inicio", use_container_width=True):
      st.session_state.etapa_actual = "portada"
      st.rerun()

  st.markdown("<h2 class='title-gradient' style='font-size: 3rem !important; margin-bottom: 40px !important;'>Seleccionar Especie de Estudio</h2>", unsafe_allow_html=True)

  import os
  import base64
  from st_clickable_images import clickable_images

  @st.cache_data
  def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
      data = f.read()
    return base64.b64encode(data).decode()

  def generar_tarjeta_animada(nombre_especie, img_url, duracion, ovulacion, r_materno, c_hex, c_rgb):
      html_card = f"""
      <style>
          /* 1. Contenedor Dashboard de la Tarjeta */
          .card-wrapper-{nombre_especie.lower()} {{
              background-color: #1A1C23;
              border-radius: 12px;
              border-left: 6px solid {c_hex};
              padding: 20px;
              margin-bottom: 0;
              box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
              transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
              position: relative;
          }}

          /* 2. HACK DEL BOTÓN INVISIBLE (OVERLAY BULLETPROOF) */
          /* Compatibilidad universal: Streamlit < 1.30 (column) y >= 1.30 (stColumn) */
          div[data-testid="column"]:has(.card-wrapper-{nombre_especie.lower()}) div[data-testid="stVerticalBlock"],
          div[data-testid="stColumn"]:has(.card-wrapper-{nombre_especie.lower()}) div[data-testid="stVerticalBlock"] {{
              position: relative !important;
          }}

          div[data-testid="column"]:has(.card-wrapper-{nombre_especie.lower()}) div[data-testid="stVerticalBlock"] > div,
          div[data-testid="stColumn"]:has(.card-wrapper-{nombre_especie.lower()}) div[data-testid="stVerticalBlock"] > div {{
              position: static !important;
              transform: none !important;
          }}

          /* Convertimos el botón de esta columna en un cristal transparente que cubre toda la tarjeta */
          div[data-testid="column"]:has(.card-wrapper-{nombre_especie.lower()}) div.stButton > button,
          div[data-testid="stColumn"]:has(.card-wrapper-{nombre_especie.lower()}) div.stButton > button {{
              position: absolute !important;
              top: 0 !important; 
              left: 0 !important;
              width: 100% !important; 
              height: 100% !important;
              opacity: 0 !important; /* TOTALMENTE INVISIBLE, LISTO PARA CLICS */
              z-index: 999 !important;
              cursor: pointer !important;
              background: transparent !important;
              border: none !important;
          }}

          div[data-testid="column"]:has(.card-wrapper-{nombre_especie.lower()}) div.stButton > button p,
          div[data-testid="stColumn"]:has(.card-wrapper-{nombre_especie.lower()}) div.stButton > button p {{
              display: none !important;
          }}

          /* 3. TRANSFERENCIA DE HOVER */
          div[data-testid="column"]:has(div.stButton > button:hover) .card-wrapper-{nombre_especie.lower()},
          div[data-testid="stColumn"]:has(div.stButton > button:hover) .card-wrapper-{nombre_especie.lower()} {{
              transform: translateY(-8px);
              box-shadow: 0 15px 25px rgba({c_rgb}, 0.4);
              border-left-color: #FFFFFF;
          }}

          div[data-testid="column"]:has(div.stButton > button:hover) .img-container-{nombre_especie.lower()} img,
          div[data-testid="stColumn"]:has(div.stButton > button:hover) .img-container-{nombre_especie.lower()} img {{
              transform: scale(1.03);
          }}

          /* 4. Imagen de Portada con Zoom Sutil en Hover */
          .img-container-{nombre_especie.lower()} {{
              overflow: hidden;
              border-radius: 8px;
              margin-bottom: 20px;
          }}
          .img-container-{nombre_especie.lower()} img {{
              width: 100%;
              height: 230px;
              object-fit: cover;
              border-radius: 8px;
              display: block;
              transition: transform 0.4s ease;
          }}

          /* 5. Tipografía y Estructura (Grid y Badges) */
          .card-title-{nombre_especie.lower()} {{
              font-size: 1.6rem;
              font-weight: 900;
              text-align: center;
              color: {c_hex};
              letter-spacing: 1px;
              margin-top: 0;
              margin-bottom: 15px;
              text-transform: uppercase;
          }}
          .tech-grid {{
              display: grid;
              grid-template-columns: 1fr;
              gap: 12px;
          }}
          .tech-badge {{
              display: flex;
              flex-direction: column;
              background-color: rgba(255, 255, 255, 0.03);
              border: 1px solid rgba({c_rgb}, 0.15);
              padding: 12px;
              border-radius: 8px;
          }}
          .tech-label {{
              font-size: 0.75rem;
              color: #8B949E;
              text-transform: uppercase;
              font-weight: 700;
              letter-spacing: 1px;
              margin-bottom: 4px;
          }}
          .tech-value {{
              font-size: 1.15rem;
              color: #FFFFFF;
              font-weight: 900;
              line-height: 1.2;
          }}
          .tech-value.highlight {{
              color: {c_hex};
          }}
      </style>
      <div class="card-wrapper-{nombre_especie.lower()}">
          <h2 class="card-title-{nombre_especie.lower()}">{nombre_especie}</h2>
          <div class="img-container-{nombre_especie.lower()}">
              <img src="{img_url}" alt="{nombre_especie}">
          </div>
          <div class="tech-grid">
              <div class="tech-badge">
                  <span class="tech-label">Duración</span>
                  <span class="tech-value">{duracion}</span>
              </div>
              <div class="tech-badge">
                  <span class="tech-label">Ovulación</span>
                  <span class="tech-value">{ovulacion}</span>
              </div>
              <div class="tech-badge">
                  <span class="tech-label">R. Materno</span>
                  <span class="tech-value highlight">{r_materno}</span>
              </div>
          </div>
      </div>
      """
      return html_card

  temas_dic = {
      "Bovino":  {"hex": "#00B4D8", "rgb": "0, 180, 216"},
      "Porcino": {"hex": "#F4A261", "rgb": "244, 162, 97"},
      "Ovino":   {"hex": "#E9C46A", "rgb": "233, 196, 106"},
      "Caprino": {"hex": "#558B2F", "rgb": "85, 139, 47"},
      "Equino":  {"hex": "#7B2CBF", "rgb": "123, 44, 191"},
      "Ave":     {"hex": "#D32F2F", "rgb": "211, 47, 47"}
  }

  # Primera fila: Bovino, Porcino, Ovino
  col1, col2, col3 = st.columns(3)
  species_list_row1 = ["Bovino", "Porcino", "Ovino"]

  for col, sp in zip([col1, col2, col3], species_list_row1):
    with col:
      img_path = f"{sp.lower()}.jpg"
      if os.path.exists(img_path):
        b64_img = get_base64_of_bin_file(img_path)
        img_str = f"data:image/jpeg;base64,{b64_img}"
      else:
        img_str = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
        
      data = SPECIES_DATA[sp]
      c_hex = temas_dic[sp]["hex"]
      c_rgb = temas_dic[sp]["rgb"]
      
      html_card = generar_tarjeta_animada(
          sp, img_str,
          f"{data['cycle_duration']} {data.get('cycle_unit', 'días')}",
          data['ovulation_timing'],
          data['maternal_recognition'] if data['maternal_recognition'] not in ['?', 'N/A'] else 'N/A',
          c_hex, c_rgb
      )
      st.markdown(html_card, unsafe_allow_html=True)
      
      # Botón nativo renderizado debajo de la tarjeta para capturar el click hacia el simulador
      if st.button(f"SELECCIONAR {sp.upper()}", use_container_width=True, key=f"btn_sel_{sp}"):
        st.session_state.especie_seleccionada = sp
        st.session_state.etapa_actual = "simulador"
        st.rerun()

  st.markdown("<br>", unsafe_allow_html=True)

  # Segunda fila: Caprino, Equino, Ave
  col4, col5, col6 = st.columns(3)
  species_list_row2 = ["Caprino", "Equino", "Ave"]

  for col, sp in zip([col4, col5, col6], species_list_row2):
    with col:
      img_path = f"{sp.lower()}.jpg"
      if os.path.exists(img_path):
        b64_img = get_base64_of_bin_file(img_path)
        img_str = f"data:image/jpeg;base64,{b64_img}"
      else:
        img_str = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
        
      data = SPECIES_DATA[sp]
      c_hex = temas_dic[sp]["hex"]
      c_rgb = temas_dic[sp]["rgb"]
      
      html_card = generar_tarjeta_animada(
          sp, img_str,
          f"{data['cycle_duration']} {data.get('cycle_unit', 'días')}",
          data['ovulation_timing'],
          data['maternal_recognition'] if data['maternal_recognition'] not in ['?', 'N/A'] else 'N/A',
          c_hex, c_rgb
      )
      st.markdown(html_card, unsafe_allow_html=True)
      
      if st.button(f"SELECCIONAR {sp.upper()}", use_container_width=True, key=f"btn_sel_{sp}"):
        st.session_state.especie_seleccionada = sp
        st.session_state.etapa_actual = "simulador"
        st.rerun()

elif st.session_state.etapa_actual == "simulador":
  col_back, _ = st.columns([1, 5])
  with col_back:
    if st.button(" Cambiar Especie", use_container_width=True):
      st.session_state.etapa_actual = "seleccion"
      st.rerun()
  renderizar_simulador()

elif st.session_state.etapa_actual == "evaluacion":
  col_back2, _ = st.columns([1, 5])
  with col_back2:
    if st.button("Volver al Inicio", use_container_width=True, key="btn_volver_eval"):
      st.session_state.etapa_actual = "portada"
      st.session_state.examen_desbloqueado = False
      st.session_state.eval_vista = "practica"
      st.rerun()

  # Cabecera del módulo
  st.markdown(
    "<div style='background:linear-gradient(135deg,rgba(22,33,25,0.9),rgba(12,22,16,0.95));"
    "padding:28px 36px;border-radius:14px;border-top:4px solid #4CAF50;"
    "border:1px solid rgba(76,175,80,0.2);margin-bottom:28px;'>"
    "<h2 style='margin:0 0 6px 0;color:#4CAF50;font-weight:700;letter-spacing:1px;'>MODULO DE EVALUACION</h2>"
    "<p style='margin:0;color:#B0BEC5;font-size:0.92rem;'>Ciclo Estral Comparado - Fisiologia Animal Aplicada</p>"
    "</div>",
    unsafe_allow_html=True
  )

  # Guardias de estado (no sobreescriben lo fijado por la portada al presionar el botón)
  if "eval_vista" not in st.session_state:
    st.session_state.eval_vista = "practica"
  if "examen_desbloqueado" not in st.session_state:
    st.session_state.examen_desbloqueado = False
  if "practica_respuestas" not in st.session_state:
    st.session_state.practica_respuestas = {}

  # ── RUTA A: Banco de Práctica (público, interactivo con st.radio) ─────────────
  if st.session_state.eval_vista == "practica":
    st.markdown(
      "<div style='background:rgba(76,175,80,0.06);padding:16px 22px;border-radius:10px;"
      "border:1px solid rgba(76,175,80,0.2);margin-bottom:24px;'>"
      "<p style='margin:0;color:#B0BEC5;font-size:0.88rem;'>"
      "Modo de practica libre. Resuelve las preguntas e identifica la respuesta correcta "
      "resaltada en verde. Sin limite de tiempo ni calificacion final."
      "</p></div>",
      unsafe_allow_html=True
    )

    GRUPOS = [
      ("Bovino - Ciclo y Fases", list(range(0, 10))),
      ("Equino - Fisiologia y Manejo", list(range(10, 15))),
      ("Porcino, Ovino y Reconocimiento Materno", list(range(15, 20))),
      ("Deteccion de Celo y Tecnologia", list(range(20, 30))),
      ("Protocolos de Sincronizacion (Ovsynch / IATF)", list(range(30, 39))),
      ("Fisiologia Comparada y Economia Reproductiva", list(range(39, 50))),
    ]
    COLORES = ["#4CAF50", "#58A6FF", "#FF9933", "#BC8BFF", "#FF3366", "#00CC99"]

    for g_idx, (titulo_g, indices) in enumerate(GRUPOS):
      cg = COLORES[g_idx % len(COLORES)]
      with st.expander(f"{titulo_g}  ({len(indices)} preguntas)", expanded=False):
        for q_idx in indices:
          q = BANCO_PREGUNTAS[q_idx]
          num = q_idx + 1
          st.markdown(
            f"<div style='background:rgba(255,255,255,0.02);padding:14px 18px;"
            f"border-radius:10px;border-left:3px solid {cg};margin-bottom:8px;'>"
            f"<p style='margin:0;color:#E8F5E9;font-size:0.95rem;font-weight:500;line-height:1.5;'>"
            f"<span style='color:{cg};font-weight:800;'>{num}.</span> {q['pregunta']}</p>"
            f"</div>",
            unsafe_allow_html=True
          )
          seleccion = st.radio(
            label=f"Pregunta {num}", options=q["opciones"],
            index=None, key=f"practica_q_{q_idx}", label_visibility="collapsed"
          )
          if seleccion is not None:
            if q["opciones"].index(seleccion) == q["correcta"]:
              st.markdown(
                "<div style='background:rgba(76,175,80,0.12);padding:10px 16px;"
                "border-radius:8px;border-left:3px solid #4CAF50;margin-bottom:16px;'>"
                "<p style='margin:0;color:#4CAF50;font-size:0.88rem;font-weight:600;'>"
                "Correcto. Respuesta exacta.</p></div>",
                unsafe_allow_html=True
              )
            else:
              st.markdown(
                f"<div style='background:rgba(239,83,80,0.08);padding:10px 16px;"
                f"border-radius:8px;border-left:3px solid #EF5350;margin-bottom:16px;'>"
                f"<p style='margin:0;color:#EF5350;font-size:0.88rem;font-weight:600;'>"
                f"Incorrecto. La respuesta correcta es: "
                f"<span style='color:#4CAF50;'>{q['opciones'][q['correcta']]}</span></p></div>",
                unsafe_allow_html=True
              )

  # ── RUTA B: Evaluación Formal (protegida con contraseña agroestral2026) ───────
  elif st.session_state.eval_vista == "examen":
    if not st.session_state.examen_desbloqueado:
      st.markdown("<br>", unsafe_allow_html=True)
      st.markdown(
        "<div style='max-width:460px;margin:0 auto;padding:36px 40px;"
        "background:rgba(22,33,25,0.92);border:1px solid rgba(76,175,80,0.3);"
        "border-top:3px solid #4CAF50;border-radius:16px;"
        "backdrop-filter:blur(14px);box-shadow:0 12px 40px rgba(0,0,0,0.5);text-align:center;'>"
        "<p style='font-size:2rem;margin:0 0 8px 0;'>&#128274;</p>"
        "<h3 style='color:#4CAF50;margin:0 0 6px 0;font-size:1.25rem;'>Evaluacion Formal Protegida</h3>"
        "<p style='color:#8B949E;font-size:0.87rem;margin:0 0 24px 0;'>"
        "Esta seccion requiere contrasena de acceso.<br>Solicitala a tu docente.</p>"
        "</div>",
        unsafe_allow_html=True
      )
      col_pw1, col_pw2, col_pw3 = st.columns([1, 2, 1])
      with col_pw2:
        clave = st.text_input(
          "Contrasena", type="password",
          placeholder="Ingresa la contrasena",
          key="input_clave_examen", label_visibility="collapsed"
        )
        if st.button("Ingresar", use_container_width=True, key="btn_unlock_examen"):
          if clave == "agroestral2026":
            st.session_state.examen_desbloqueado = True
            st.success("Acceso concedido. Cargando evaluacion...")
            st.rerun()
          else:

            st.error("Contrasena incorrecta. Intentalo de nuevo.")
    else:
      # Los reruns internos del examen (avance de pregunta, calificacion) no
      # repiden la clave porque examen_desbloqueado persiste en session_state.
      renderizar_evaluacion()

