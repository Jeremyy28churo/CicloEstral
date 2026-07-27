import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import json
from evaluacion import renderizar_evaluacion, BANCO_PREGUNTAS, get_global_exam_state

import time
import datetime
import base64
import os

def get_image_base64(ruta_local):
    if not os.path.exists(ruta_local):
        return ""
    with open(ruta_local, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded_string}"

global_state = get_global_exam_state()

# ROUTING PARA TARJETAS CLICKABLES NATIVAS
if "nav_to" in st.query_params:
    nav = st.query_params["nav_to"]
    if nav == "banco":
        st.session_state.etapa_actual = "evaluacion"
        st.session_state.eval_vista = "practica"
        st.session_state.practica_respuestas = {}
    elif nav == "examen":
        st.session_state.etapa_actual = "evaluacion"
        st.session_state.eval_vista = "examen"
        st.session_state.examen_desbloqueado = False
    st.query_params.clear()

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

# INICIALIZACIÓN GLOBAL DE ESTADO (Para evitar State Loss en Refresh)
if 'etapa_actual' not in st.session_state:
  st.session_state.etapa_actual = st.query_params.get('etapa', 'portada')
if 'especie_seleccionada' not in st.session_state:
  st.session_state.especie_seleccionada = st.query_params.get('especie', None)
if 'seccion_activa' not in st.session_state:
  st.session_state.seccion_activa = st.query_params.get('seccion', 'Fases del Ciclo Estral')

