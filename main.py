import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import json
from evaluacion import renderizar_evaluacion, BANCO_PREGUNTAS


# FUNCIONES UNIVERSALES DE SINCRONIZACIÓN DE ESTADO
def sync_state(temp_key, real_key):
  st.session_state[real_key] = st.session_state[temp_key]

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

  /* Ocultar boton toggle del sidebar — sidebar eliminado del diseno */
  [data-testid="collapsedControl"] {display: none !important;}
  [data-testid="stSidebar"] {display: none !important;}
  
  /* Variables y Base */
  [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #162119 !important;
  }
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #162119;
    color: #F5F5F5;
  }
  
  /* Animaciones Generales */
  @keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes pulseGlow {
    0% { box-shadow: 0 0 15px rgba(0, 242, 254, 0.4); }
    50% { box-shadow: 0 0 30px rgba(0, 242, 254, 0.7); }
    100% { box-shadow: 0 0 15px rgba(0, 242, 254, 0.4); }
  }

  /* ====== CINEMATIC BLUR REVEAL — SELECTORES RAIZ ====== */
  /*
   * Por que fallo la version anterior:
   *   stMainBlockContainer y block-container son nodos HIJOS sujetos
   *   a re-renders parciales de React. Streamlit puede desmontarlos y
   *   remontarlos en cada interaccion, anulando la animacion.
   *
   * Por que este si funciona:
   *   stAppViewContainer es el nodo raiz estatico de la app.
   *   Streamlit lo monta UNA SOLA VEZ y no lo toca.
   *   animation-fill-mode: both garantiza que el estado 0% se aplique
   *   ANTES de que el elemento sea visible (evita flash de contenido).
   *   animation-delay: 0ms asegura disparo inmediato.
   */

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

  /* Nodo raiz estatico — montado una sola vez por Streamlit */
  [data-testid="stAppViewContainer"] {
    animation: cinematicReveal 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0ms both !important;
    will-change: transform, filter, opacity !important;
    transform-origin: center top !important;
  }

  /* Sidebar: deslizamiento lateral escalonado */
  [data-testid="stSidebar"] {
    animation: cinematicRevealSidebar 0.85s cubic-bezier(0.16, 1, 0.3, 1) 120ms both !important;
    will-change: transform, filter, opacity !important;
  }

  /* Garantia adicional: header de Streamlit con la misma revelacion */
  [data-testid="stHeader"] {
    animation: cinematicReveal 0.7s cubic-bezier(0.16, 1, 0.3, 1) 0ms both !important;
  }

  .animate-fade-in {
    animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
  }
  
  /* Glassmorphism Containers */
  .glass-card {
    background: #2A3B2D;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
  }
  .glass-card:hover {
    transform: translateY(-4px);
    border-color: rgba(255, 255, 255, 0.15);
    box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
  }
  
  /* Variantes de color para Glass Cards */
  .glass-cyan { border-top: 3px solid #4CAF50; }
  .glass-emerald { border-top: 3px solid #4CAF50; }
  .glass-orange { border-top: 3px solid #FF9933; }
  .glass-purple { border-top: 3px solid #9c27b0; }
  .glass-red { border-top: 3px solid #FF3366; }
  
  /* Tipografía Premium */
  .title-gradient {
    font-size: clamp(3rem, 5vw, 5rem) !important;
    font-weight: 900 !important;
    line-height: 1.1 !important;
    color: #4CAF50 !important;
    background: none !important;
    -webkit-text-fill-color: initial !important;
    text-shadow: none !important;
    letter-spacing: -1px !important;
    margin-bottom: 10px !important;
    text-align: center;
  }
  .subtitle-elegant {
    font-size: clamp(1.1rem, 2vw, 1.5rem) !important;
    color: #8b949e !important;
    font-weight: 400 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 30px !important;
  }
  
  .texto-lectura-grande {
    font-size: 16px !important;
    line-height: 1.7 !important;
    color: #F5F5F5 !important;
  }
  
  /* Botones Pro */
  .btn-primary-custom {
    background: #4CAF50;
    color: #FFFFFF !important;
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
    background: #388E3C;
    color: #FFFFFF !important;
    text-decoration: none;
  }
  
  /* Tarjetas de Patologías (Laboratorio) */
  .pathology-card {
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 15px;
    border: 1px solid rgba(255,255,255,0.1);
  }
  .path-ben { background: linear-gradient(145deg, rgba(239, 83, 80, 0.1), rgba(0,0,0,0.2)); border-left: 4px solid #EF5350; }
  .path-cl { background: linear-gradient(145deg, rgba(186, 104, 200, 0.1), rgba(0,0,0,0.2)); border-left: 4px solid #BA68C8; }
  .path-heat { background: linear-gradient(145deg, rgba(212, 175, 55, 0.1), rgba(0,0,0,0.2)); border-left: 4px solid #D4AF37; }
  
  /* Ajustes Nativos de Streamlit */
  [data-testid="stMetric"] {
    background: #2A3B2D;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    transition: transform 0.2s ease;
  }
  [data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    background: rgba(22, 27, 34, 0.8);
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

  /* Base para TODOS los st.button */
  div.stButton > button:first-child {
    background-color: #1B5E20 !important;
    color: #FFFFFF !important;
    font-weight: 900 !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    font-size: 15px !important;
    border: 2px solid #4CAF50 !important;
    border-radius: 8px !important;
    padding: 14px 24px !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
  }
  div.stButton > button:first-child p {
    font-weight: 900 !important;
    font-size: 15px !important;
    letter-spacing: 2px !important;
  }
  div.stButton > button:first-child:hover {
    background-color: #2E7D32 !important;
    border-color: #81C784 !important;
    color: #FFFFFF !important;
    box-shadow: 0px 4px 14px rgba(76, 175, 80, 0.45) !important;
    transform: translateY(-2px) !important;
  }
  div.stButton > button:first-child:active {
    transform: translateY(0) !important;
    box-shadow: none !important;
  }

  /* FASES DEL CICLO ESTRAL — cyan */
  button[aria-label="FASES DEL CICLO ESTRAL"] {
    background: linear-gradient(135deg, #006064, #00838F) !important;
    border: 2px solid #00BCD4 !important;
    color: #FFFFFF !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.1) !important;
  }
  button[aria-label="FASES DEL CICLO ESTRAL"]:hover {
    background: linear-gradient(135deg, #00838F, #00BCD4) !important;
    border-color: #80DEEA !important;
    box-shadow: 0 6px 20px rgba(0, 188, 212, 0.5) !important;
  }

  /* CHECKLIST DE CELO E IA — naranja */
  button[aria-label="CHECKLIST DE CELO E IA"] {
    background: linear-gradient(135deg, #BF360C, #E64A19) !important;
    border: 2px solid #FF7043 !important;
    color: #FFFFFF !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.1) !important;
  }
  button[aria-label="CHECKLIST DE CELO E IA"]:hover {
    background: linear-gradient(135deg, #E64A19, #FF5722) !important;
    border-color: #FFAB91 !important;
    box-shadow: 0 6px 20px rgba(255, 87, 34, 0.5) !important;
  }

  /* LABORATORIO DE SIMULACION — purpura */
  button[aria-label="LABORATORIO DE SIMULACION"] {
    background: linear-gradient(135deg, #4A148C, #6A1B9A) !important;
    border: 2px solid #AB47BC !important;
    color: #FFFFFF !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.1) !important;
  }
  button[aria-label="LABORATORIO DE SIMULACION"]:hover {
    background: linear-gradient(135deg, #6A1B9A, #9C27B0) !important;
    border-color: #CE93D8 !important;
    box-shadow: 0 6px 20px rgba(156, 39, 176, 0.5) !important;
  }

  /* Boton secundario en sidebar (Cambiar Especie / Volver) */
  [data-testid="stSidebar"] .stButton > button:first-child {
    background-color: transparent !important;
    background: transparent !important;
    border: 1px solid rgba(76, 175, 80, 0.5) !important;
    color: #81C784 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
  }
  [data-testid="stSidebar"] .stButton > button:first-child:hover {
    background-color: rgba(76, 175, 80, 0.12) !important;
    background: rgba(76, 175, 80, 0.12) !important;
    border-color: #4CAF50 !important;
    color: #A5D6A7 !important;
    box-shadow: none !important;
    transform: none !important;
  }

  /* ======================================================================
   * RESPONSIVE DESIGN — DISPOSITIVOS MOVILES
   * Breakpoint principal : max-width 768 px  (tablets pequeñas y telefonos)
   * Breakpoint secundario: max-width 480 px  (telefonos compactos)
   *
   * Reglas de alcance:
   *   - Solo ajustes de tamano, espaciado y disposicion visual.
   *   - Paleta de colores, bordes redondeados y Cinematic Blur Reveal
   *     se conservan intactos.
   *   - Ningun cambio en logica Python ni en st.session_state.
   * ====================================================================== */

  @media (max-width: 768px) {

    /* --- Contenedor principal: eliminar padding lateral excesivo --- */
    [data-testid="stAppViewContainer"] > section > div {
      padding-left: 12px !important;
      padding-right: 12px !important;
    }
    [data-testid="block-container"] {
      padding: 1rem 0.75rem !important;
    }

    /* --- Tipografia: titulo principal --- */
    /* clamp ya escala, pero se refuerza el minimo para pantallas angostas */
    .title-gradient {
      font-size: clamp(2rem, 8vw, 3rem) !important;
      letter-spacing: -0.5px !important;
      margin-bottom: 6px !important;
    }

    /* --- Tipografia: subtitulo --- */
    .subtitle-elegant {
      font-size: clamp(0.75rem, 3.5vw, 1rem) !important;
      letter-spacing: 1px !important;
      margin-bottom: 16px !important;
    }

    /* --- Tipografia: cuerpo de lectura --- */
    .texto-lectura-grande {
      font-size: 14px !important;
      line-height: 1.6 !important;
    }

    /* --- Glass Cards: reducir padding y radio en movil --- */
    .glass-card {
      padding: 16px !important;
      border-radius: 12px !important;
      margin-bottom: 14px !important;
      /* Deshabilitar hover transform en tactil para evitar estado "pegado" */
      transform: none !important;
    }
    .glass-card:hover {
      transform: none !important;
    }

    /* --- Tarjetas de patologia: padding compacto --- */
    .pathology-card {
      padding: 14px !important;
    }

    /* --- Botones globales de st.button: area tactil minima 44 px (WCAG) --- */
    div.stButton > button:first-child {
      font-size: 12px !important;
      letter-spacing: 1px !important;
      padding: 12px 14px !important;
      min-height: 44px !important;
      /* Deshabilitar translateY en tactil */
      transform: none !important;
    }
    div.stButton > button:first-child p {
      font-size: 12px !important;
      letter-spacing: 1px !important;
    }
    div.stButton > button:first-child:hover {
      transform: none !important;
    }
    div.stButton > button:first-child:active {
      background-color: #2E7D32 !important;
      transform: none !important;
    }

    /* --- Botones de navegacion de seccion (Fases / Checklist / Lab) --- */
    button[aria-label="FASES DEL CICLO ESTRAL"],
    button[aria-label="CHECKLIST DE CELO E IA"],
    button[aria-label="LABORATORIO DE SIMULACION"] {
      font-size: 11px !important;
      letter-spacing: 0.5px !important;
      padding: 10px 8px !important;
    }

    /* --- Boton personalizado (.btn-primary-custom) --- */
    .btn-primary-custom {
      padding: 12px 20px !important;
      font-size: 1rem !important;
      letter-spacing: 0.5px !important;
      border-radius: 10px !important;
    }

    /* --- Metricas de Streamlit: padding reducido --- */
    [data-testid="stMetric"] {
      padding: 10px !important;
    }
    [data-testid="stMetric"]:hover {
      transform: none !important;
    }

    /* --- Radio buttons: area tactil ampliada para dedo --- */
    [data-testid="stRadio"] label {
      padding: 10px 8px !important;
      min-height: 44px !important;
      display: flex !important;
      align-items: center !important;
    }
    [data-testid="stCheckbox"] label {
      min-height: 44px !important;
      display: flex !important;
      align-items: center !important;
    }

    /* --- Sidebar: reducir padding interno en movil --- */
    [data-testid="stSidebar"] > div:first-child {
      padding: 1rem 0.75rem !important;
    }
    [data-testid="stSidebar"] .stButton > button:first-child {
      font-size: 12px !important;
      padding: 10px 12px !important;
      min-height: 44px !important;
    }

    /* --- Barra de progreso de evaluacion: texto auxiliar legible --- */
    div[style*="font-size:0.82rem"] {
      font-size: 0.75rem !important;
    }

    /* --- Separadores horizontales: margen reducido --- */
    hr {
      margin: 12px 0 !important;
    }
  }

  /* ======================================================================
   * BREAKPOINT SECUNDARIO — Telefonos compactos (max-width: 480 px)
   * Ajustes adicionales para pantallas menores a 5 pulgadas.
   * ====================================================================== */

  @media (max-width: 480px) {

    /* Titulo aun mas compacto */
    .title-gradient {
      font-size: clamp(1.6rem, 9vw, 2.4rem) !important;
    }

    /* Subtitulo minimalista */
    .subtitle-elegant {
      font-size: clamp(0.65rem, 3vw, 0.85rem) !important;
      letter-spacing: 0.5px !important;
    }

    /* Glass cards: padding minimo funcional */
    .glass-card {
      padding: 12px !important;
      border-radius: 10px !important;
    }

    /* Botones: tamano tactil critico */
    div.stButton > button:first-child {
      font-size: 11px !important;
      letter-spacing: 0.5px !important;
      padding: 11px 10px !important;
    }

    /* Botones de seccion: solo letras, sin desborde */
    button[aria-label="FASES DEL CICLO ESTRAL"],
    button[aria-label="CHECKLIST DE CELO E IA"],
    button[aria-label="LABORATORIO DE SIMULACION"] {
      font-size: 10px !important;
      letter-spacing: 0 !important;
      padding: 9px 6px !important;
      white-space: normal !important;
      word-break: break-word !important;
    }

    /* Texto de lectura */
    .texto-lectura-grande {
      font-size: 13px !important;
    }

    /* Metricas: fuente reducida para no desbordar columnas */
    [data-testid="stMetric"] {
      padding: 8px !important;
    }
    [data-testid="stMetricLabel"] {
      font-size: 11px !important;
    }
    [data-testid="stMetricValue"] {
      font-size: 1.2rem !important;
    }
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

@st.fragment
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

    # Fases del Ciclo
    fases_css = "border: 2px solid #00bcd4 !important; background-color: #00bcd4 !important; color: #000 !important; opacity: 1.0 !important;" if act_sec == "Fases del Ciclo Estral" else "background-color: rgba(0,188,212,0.25) !important; color: #00bcd4 !important; border: 1px solid #00bcd4 !important; opacity: 0.7 !important;"
    st.markdown(f'<style>div[data-testid="column"]:nth-child(2) div[data-testid="stVerticalBlock"] div:nth-child(1) button {{ {fases_css} }}</style>', unsafe_allow_html=True)
    if st.button("FASES DEL CICLO ESTRAL", key="btn_nav_fases", on_click=_ir_fases, use_container_width=True):
      pass

    # Checklist
    check_css = "border: 2px solid #ff9800 !important; background-color: #ff9800 !important; color: #000 !important; opacity: 1.0 !important;" if act_sec == "Checklist de Celo e IA" else "background-color: rgba(255,152,0,0.2) !important; color: #ff9800 !important; border: 1px solid #ff9800 !important; opacity: 0.7 !important;"
    st.markdown(f'<style>div[data-testid="column"]:nth-child(2) div[data-testid="stVerticalBlock"] div:nth-child(2) button {{ {check_css} }}</style>', unsafe_allow_html=True)
    if st.button("CHECKLIST DE CELO E IA", key="btn_nav_checklist", on_click=_ir_checklist, use_container_width=True):
      pass

    # Laboratorio
    simul_css = "border: 2px solid #9c27b0 !important; background-color: #9c27b0 !important; color: #fff !important; opacity: 1.0 !important;" if act_sec == "Laboratorio de Simulacion" else "background-color: rgba(156,39,176,0.2) !important; color: #ce93d8 !important; border: 1px solid #9c27b0 !important; opacity: 0.7 !important;"
    st.markdown(f'<style>div[data-testid="column"]:nth-child(2) div[data-testid="stVerticalBlock"] div:nth-child(3) button {{ {simul_css} }}</style>', unsafe_allow_html=True)
    if st.button("LABORATORIO DE SIMULACION", key="btn_nav_simul", on_click=_ir_simulador, use_container_width=True):
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
    <div class='glass-card glass-cyan animate-fade-in' style='padding: 20px;'>
      <h3 style='margin-top:0; color:#4CAF50;'> Línea de Tiempo Fisiológica: {species}</h3>
      <p style='margin-bottom:0; color:#8b949e;'>Dinámica hormonal y biológica ajustada específicamente para el modelo <b>{species}</b>.</p>
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
        <div class="glass-card {glass_styles[i]} animate-fade-in" style="height: 100%; padding: 20px; background: {bg_colors[i]};">
          <h3 style="color: {h_color}; margin-top:0; border-bottom: 1px solid {border_rgbas[i]}; padding-bottom: 10px;">{h_icon} {h_name}</h3>
          <p style="font-size: 0.85rem; color:#A0AAB5; margin-top: 10px;"><i>️ {sd[key]['dur']}</i></p>
          <p style="font-size: 1.1rem; color: #fff;">{sd[key]['icon']} <b>{sd[key]['title']}</b></p>
          <p class="texto-lectura-grande" style="font-size: 0.95rem !important;">{sd[key]['text']}</p>
        </div>
        """, unsafe_allow_html=True)

  
  # --- SECCIÓN 2: CALCULADORA DE DIAGNÓSTICO E IA ---
  if st.session_state.seccion_activa == "Checklist de Celo e IA":
    st.markdown("""
    <div class='glass-card glass-emerald animate-fade-in' style='padding: 20px;'>
      <h3 style='margin-top:0; color:#00CC99;'> Calculadora Diagnóstica y Decisiones Clínicas</h3>
      <p style='margin-bottom:0; color:#8B949E;'>Evaluación interactiva del paciente y análisis de impacto económico en finca.</p>
    </div>
    """, unsafe_allow_html=True)
  
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.2, 1])
  
    with c1:
      with st.container(border=False):
        score_label = "Score de Postura" if species == "Ave" else "Score de Celo"
        st.markdown(f"""
        <div class='glass-card glass-orange' style='margin-bottom:15px; padding: 15px 20px;'>
          <h4 style='margin:0; color:#FF9933;'>️ {score_label} ({species})</h4>
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
        <div class='glass-card glass-cyan' style='margin-bottom:15px; padding: 15px 20px;'>
          <h4 style='margin:0; color:#4CAF50;'> {ia_label} ({species})</h4>
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
            st.success(" **Ventana Óptima de IA:** Inseminar hoy por la tarde (estimado 3:00 PM - 5:00 PM). Ovulación estimada: 7:00 PM (12 horas post-celo).")
          else:
            st.info(" **Ventana Óptima de IA:** Inseminar mañana por la mañana a primera hora (estimado 7:00 AM). Ovulación estimada: 5:00 AM del día siguiente.")
        else:
          for regla in data["ia_window"]:
            st.markdown(f"- {regla}")
          
      with st.container(border=False):
        st.markdown("""
        <div class='glass-card glass-emerald' style='margin-bottom:15px; padding: 15px 20px;'>
          <h4 style='margin:0; color:#00CC99;'> Retorno de Inversión (ROI)</h4>
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
          st.error(roi["obs_msg"])
        else:
          st.success(roi["tech_msg"])
  
  # --- SECCIÓN 3: LABORATORIO DE SIMULACIÓN Y COMPLICACIONES ---
  if st.session_state.seccion_activa == "Laboratorio de Simulacion":
  
    # 1. Modificadores de Salud Condicionales
    st.markdown("""
    <div class='glass-card glass-orange animate-fade-in' style='padding: 20px;'>
      <h3 style='margin-top:0; color:#FF9933;'> Modificadores de Salud y Estado de Gestación</h3>
      <p style='margin-bottom:0; color:#8B949E;'>Configura las variables patológicas para simular el comportamiento endocrino.</p>
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

    col_play, col_slider = st.columns([1.2, 4])
    
    with col_play:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.session_state.is_playing:
            if st.button("⏸️ Pausar", use_container_width=True):
                st.session_state.is_playing = False
                st.rerun()
        else:
            if st.button("▶️ Reproducir", use_container_width=True):
                if st.session_state.current_time >= max_days:
                    st.session_state.current_time = 0.0
                st.session_state.is_playing = True
                st.rerun()
  
    with col_slider:
        slider_label = f"Desliza para avanzar {'la Hora' if species == 'Ave' else 'el Día'} del Ciclo manualmente:"
        # Usamos value en lugar de key para evitar StreamlitAPIException al mutarlo en el bucle
        tiempo_actual = st.slider(slider_label, min_value=0.0, max_value=float(max_days), value=float(st.session_state.current_time), step=0.1)
        
        # Si NO está reproduciendo automáticamente, permitimos actualización manual
        if not st.session_state.is_playing:
            if abs(tiempo_actual - st.session_state.current_time) > 0.01:
                st.session_state.current_time = tiempo_actual  
    # ---------------------------
    # Generar HUD states y KPIs dinámicos
    # ---------------------------
    idx = (df["Día"] - tiempo_actual).abs().idxmin()
    row = df.iloc[idx]
    
    c_phase = get_current_phase(row["Día"], data["phases"])
    diag_txt, diag_typ = get_hud_diagnosis(row["Día"], c_phase["name"], complication, pregnancy, species)
    
    # Render HUD
    if diag_typ == "success":
        st.success(diag_txt)
    elif diag_typ == "error":
        st.error(diag_txt)
    elif diag_typ == "warning":
        st.warning(diag_txt)
    else:
        st.info(diag_txt)
        
    # Render KPIs
    matLabel = "🟠 PGF2α (%)"
    matKey = "PGF2α"
    if pregnancy:
        if species == "Porcino": matLabel = " Estrógenos Emb. (%)"
        elif species == "Equino": matLabel = " Movilidad Emb. (%)"
        else: matLabel = " IFN-τ (%)"
        matKey = "Señal Materna"
        
    kpi_html = f"""
    <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 20px; background: rgba(22, 27, 34, 0.6); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.08);">
        <div style="flex: 1; text-align: center; min-width: 100px;"><span style="font-size: 14px; color: #8b949e; display: block; margin-bottom: 8px;">🟣 FSH (%)</span><span style="font-size: 28px; font-weight: 800; color: #BC8BFF;">{row['FSH']:.1f}%</span></div>
        <div style="flex: 1; text-align: center; min-width: 100px;"><span style="font-size: 14px; color: #8b949e; display: block; margin-bottom: 8px;"> LH (%)</span><span style="font-size: 28px; font-weight: 800; color: #FF3366;">{row['LH']:.1f}%</span></div>
        <div style="flex: 1; text-align: center; min-width: 100px;"><span style="font-size: 14px; color: #8b949e; display: block; margin-bottom: 8px;"> E2 (%)</span><span style="font-size: 28px; font-weight: 800; color: #58A6FF;">{row['Estradiol (E2)']:.1f}%</span></div>
        <div style="flex: 1; text-align: center; min-width: 100px;"><span style="font-size: 14px; color: #8b949e; display: block; margin-bottom: 8px;">🟢 P4 (%)</span><span style="font-size: 28px; font-weight: 800; color: #00CC99;">{row['Progesterona (P4)']:.1f}%</span></div>
        <div style="flex: 1; text-align: center; min-width: 100px;"><span style="font-size: 14px; color: #8b949e; display: block; margin-bottom: 8px;">{matLabel}</span><span style="font-size: 28px; font-weight: 800; color: #FF9933;">{row[matKey]:.1f}%</span></div>
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)
  
    # ---------------------------
    # Gráfica Plotly — Arquitectura st.empty() + while loop (sin st.rerun())
    # Elimina el flickering y los saltos de tiempo al actualizar el placeholder
    # in-place en lugar de forzar un re-render completo del script.
    # ---------------------------
    import plotly.graph_objects as go
    import time

    dayLabel   = 'HORA' if species == 'Ave' else 'DÍA'
    xAxisTitle = 'Horas del Ciclo Ovulatorio' if species == 'Ave' else 'Días del Ciclo'

    # ── Layout estático: se construye UNA sola vez por escenario ──────────────
    if "base_fig" not in st.session_state or st.session_state.base_fig is None:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name='FSH',
                                 line=dict(color='#BC8BFF', width=3.5)))
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name='LH',
                                 line=dict(color='#FF3366', width=3.5)))
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name='Estradiol (E2)',
                                 line=dict(color='#58A6FF', width=3.5)))
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name='Progesterona (P4)',
                                 line=dict(color='#00CC99', width=3.5)))
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name=matKey,
                                 line=dict(color='#FF9933', width=3.5)))

        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            dragmode=False,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis=dict(
                title=xAxisTitle,
                range=[0, max_days],
                gridcolor='rgba(255,255,255,0.05)',
                fixedrange=True
            ),
            yaxis=dict(
                title='Concentración (%)',
                range=[0, 105],
                gridcolor='rgba(255,255,255,0.05)',
                fixedrange=True
            ),
            legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
            height=400
        )

        fig.add_shape(type='line', x0=0, x1=0, y0=0, y1=105,
                      line=dict(color='#FFF', width=3))
        fig.add_annotation(
            x=0.02, y=0.98, xref='paper', yref='paper', text="", showarrow=False,
            xanchor='left', yanchor='top', font=dict(color='#FFF', size=20),
            bgcolor='rgba(0,0,0,0.8)', bordercolor='#FFF', borderpad=6, borderwidth=1
        )
        st.session_state.base_fig = fig

    # ── Placeholder dedicado: el gráfico nunca se destruye ni se recrea ───────
    grafico_placeholder = st.empty()
    fig_plot = st.session_state.base_fig

    def _render_frame(t_actual):
        """Actualiza solo los arrays de datos y el cursor; NO toca el layout."""
        mask   = df["Día"].values <= t_actual
        x_vals = df["Día"].values[mask]

        fig_plot.data[0].x = x_vals;  fig_plot.data[0].y = df["FSH"].values[mask]
        fig_plot.data[1].x = x_vals;  fig_plot.data[1].y = df["LH"].values[mask]
        fig_plot.data[2].x = x_vals;  fig_plot.data[2].y = df["Estradiol (E2)"].values[mask]
        fig_plot.data[3].x = x_vals;  fig_plot.data[3].y = df["Progesterona (P4)"].values[mask]
        fig_plot.data[4].x = x_vals;  fig_plot.data[4].y = df[matKey].values[mask]

        fig_plot.layout.shapes[0].x0      = t_actual
        fig_plot.layout.shapes[0].x1      = t_actual
        fig_plot.layout.annotations[0].text = f"{dayLabel} {t_actual:.1f}"

        # Actualización in-place: solo cambia este contenedor,
        # el resto de la UI permanece completamente estático.
        grafico_placeholder.plotly_chart(
            fig_plot,
            use_container_width=True,
            config={'staticPlot': True, 'displayModeBar': False}
        )

    # ── Render inicial (frame estático o primer cuadro de animación) ──────────
    _render_frame(tiempo_actual)

    # ── Bucle de animación continua (sin st.rerun()) ──────────────────────────
    # El bucle while corre en el mismo hilo de Python y actualiza el
    # placeholder in-place: el DOM del navegador recibe SOLO el diff del
    # gráfico, sin redibujar ningún otro elemento de la página.
    if st.session_state.is_playing:
        # Paso calibrado: 0.1 unidades por cuadro → velocidad perceptualmente
        # suave; sleep de 0.05 s da ~20 fps reales en el round-trip HTTP de
        # Streamlit (límite práctico del protocolo websocket).
        paso_animacion = 0.1
        t = st.session_state.current_time

        while st.session_state.is_playing and t < max_days:
            t = min(t + paso_animacion, max_days)
            _render_frame(t)
            time.sleep(0.05)

        # Al terminar el bucle: persiste el tiempo final y detiene la reproducción
        st.session_state.current_time = t
        if t >= max_days:
            st.session_state.is_playing = False
  

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
    div.stButton > button:first-child {
      background: linear-gradient(135deg, #4CAF50, #4facfe) !important;
      color: #000000 !important;
      padding: 16px 32px !important;
      border-radius: 12px !important;
      border: none !important;
      box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4) !important;
      transition: all 0.3s ease-in-out !important;
      animation: pulseGlow 3s infinite;
    }
    div.stButton > button:first-child:hover {
      transform: scale(1.05) translateY(-2px) !important;
      box-shadow: 0 10px 40px rgba(0, 242, 254, 0.8) !important;
    }
    div.stButton > button:first-child p {
      font-size: 1.3rem !important;
      font-weight: 900 !important;
      text-transform: uppercase !important;
      letter-spacing: 1.5px !important;
      color: #000000 !important;
      margin: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button("INICIAR SIMULACION", use_container_width=True, key="btn_iniciar_sim"):
      st.session_state.etapa_actual = "seleccion"
      st.rerun()

  st.markdown("<br>", unsafe_allow_html=True)

  col_eval1, col_eval2, col_eval3 = st.columns([1, 1.2, 1])
  with col_eval2:
    st.markdown("""
    <div style='background: rgba(76,175,80,0.07); padding: 20px 28px; border-radius: 12px;
                border: 1px solid rgba(76,175,80,0.25); text-align: center; margin-bottom: 10px;'>
        <p style='margin: 0 0 6px 0; color:#4CAF50; font-weight:700; font-size:0.8rem;
                  letter-spacing:2px; text-transform:uppercase;'>Banco: 50 preguntas | Examen: 20 aleatorias</p>
        <p style='margin: 0; color:#B0BEC5; font-size:0.85rem;'>
            Umbral de aprobacion: 16 / 20 respuestas correctas (80%)
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("ACCEDER A LA EVALUACION FORMAL", use_container_width=True, key="btn_ir_evaluacion"):
      st.session_state.etapa_actual = "evaluacion"
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

  # Primera fila: Bovino, Porcino, Ovino
  col1, col2, col3 = st.columns(3)
  species_list_row1 = ["Bovino", "Porcino", "Ovino"]
  
  for col, sp in zip([col1, col2, col3], species_list_row1):
    with col:
      st.markdown(f"<h3 style='color: #4CAF50; text-align: center; margin-top: 0;'>{sp}</h3>", unsafe_allow_html=True)
      img_path = f"{sp.lower()}.jpg"
      
      if os.path.exists(img_path):
        b64_img = get_base64_of_bin_file(img_path)
        img_str = f"data:image/jpeg;base64,{b64_img}"
      else:
        img_str = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="

      clicked = clickable_images(
        [img_str],
        titles=[sp],
        div_style={"display": "flex", "justify-content": "center", "width": "100%", "margin": "0"},
        img_style={
          "cursor": "pointer",
          "width": "100%",
          "border-radius": "12px",
          "object-fit": "cover",
          "aspect-ratio": "16/9",
          "transition": "transform 0.3s ease, box-shadow 0.3s ease",
          "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.4)"
        },
        key=f"img_{sp}"
      )
      
      if not os.path.exists(img_path):
        st.markdown(f"<div style='background:rgba(0,0,0,0.3); backdrop-filter:blur(5px); height:150px; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#8b949e; margin-top: -150px; position:relative; pointer-events: none; border:1px dashed rgba(255,255,255,0.2);'><i>Sin Imagen ({sp})</i></div>", unsafe_allow_html=True)
      
      data = SPECIES_DATA[sp]
      st.markdown(f"""
      <div style='font-size: 14px; color: #F5F5F5; margin-top: 20px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);'>
        <p style='margin: 0 0 8px 0;'><span style='color:#4CAF50;'>️ Duración:</span> {data['cycle_duration']} {data.get('cycle_unit', 'días')}</p>
        <p style='margin: 0 0 8px 0;'><span style='color:#4CAF50;'> Ovulación:</span> {data['ovulation_timing']}</p>
        <p style='margin: 0;'><span style='color:#4CAF50;'> R. Materno:</span> {data['maternal_recognition'] if data['maternal_recognition'] not in ['?', 'N/A'] else 'N/A'}</p>
      </div>
      """, unsafe_allow_html=True)
      
      if clicked > -1:
        st.session_state.especie_seleccionada = sp
        st.session_state.etapa_actual = "simulador"
        st.rerun()

  st.markdown("<br>", unsafe_allow_html=True)
  
  # Segunda fila: Caprino, Equino, Ave
  col4, col5, col6 = st.columns(3)
  species_list_row2 = ["Caprino", "Equino", "Ave"]
  
  for col, sp in zip([col4, col5, col6], species_list_row2):
    with col:
      st.markdown(f"<h3 style='color: #4CAF50; text-align: center; margin-top: 0;'>{sp}</h3>", unsafe_allow_html=True)
      img_path = f"{sp.lower()}.jpg"
      
      if os.path.exists(img_path):
        b64_img = get_base64_of_bin_file(img_path)
        img_str = f"data:image/jpeg;base64,{b64_img}"
      else:
        img_str = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="

      clicked = clickable_images(
        [img_str],
        titles=[sp],
        div_style={"display": "flex", "justify-content": "center", "width": "100%", "margin": "0"},
        img_style={
          "cursor": "pointer",
          "width": "100%",
          "border-radius": "12px",
          "object-fit": "cover",
          "aspect-ratio": "16/9",
          "transition": "transform 0.3s ease, box-shadow 0.3s ease",
          "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.4)"
        },
        key=f"img_{sp}"
      )
      
      if not os.path.exists(img_path):
        st.markdown(f"<div style='background:rgba(0,0,0,0.3); backdrop-filter:blur(5px); height:150px; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#8b949e; margin-top: -150px; position:relative; pointer-events: none; border:1px dashed rgba(255,255,255,0.2);'><i>Sin Imagen ({sp})</i></div>", unsafe_allow_html=True)
      
      data = SPECIES_DATA[sp]
      st.markdown(f"""
      <div style='font-size: 14px; color: #F5F5F5; margin-top: 20px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);'>
        <p style='margin: 0 0 8px 0;'><span style='color:#4CAF50;'>️ Duración:</span> {data['cycle_duration']} {data.get('cycle_unit', 'días')}</p>
        <p style='margin: 0 0 8px 0;'><span style='color:#4CAF50;'> Ovulación:</span> {data['ovulation_timing']}</p>
        <p style='margin: 0;'><span style='color:#4CAF50;'> R. Materno:</span> {data['maternal_recognition'] if data['maternal_recognition'] not in ['?', 'N/A'] else 'N/A'}</p>
      </div>
      """, unsafe_allow_html=True)
      
      if clicked > -1:
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
      st.session_state.examen_desbloqueado = False   # Resetea acceso al salir
      st.rerun()

  # ── Barrera de contraseña ────────────────────────────────────────────────────
  # La clave se guarda en session_state para que los reruns internos del examen
  # (selección de respuestas, calificación) no vuelvan a pedir la contraseña.
  if "examen_desbloqueado" not in st.session_state:
    st.session_state.examen_desbloqueado = False

  if not st.session_state.examen_desbloqueado:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='max-width: 480px; margin: 0 auto; padding: 36px 40px;
                background: rgba(22, 33, 25, 0.92);
                border: 1px solid rgba(76,175,80,0.3);
                border-top: 3px solid #4CAF50;
                border-radius: 16px;
                backdrop-filter: blur(14px);
                box-shadow: 0 12px 40px rgba(0,0,0,0.5);
                text-align: center;'>
      <p style='font-size: 2rem; margin: 0 0 8px 0;'>🔒</p>
      <h3 style='color: #4CAF50; margin: 0 0 6px 0; font-size: 1.3rem;'>
        Evaluación Formal Protegida
      </h3>
      <p style='color: #8B949E; font-size: 0.88rem; margin: 0 0 24px 0;'>
        Esta sección requiere contraseña de acceso.<br>
        Solicítala a tu docente.
      </p>
    </div>
    """, unsafe_allow_html=True)

    col_pw1, col_pw2, col_pw3 = st.columns([1, 2, 1])
    with col_pw2:
      clave_ingresada = st.text_input(
        "Contraseña de acceso",
        type="password",
        placeholder="••••••••••••••",
        key="input_clave_examen",
        label_visibility="collapsed"
      )
      if st.button("🔓 Ingresar", use_container_width=True, key="btn_unlock_examen"):
        if clave_ingresada == "agroestral2026":
          st.session_state.examen_desbloqueado = True
          st.success("✅ Acceso concedido. Cargando evaluación…")
          st.rerun()
        else:
          st.error("❌ Contraseña incorrecta. Inténtalo de nuevo.")

  else:
    # ── Contenido completo del examen (solo visible tras autenticación) ─────────
    renderizar_evaluacion()