# Configuración de página
st.set_page_config(page_title="Ciclo Estral", layout="wide", initial_sidebar_state="collapsed")

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

  /* Ocultar ABSOLUTAMENTE TODOS los iconos de enlace (cadenas) en encabezados */
  h1 a, h2 a, h3 a, h4 a, h5 a, h6 a,
  .stMarkdown a.header-anchor,
  .stMarkdown a[href^="#"],
  a[data-testid="stHeaderAnchor"],
  [data-testid="stMarkdownContainer"] h1 svg,
  [data-testid="stMarkdownContainer"] h2 svg,
  [data-testid="stMarkdownContainer"] h3 svg {
      display: none !important;
      visibility: hidden !important;
      opacity: 0 !important;
      pointer-events: none !important;
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
    "metaestro": {"dur": "3-4 días", "icon": "", "title": "CL en formación", "text": "Ovulación ocurre 10-14h post-fin del estro. Luteinización del folículo ovulado para formar el Cuerpo Lúteo (CL) e inicio de secreción de P4. Posible sangrado metéstrico vaginal (24-48h post-ovulación)."},
    "diestro": {"dur": "12-14 días", "icon": "", "title": "CL Maduro", "text": "Fase más larga (CL maduro con P4 máxima). Sin reconocimiento materno (días 17-18), la PGF2α endometrial destruye el CL (luteólisis) para reiniciar el ciclo. Si hay preñez, el embrión libera IFN-τ."}
  },
  "Porcino": {
    "proestro": {"dur": "2-3 días", "icon": "", "title": "Crecimiento Múltiple", "text": "Fase folicular rápida. Crecimiento de múltiples folículos simultáneos (poliovulatorio)."},
    "estro": {"dur": "24-72 horas", "icon": "", "title": "Receptividad prolongada", "text": "Receptividad sexual prolongada. Signo clave: Reflejo de inmovilidad (lordosis con orejas rígidas) ante presión dorsal y feromonas del verraco."},
    "metaestro": {"dur": "2-3 días", "icon": "", "title": "Formación de CLs", "text": "Ovulación de 15-25 folículos entre las 36-44h post-inicio del estro. Formación de múltiples cuerpos lúteos e inicio de la secreción de Progesterona (P4)."},
    "diestro": {"dur": "11-13 días", "icon": "", "title": "Dominio de P4", "text": "Producción masiva de P4. Para evitar la luteólisis, se requiere el reconocimiento materno mediado por los estrógenos de mínimo 4 embriones."}
  },
  "Ovino": {
    "proestro": {"dur": "1-2 días", "icon": "", "title": "Desarrollo Rápido", "text": "Crecimiento folicular rápido. Ciclicidad poliéstrica estacional de días cortos (otoño) estimulada por melatonina."},
    "estro": {"dur": "24-36 horas", "icon": "", "title": "Celo Discreto", "text": "Signos conductuales muy discretos. Búsqueda activa del macho. Ovulación de 1-3 folículos hacia el final de esta fase."},
    "metaestro": {"dur": "2-3 días", "icon": "", "title": "CL Temprano", "text": "Formación del cuerpo lúteo joven y transición rápida hacia la secreción de progesterona (P4)."},
    "diestro": {"dur": "10-12 días", "icon": "", "title": "Fase Lútea Acortada", "text": "Fase lútea acortada en comparación con bovinos. Dominio de P4. Reconocimiento materno embrionario mediado por IFN-τ en el útero."}
  },
  "Caprino": {
    "proestro": {"dur": "2-3 días", "icon": "", "title": "Reclutamiento", "text": "Fase de reclutamiento y dominancia de 1-3 folículos. Poliéstrica estacional (con menor estacionalidad en regiones tropicales)."},
    "estro": {"dur": "24-48 horas", "icon": "", "title": "Celo Evidente", "text": "Signos de celo evidentes por vocalización y movimiento continuo de cola. Inducción de la ciclicidad por el 'Efecto Macho'."},
    "metaestro": {"dur": "2-3 días", "icon": "", "title": "Luteinización", "text": "Ovulación ocurre unas 30 horas post-inicio de estro. Organización de 1-3 cuerpos lúteos en los ovarios."},
    "diestro": {"dur": "13-15 días", "icon": "", "title": "Dominio Lúteo", "text": "Dominio lúteo clásico de P4. Sin gestación, la PGF2α induce la luteólisis. Si hay preñez, el reconocimiento embrionario se realiza por IFN-τ."}
  },
  "Equino": {
    "proestro": {"dur": "2-3 días", "icon": "", "title": "Transición Inicial", "text": "Fase folicular inicial bajo influencia del fotoperíodo (poliéstrica estacional de días largos / primavera)."},
    "estro": {"dur": "4-7 días", "icon": "", "title": "Celo Muy Prolongado", "text": "Signos severos ante el semental (postura de monta, cola levantada, micción y 'guiño' de vulva rítmico)."},
    "metaestro": {"dur": "2-3 días", "icon": "", "title": "Ovulación Especial", "text": "¡Particularidad única!: La ovulación ocurre 24-48h ANTES de terminar el estro. Inicio del desarrollo lúteo. La IA se debe programar DURANTE el celo."},
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
    .section-header-jump p span.species-badge {{
        color: #FFFFFF !important; 
        background-color: var(--color-hex) !important; 
        padding: 3px 10px; 
        border-radius: 6px; 
        font-weight: 900; 
        text-transform: uppercase;
    }}
  </style>
  """, unsafe_allow_html=True)
  
  # --- SECCIÓN 1: FASES DEL CICLO DINÁMICAS ---
  if st.session_state.seccion_activa == "Fases del Ciclo Estral":
    st.markdown("""
    <div class='section-header-jump animate-fade-in'>
      <h3>LÍNEA DE TIEMPO FISIOLÓGICA</h3>
      <p>Dinámica hormonal y biológica interactiva y parametrizada.</p>
    </div>
    """, unsafe_allow_html=True)
  
    # Base de datos interactiva para la Línea de Tiempo (movida a nivel de módulo por rendimiento)
    sd = TIMELINE_DATA[species]

    # Headers dinámicos: mamíferos usan nombres estral, Ave usa nombres ovulatorios
    if species == "Ave":
      phase_headers = [
        ("Post-oviposición", "#FF9933", ""),
        ("Pico LH / Ovulación", "#FF3366", ""),
        ("Formación del Huevo", "#3399FF", ""),
        ("Oviposición", "#00CC99", "")
      ]
    else:
      phase_headers = [
        ("Proestro", "#FF3366", ""),
        ("Estro", "#4CAF50", ""),
        ("Metaestro", "#F8961E", ""),
        ("Diestro", "#00CC99", "")
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
          <p style="font-size: 0.85rem; color:#A0AAB5; margin-top: 10px;"><i> {sd[key]['dur']}</i></p>
          <p class="text-heavy text-neon-orange" style="font-size: 1.2rem !important; margin-bottom: 5px;">{sd[key]['icon']} {sd[key]['title']}</p>
          <p class="text-heavy" style="font-weight: 500 !important; font-size: 1.1rem !important;">{sd[key]['text']}</p>
        </div>
        """, unsafe_allow_html=True)

  
  # --- SECCIÓN 2: CALCULADORA DE DIAGNÓSTICO E IA ---
  if st.session_state.seccion_activa == "Checklist de Celo e IA":
    st.markdown("""
    <div class='section-header-jump animate-fade-in'>
      <h3>CALCULADORA DIAGNÓSTICA Y DECISIONES CLÍNICAS</h3>
      <p>Evaluación interactiva del paciente y análisis de impacto económico.</p>
    </div>
    """, unsafe_allow_html=True)
  
    st.markdown("<br>", unsafe_allow_html=True)
    
    especie_actual = st.session_state.get("especie_seleccionada", "Bovino")
    if not especie_actual:
        especie_actual = "Bovino"

    # Diccionario Maestro (datos_especies)
    datos_especies = {
        "Bovino": {
            "checklist": {"Reflejo de inmovilidad (dejarse montar)": 40, "Descarga de moco cervical claro (cristalino)": 20, "Inquietud y vocalización": 20, "Grupa o base de la cola raspada": 10, "Búsqueda del macho / intento de montar": 10},
            "decisiones_ia": "**Regla AM/PM:** Detectado AM -> Inseminar PM. Dosis: 1 pajuela (0.5cc) en cuerpo del útero.",
            "estrategias_deteccion": ["Observación Visual Tradicional (~40% de éxito)", "Collares de Precisión o Podómetros (~90% de éxito)"],
            "roi_base": 150,
            "desglose_perdidas": "Incluye: Costos de alimentación por días abiertos extras, pérdida de producción lechera (o kilos al destete) y gastos de mantenimiento improductivo."
        },
        "Porcino": {
            "checklist": {"Reflejo de inmovilidad ante el verraco/presión en lomo": 40, "Orejas erguidas (paradas)": 20, "Vulva inflamada y enrojecida": 20, "Gruñidos característicos": 10, "Pérdida de apetito": 10},
            "decisiones_ia": "**Inseminación:** A las 12-24 horas del inicio del reflejo de inmovilidad. Dosis: 80-100cc (2-3 mil millones espermatozoides).",
            "estrategias_deteccion": ["Observación Visual sin Verraco (~50% de éxito)", "Detección con Verraco Marcador + Sensores (~90% de éxito)"],
            "roi_base": 50,
            "desglose_perdidas": "Incluye: Días no productivos (DNP) de la cerda, costo de ración diaria desperdiciada y reducción del índice de lechones por hembra al año."
        },
        "Ovino": {
            "checklist": {"Búsqueda activa del carnero": 40, "Movimientos rápidos de la cola (coleo)": 30, "Vulva ligeramente hiperémica": 10, "Inquietud": 10, "Reflejo de inmovilidad ante el carnero": 10},
            "decisiones_ia": "**Inseminación:** A las 12-18 horas de detectado el celo. Dosis: Intrauterina vía laparoscópica o intracervical profunda.",
            "estrategias_deteccion": ["Detección Visual sin Macho Marcador (~30% de éxito)", "Efecto Macho + Implantes de Melatonina (~80% de éxito)"],
            "roi_base": 30,
            "desglose_perdidas": "Incluye: Menor número de corderos destetados al año, gastos de suplementación alimenticia improductiva y desincronización del rebaño."
        },
        "Caprino": {
            "checklist": {"Vocalización constante (balidos)": 30, "Movimiento enérgico de la cola": 30, "Búsqueda del macho": 20, "Micción frecuente": 10, "Vulva hinchada con moco claro": 10},
            "decisiones_ia": "**Inseminación:** A las 12-24 horas post detección. Dosis: Intracervical profunda (semen fresco/congelado).",
            "estrategias_deteccion": ["Detección Visual sin Macho Marcador (~35% de éxito)", "Efecto Macho Programado + Esponjas/CIDR (~85% de éxito)"],
            "roi_base": 25,
            "desglose_perdidas": "Incluye: Días de lactancia perdidos, reducción en la cuota lechera anual y gastos de forraje en periodos secos extendidos."
        },
        "Equino": {
            "checklist": {"Postura de micción frecuente (espejeo)": 40, "Elevación de la cola": 20, "Aceptación del padrillo (orejas hacia adelante)": 20, "Contracción rítmica de la vulva": 10, "Relajación pélvica": 10},
            "decisiones_ia": "**Inseminación:** Antes de la ovulación (folículo > 35mm por ecografía). Dosis: 10-20cc de semen fresco/refrigerado.",
            "estrategias_deteccion": ["Observación Conductual sin Ecografía (~45% de éxito)", "Ecografía Folicular Seriada + IA Dirigida (~90% de éxito)"],
            "roi_base": 250,
            "desglose_perdidas": "Incluye: Alta inversión en pensión/mantenimiento mensual de la yegua, devaluación comercial del potro por nacer tarde y honorarios veterinarios."
        },
        "Ave": {
            "checklist": {"Receptividad a la monta (sentadilla)": 40, "Cresta y barbillas rojas turgentes": 20, "Distancia entre huesos pélvicos (> 2 dedos)": 20, "Cloaca húmeda y dilatada": 10, "Canto o vocalización receptiva": 10},
            "decisiones_ia": "**Manejo:** Fotoperíodo 16L:8O. IA semanal para mantener fertilidad. Dosis: 0.05cc vía intravaginal.",
            "estrategias_deteccion": ["Fotoperíodo Natural sin Control (~60% postura)", "Programa de Luz 16L:8O Automatizado (~85-90% postura)"],
            "roi_base": 2,
            "desglose_perdidas": "Incluye: Caída en la curva de postura (huevos no producidos), desperdicio de ración balanceada diaria y reducción del porcentaje de incubabilidad."
        }
    }

    data_esp = datos_especies.get(especie_actual, datos_especies["Bovino"])
  
    c1, c2 = st.columns([1.2, 1])
  
    with c1:
      score_label = "Score de Postura" if especie_actual == "Ave" else "Score de Celo"
      
      with st.container(border=True):
        st.markdown(f"""
        <style>
        .hover-jump {{
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        }}
        .hover-jump:hover {{
            transform: translateY(-4px) scale(1.015) !important;
            box-shadow: 0 15px 30px rgba(var(--color-rgb), 0.25) !important;
            border-color: rgba(var(--color-rgb), 0.5) !important;
            z-index: 10;
        }}
        .hover-jump-red {{
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        }}
        .hover-jump-red:hover {{
            transform: translateY(-4px) scale(1.015) !important;
            box-shadow: 0 15px 30px rgba(231, 29, 54, 0.25) !important;
            border-color: rgba(231, 29, 54, 0.5) !important;
            z-index: 10;
        }}
        </style>
        <div class='hover-jump' style='background: rgba(var(--color-rgb), 0.05); border: 1px solid rgba(var(--color-rgb), 0.2); border-left: 4px solid var(--color-hex); padding: 15px; border-radius: 6px; margin-bottom: 20px;'>
            <h3 style='color: var(--color-hex); margin: 0 0 8px 0; font-size: 1.4rem; padding: 0; border: none; font-weight: 900; text-transform: uppercase; text-shadow: 0 0 12px rgba(var(--color-rgb), 0.6); letter-spacing: 1px;'>{score_label}</h3>
            <p style='color: #B0B3B8; font-size: 0.9rem; margin: 0; line-height: 1.4;'>
                Evalúe los signos clínicos de receptividad sexual. Marque cada comportamiento observado para calcular el índice y determinar el momento óptimo de servicio.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Inyectar CSS para colapsar márgenes de los switches y colorearlos a la fuerza
        st.markdown("""
        <style>
        div[data-testid="stToggle"] { margin-bottom: -5px; }
        div[data-testid="stToggle"] label > div:first-of-type { background-color: rgba(231, 29, 54, 0.4) !important; }
        div[data-testid="stToggle"] label:has(input:checked) > div:first-of-type { background-color: #27AE60 !important; }
        </style>
        """, unsafe_allow_html=True)
        
        score = 0
        for i, (signo, puntos) in enumerate(data_esp["checklist"].items()):
          temp_k = f"temp_chk_{especie_actual}_{i}"
          real_k = f"chk_{especie_actual}_{i}"
          if temp_k not in st.session_state:
            st.session_state[temp_k] = st.session_state.get(real_k, False)
          st.toggle(f"{signo}", key=temp_k, on_change=sync_state, args=(temp_k, real_k))
          is_checked = st.session_state.get(real_k, False)
          if is_checked:
            score += puntos
    
        st.markdown("<hr style='margin: 15px 0; border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        # Alertas de diagnóstico estáticas rediseñadas
        if score >= 80:
            st.markdown("<div style='padding:15px; background:rgba(39, 174, 96, 0.1); border-left:4px solid #27AE60; border-radius:4px;'><span style='color:#27AE60; font-weight:bold;'>ÓPTIMO CONFIRMADO:</span> Proceder con el manejo o IA.</div>", unsafe_allow_html=True)
        elif score >= 40:
            st.markdown("<div style='padding:15px; background:rgba(249, 160, 63, 0.1); border-left:4px solid #F9A03F; border-radius:4px;'><span style='color:#F9A03F; font-weight:bold;'>EN PROGRESO / SOSPECHOSO:</span> Monitorear activamente. No inseminar aún.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='padding:15px; background:rgba(231, 29, 54, 0.1); border-left:4px solid #E71D36; border-radius:4px;'><span style='color:#E71D36; font-weight:bold;'>INACTIVO:</span> Marque los signos clínicos observados.</div>", unsafe_allow_html=True)
  
    with c2:
      with st.container(border=False):
        # Lógica del semáforo
        if score < 40:
            color_semaforo = "#E71D36" # Rojo
            estado_texto = "INACTIVO / RIESGO"
        elif score < 80:
            color_semaforo = "#F9A03F" # Naranja
            estado_texto = "EN PROGRESO / SOSPECHOSO"
        else:
            color_semaforo = "#27AE60" # Verde
            estado_texto = "ÓPTIMO / PROCEDER"

        # Visor 3D con Mapa de Calor
        img_path = f"{especie_actual.lower()}_base.png"
        img_b64 = get_image_base64(img_path)
        img_src = img_b64 if img_b64 else img_path

        st.markdown(f"""
        <style>
        .visor-3d-container {{
            background: radial-gradient(circle, rgba(255,255,255,0.03) 0%, transparent 60%);
            border-radius: 16px;
            text-align: center;
            margin-bottom: 20px;
            padding: 15px;
        }}
        .animal-wrapper {{
            position: relative;
            display: inline-block;
            width: 80%;
            max-width: 250px;
            transition: transform 0.3s ease;
            filter: drop-shadow(0 15px 30px {color_semaforo}90);
        }}
        .animal-wrapper:hover {{
            transform: scale(1.05) rotate(2deg);
        }}
        .animal-image {{
            width: 100%;
            display: block;
        }}
        .animal-tint {{
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background-color: {color_semaforo};
            mix-blend-mode: multiply;
            pointer-events: none;
            transition: background-color 0.8s ease-in-out;
            -webkit-mask-size: 100% 100%;
            -webkit-mask-repeat: no-repeat;
            -webkit-mask-position: center;
            mask-size: 100% 100%;
            mask-repeat: no-repeat;
            mask-position: center;
        }}
        .visor-badge {{
            background-color: {color_semaforo};
            color: #FFFFFF;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 10px;
            letter-spacing: 1px;
            font-size: 0.9rem;
            transition: background-color 0.8s ease-in-out;
        }}
        </style>
        <div class="visor-3d-container">
            <div class="visor-badge">DIAGNÓSTICO: {estado_texto} (SCORE: {score})</div>
            <br>
            <div class="animal-wrapper">
                <img class="animal-image" src="{img_src}" alt="Visor Anatómico {especie_actual}">
                <div class="animal-tint" style="-webkit-mask-image: url('{img_src}'); mask-image: url('{img_src}');"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        ia_label = "Manejo Reproductivo" if especie_actual == "Ave" else "Decisiones de IA"
        
        with st.container(border=True):
            st.markdown(f"<h3 style='color: var(--color-hex); margin-top: 0; padding-bottom: 10px; border-bottom: 1px solid rgba(var(--color-rgb), 0.2); font-weight: 900; text-transform: uppercase; text-shadow: 0 0 12px rgba(var(--color-rgb), 0.6); letter-spacing: 1px;'>{ia_label}</h3>", unsafe_allow_html=True)
            
            recomendacion = data_esp['decisiones_ia'].replace('**Manejo:** ', '').replace('**Manejo:**', '')
            st.markdown(f"""
            <div class="hover-jump" style="background: rgba(var(--color-rgb), 0.05); border: 1px solid rgba(var(--color-rgb), 0.1); border-left: 3px solid var(--color-hex); padding: 12px 15px; border-radius: 4px; margin-bottom: 15px;">
                <span style="color: var(--color-hex); font-weight: bold; font-size: 0.9rem;">RECOMENDACIÓN CLÍNICA</span><br>
                <span style="color: #E2E8F0; font-size: 0.95rem;">{recomendacion}</span>
            </div>
            """, unsafe_allow_html=True)
            
            c_est, c_hato = st.columns([2.2, 1.3])
            with c_est:
                if "temp_estrategia_select" not in st.session_state:
                    st.session_state.temp_estrategia_select = st.session_state.get("estrategia_select", data_esp["estrategias_deteccion"][0])
                if st.session_state.temp_estrategia_select not in data_esp["estrategias_deteccion"]:
                    st.session_state.temp_estrategia_select = data_esp["estrategias_deteccion"][0]
                    st.session_state.estrategia_select = data_esp["estrategias_deteccion"][0]
        
                st.markdown("<div style='display:inline-block; background:rgba(var(--color-rgb),0.1); border:1px solid rgba(var(--color-rgb),0.4); color:var(--color-hex); padding:4px 10px; border-radius:4px; font-size:0.75rem; font-weight:bold; letter-spacing:1px; margin-bottom:8px; box-shadow: 0 0 8px rgba(var(--color-rgb),0.2);'>ESTRATEGIA DE DETECCIÓN</div>", unsafe_allow_html=True)
                st.selectbox("Estrategia de Detección:", data_esp["estrategias_deteccion"], key="temp_estrategia_select", on_change=sync_state, args=("temp_estrategia_select", "estrategia_select"), label_visibility="collapsed")
                
            with c_hato:
                st.markdown("<div style='display:inline-block; background:rgba(var(--color-rgb),0.1); border:1px solid rgba(var(--color-rgb),0.4); color:var(--color-hex); padding:4px 10px; border-radius:4px; font-size:0.75rem; font-weight:bold; letter-spacing:1px; margin-bottom:8px; box-shadow: 0 0 8px rgba(var(--color-rgb),0.2);'>TAMAÑO DE LOTE</div>", unsafe_allow_html=True)
                hato_size = st.number_input("Tamaño del Hato / Lote:", min_value=1, max_value=100000, value=100, step=10, label_visibility="collapsed")
                
            perdida_total = data_esp["roi_base"] * hato_size
            
            st.markdown(f"""
            <div class="hover-jump-red" style="background: rgba(231, 29, 54, 0.05); border: 1px solid rgba(231, 29, 54, 0.3); border-left: 4px solid #E71D36; padding: 15px; border-radius: 6px; margin-top: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="background-color: #E71D36; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: bold; letter-spacing: 1px;">IMPACTO ECONÓMICO</span>
                </div>
                <h3 style="color: #E71D36; margin: 10px 0 5px 0; font-size: 1.5rem;">Pérdida Potencial: ${perdida_total:,.2f} USD</h3>
                <p style="font-size: 0.85rem; color: #A0AEC0; margin-bottom: 0;">
                    <strong style="color: #FC8181;">Costo Base: ${data_esp['roi_base']} USD/animal</strong> por falla técnica/reproductiva.<br>
                    <span style="color: #E2E8F0; font-weight: bold;">{data_esp.get('desglose_perdidas', '')}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
  
  # --- SECCIÓN 3: LABORATORIO DE SIMULACIÓN Y COMPLICACIONES ---
  if st.session_state.seccion_activa == "Laboratorio de Simulacion":
  
    # 1. Modificadores de Salud Condicionales
    st.markdown("""
    <div class='section-header-jump animate-fade-in'>
      <h3>MODIFICADORES DE SALUD Y ESTADO DE GESTACIÓN</h3>
      <p>Configura las variables patológicas para simular el comportamiento endocrino.</p>
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
        st.info("ℹ **Nota:** La gallina no tiene gestación uterina. El ciclo ovulatorio es continuo bajo fotoperíodo adecuado.")
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
          if complication == "Balance Energético Negativo (BEN)":
            textos_ben = {
                "Bovino": "El BEN en vacas de alta producción (lipomovilización) inhibe los pulsos de GnRH, causando anestro posparto. Sin onda folicular ovulatoria, no hay gestación.",
                "Porcino": "En cerdas hiperprolíficas, el desgaste por lactación severa (BEN) detiene el crecimiento folicular, retrasando el estro post-destete y bloqueando la preñez.",
                "Ovino": "Una condición corporal pobre por deficiencia nutricional (falta de flushing) frena la tasa ovulatoria a cero, haciendo imposible la gestación.",
                "Caprino": "El déficit energético crítico en cabras lecheras paraliza el eje hipotálamo-hipófisis-gónada, deteniendo la ovulación y por ende la gestación.",
                "Equino": "Las yeguas con pobre condición corporal entran en anestro nutricional; al no haber desarrollo de un folículo preovulatorio dominante, la fecundación es nula."
            }
            st.info(f"ℹ **Nota Fisiológica ({species}):** {textos_ben.get(species, '')}")
            
          elif complication == "Cuerpo Lúteo Persistente":
            textos_cl = {
                "Bovino": "Una falla uterina (ej. piómetra) impide la liberación de PGF2α endometrial. El CL sobrevive y secreta progesterona, simulando una falsa gestación sin embrión.",
                "Caprino": "La retención del CL frecuentemente desencadena hidrómetra (pseudogestación caprina), acumulando fluido estéril con progesterona alta pero sin feto.",
                "Equino": "Fallas en la secreción de PGF2α en el diestro tardío prolongan la vida del CL. La yegua queda en anestro prolongado sin estar preñada."
            }
            st.info(f"ℹ **Nota Fisiológica ({species}):** {textos_cl.get(species, '')}")

    # Caso Especial: Estrés Calórico + Gestación Activa (solo mamíferos)
    if species != "Ave" and complication == "Estrés Calórico" and pregnancy:
      st.error("** Alerta de Impacto Económico (Mortalidad Embrionaria Temprana):** El estrés por calor severo en zonas tropicales incrementa la temperatura uterina, deprime la viabilidad del embrión y bloquea su señal de reconocimiento antes del día 15. Esto genera una reabsorción embrionaria silenciosa, provocando el retorno de la hembra al celo. Pérdidas directas de $3.00 USD por día abierto adicional por animal.")
      
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
        with st.expander(" Alerta Económica - Estrés por Calor (Ave)", expanded=True):
          st.markdown("""
          <div class="tinted-card" style="border-left: 6px solid #EF5350; background: rgba(239, 83, 80, 0.05); padding: 20px; border-radius: 8px;">
            <div style="margin-bottom: 15px;">
              <span class="agro-badge" style="background-color: #EF5350 !important; color: white !important;">ALERTA CRÍTICA</span>
            </div>
            <h4 style="color: #EF5350; margin-top: 0px; font-size: 20px; font-weight: bold;"> Estrés por Calor en Aves</h4>
            <ul class="texto-lectura-grande" style="color: #E0E4E8;">
              <li class='item-lista-grande'><b>Diagnóstico Económico:</b> Caída del 15-30% en postura diaria. Pérdida estimada de $0.10-0.15 USD por ave/día en huevos no producidos. En un lote de 1,000 aves: $100-150 USD/día.</li>
              <li class='item-lista-grande'><b>Fisiología Productiva:</b> El calor suprime la secreción de GnRH, deprime el pico preovulatorio de LH y altera la calcificación en la glándula cascarígena. Cáscaras delgadas y huevos deformes son signos frecuentes.</li>
              <li class='item-lista-grande'><b>Soluciones Técnicas de Gestión:</b> Instalar ventiladores y nebulizadores en el galpón. Suplementar electrolitos y vitamina C en el agua. Reducir la densidad de aves por metro cuadrado. Ajustar la alimentación a las horas más frescas del día.</li>
            </ul>
          </div>
          """, unsafe_allow_html=True)
      elif complication == "Fotoperíodo Inadecuado (<14h luz)":
        with st.expander(" Alerta Económica - Fotoperíodo Inadecuado (Ave)", expanded=True):
          st.markdown("""
          <div class="tinted-card" style="border-left: 6px solid #EF5350; background: rgba(239, 83, 80, 0.05); padding: 20px; border-radius: 8px;">
            <div style="margin-bottom: 15px;">
              <span class="agro-badge" style="background-color: #EF5350 !important; color: white !important;">ALERTA CRÍTICA</span>
            </div>
            <h4 style="color: #EF5350; margin-top: 0px; font-size: 20px; font-weight: bold;"> Fotoperíodo Inadecuado (&lt;14h luz)</h4>
            <ul class="texto-lectura-grande" style="color: #E0E4E8;">
              <li class='item-lista-grande'><b>Diagnóstico Económico:</b> Cese parcial o total de la postura. Pérdida directa del 100% de la producción de huevos durante el período de supresión. Activación de muda de plumas forzada.</li>
              <li class='item-lista-grande'><b>Fisiología Productiva:</b> Con menos de 14 horas de luz, la melatonina se eleva y suprime el eje HHG (Hipotálamo-Hipófisis-Gónada). La jerarquía folicular F1-F5 se detiene progresivamente. La gallina entra en un estado de reposo reproductivo.</li>
              <li class='item-lista-grande'><b>Soluciones Técnicas de Gestión:</b> Implementar programa de luz artificial con temporizador automatizado (16L:8O). Verificar la intensidad lumínica ≥20 lux a nivel de comedero. Evitar cortes de luz imprevistos que rompan la continuidad del fotoperíodo.</li>
            </ul>
          </div>
          """, unsafe_allow_html=True)
      elif complication == "Agotamiento Ovárico / Muda":
        with st.expander(" Alerta Económica - Agotamiento Ovárico / Muda (Ave)", expanded=True):
          st.markdown("""
          <div class="tinted-card" style="border-left: 6px solid #FF9800; background: rgba(255, 152, 0, 0.05); padding: 20px; border-radius: 8px;">
            <div style="margin-bottom: 15px;">
              <span class="agro-badge" style="background-color: #FF9800 !important; color: white !important;">ALERTA PRODUCTIVA</span>
            </div>
            <h4 style="color: #FF9800; margin-top: 0px; font-size: 20px; font-weight: bold;"> Agotamiento Ovárico / Muda Forzada</h4>
            <ul class="texto-lectura-grande" style="color: #E0E4E8;">
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
        with st.expander(" Alerta Económica - BEN", expanded=True):
          st.markdown("""
          <div class="tinted-card" style="border-left: 6px solid #EF5350; background: rgba(239, 83, 80, 0.05); padding: 20px; border-radius: 8px;">
            <div style="margin-bottom: 15px;">
              <span class="agro-badge" style="background-color: #EF5350 !important; color: white !important;">ALERTA CRÍTICA</span>
            </div>
            <h4 style="color: #EF5350; margin-top: 0px; font-size: 20px; font-weight: bold;"> Balance Energético Negativo (BEN)</h4>
            <ul class="texto-lectura-grande" style="color: #E0E4E8;">
              <li class='item-lista-grande'><b>Diagnóstico Económico:</b> Incremento drástico de "Días Abiertos". Cada día extra por encima de los 85 días post-parto le cuesta al hato $3 USD en alimentación de mantenimiento y leche no producida. En un hato de 100 vacas, 30 días de BEN representan $9,000 USD de pérdida evitable al año.</li>
              <li class='item-lista-grande'><b>Fisiología Productiva:</b> La alta producción de leche supera el consumo de materia seca. El cerebro detecta el déficit de energía y apaga el eje reproductivo (FSH/LH) para priorizar la supervivencia y la lactancia.</li>
              <li class='item-lista-grande'><b>Soluciones Técnicas de Gestión:</b> Balancear raciones aumentando la densidad energética en el tercio inicial de lactancia (grasas sobrepasantes, carbohidratos fermentables). En cerdas lactantes, planificar el "Destete Sincronizado" del lote para agrupar el retorno al celo.</li>
            </ul>
          </div>
          """, unsafe_allow_html=True)
      elif complication == "Cuerpo Lúteo Persistente":
        with st.expander(" Alerta Económica - CL Persistente", expanded=True):
          st.markdown("""
          <div class="tinted-card" style="border-left: 6px solid #EF5350; background: rgba(239, 83, 80, 0.05); padding: 20px; border-radius: 8px;">
            <div style="margin-bottom: 15px;">
              <span class="agro-badge" style="background-color: #EF5350 !important; color: white !important;">ALERTA CRÍTICA</span>
            </div>
            <h4 style="color: #EF5350; margin-top: 0px; font-size: 20px; font-weight: bold;"> Cuerpo Lúteo Persistente</h4>
            <ul class="texto-lectura-grande" style="color: #E0E4E8;">
              <li class='item-lista-grande'><b>Diagnóstico Económico:</b> Provoca anestro prolongado (falsa preñez) que eleva los días abiertos y disminuye el índice de partos por año del hato.</li>
              <li class='item-lista-grande'><b>Fisiología Productiva:</b> Inflamaciones o infecciones uterinas subclínicas bloquean físicamente la liberación de prostaglandina (PGF2α). El CL se mantiene intacto y la progesterona bloquea el ciclo.</li>
              <li class='item-lista-grande'><b>Soluciones Técnicas de Gestión:</b> Reemplazar la observación visual ineficiente con protocolos de Inseminación Artificial a Tiempo Fijo (IATF, ej. Ovsynch o CIDR/DIB con progesterona) para inducir la ovulación y preñar el 100% de las hembras sincronizadas. Realizar ecografías post-parto preventivas a los 30 días.</li>
            </ul>
          </div>
          """, unsafe_allow_html=True)
      elif complication == "Estrés Calórico":
        with st.expander(" Alerta Económica - Estrés Calórico", expanded=True):
          st.markdown("""
          <div class="tinted-card" style="border-left: 6px solid #EF5350; background: rgba(239, 83, 80, 0.05); padding: 20px; border-radius: 8px;">
            <div style="margin-bottom: 15px;">
              <span class="agro-badge" style="background-color: #EF5350 !important; color: white !important;">ALERTA CRÍTICA</span>
            </div>
            <h4 style="color: #EF5350; margin-top: 0px; font-size: 20px; font-weight: bold;"> Estrés Calórico</h4>
            <ul class="texto-lectura-grande" style="color: #E0E4E8;">
              <li class='item-lista-grande'><b>Diagnóstico Económico:</b> Ganaderías tropicales (ej. provincia de El Oro) sufren una caída crítica en la Tasa de Detección de Celo (TDC) visual a un 30-40%, provocando pérdidas de hasta $200 USD anuales por vaca.</li>
              <li class='item-lista-grande'><b>Fisiología Productiva:</b> Las hembras suprimen el comportamiento de monta para no generar calor corporal. El 60-70% de los celos ocurren de forma nocturna en la fresca madrugada. Además, se altera drásticamente la calidad ovocitaria y la viabilidad del embrión.</li>
              <li class='item-lista-grande'><b>Soluciones Técnicas de Gestión:</b> Inversión en collares de actividad con acelerómetro 3D para registrar celos silenciosos nocturnos. Instalar infraestructura de enfriamiento activo (sombras, aspersores, ventiladores) en áreas de espera y comederos para disminuir el ITH.</li>
            </ul>
          </div>
          """, unsafe_allow_html=True)
  
    # Data generation
    df = generate_hormone_data(species, complication, pregnancy)
    max_days = data['cycle_duration']
  
    # 2. Simulador Endocrino – Motor 100% JavaScript / Plotly.js (60 FPS cliente)
    st.markdown("---")
    st.markdown("""
    <div class='section-header-jump animate-fade-in'>
      <h3>SIMULADOR ENDOCRINO EN TIEMPO REAL</h3>
      <p>Visualización gráfica e interactiva del perfil hormonal en tiempo real.</p>
    </div>
    """, unsafe_allow_html=True)
  
    #  Serializar datos de hormonas a JSON para el motor JS 
    import json as _json
    import numpy as _np

    mat_key  = "Señal Materna" if pregnancy else "PGF2α"
    if pregnancy:
        if species == "Porcino":  mat_label = " Estrógenos Emb. (%)"
        elif species == "Equino": mat_label = " Movilidad Emb. (%)"
        else:                     mat_label = " IFN-τ (%)"
    else:
        mat_label = " PGF2α (%)"

    day_label   = "HORA" if species == "Ave" else "DÍA"
    x_axis_lbl  = "Horas del Ciclo Ovulatorio" if species == "Ave" else "Días del Ciclo"

    payload = _json.dumps({
        "t":         df["Día"].tolist(),
        "fsh":       df["FSH"].tolist(),
        "lh":        df["LH"].tolist(),
        "e2":        df["Estradiol (E2)"].tolist(),
        "p4":        df["Progesterona (P4)"].tolist(),
        "mat":       df[mat_key].tolist(),
        "maxDays":   float(max_days),
        "dayLabel":  day_label,
        "xAxisLbl":  x_axis_lbl,
        "matLabel":  mat_label,
        "species":   species,
        "complication": complication,
        "pregnancy": pregnancy,
        "phases":    [{"name": p["name"], "start": p["range"][0],
                       "end": p["range"][1], "color": p["color"]}
                      for p in data["phases"]],
    }, ensure_ascii=False)

    num_frames = len(df) - 1

    sim_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: transparent; font-family: 'Inter', sans-serif; color: #fff; }}

  #sim-wrapper {{
    background: rgba(22,27,34,0.97);
    border-radius: 16px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.07);
  }}

  /*  Fila 1: controles  */
  #controls {{
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 14px;
  }}
  #btn-play {{
    flex-shrink: 0;
    width: 160px;
    padding: 12px 0;
    border-radius: 10px;
    border: none;
    font-size: 1rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    cursor: pointer;
    text-transform: uppercase;
    transition: all 0.25s ease;
    background: #00E676;
    color: #121212;
    box-shadow: 0 4px 18px rgba(0,230,118,0.45);
  }}
  #btn-play:hover:not(:disabled) {{ background:#00C853; transform:translateY(-2px); box-shadow:0 8px 24px rgba(0,230,118,0.6); }}
  #btn-play.paused {{ background:#FF3366; color:#fff; box-shadow:0 4px 18px rgba(255,51,102,0.45); }}
  #btn-play.paused:hover {{ background:#E0003A; box-shadow:0 8px 24px rgba(255,51,102,0.6); }}
  #btn-play:disabled {{ background: #555; color: #aaa; cursor: not-allowed; box-shadow: none; transform: none; }}

  #slider-wrap {{ flex:1; }}
  #slider-lbl {{ font-size:0.78rem; color:#8b949e; margin-bottom:6px; text-transform:uppercase; letter-spacing:1px; }}
  #t-slider {{
    -webkit-appearance:none; appearance:none;
    width:100%; height:6px; border-radius:3px; outline:none; cursor:pointer;
    background: rgba(255,255,255,0.12);
  }}
  #t-slider::-webkit-slider-thumb {{
    -webkit-appearance:none; appearance:none;
    width:18px; height:18px; border-radius:50%;
    background:#00E676; border:2px solid #fff;
    box-shadow:0 0 8px rgba(0,230,118,0.7); cursor:pointer;
  }}
  #t-slider:disabled::-webkit-slider-thumb {{ background: #555; border-color: #888; box-shadow: none; cursor: not-allowed; }}

  /*  Fila 2: alerta diagnóstico  */
  #diag-box {{
    border-radius:10px; padding:12px 16px; margin-bottom:14px;
    font-size:0.92rem; font-weight:600; line-height:1.5;
    border-left:5px solid #58A6FF;
    background:rgba(88,166,255,0.1); color:#E8F0FF;
    transition: background 0.4s, border-color 0.4s;
  }}
  #diag-box.success {{ background:rgba(0,204,100,0.12); border-color:#00CC64; color:#B9F5D8; }}
  #diag-box.error   {{ background:rgba(255,51,102,0.12); border-color:#FF3366; color:#FFD0DC; }}
  #diag-box.warning {{ background:rgba(255,193,7,0.12);  border-color:#FFC107; color:#FFF3CD; }}

  /*  Fila 3: KPIs  */
  #kpi-row {{
    display:flex; flex-wrap:wrap; gap:12px; margin-bottom:14px;
    background:rgba(22,27,34,0.6); padding:16px; border-radius:14px;
    border:1px solid rgba(255,255,255,0.06);
  }}
  .kpi-card {{
    flex:1; min-width:90px; text-align:center;
  }}
  .kpi-lbl {{ font-size:12px; color:#8b949e; display:block; margin-bottom:6px; }}
  .kpi-val {{ font-size:26px; font-weight:800; }}

  /*  Fila 4: gráfica  */
  #chart {{ width:100%; height:400px; }}
</style>
</head>
<body>
<div id="sim-wrapper">

  <!-- Fila 1: Controles -->
  <div id="controls">
    <button id="btn-play" disabled>Cargando...</button>
    <div id="slider-wrap">
      <div id="slider-lbl">Desliza para avanzar el {day_label} del ciclo manualmente</div>
      <input id="t-slider" type="range" min="0" max="{num_frames}" value="0" step="1" disabled>
    </div>
  </div>

  <!-- Fila 2: Diagnóstico -->
  <div id="diag-box">Generando motor de animación...</div>

  <!-- Fila 3: KPIs -->
  <div id="kpi-row">
    <div class="kpi-card"><span class="kpi-lbl"> FSH (%)</span><span class="kpi-val" id="k-fsh" style="color:#BC8BFF">0.0%</span></div>
    <div class="kpi-card"><span class="kpi-lbl"> LH (%)</span><span class="kpi-val" id="k-lh"  style="color:#FF3366">0.0%</span></div>
    <div class="kpi-card"><span class="kpi-lbl"> E2 (%)</span><span class="kpi-val" id="k-e2"  style="color:#58A6FF">0.0%</span></div>
    <div class="kpi-card"><span class="kpi-lbl"> P4 (%)</span><span class="kpi-val" id="k-p4"  style="color:#00CC99">0.0%</span></div>
    <div class="kpi-card"><span class="kpi-lbl" id="k-mat-lbl"> PGF2α (%)</span><span class="kpi-val" id="k-mat" style="color:#FF9933">0.0%</span></div>
  </div>

  <!-- Fila 4: Gráfica -->
  <div id="chart"></div>

</div>

<script>
(function() {{
  const D = {payload};
  const n = D.t.length;
  const maxDays = D.maxDays;

  const btn    = document.getElementById('btn-play');
  const slider = document.getElementById('t-slider');
  const diagEl = document.getElementById('diag-box');
  const kLbl   = document.getElementById('k-mat-lbl');
  kLbl.textContent = D.matLabel;

  /*  Inicializar Plotly con base vacía  */
  const layout = {{
    paper_bgcolor:'rgba(0,0,0,0)',
    plot_bgcolor:'rgba(0,0,0,0)',
    font:{{ color:'#ccc', family:'Inter,sans-serif' }},
    margin:{{ l:50, r:15, t:40, b:50 }},
    height:450,
    showlegend: false,
    xaxis:{{ title:D.xAxisLbl, range:[0,maxDays], color:'#aaa',
             gridcolor:'rgba(255,255,255,0.05)', zeroline:false, fixedrange:true, automargin:true }},
    yaxis:{{ title:'Concentración (%)', range:[0,105], color:'#aaa',
             gridcolor:'rgba(255,255,255,0.05)', zeroline:false, fixedrange:true, automargin:true }},
    shapes:[{{
      type:'line', x0:0, x1:0, y0:0, y1:105,
      line:{{color:'white',width:2,dash:'dot'}}
    }}],
    annotations:[{{
      x:0.02, y:0.97, xref:'paper', yref:'paper',
      text:D.dayLabel+' 0.0', showarrow:false,
      xanchor:'left', yanchor:'top',
      font:{{color:'white',size:17,family:'monospace'}},
      bgcolor:'rgba(0,0,0,0.55)', borderpad:5
    }}],
    dragmode:false,
  }};

  const config = {{ displayModeBar:false, staticPlot:true, responsive:true }};
  
  // Trazos iniciales vacíos
  const initialTraces = [
    {{ x: D.t, y: Array(n).fill(null), mode:'lines', name:'FSH',             line:{{color:'#BC8BFF',width:3}} }},
    {{ x: D.t, y: Array(n).fill(null), mode:'lines', name:'LH',              line:{{color:'#FF3366',width:3}} }},
    {{ x: D.t, y: Array(n).fill(null), mode:'lines', name:'Estradiol (E2)',   line:{{color:'#58A6FF',width:3}} }},
    {{ x: D.t, y: Array(n).fill(null), mode:'lines', name:'Progesterona (P4)',line:{{color:'#00CC99',width:3}} }},
    {{ x: D.t, y: Array(n).fill(null), mode:'lines', name:D.matLabel.replace(/ /,'').replace(' (%)',''), line:{{color:'#FF9933',width:3}} }},
  ];

  /*  Estado de animación  */
  let curIdx    = 0;
  let playing   = false;
  let rafId     = null;
  let lastTime  = null;
  const stepsPerSec = n / 22.0;

  /*  Montaje Seguro de Gráfica  */
  Plotly.newPlot('chart', initialTraces, layout, config).then(() => {{
    btn.disabled = false;
    btn.textContent = ' Reproducir';
    slider.disabled = false;
    render(0);
  }});

  /*  Helpers de lógica  */
  function lerp(arr, i) {{
    const fi = Math.floor(i), ci = Math.min(fi+1, n-1);
    const frac = i - fi;
    return arr[fi] + frac*(arr[ci]-arr[fi]);
  }}

  function getPhase(t) {{
    for (const p of D.phases) {{
      if (t >= p.start && t < p.end) return p;
    }}
    return D.phases[D.phases.length-1];
  }}

  function getDiag(t) {{
    const phase = getPhase(t);
    const name  = phase.name;
    const sp    = D.species;
    const comp  = D.complication;
    const preg  = D.pregnancy;
    const unit  = sp==='Ave' ? 'Hora' : 'Día';
    const val   = t.toFixed(1);

    if (sp==='Ave') {{
      if (comp==='Estrés por Calor')
        return [unit+' '+val+' — Estrés Calor: Supresión GnRH, pico LH caído. Postura reducida 15-30%.','error'];
      if (comp.startsWith('Fotop'))
        return [unit+' '+val+' — Fotoperíodo Inadecuado: Melatonina suprime eje HHG. Jerarquía folicular detenida.','error'];
      if (comp.startsWith('Agot'))
        return [unit+' '+val+' — Agotamiento Ovárico / Muda: Reposo reproductivo forzado.','error'];
      if (name==='Post-oviposición') return [unit+' '+val+' — Normal: Oviposición completada. Nuevo ciclo ovulatorio iniciando.','info'];
      if (name==='Pico LH / Ovulación') return [unit+' '+val+' — Normal: Pico LH activo. Folículo F1 ovulando.','success'];
      if (name==='Formación del huevo') return [unit+' '+val+' — Normal: Tránsito oviductal en curso. Calcificación activa.','info'];
      return [unit+' '+val+' — Normal: Oviposición inminente. Contracciones uterinas.','success'];
    }}

    if (preg) {{
      if (['Bovino','Ovino','Caprino'].includes(sp))
        return [unit+' '+val+' — GESTACIÓN ACTIVA: Reconocimiento materno (IFN-τ) exitoso. PGF2α bloqueada, CL mantenido.','success'];
      if (sp==='Porcino') return [unit+' '+val+' — GESTACIÓN ACTIVA: Estrógenos embrionarios bloquean luteólisis.','success'];
      if (sp==='Equino')  return [unit+' '+val+' — GESTACIÓN ACTIVA: Movilidad del concepto frena PGF2α. CL mantenido.','success'];
    }}
    if (comp==='Balance Energético Negativo (BEN)')
      return [unit+' '+val+' — BEN: Anestro por déficit energético. Eje HHG apagado.','error'];
    if (comp==='Cuerpo Lúteo Persistente')
      return [unit+' '+val+' — CL Persistente: Bloqueo en fase lútea. Falla uterina de PGF2α.','error'];
    if (comp==='Estrés Calórico') {{
      if (name==='Estro') return [unit+' '+val+' — Estrés Calórico: Celo Silencioso. Pico E2 deprimido.','warning'];
      return [unit+' '+val+' — Estrés Calórico: Calidad ovocitaria comprometida.','warning'];
    }}
    if (name==='Estro')    return [unit+' '+val+' — Normal (Estro): Máxima receptividad. Verificar ventana IA.','success'];
    if (name==='Proestro') return [unit+' '+val+' — Normal (Proestro): Crecimiento folicular. E2 en ascenso.','info'];
    if (name==='Metaestro')return [unit+' '+val+' — Normal (Metaestro): Luteinización en curso. P4 iniciando.','info'];
    return [unit+' '+val+' — Normal (Diestro): Dominancia P4. Útero preparado para gestación.','info'];
  }}

  /*  Motor de Rendering Pre-grabado  */
  function render(i) {{
    i = Math.max(0, Math.min(i, n-1));
    curIdx = i;
    const t   = D.t[Math.floor(i)]; // Evitar interpolar el tiempo
    const fsh = lerp(D.fsh, i);
    const lh  = lerp(D.lh,  i);
    const e2  = lerp(D.e2,  i);
    const p4  = lerp(D.p4,  i);
    const mat = lerp(D.mat, i);

    // KPIs
    document.getElementById('k-fsh').textContent = fsh.toFixed(1)+'%';
    document.getElementById('k-lh').textContent  = lh.toFixed(1)+'%';
    document.getElementById('k-e2').textContent  = e2.toFixed(1)+'%';
    document.getElementById('k-p4').textContent  = p4.toFixed(1)+'%';
    document.getElementById('k-mat').textContent = mat.toFixed(1)+'%';

    // Diagnóstico
    const [msg, tipo] = getDiag(t);
    diagEl.textContent = msg;
    diagEl.className = tipo;

    // Slider
    slider.value = i;
    const pct = (i/(n-1)*100).toFixed(1);
    slider.style.background = `linear-gradient(to right,#00E676 0%,#00E676 ${{pct}}%,rgba(255,255,255,0.12) ${{pct}}%)`;

    // Reconstruir los frames exactos (pre-grabados)
    const newTraces = [
      {{ x: D.t, y: D.fsh.map((v,j) => j<=i ? v : null), mode:'lines', name:'FSH', line:{{color:'#BC8BFF',width:3}} }},
      {{ x: D.t, y: D.lh.map((v,j) => j<=i ? v : null),  mode:'lines', name:'LH', line:{{color:'#FF3366',width:3}} }},
      {{ x: D.t, y: D.e2.map((v,j) => j<=i ? v : null),  mode:'lines', name:'Estradiol (E2)', line:{{color:'#58A6FF',width:3}} }},
      {{ x: D.t, y: D.p4.map((v,j) => j<=i ? v : null),  mode:'lines', name:'Progesterona (P4)', line:{{color:'#00CC99',width:3}} }},
      {{ x: D.t, y: D.mat.map((v,j) => j<=i ? v : null), mode:'lines', name:D.matLabel.replace(/ /,'').replace(' (%)',''), line:{{color:'#FF9933',width:3}} }}
    ];

    layout.shapes[0].x0 = t;
    layout.shapes[0].x1 = t;
    layout.annotations[0].text = D.dayLabel+' '+t.toFixed(1);

    // Reactualización balística en la tarjeta gráfica del navegador
    Plotly.react('chart', newTraces, layout, config);
  }}

  /*  Loop de animación  */
  function animLoop(ts) {{
    if (!playing) return;
    if (lastTime === null) lastTime = ts;
    const dt = (ts - lastTime) / 1000.0;
    lastTime  = ts;
    
    const step = stepsPerSec * dt;
    const next = curIdx + step;
    
    if (next >= n-1) {{
      render(n-1);
      stopPlay();
      return;
    }}
    render(next);
    rafId = requestAnimationFrame(animLoop);
  }}

  function startPlay() {{
    if (curIdx >= n-1) curIdx = 0;
    playing  = true;
    lastTime = null;
    btn.textContent = ' Pausar';
    btn.classList.add('paused');
    slider.disabled = true;
    rafId = requestAnimationFrame(animLoop);
  }}

  function stopPlay() {{
    playing = false;
    if (rafId) cancelAnimationFrame(rafId);
    rafId = null;
    lastTime = null;
    btn.textContent = ' Reproducir';
    btn.classList.remove('paused');
    slider.disabled = false;
  }}

  btn.addEventListener('click', () => {{
    if (playing) stopPlay(); else startPlay();
  }});

  slider.addEventListener('input', () => {{
    if (playing) stopPlay();
    render(parseInt(slider.value));
  }});

}})();
</script>
</body>
</html>
"""

    import streamlit.components.v1 as _components
    _components.html(sim_html, height=800, scrolling=False)


if st.session_state.etapa_actual == "portada":
  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown("""
  <style>
    .portada-container {
        /* Fondo con imagen de vacas en el prado, superpuesto con un gradiente oscuro para legibilidad */
        background: linear-gradient(to bottom, rgba(14, 17, 23, 0.7), rgba(14, 17, 23, 0.95)),
                    url('https://images.unsplash.com/photo-1546445317-29f4545e9d53?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        padding: 60px 20px 40px 20px;
        border-radius: 24px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(0, 230, 118, 0.2);
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        animation: panBg 30s infinite alternate ease-in-out;
    }
    @keyframes panBg {
        0% { background-position: 0% 50%; background-size: 110%; }
        100% { background-position: 100% 50%; background-size: 125%; }
    }
    .hero-badge {
        display: inline-block;
        background: rgba(0, 230, 118, 0.1);
        border: 1px solid rgba(0, 230, 118, 0.3);
        color: #00E676;
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 24px;
        box-shadow: 0 0 20px rgba(0,230,118,0.15);
    }
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        background: linear-gradient(180deg, #ffffff 0%, #b0bec5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.1;
        letter-spacing: -1.5px;
        text-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .hero-subtitle {
        font-size: 1.4rem;
        font-weight: 400;
        color: #8b949e;
        margin: 15px 0 40px 0;
        letter-spacing: 0.5px;
    }
    .sazon-card {
        background: linear-gradient(145deg, rgba(22, 33, 25, 0.6) 0%, rgba(12, 22, 16, 0.8) 100%);
        padding: 45px 50px;
        border-radius: 20px;
        border: 1px solid rgba(76, 175, 80, 0.2);
        border-top: 4px solid #00E676;
        text-align: center;
        margin: 0 auto 40px auto;
        max-width: 900px;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        position: relative;
        overflow: hidden;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.4s ease;
    }
    .sazon-card:hover {
        transform: translateY(-8px);
        border-color: rgba(0, 230, 118, 0.5);
        box-shadow: 0 30px 60px rgba(0,230,118,0.15);
    }
    .features-grid {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 16px;
        margin-top: 32px;
    }
    .feat-item {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 12px 24px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 12px;
        color: #e6edf3;
        font-weight: 600;
        font-size: 0.95rem;
        transition: background 0.3s ease;
    }
    .feat-item:hover {
        background: rgba(255,255,255,0.08);
    }
    .feat-icon {
        font-size: 1.4rem;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }
  </style>

  <div class="portada-container animate-fade-in">
    <div style="text-align: center;">
      <h1 class="hero-title">CICLO ESTRAL</h1>
      <h3 class="hero-subtitle">Fisiología Reproductiva Comparada y Tecnologías de IA</h3>
    </div>
    <div class="sazon-card">
      <p style='font-size: 1.18rem; font-weight: 300; line-height: 1.8; color: #E8F5E9; margin: 0; text-align: justify;'>
        El ciclo estral es el motor biológico de la producción pecuaria. Esta herramienta simula con rigor científico el comportamiento endocrino (FSH, LH, E₂, P₄, PGF₂α) de las principales especies de granja. Analiza de manera fluida y precisa las curvas hormonales, diagnostica patologías y domina la fisiología comparada para optimizar la eficiencia reproductiva y el manejo veterinario.
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

  #  Dos botones de ruta directa al módulo de preguntas 
  col_b1, col_b2, col_b3 = st.columns([1, 1.2, 1])
  with col_b2:

    st.markdown("""
    <style>
    .link-card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-decoration: none !important;
        display: block;
        height: 100%;
        box-sizing: border-box;
    }
    .link-card * {
        text-decoration: none !important;
    }
    .link-card:hover {
        transform: translateY(-5px);
    }
    .link-card-green:hover {
        box-shadow: 0 12px 40px rgba(0,230,118,0.3) !important;
        border: 1px solid #00E676 !important;
    }
    .link-card-purple:hover {
        box-shadow: 0 12px 40px rgba(224,64,251,0.3) !important;
        border: 1px solid #E040FB !important;
    }
    </style>
    <div style='display:flex;gap:20px;margin-bottom:20px;justify-content:center;align-items:stretch;'>
      
      <a href="?nav_to=banco" target="_self" class="link-card link-card-green" style='text-decoration:none !important;flex:1;background:linear-gradient(145deg, rgba(76,175,80,0.1) 0%, rgba(20,40,25,0.85) 100%);padding:22px 18px;border-radius:16px;border:1px solid rgba(76,175,80,0.4);border-top:5px solid #00E676;text-align:center;box-shadow:0 8px 30px rgba(0,0,0,0.6);'>
        <p style='margin:0 0 10px 0;color:#00E676;font-weight:900;font-size:1.05rem;letter-spacing:2px;text-transform:uppercase;text-shadow:0 2px 8px rgba(0,230,118,0.4);'>Banco de Preguntas</p>
        <p style='margin:0;color:#E0E0E0;font-size:0.85rem;line-height:1.6;'><b>55 preguntas interactivas.</b><br>Prepárate para la evaluación real.</p>
      </a>

      <a href="?nav_to=examen" target="_self" class="link-card link-card-purple" style='text-decoration:none !important;flex:1;background:linear-gradient(145deg, rgba(156,39,176,0.1) 0%, rgba(40,20,45,0.85) 100%);padding:22px 18px;border-radius:16px;border:1px solid rgba(156,39,176,0.4);border-top:5px solid #E040FB;text-align:center;box-shadow:0 8px 30px rgba(0,0,0,0.6);'>
        <p style='margin:0 0 10px 0;color:#E040FB;font-weight:900;font-size:1.05rem;letter-spacing:2px;text-transform:uppercase;text-shadow:0 2px 8px rgba(224,64,251,0.4);'>Evaluación Estral</p>
        <p style='margin:0;color:#E0E0E0;font-size:0.85rem;line-height:1.6;'><b>20 preguntas aleatorias.</b><br>Umbral de aprobación: 80%.</p>
      </a>

    </div>
    """, unsafe_allow_html=True)

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
  if not (st.session_state.get("eval_vista") == "examen" and st.session_state.get("eval_fase") == "activo"):
    col_back2, _ = st.columns([1, 5])
    with col_back2:
      if st.button("Volver al Inicio", use_container_width=True, key="btn_volver_eval"):
        st.session_state.etapa_actual = "portada"
        st.session_state.examen_desbloqueado = False
        st.session_state.examen_registrado = False
        st.session_state.eval_vista = "practica"
        st.rerun()

  # CSS Premium para Radio Buttons y Evaluación
  st.markdown("""
    <style>
      .stRadio div[role="radiogroup"] { gap: 14px; }
      .stRadio div[role="radiogroup"] > label {
          background: rgba(255, 255, 255, 0.03);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 12px;
          padding: 16px 22px;
          transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
          cursor: pointer;
          margin: 0;
      }
      .stRadio div[role="radiogroup"] > label:hover {
          background: rgba(239, 83, 80, 0.08);
          border-color: rgba(239, 83, 80, 0.4);
          transform: translateY(-3px);
          box-shadow: 0 6px 20px rgba(0,0,0,0.25);
      }
      .stRadio div[role="radiogroup"] > label:has(input:checked) {
          background: rgba(76, 175, 80, 0.15) !important;
          border-color: #4CAF50 !important;
          box-shadow: 0 0 0 1px #4CAF50, 0 6px 20px rgba(76,175,80,0.25) !important;
      }
      .stRadio div[role="radiogroup"] > label p {
          font-size: 1.05rem !important;
          color: #E0E0E0 !important;
          font-weight: 500;
          margin: 0 !important;
      }
      .stRadio div[role="radiogroup"] > label:has(input:checked) p {
          color: #4CAF50 !important;
          font-weight: 700;
      }
      /* Ocultar el círculo nativo */
      .stRadio div[role="radiogroup"] > label > div:first-child { display: none; }
      /* Forzar borde rojo para botón de volver al inicio u otros */
      div.stButton > button { border-left-color: #EF5350 !important; }
    </style>
  """, unsafe_allow_html=True)

  # Cabecera del módulo
  fase_actual = st.session_state.get("eval_fase", "")
  
  render_header = st.session_state.get("eval_estudiante", {}).get("rol", "") != "admin"
  if render_header:
      if fase_actual == "activo":
          # Diseño de Electrocardiograma para EVALUACION REAL (vida o muerte)
          color_latido = "#EF5350"
          velocidad_corazon = "0.35s"
          path_points = ["M 0 60"]
          x = 0
          for _ in range(7):
              path_points.append(f"L {x+15} 60 Q {x+25} 50 {x+35} 60 L {x+40} 60 L {x+45} 75 L {x+55} -10 L {x+65} 130 L {x+70} 60 L {x+80} 60 Q {x+90} 45 {x+105} 60")
              x += 125
          path_points.append("L 1000 60")
          path_d_active = " ".join(path_points)
          
          st.markdown(
            f"<style>"
            f"@keyframes heartbeat {{ 0% {{ transform: scale(1); }} 15% {{ transform: scale(1.15); }} 30% {{ transform: scale(1); }} 45% {{ transform: scale(1.15); }} 70% {{ transform: scale(1); }} 100% {{ transform: scale(1); }} }}"
            f"@keyframes drawSweepActive {{ 0% {{ stroke-dashoffset: 3500; opacity: 1; }} 75% {{ stroke-dashoffset: 0; opacity: 1; }} 90% {{ stroke-dashoffset: 0; opacity: 0; }} 95% {{ stroke-dashoffset: 3500; opacity: 0; }} 100% {{ stroke-dashoffset: 3500; opacity: 1; }} }}"
            f"</style>"
            f"<div style='background:linear-gradient(135deg,rgba(18,18,18,0.9),rgba(8,8,8,0.95)); padding:28px 36px; border-radius:14px; border-top:4px solid #EF5350; border:1px solid rgba(239,83,80,0.5); box-shadow: 0 0 25px rgba(239,83,80,0.4); margin-bottom:28px; position:relative; overflow:hidden;'>"
            f"  <svg width='100%' height='100%' viewBox=\"0 0 1000 120\" preserveAspectRatio=\"none\" style='position:absolute; top:0; left:0; z-index:0; opacity: 0.35;'>"
            f"    <path d='{path_d_active}' fill='none' stroke='{color_latido}' stroke-width='4' stroke-linecap='round' stroke-linejoin='round' style='stroke-dasharray: 3500; stroke-dashoffset: 3500; animation: drawSweepActive 1.2s infinite;'/>"
            f"  </svg>"
            f"  <svg width='80' height='80' viewBox='0 0 100 100' style='position:absolute; top:50%; right:20px; transform:translateY(-50%); z-index:5; filter: drop-shadow(0px 0px 15px {color_latido}); animation: heartbeat {velocidad_corazon} infinite;'>"
            f"    <g fill='{color_latido}' stroke='{color_latido}' stroke-width='2' stroke-linejoin='round'>"
            f"      <path d='M45,28 C45,10 55,5 65,15 C68,18 68,22 62,26' fill='none' stroke-width='8'/>"
            f"      <path d='M35,32 C35,15 40,10 45,10' fill='none' stroke-width='6'/>"
            f"      <path d='M58,35 C70,25 80,25 82,32' fill='none' stroke-width='7'/>"
            f"      <path d='M38,30 C15,25 10,55 35,78 C45,88 52,92 55,90 C70,75 88,50 72,32 C65,22 55,22 48,28 C45,25 42,25 38,30 Z' />"
            f"    </g>"
            f"  </svg>"
            f"  <div style='position:relative; z-index:10; pointer-events:none;'>"
            f"    <h2 style='margin:0 0 6px 0;color:#FFCDD2;font-weight:900;letter-spacing:1.5px; text-shadow: 0 0 12px rgba(239,83,80,0.8);'>MODULO DE EVALUACIÓN</h2>"
            f"    <p style='margin:0;color:#E2E8F0;font-size:0.95rem; font-weight: 500;'>Ciclo Estral Comparado - Fisiología Animal Aplicada</p>"
            f"  </div>"
            f"</div>",
            unsafe_allow_html=True
          )
      else:
          # Diseño sobrio y academico para MODO PRACTICA (Banco de Preguntas)
          st.markdown(
            f"<div style='background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 1)); padding:28px 36px; border-radius:14px; border-left: 5px solid #3B82F6; border: 1px solid rgba(59, 130, 246, 0.2); box-shadow: 0 10px 25px rgba(0,0,0,0.3); margin-bottom:28px;'>"
            f"  <div style='position:relative; z-index:10;'>"
            f"    <h2 style='margin:0 0 6px 0; color:#F8FAFC; font-weight:800; letter-spacing:1px;'>MODULO DE EVALUACIÓN (PRÁCTICA)</h2>"
            f"    <p style='margin:0; color:#94A3B8; font-size:0.95rem; font-weight: 500;'>Ciclo Estral Comparado - Fisiología Animal Aplicada</p>"
            f"  </div>"
            f"</div>",
            unsafe_allow_html=True
          )

  # Guardias de estado
  if "eval_vista" not in st.session_state:
    st.session_state.eval_vista = st.query_params.get("vista", "practica")
  if "examen_desbloqueado" not in st.session_state:
    st.session_state.examen_desbloqueado = False
  if "practica_respuestas" not in st.session_state:
    st.session_state.practica_respuestas = {}
    
  if "practica_orden" not in st.session_state or len(st.session_state.practica_orden) != len(BANCO_PREGUNTAS):
    import random
    orden = list(range(len(BANCO_PREGUNTAS)))
    random.shuffle(orden)
    st.session_state.practica_orden = orden

  #  RUTA A: Banco de Práctica (público, interactivo con st.radio) 
  if st.session_state.eval_vista == "practica":
    st.markdown(
      "<div style='background:rgba(76,175,80,0.06);padding:16px 22px;border-radius:10px;"
      "border:1px solid rgba(76,175,80,0.2);margin-bottom:24px;'>"
      "<p style='margin:0;color:#B0BEC5;font-size:0.88rem;'>"
      "Modo de practica libre. Las preguntas han sido aleatorizadas. Resuelve las preguntas e identifica la respuesta correcta "
      "resaltada en verde. Sin limite de tiempo ni calificacion final."
      "</p></div>",
      unsafe_allow_html=True
    )

    COLORES = ["#4CAF50", "#58A6FF", "#FF9933", "#BC8BFF", "#FF3366", "#00CC99"]

    for i, q_idx in enumerate(st.session_state.practica_orden):
      # Prevención de IndexError si el caché está desincronizado
      if q_idx >= len(BANCO_PREGUNTAS):
          continue
          
      q = BANCO_PREGUNTAS[q_idx]
      num = i + 1
      cg = COLORES[i % len(COLORES)]
      
      st.markdown(
        f"<div style='background: linear-gradient(145deg, rgba(30,41,35,0.8), rgba(20,28,24,0.9));"
        f"border-left: 5px solid {cg}; padding: 24px 30px; border-radius: 12px;"
        f"box-shadow: 0 8px 32px rgba(0,0,0,0.3); margin-bottom: 20px; backdrop-filter: blur(10px);'>"
        f"<h3 style='margin:0;color:#E8F5E9;font-size:1.25rem;font-weight:600;line-height:1.6;'>"
        f"<span style='color:{cg};font-size:1.4rem;margin-right:8px;'>{num}.</span> {q['pregunta']}</h3>"
        f"</div>",
        unsafe_allow_html=True
      )
      
      is_answered = f"practica_q_{q_idx}_done" in st.session_state and st.session_state[f"practica_q_{q_idx}_done"]
      seleccion = None
      
      if q["tipo"] == "opcion_multiple":
          val = st.radio(
            label=f"Pregunta {num}", options=q["opciones"],
            index=None, key=f"practica_q_{q_idx}", label_visibility="collapsed",
            disabled=is_answered
          )
          if val is not None:
              seleccion = q["opciones"].index(val)

      elif q["tipo"] == "emparejar":
          st.markdown("<p style='color:#B0BEC5; font-weight:500; font-size: 1.05rem; margin-bottom: 12px;'>Empareja cada concepto:</p>", unsafe_allow_html=True)
          sel_dict = {}
          for par in q["pares"]:
              c1, c2 = st.columns([1, 1.2])
              with c1:
                  st.markdown(f"<div style='background:rgba(255,255,255,0.03); padding:10px 15px; border-radius:8px; border-left:4px solid #58A6FF; display:flex; align-items:center; height:100%;'><p style='margin:0; font-weight:500; font-size:1rem; color:#E0E0E0;'>{par}</p></div>", unsafe_allow_html=True)
              with c2:
                  opts = ["Seleccionar..."] + q["opciones"]
                  val = st.selectbox(f"Match {par}", opts, key=f"prac_emp_{q_idx}_{par}", disabled=is_answered, label_visibility="collapsed")
                  if val != "Seleccionar...":
                      sel_dict[par] = val
              st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)
          
          if len(sel_dict) == len(q["pares"]):
              seleccion = sel_dict

      elif q["tipo"] == "completar_espacios":
          st.markdown("<p style='color:#B0BEC5; font-weight:500; font-size: 1.05rem; margin-bottom: 12px;'>Completa los espacios en blanco:</p>", unsafe_allow_html=True)
          sel_dict = {}
          cols = st.columns(len(q["opciones"]))
          for col_idx, (esp_num, opts_esp) in enumerate(q["opciones"].items()):
              with cols[col_idx]:
                  st.markdown(f"<p style='color:#4CAF50; font-weight:600; margin-bottom:4px;'>Espacio [{esp_num}]:</p>", unsafe_allow_html=True)
                  opts = ["Seleccionar..."] + opts_esp
                  val = st.selectbox(f"Espacio {esp_num}", opts, key=f"prac_comp_{q_idx}_{esp_num}", disabled=is_answered, label_visibility="collapsed")
                  if val != "Seleccionar...":
                      sel_dict[esp_num] = val
          st.markdown("<br/>", unsafe_allow_html=True)
          
          if len(sel_dict) == len(q["opciones"]):
              seleccion = sel_dict

      if is_answered or seleccion is not None:
          if not is_answered:
              st.session_state[f"practica_q_{q_idx}_done"] = True
              st.session_state[f"practica_q_{q_idx}_ans"] = seleccion
              st.rerun()

          ans = st.session_state.get(f"practica_q_{q_idx}_ans")
          es_correcta = (ans == q["correcta"])

          if es_correcta:
            st.markdown(
              "<div style='background: rgba(76,175,80,0.15); padding: 16px 22px;"
              "border-radius: 10px; border-left: 4px solid #4CAF50; margin-bottom: 30px;"
              "box-shadow: 0 4px 20px rgba(76,175,80,0.15);'>"
              "<p style='margin:0; color:#4CAF50; font-size:1.05rem; font-weight:700;'>"
              " Respuesta correcta.</p></div>",
              unsafe_allow_html=True
            )
          else:
            if q["tipo"] == "opcion_multiple":
                correct_text = q['opciones'][q['correcta']]
            elif q["tipo"] == "emparejar":
                correct_text = "<br/>" + "<br/>".join([f"• <b style='color:#58A6FF;'>{k}</b>: {v}" for k, v in q['correcta'].items()])
            else:
                correct_text = "<br/>" + "<br/>".join([f"• <b>Espacio [{k}]</b>: {v}" for k, v in q['correcta'].items()])

            st.markdown(
              f"<div style='background: rgba(239,83,80,0.1); padding: 16px 22px;"
              f"border-radius: 10px; border-left: 4px solid #EF5350; margin-bottom: 30px;"
              f"box-shadow: 0 4px 20px rgba(239,83,80,0.15);'>"
              f"<p style='margin:0; color:#EF5350; font-size:1.05rem; font-weight:700; margin-bottom: 6px;'>"
              f" Respuesta incorrecta.</p>"
              f"<p style='margin:0; color:#E0E0E0; font-size:1rem;'>"
              f"La respuesta correcta es: <span style='color:#4CAF50; font-weight:600;'>{correct_text}</span></p></div>",
              unsafe_allow_html=True
            )
      st.markdown("<br>", unsafe_allow_html=True)

  #  RUTA B: Evaluación Formal (protegida con contraseña agroestral2026) 
  elif st.session_state.eval_vista == "examen":
    if not st.session_state.examen_desbloqueado:
      st.markdown("<br>", unsafe_allow_html=True)
      st.markdown(
        "<div style='max-width:460px; margin:0 auto; padding:40px 45px;"
        "background: linear-gradient(135deg, rgba(22,10,10,0.8), rgba(12,8,8,0.95));"
        "border: 1px solid rgba(239, 83, 80, 0.4); border-top: 4px solid #EF5350; border-radius: 20px;"
        "backdrop-filter: blur(15px); box-shadow: 0 15px 40px rgba(0,0,0,0.6); text-align:center; position: relative; overflow: hidden;'>"
        "<div style='position:absolute; top:-50%; left:-50%; width:200%; height:200%; background: radial-gradient(circle, rgba(239,83,80,0.08) 0%, transparent 60%); pointer-events:none;'></div>"
        "<h3 style='color:#F8FAFC; margin:0 0 10px 0; font-size:1.4rem; font-weight:700; letter-spacing: 0.5px;'>Evaluacion Formal Protegida</h3>"
        "<p style='color:#94A3B8; font-size:0.95rem; margin:0 0 25px 0; line-height: 1.5;'>"
        "Esta seccion requiere contrasena de acceso.<br>Solicitala a tu docente.</p>"
        "</div>",
        unsafe_allow_html=True
      )
      col_pw1, col_pw2, col_pw3 = st.columns([1, 1, 1])
      with col_pw2:
        st.markdown("<br>", unsafe_allow_html=True)
        clave = st.text_input(
          "Contrasena", type="password",
          placeholder="Ingresa la contrasena",
          key="input_clave_examen", label_visibility="collapsed"
        )
        if st.button("INGRESAR", use_container_width=True, type="primary", key="btn_unlock_examen"):
          if clave == "agroestral2026":
            st.session_state.examen_desbloqueado = True
            st.session_state.examen_registrado = False
            st.success("Acceso concedido. Cargando registro...")
            st.rerun()
          else:
            st.error("Contrasena incorrecta. Intentalo de nuevo.")
    else:
      if not st.session_state.get("examen_registrado", False):
        st.markdown("<br>", unsafe_allow_html=True)
        col_reg1, col_reg2, col_reg3 = st.columns([1, 1, 1])
        with col_reg2:
          st.markdown(
            "<div style='padding:35px 40px; background: linear-gradient(135deg, rgba(18,18,18,0.9), rgba(8,8,8,0.95));"
            "border: 1px solid rgba(239, 83, 80, 0.4); border-top: 4px solid #EF5350; border-radius: 20px;"
            "margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);'>"
            "<h3 style='color:#F8FAFC; margin:0 0 15px 0; text-align:center; font-weight:700; font-size:1.3rem;'>Registro de Estudiante</h3>"
            "<p style='color:#94A3B8; font-size:0.95rem; text-align:center; margin-bottom:0; line-height:1.6;'>"
            "Por favor, completa tus datos para iniciar la evaluación.<br>"
            "<span style='color:#EF5350; font-weight:600;'>Nota:</span> Tendrás un límite estricto de 20 minutos una vez inicies.</p>"
            "</div>", unsafe_allow_html=True
          )
          nombre = st.text_input("Nombre y Apellido", key="reg_nombre")
          carrera = st.text_input("Carrera", key="reg_carrera")
          curso = st.text_input("Curso", key="reg_curso")
          
          st.markdown("<br>", unsafe_allow_html=True)
          if st.button("CONTINUAR A LA EVALUACIÓN", use_container_width=True, type="primary"):
            if nombre and carrera and curso:
              if nombre.strip() == "ADMIN" and carrera.strip() == "ESTRAL" and curso.strip() == "2026":
                st.session_state.eval_estudiante = {"nombre": "ADMIN", "rol": "admin"}
                st.session_state.examen_registrado = True
                st.session_state.eval_fase = "admin_dashboard"
                st.rerun()
              else:
                st.session_state.eval_estudiante = {"nombre": nombre, "carrera": carrera, "curso": curso, "rol": "student"}
                st.session_state.examen_registrado = True
                st.session_state.eval_fase = "inicio"
                st.rerun()
            else:
              st.error("Por favor, llena todos los campos.")
      else:
        rol = st.session_state.eval_estudiante.get("rol", "student")
        if rol == "admin":
            st.markdown("""
<div style='text-align:center; padding:35px 25px; background:linear-gradient(135deg, rgba(15, 23, 42, 0.85), rgba(8, 15, 30, 0.95)); border-radius:16px; margin-bottom:30px; border: 1px solid rgba(99, 102, 241, 0.4); border-top: 4px solid #6366F1; box-shadow: 0 15px 40px rgba(0,0,0,0.5); backdrop-filter: blur(15px); position:relative; overflow:hidden;'>
    <div style='position:absolute; top:-50%; left:-50%; width:200%; height:200%; background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 50%); pointer-events:none;'></div>
    <h2 style='color:#F8FAFC; margin:0; font-weight:800; font-size:1.6rem; letter-spacing: 1.5px; position:relative; z-index:2; text-shadow: 0 0 15px rgba(99,102,241,0.6);'>
        <span style='color:#6366F1;'>■</span> PANEL DE CONTROL DOCENTE
    </h2>
    <p style='color:#94A3B8; margin-top:10px; margin-bottom:0; font-size:0.95rem; font-weight:500; position:relative; z-index:2;'>Centro de Mando Analítico en Tiempo Real</p>
</div>
""", unsafe_allow_html=True)
            gs = get_global_exam_state()
            
            # --- TARJETAS DE CONTROL ---
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("""
                <div style='background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.9)); padding: 25px; border-radius: 12px; border: 1px solid rgba(99, 102, 241, 0.5); box-shadow: 0 0 20px rgba(99, 102, 241, 0.2); margin-bottom: 20px; text-align: center;'>
                    <h3 style='color:#818CF8; margin:0 0 10px 0; font-weight:800; letter-spacing:1px;'>AGENDAMIENTO</h3>
                    <p style='color:#94A3B8; font-size:0.95rem; margin:0;'>Programa la hora exacta de inicio de la evaluación.</p>
                </div>
                <style>
                div[data-testid="stTextInput"] input {
                    font-size: 1.25rem !important;
                    padding: 16px !important;
                    border: 2px solid #818CF8 !important;
                    border-radius: 10px !important;
                    background-color: rgba(15, 23, 42, 0.9) !important;
                    color: #FFFFFF !important;
                    text-align: center !important;
                    box-shadow: 0 0 15px rgba(129, 140, 248, 0.2) !important;
                    transition: all 0.3s ease;
                }
                div[data-testid="stTextInput"] input:focus {
                    border-color: #A5B4FC !important;
                    box-shadow: 0 0 25px rgba(165, 180, 252, 0.4) !important;
                }
                </style>
                """, unsafe_allow_html=True)
                if not gs["activo"]:
                    hora_prog_str = st.text_input("Hora", value="", placeholder="Escribe la hora (Ej: 14:00) o deja vacío para iniciar AHORA", label_visibility="collapsed")
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("INICIAR / AGENDAR EXAMEN", type="primary", use_container_width=True):
                        try:
                            gs["activo"] = True
                            if not hora_prog_str.strip():
                                gs["hora_inicio"] = datetime.datetime.now()
                            else:
                                hora_prog = datetime.datetime.strptime(hora_prog_str.strip(), "%H:%M").time()
                                hoy = datetime.datetime.now().date()
                                gs["hora_inicio"] = datetime.datetime.combine(hoy, hora_prog)
                            st.rerun()
                        except ValueError:
                            gs["activo"] = False
                            st.error("Formato incorrecto (usa HH:MM, Ej: 14:30)")
                else:
                    ahora = datetime.datetime.now()
                    if ahora < gs["hora_inicio"]:
                        st.info(f"Examen agendado para las {gs['hora_inicio'].strftime('%H:%M:%S')}")
                    else:
                        st.success(f"Examen Activo (Iniciado a las {gs['hora_inicio'].strftime('%H:%M:%S')})")
                        faltan = 1200 - (ahora - gs["hora_inicio"]).total_seconds()
                        if faltan > 0:
                            st.info(f"Tiempo restante: {int(faltan//60)}m {int(faltan%60)}s")
                        else:
                            st.error("Ventana de 20 minutos expirada.")
                
            with c2:
                st.markdown("""
                <div style='background: linear-gradient(145deg, rgba(69, 10, 10, 0.9), rgba(30, 10, 10, 0.9)); padding: 25px; border-radius: 12px; border: 1px solid rgba(239, 83, 80, 0.5); box-shadow: 0 0 20px rgba(239, 83, 80, 0.2); margin-bottom: 20px; text-align: center;'>
                    <h3 style='color:#EF5350; margin:0 0 10px 0; font-weight:800; letter-spacing:1px;'>CIERRE DE EMERGENCIA</h3>
                    <p style='color:#FCA5A5; font-size:0.95rem; margin:0;'>Forzar el cierre detendrá la evaluación global y reiniciará el reloj.</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("CERRAR Y RESETEAR EXAMEN", use_container_width=True):
                    gs["activo"] = False
                    gs["hora_inicio"] = None
                    st.rerun()

            st.markdown("<br><hr style='border-color:rgba(255,255,255,0.05);'><br>", unsafe_allow_html=True)
            
            # --- ANALÍTICAS Y MÉTRICAS ---
            st.markdown("<h3 style='color:#F8FAFC; margin-bottom:20px;'>Analíticas de Rendimiento</h3>", unsafe_allow_html=True)
            registros = gs["registros"]
            if not registros:
                st.info("No hay estudiantes registrados o evaluaciones completadas todavía.")
            else:
                aprobados = sum(1 for r in registros if r["nota"] >= 16)
                reprobados = len(registros) - aprobados
                tasa_aprobacion = (aprobados / len(registros)) * 100
                tiempos = [r["tiempo"] for r in registros]
                tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0
                
                fallos_totales = {}
                for r in registros:
                    for f in r.get("fallos", []):
                        fallos_totales[f] = fallos_totales.get(f, 0) + 1
                pregunta_mas_fallada = max(fallos_totales, key=fallos_totales.get) if fallos_totales else "N/A"
                
                # Tarjetas HTML
                st.markdown(f"""
                <div style='display:flex; gap:15px; margin-bottom:25px; flex-wrap:wrap;'>
                    <div style='flex:1; min-width:200px; background:rgba(22,33,25,0.7); padding:20px; border-radius:10px; border-top:3px solid #4CAF50; text-align:center;'>
                        <p style='margin:0; color:#94A3B8; font-size:0.9rem; font-weight:600; text-transform:uppercase;'>Tasa de Aprobación</p>
                        <h2 style='margin:10px 0 0 0; color:#F8FAFC; font-size:2.5rem;'>{tasa_aprobacion:.1f}%</h2>
                        <p style='margin:0; color:#64748B; font-size:0.85rem;'>{aprobados} de {len(registros)} aprobados</p>
                    </div>
                    <div style='flex:1; min-width:200px; background:rgba(22,33,25,0.7); padding:20px; border-radius:10px; border-top:3px solid #34D399; text-align:center;'>
                        <p style='margin:0; color:#94A3B8; font-size:0.9rem; font-weight:600; text-transform:uppercase;'>Tiempo Promedio</p>
                        <h2 style='margin:10px 0 0 0; color:#F8FAFC; font-size:2.5rem;'>{int(tiempo_promedio//60)}m {int(tiempo_promedio%60)}s</h2>
                        <p style='margin:0; color:#64748B; font-size:0.85rem;'>Resolución por estudiante</p>
                    </div>
                    <div style='flex:1; min-width:200px; background:rgba(22,33,25,0.7); padding:20px; border-radius:10px; border-top:3px solid #EF5350; text-align:center;'>
                        <p style='margin:0; color:#94A3B8; font-size:0.9rem; font-weight:600; text-transform:uppercase;'>Tema Crítico</p>
                        <h2 style='margin:10px 0 0 0; color:#F8FAFC; font-size:1.5rem; word-break:break-word;'>Pregunta #{pregunta_mas_fallada}</h2>
                        <p style='margin:0; color:#64748B; font-size:0.85rem;'>Ítem con más errores</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Gráficos de Plotly y Ranking
                chart_col1, chart_col2 = st.columns([1, 1.5])
                with chart_col1:
                    st.markdown("<h4 style='color:#E2E8F0; margin-bottom:0;'>Distribución de Rendimiento</h4>", unsafe_allow_html=True)
                    fig_pie = go.Figure(data=[go.Pie(labels=['Aprobados (≥16)', 'Reprobados (<16)'], 
                                                     values=[aprobados, reprobados], 
                                                     hole=.5,
                                                     marker_colors=['#34D399', '#F87171'],
                                                     textinfo='label+percent')])
                    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0'), showlegend=False, margin=dict(t=30, b=0, l=0, r=0), height=300)
                    st.plotly_chart(fig_pie, use_container_width=True)
                with chart_col2:
                    import pandas as pd
                    from collections import defaultdict

                    st.markdown("<h4 style='color:#E2E8F0; margin-bottom:15px;'>Historial y Ranking por Día</h4>", unsafe_allow_html=True)
                    
                    df = pd.DataFrame(registros)
                    if not df.empty:
                        df_export = df.copy()
                        if "key" in df_export.columns:
                            df_export = df_export.drop(columns=["key"])
                        if "fallos" in df_export.columns:
                            df_export = df_export.drop(columns=["fallos"])
                        
                        if "timestamp" in df_export.columns:
                            df_export["timestamp"] = df_export["timestamp"].apply(lambda x: str(x)[:10] if str(x) else x)
                            df_export = df_export.rename(columns={"timestamp": "Fecha"})
                            
                        if "nota" in df_export.columns:
                            df_export = df_export.rename(columns={"nota": "Nota (/20)"})
                            
                        if "tiempo" in df_export.columns:
                            df_export["tiempo"] = df_export["tiempo"].apply(lambda x: f"{int(x // 60):02d}:{int(x % 60):02d}")
                            df_export = df_export.rename(columns={"tiempo": "Tiempo (minutos)"})
                            
                        df_export.columns = [col.capitalize() if col not in ["Nota (/20)", "Tiempo (minutos)"] else col for col in df_export.columns]
                        
                        csv = df_export.to_csv(sep=';', encoding='utf-8-sig', index=False)
                        st.download_button(
                            label="Descargar Reporte (Excel CSV)",
                            data=csv,
                            file_name='reporte_calificaciones.csv',
                            mime='text/csv',
                        )
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        por_dia = defaultdict(list)
                        for r in registros:
                            dia = r.get("timestamp", "Desconocido")[:10] if "timestamp" in r else "Fecha Desconocida"
                            por_dia[dia].append(r)
                        
                        for dia in sorted(por_dia.keys(), reverse=True):
                            st.markdown(f"<h5 style='color:#94A3B8; border-bottom:1px solid #334155; padding-bottom:5px; margin-top:10px;'>Fecha: {dia}</h5>", unsafe_allow_html=True)
                            registros_dia = sorted(por_dia[dia], key=lambda x: x["nota"], reverse=True)
                            
                            for i, r in enumerate(registros_dia):
                                es_aprobado = r["nota"] >= 16
                                color_fondo = "rgba(52, 211, 153, 0.1)" if es_aprobado else "rgba(248, 113, 113, 0.1)"
                                color_borde = "#34D399" if es_aprobado else "#F87171"
                                color_texto = "#6EE7B7" if es_aprobado else "#FCA5A5"
                                
                                medalla = ""
                                if i == 0: medalla = "1er"
                                elif i == 1: medalla = "2do"
                                elif i == 2: medalla = "3er"
                                else: medalla = f"<span style='color:#64748B; font-size:0.9rem; padding:0 5px;'>#{i+1}</span>"
                                
                                m = int(r["tiempo"] // 60)
                                s = int(r["tiempo"] % 60)
                                tiempo_str = f"{m:02d}:{s:02d}"
                                
                                st.markdown(f"""
                                <div class='hover-jump' style='background:{color_fondo}; padding:12px 18px; border-radius:8px; border-left:4px solid {color_borde}; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;'>
                                    <div>
                                        <span style='font-size:1.1rem; font-weight:700; color:#94A3B8; margin-right:10px;'>{medalla}</span>
                                        <span style='font-size:1.05rem; font-weight:600; color:#F8FAFC;'>{r.get('nombre', 'N/A')}</span>
                                        <span style='color:#94A3B8; font-size:0.85rem; margin-left:8px;'>({r.get('carrera', 'N/A')} - {r.get('curso', 'N/A')})</span>
                                    </div>
                                    <div style='text-align:right;'>
                                        <div style='font-size:1.15rem; font-weight:800; color:{color_texto};'>{r.get('nota', 0)}/20</div>
                                        <div style='color:#94A3B8; font-size:0.8rem;'>Tiempo: {tiempo_str} min</div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                    
        else:
            gs = get_global_exam_state()
            ahora = datetime.datetime.now()
            
            est = st.session_state.eval_estudiante
            estudiante_key = f"{est['nombre']}_{est['carrera']}_{est['curso']}"
            ya_rindio = any(r["key"] == estudiante_key for r in gs["registros"])
            
            if ya_rindio:
                nota = next(r["nota"] for r in gs["registros"] if r["key"] == estudiante_key)
                st.error("Ya has rendido esta evaluación en esta sesión.")
                st.info(f"Tu nota final registrada es: {nota}/20")
            elif not gs["activo"]:
                st.error("La Evaluación está cerrada. El administrador aún no ha iniciado el examen para el grupo.")
                if st.button("Actualizar Estado"):
                    st.rerun()
            elif gs["hora_inicio"] and ahora < gs["hora_inicio"]:
                st.info(f" La evaluación está agendada para las {gs['hora_inicio'].strftime('%H:%M:%S')}. Por favor, espera.")
                if st.button("Actualizar Estado"):
                    st.rerun()
            elif gs["hora_inicio"] and (ahora - gs["hora_inicio"]).total_seconds() > 1200:
                st.error("La ventana global de 20 minutos ha expirado. Evaluación Cerrada definitivamente para este turno.")
            else:
                st.session_state.eval_global_end_time = gs["hora_inicio"] + datetime.timedelta(minutes=20)
                renderizar_evaluacion()

# --- SINCRONIZACIÓN DE ESTADO CON URL (PERSISTENCIA AL REFRESCAR) ---
st.query_params["etapa"] = st.session_state.etapa_actual
if st.session_state.get("especie_seleccionada"):
    st.query_params["especie"] = st.session_state.especie_seleccionada
if st.session_state.get("seccion_activa"):
    st.query_params["seccion"] = st.session_state.seccion_activa
if st.session_state.get("eval_vista"):
    st.query_params["vista"] = st.session_state.eval_vista
