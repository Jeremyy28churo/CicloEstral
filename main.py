import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import json

# Configuración de página
st.set_page_config(page_title="Granja Digital - Fisiología Reproductiva", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS (DARK PRO THEME) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0E1117;
        color: #C9D1D9;
    }
    
    .texto-lectura-grande {
        font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    .titulo-seccion-grande {
        font-size: 24px !important;
        font-weight: 700 !important;
        margin-bottom: 15px !important;
    }
    .item-lista-grande {
        font-size: 16px !important;
        line-height: 1.6 !important;
        margin-bottom: 12px !important;
    }
    
    .tarjeta-ben {
        background-color: rgba(139, 38, 38, 0.25) !important;
        border: 1px solid rgba(239, 83, 80, 0.4) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-top: 10px !important;
        margin-bottom: 15px !important;
    }
    .tarjeta-estres {
        background-color: rgba(128, 128, 0, 0.18) !important;
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-top: 10px !important;
        margin-bottom: 15px !important;
    }
    .tarjeta-cl {
        background-color: rgba(74, 20, 140, 0.2) !important;
        border: 1px solid rgba(186, 104, 200, 0.4) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-top: 10px !important;
        margin-bottom: 15px !important;
    }
    
    /* (Se han eliminado los estilos obsoletos de st.tabs) */

    .titulo-principal-grande {
        font-size: 56px !important;
        font-weight: 900 !important;
        line-height: 1.1 !important;
        background: linear-gradient(45deg, #00f2fe, #4facfe, #00ff87) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        text-shadow: 0 0 25px rgba(0, 242, 254, 0.4) !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        margin-bottom: 5px !important;
    }
    .subtitulo-limpio {
        font-size: 18px !important;
        color: #a0aec0 !important;
        font-weight: 500 !important;
        letter-spacing: 1px !important;
    }
    .sub-title {
        font-weight: 400;
        font-size: 1.1rem;
        color: #8B949E;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }
    
    /* Contenedores Pro */
    .pro-box {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    /* Timeline estática */
    .timeline-container {
        display: flex; 
        height: 25px; 
        border-radius: 6px; 
        overflow: hidden; 
        margin-top: 10px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
    }
    .timeline-segment {
        display: flex; 
        align-items: center; 
        justify-content: center; 
        font-size: 0.75rem; 
        font-weight: 600; 
        color: #FFF; 
        transition: all 0.3s ease;
    }
    
    .footer {
        text-align: center;
        padding: 30px;
        color: #8B949E;
        font-size: 0.9rem;
        border-top: 1px solid #30363D;
        margin-top: 50px;
    }
    
    /* --- HÍBRIDO ADAPTATIVO MÓVIL --- */
    @media (max-width: 768px) {
        [data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
            flex: 1 1 100% !important;
            margin-bottom: 1rem;
        }
        .main-title {
            font-size: 1.8rem;
        }
    }
    
    /* --- REDISEÑO UI/UX AVANZADO --- */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stTabs [data-baseweb="tab-panel"] {
        animation: fadeIn 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .browser-window {
        border-radius: 12px;
        background: linear-gradient(145deg, #161B22, #0E1117);
        border: 1px solid #30363D;
        margin-bottom: 20px;
        overflow: hidden;
        transition: all 0.3s ease-in-out;
    }
    .browser-window:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    .window-header {
        background-color: #21262D;
        padding: 8px 15px;
        display: flex;
        align-items: center;
        border-bottom: 1px solid #30363D;
    }
    .dot {
        height: 12px;
        width: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    .dot.red { background-color: #FF5F56; }
    .dot.yellow { background-color: #FFBD2E; }
    .dot.green { background-color: #27C93F; }
    
    .window-content { padding: 15px 20px; }
    .window-content h2, .window-content h3, .window-content h4 { margin-top: 0; font-weight: 700; font-family: 'Inter', sans-serif; }
    
    .neon-cyan { border: 1px solid #00FFFF; box-shadow: 0 0 10px rgba(0,255,255,0.1); }
    .neon-cyan:hover { box-shadow: 0 0 20px rgba(0,255,255,0.3); }
    .neon-cyan .window-content h2, .neon-cyan .window-content h3, .neon-cyan .window-content h4 { color: #00FFFF; }
    
    .neon-emerald { border: 1px solid #00CC99; box-shadow: 0 0 10px rgba(0,204,153,0.1); }
    .neon-emerald:hover { box-shadow: 0 0 20px rgba(0,204,153,0.3); }
    .neon-emerald .window-content h2, .neon-emerald .window-content h3, .neon-emerald .window-content h4 { color: #00CC99; }
    
    .neon-orange { border: 1px solid #FF9933; box-shadow: 0 0 10px rgba(255,153,51,0.1); }
    .neon-orange:hover { box-shadow: 0 0 20px rgba(255,153,51,0.3); }
    .neon-orange .window-content h2, .neon-orange .window-content h3, .neon-orange .window-content h4 { color: #FF9933; }

    /* Hover interactivo general */
    [data-testid="stMetric"], [data-testid="stExpander"], div[data-testid="stVerticalBlock"] > div[style*="border"] {
        transition: all 0.3s ease-in-out !important;
    }
    [data-testid="stMetric"]:hover, [data-testid="stExpander"]:hover, div[data-testid="stVerticalBlock"] > div[style*="border"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 16px rgba(255,255,255,0.06) !important;
    }
    
    /* Highlight Radio and Checkboxes on Hover */
    [data-testid="stCheckbox"], [data-testid="stRadio"] {
        transition: all 0.2s ease-in-out;
        border-radius: 6px;
        padding: 4px;
    }
    [data-testid="stCheckbox"]:hover, [data-testid="stRadio"]:hover {
        background-color: rgba(255,255,255,0.05);
        padding-left: 10px;
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
    }
}

def generate_hormone_data(species, complication="Normal", pregnancy=False):
    data = SPECIES_DATA[species]
    days = data["cycle_duration"]
    t = np.linspace(0, days, 500)
    lh_peak = data["lh_peak"]
    
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


# --- LÓGICA DE ESTADO (NAVEGACIÓN) ---
if "seccion_activa" not in st.session_state:
    st.session_state.seccion_activa = "Fases del Ciclo Estral"

# Fuerza bruta para navegación vía URL (Botones HTML Inline)
if hasattr(st, "query_params"):
    if "nav" in st.query_params:
        nav = st.query_params["nav"]
        if nav == "fases": st.session_state.seccion_activa = "Fases del Ciclo Estral"
        elif nav == "check": st.session_state.seccion_activa = "Checklist de Celo e IA"
        elif nav == "simul": st.session_state.seccion_activa = "Laboratorio de Simulación"
else:
    params = st.experimental_get_query_params()
    if "nav" in params:
        nav = params["nav"][0]
        if nav == "fases": st.session_state.seccion_activa = "Fases del Ciclo Estral"
        elif nav == "check": st.session_state.seccion_activa = "Checklist de Celo e IA"
        elif nav == "simul": st.session_state.seccion_activa = "Laboratorio de Simulación"

# CSS Dinámico ultra-agresivo (inyección global)
btn_css = """
<style>
/* Contenedor del bloque derecho */
.menu-vertical-container {
    display: flex;
    flex-direction: column;
    gap: 12px !important;
    max-width: 100% !important;
}

/* Estilo común e inicial para los botones de navegación */
.btn-nav, 
div[data-testid="column"]:nth-of-type(2) button[kind="secondary"] {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important; /* Centra el texto y el icono */
    width: 100% !important;
    padding: 16px 20px !important;
    font-size: 18px !important; /* Letra más grande */
    font-weight: 900 !important; /* Negrita extrema */
    text-transform: uppercase !important; /* Todo en MAYÚSCULAS */
    letter-spacing: 1.5px !important; /* Espaciado entre letras para mayor legibilidad */
    border-radius: 10px !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.25s ease-in-out !important; /* Movimiento suave */
}

/* Forzar mayúsculas en el párrafo interno de Streamlit */
div[data-testid="column"]:nth-of-type(2) button[kind="secondary"] p {
    font-size: 18px !important;
    font-weight: 900 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    color: inherit !important;
    margin: 0 !important;
}

/* --- COLORES SÓLIDOS DE LA IDENTIDAD DE LA APP --- */

/* Botón 1: Fases (Cyan Sólido) */
.btn-fases, 
div.element-container:has(.marker-fases) + div.element-container button[kind="secondary"],
div[data-testid="stVerticalBlock"] > div:has(.marker-fases) + div button[kind="secondary"] {
    background-color: #00bcd4 !important;
    color: #000000 !important; /* Letra negra para que no se tape */
}
.btn-fases:hover, 
div[data-testid="stVerticalBlock"] > div:has(.marker-fases) + div button[kind="secondary"]:hover {
    transform: translateY(-3px) !important; /* Movimiento hacia arriba */
    box-shadow: 0 8px 20px rgba(0, 188, 212, 0.5) !important; /* Glow neón */
}

/* Botón 2: Checklist (Naranja Sólido) */
.btn-checklist, 
div.element-container:has(.marker-checklist) + div.element-container button[kind="secondary"],
div[data-testid="stVerticalBlock"] > div:has(.marker-checklist) + div button[kind="secondary"] {
    background-color: #ff9800 !important;
    color: #000000 !important; /* Letra negra para que no se tape */
}
.btn-checklist:hover, 
div[data-testid="stVerticalBlock"] > div:has(.marker-checklist) + div button[kind="secondary"]:hover {
    transform: translateY(-3px) !important; /* Movimiento hacia arriba */
    box-shadow: 0 8px 20px rgba(255, 152, 0, 0.5) !important; /* Glow neón */
}

/* Botón 3: Simulador (Púrpura Sólido) */
.btn-simulador, 
div.element-container:has(.marker-simulador) + div.element-container button[kind="secondary"],
div[data-testid="stVerticalBlock"] > div:has(.marker-simulador) + div button[kind="secondary"] {
    background-color: #9c27b0 !important;
    color: #ffffff !important; /* Letra blanca para contrastar con el fondo oscuro */
}
.btn-simulador:hover, 
div[data-testid="stVerticalBlock"] > div:has(.marker-simulador) + div button[kind="secondary"]:hover {
    transform: translateY(-3px) !important; /* Movimiento hacia arriba */
    box-shadow: 0 8px 20px rgba(156, 39, 176, 0.5) !important; /* Glow neón */
}

/* --- INDICADORES DE ESTADO (ACTIVO VS INACTIVO) --- */

.btn-activo {
    transform: scale(1.03) !important; /* Se hace un poquito más grande */
    opacity: 1.0 !important; /* Opacidad total */
    /* Un sutil borde luminoso alrededor de todo el botón en lugar de una barra blanca */
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.2) !important; 
}
.btn-inactivo {
    opacity: 0.65 !important;
}
</style>
"""

st.markdown(btn_css, unsafe_allow_html=True)

# --- INTERFAZ DE USUARIO (CABECERA) ---
st.markdown("<br>", unsafe_allow_html=True)
col_nav1, col_nav2 = st.columns([1.5, 1])

with col_nav1:
    st.markdown('<p class="titulo-principal-grande">CICLO ESTRAL</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitulo-limpio">Fisiología Reproductiva Comparada</p>', unsafe_allow_html=True)

with col_nav2:
    act_sec = st.session_state.seccion_activa
    c_fases = "btn-activo" if act_sec == "Fases del Ciclo Estral" else "btn-inactivo"
    c_check = "btn-activo" if act_sec == "Checklist de Celo e IA" else "btn-inactivo"
    c_simul = "btn-activo" if act_sec == "Laboratorio de Simulación" else "btn-inactivo"

    st.markdown(f"""
    <a href="/?nav=fases" target="_self" style="text-decoration: none;">
        <div role="button" class="btn-nav btn-fases {c_fases}" style="
            background-color: #00bcd4 !important; 
            color: #000000 !important; 
            font-size: 20px !important; 
            font-weight: 900 !important; 
            text-transform: uppercase !important; 
            width: 100%; 
            border: none; 
            padding: 16px; 
            border-radius: 10px; 
            cursor: pointer;
            letter-spacing: 1.5px;
            margin-bottom: 12px;
            text-align: center;
        ">
            📅 FASES DEL CICLO ESTRAL
        </div>
    </a>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <a href="/?nav=check" target="_self" style="text-decoration: none;">
        <div role="button" class="btn-nav btn-checklist {c_check}" style="
            background-color: #ff9800 !important; 
            color: #000000 !important; 
            font-size: 20px !important; 
            font-weight: 900 !important; 
            text-transform: uppercase !important; 
            width: 100%; 
            border: none; 
            padding: 16px; 
            border-radius: 10px; 
            cursor: pointer;
            letter-spacing: 1.5px;
            margin-bottom: 12px;
            text-align: center;
        ">
            📋 CHECKLIST DE CELO E IA
        </div>
    </a>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <a href="/?nav=simul" target="_self" style="text-decoration: none;">
        <div role="button" class="btn-nav btn-simulador {c_simul}" style="
            background-color: #9c27b0 !important; 
            color: #ffffff !important; 
            font-size: 20px !important; 
            font-weight: 900 !important; 
            text-transform: uppercase !important; 
            width: 100%; 
            border: none; 
            padding: 16px; 
            border-radius: 10px; 
            cursor: pointer;
            letter-spacing: 1.5px;
            margin-bottom: 12px;
            text-align: center;
        ">
            🔬 LABORATORIO DE SIMULACIÓN
        </div>
    </a>
    """, unsafe_allow_html=True)

st.markdown("---")

# SIDEBAR: SELECTOR LATERAL DE ESPECIE
with st.sidebar:
    st.markdown("### 🧬 Especie de Estudio")
    species = st.selectbox("", ["Bovino", "Porcino", "Ovino", "Caprino", "Equino"])
    
    data = SPECIES_DATA[species]
    
    st.markdown("---")
    st.markdown("### 📊 Parámetros Fisiológicos")
    st.info(f"**Duración Ciclo:** {data['cycle_duration']} días")
    st.success(f"**Momento de Ovulación:** {data['ovulation_timing']}")
    if data['maternal_recognition'] and data['maternal_recognition'] != "?":
        st.warning(f"**Reconocimiento Materno:** {data['maternal_recognition']}")

# --- SECCIÓN 1: FASES DEL CICLO DINÁMICAS ---
if st.session_state.seccion_activa == "Fases del Ciclo Estral":
    st.markdown(f"""
    <div class='browser-window neon-cyan'>
        <div class='window-header'>
            <span class='dot red'></span><span class='dot yellow'></span><span class='dot green'></span>
        </div>
        <div class='window-content'>
            <h3>📅 Línea de Tiempo Fisiológica: {species}</h3>
            <p>Dinámica hormonal y biológica ajustada específicamente para el modelo <b>{species}</b>.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Base de datos interactiva para la Línea de Tiempo
    TIMELINE_DATA = {
        "Bovino": {
            "proestro": {"dur": "2-3 días", "icon": "🫧", "title": "Folículo en crecimiento", "text": "Crecimiento del folículo dominante (4mm a 12-18mm). El Estradiol (E2) aumenta causando moco cervical transparente/filante, edema vulvar y relajación cervical."},
            "estro": {"dur": "12-18 horas (Holstein alta prod.: <10h)", "icon": "🎯", "title": "Receptividad sexual", "text": "Período de receptividad sexual activa. Monta aceptada es el signo primario debido a E2 alto. Surge preovulatorio de LH."},
            "metaestro": {"dur": "3-4 días", "icon": "🏗️", "title": "CL en formación", "text": "Ovulación ocurre 10-14h post-fin del estro. Luteinización del folículo ovulado para formar el Cuerpo Lúteo (CL) e inicio de secreción de P4. Posible sangrado metéstrico vaginal (24-48h post-ovulación)."},
            "diestro": {"dur": "12-14 días", "icon": "🏰", "title": "CL Maduro", "text": "Fase más larga (CL maduro con P4 máxima). Sin reconocimiento materno (días 17-18), la PGF2α endometrial destruye el CL (luteólisis) para reiniciar el ciclo. Si hay preñez, el embrión libera IFN-τ."}
        },
        "Porcino": {
            "proestro": {"dur": "2-3 días", "icon": "🫧", "title": "Crecimiento Múltiple", "text": "Fase folicular rápida. Crecimiento de múltiples folículos simultáneos (poliovulatorio)."},
            "estro": {"dur": "24-72 horas", "icon": "🎯", "title": "Receptividad prolongada", "text": "Receptividad sexual prolongada. Signo clave: Reflejo de inmovilidad (lordosis con orejas rígidas) ante presión dorsal y feromonas del verraco."},
            "metaestro": {"dur": "2-3 días", "icon": "🏗️", "title": "Formación de CLs", "text": "Ovulación de 15-25 folículos entre las 36-44h post-inicio del estro. Formación de múltiples cuerpos lúteos e inicio de la secreción de Progesterona (P4)."},
            "diestro": {"dur": "11-13 días", "icon": "🏰", "title": "Dominio de P4", "text": "Producción masiva de P4. Para evitar la luteólisis, se requiere el reconocimiento materno mediado por los estrógenos de mínimo 4 embriones."}
        },
        "Ovino": {
            "proestro": {"dur": "1-2 días", "icon": "🫧", "title": "Desarrollo Rápido", "text": "Crecimiento folicular rápido. Ciclicidad poliéstrica estacional de días cortos (otoño) estimulada por melatonina."},
            "estro": {"dur": "24-36 horas", "icon": "🎯", "title": "Celo Discreto", "text": "Signos conductuales muy discretos. Búsqueda activa del macho. Ovulación de 1-3 folículos hacia el final de esta fase."},
            "metaestro": {"dur": "2-3 días", "icon": "🏗️", "title": "CL Temprano", "text": "Formación del cuerpo lúteo joven y transición rápida hacia la secreción de progesterona (P4)."},
            "diestro": {"dur": "10-12 días", "icon": "🏰", "title": "Fase Lútea Acortada", "text": "Fase lútea acortada en comparación con bovinos. Dominio de P4. Reconocimiento materno embrionario mediado por IFN-τ en el útero."}
        },
        "Caprino": {
            "proestro": {"dur": "2-3 días", "icon": "🫧", "title": "Reclutamiento", "text": "Fase de reclutamiento y dominancia de 1-3 folículos. Poliéstrica estacional (con menor estacionalidad en regiones tropicales)."},
            "estro": {"dur": "24-48 horas", "icon": "🎯", "title": "Celo Evidente", "text": "Signos de celo evidentes por vocalización y movimiento continuo de cola. Inducción de la ciclicidad por el 'Efecto Macho'."},
            "metaestro": {"dur": "2-3 días", "icon": "🏗️", "title": "Luteinización", "text": "Ovulación ocurre unas 30 horas post-inicio de estro. Organización de 1-3 cuerpos lúteos en los ovarios."},
            "diestro": {"dur": "13-15 días", "icon": "🏰", "title": "Dominio Lúteo", "text": "Dominio lúteo clásico de P4. Sin gestación, la PGF2α induce la luteólisis. Si hay preñez, el reconocimiento embrionario se realiza por IFN-τ."}
        },
        "Equino": {
            "proestro": {"dur": "2-3 días", "icon": "🫧", "title": "Transición Inicial", "text": "Fase folicular inicial bajo influencia del fotoperíodo (poliéstrica estacional de días largos / primavera)."},
            "estro": {"dur": "4-7 días", "icon": "🎯", "title": "Celo Muy Prolongado", "text": "Signos severos ante el semental (postura de monta, cola levantada, micción y 'guiño' de vulva rítmico)."},
            "metaestro": {"dur": "2-3 días", "icon": "🏗️", "title": "Ovulación Especial", "text": "¡Particularidad única!: La ovulación ocurre 24-48h ANTES de terminar el estro. Inicio del desarrollo lúteo. La IA se debe programar DURANTE el celo."},
            "diestro": {"dur": "10-12 días", "icon": "🏰", "title": "Reinicio Rápido", "text": "Dominio estricto de P4. Si no hay gestación, la yegua regresa al proestro rápidamente debido a la luteólisis fisiológica."}
        }
    }
    
    sd = TIMELINE_DATA[species]
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #2D142C, #511845); border-radius: 12px; padding: 20px; border: 1px solid #FF3366; height: 100%;">
            <h3 style="color: #FF3366; margin-top:0;">🔴 Proestro</h3>
            <p style="font-size: 0.85rem; color:#A0AAB5;"><i>Duración: {sd['proestro']['dur']}</i></p>
            <p style="font-size: 1.2rem;">{sd['proestro']['icon']} <b>{sd['proestro']['title']}</b></p>
            <hr style="border-color: #FF3366; opacity: 0.3;">
            <p class="texto-lectura-grande">{sd['proestro']['text']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #3A0CA3, #4361EE); border-radius: 12px; padding: 20px; border: 1px solid #4CC9F0; height: 100%;">
            <h3 style="color: #4CC9F0; margin-top:0;">🔥 Estro</h3>
            <p style="font-size: 0.85rem; color:#A0AAB5;"><i>Duración: {sd['estro']['dur']}</i></p>
            <p style="font-size: 1.2rem;">{sd['estro']['icon']} <b>{sd['estro']['title']}</b></p>
            <hr style="border-color: #4CC9F0; opacity: 0.3;">
            <p class="texto-lectura-grande">{sd['estro']['text']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #4A3A15, #7D5A29); border-radius: 12px; padding: 20px; border: 1px solid #F8961E; height: 100%;">
            <h3 style="color: #F8961E; margin-top:0;">🟡 Metaestro</h3>
            <p style="font-size: 0.85rem; color:#A0AAB5;"><i>Duración: {sd['metaestro']['dur']}</i></p>
            <p style="font-size: 1.2rem;">{sd['metaestro']['icon']} <b>{sd['metaestro']['title']}</b></p>
            <hr style="border-color: #F8961E; opacity: 0.3;">
            <p class="texto-lectura-grande">{sd['metaestro']['text']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c4:
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1A3A28, #2D6A4F); border-radius: 12px; padding: 20px; border: 1px solid #52B788; height: 100%;">
            <h3 style="color: #52B788; margin-top:0;">🟢 Diestro</h3>
            <p style="font-size: 0.85rem; color:#A0AAB5;"><i>Duración: {sd['diestro']['dur']}</i></p>
            <p style="font-size: 1.2rem;">{sd['diestro']['icon']} <b>{sd['diestro']['title']}</b></p>
            <hr style="border-color: #52B788; opacity: 0.3;">
            <p class="texto-lectura-grande">{sd['diestro']['text']}</p>
        </div>
        """, unsafe_allow_html=True)

# --- SECCIÓN 2: CALCULADORA DE DIAGNÓSTICO E IA ---
if st.session_state.seccion_activa == "Checklist de Celo e IA":
    st.markdown("""
    <div class='browser-window neon-emerald'>
        <div class='window-header'>
            <span class='dot red'></span><span class='dot yellow'></span><span class='dot green'></span>
        </div>
        <div class='window-content'>
            <h3>🧮 Calculadora Diagnóstica y Decisiones Clínicas</h3>
            <p style='margin:0; color:#8B949E;'>Evaluación interactiva del paciente y análisis de impacto económico en finca.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.2, 1])
    
    with c1:
        with st.container(border=True):
            st.markdown(f"""
            <div class='browser-window neon-orange' style='margin-bottom:15px;'>
                <div class='window-header'>
                    <span class='dot red'></span><span class='dot yellow'></span><span class='dot green'></span>
                </div>
                <div class='window-content' style='padding:10px 15px;'>
                    <h4 style='margin:0;'>☑️ Score de Celo ({species})</h4>
                </div>
            </div>
            """, unsafe_allow_html=True)
            score = 0
            
            # El primer signo de la lista siempre lo consideramos el Primario (100 pts)
            for i, signo in enumerate(data["checklist"]):
                is_checked = st.checkbox(signo, key=f"chk_{species}_{i}")
                if is_checked:
                    if i == 0:
                        score += 100
                    else:
                        score += 25
            
            st.markdown("---")
            if score >= 100:
                st.success("📢 **¡CELO CONFIRMADÍSIMO!** Proceder al protocolo de Inseminación Artificial o Monta Dirigida.")
            elif score > 0 and score < 75:
                st.warning("⚠️ **SOSPECHA DE CELO (ESTRO INCOMPLETO).** No inseminar aún; se recomienda monitorear activamente.")
            elif score >= 75 and score < 100:
                st.warning("⚠️ **ALTA PROBABILIDAD DE CELO.** Signos secundarios evidentes. Observar de cerca para conformación primaria.")
            else:
                st.markdown("<div style='padding:1rem; background-color:#161B22; border-radius:8px; border:1px solid #30363D; color:#8B949E;'>ℹ️ Marque los signos clínicos observados en el hato para generar el diagnóstico reproductivo automático.</div>", unsafe_allow_html=True)

    with c2:
        with st.container(border=True):
            st.markdown(f"""
            <div class='browser-window neon-cyan' style='margin-bottom:15px;'>
                <div class='window-header'>
                    <span class='dot red'></span><span class='dot yellow'></span><span class='dot green'></span>
                </div>
                <div class='window-content' style='padding:10px 15px;'>
                    <h4 style='margin:0;'>🎯 Decisiones de IA ({species})</h4>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if species == "Bovino":
                st.markdown("**Simulador Interactivo de Regla AM/PM:**")
                hora_celo = st.radio(
                    "¿A qué hora del día detectó el inicio del celo activo?",
                    ["Celo Detectado en la Mañana (AM - ej. 07:00 AM)", "Celo Detectado en la Tarde/Noche (PM - ej. 05:00 PM)"]
                )
                st.markdown("<br>", unsafe_allow_html=True)
                if "AM" in hora_celo:
                    st.success("🎯 **Ventana Óptima de IA:** Inseminar hoy por la tarde (estimado 3:00 PM - 5:00 PM). Ovulación estimada: 7:00 PM (12 horas post-celo).")
                else:
                    st.info("🎯 **Ventana Óptima de IA:** Inseminar mañana por la mañana a primera hora (estimado 7:00 AM). Ovulación estimada: 5:00 AM del día siguiente.")
            else:
                for regla in data["ia_window"]:
                    st.markdown(f"- {regla}")
                    
        with st.container(border=True):
            st.markdown("""
            <div class='browser-window neon-emerald' style='margin-bottom:15px;'>
                <div class='window-header'>
                    <span class='dot red'></span><span class='dot yellow'></span><span class='dot green'></span>
                </div>
                <div class='window-content' style='padding:10px 15px;'>
                    <h4 style='margin:0;'>💰 Retorno de Inversión (ROI)</h4>
                </div>
            </div>
            """, unsafe_allow_html=True)
            tech = st.selectbox("Estrategia de Detección de Celo en Finca:", ["Observación Visual Tradicional (~40% de éxito)", "Collares de Precisión o Monitoreo Automatizado (~90% de éxito)"])
            
            if "Observación" in tech:
                st.error("📉 **Pérdida anual silenciosa de $150-200 USD por vaca.** El 60-70% de las montas de celo ocurren de noche cuando no hay personal vigilando.")
            else:
                st.success("📈 **Sincronización de datos en tiempo real.** Retorno de inversión (ROI) tecnológico estimado en menos de 6 meses al reducir días abiertos.")

# --- SECCIÓN 3: LABORATORIO DE SIMULACIÓN Y COMPLICACIONES ---
if st.session_state.seccion_activa == "Laboratorio de Simulación":
    
    # 1. Modificadores de Salud Condicionales
    st.markdown("""
    <div class='browser-window neon-orange'>
        <div class='window-header'>
            <span class='dot red'></span><span class='dot yellow'></span><span class='dot green'></span>
        </div>
        <div class='window-content'>
            <h3>🩺 Modificadores de Salud y Estado de Gestación</h3>
            <p style='margin:0; color:#8B949E;'>Configura las variables patológicas para simular el comportamiento endocrino.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar session_state si no existe
    if 'escenario_radio' not in st.session_state:
        st.session_state.escenario_radio = "Ciclo Vacío (Sin Embrión - Actúa PGF2α)"
    if 'patologia_radio' not in st.session_state:
        st.session_state.patologia_radio = "Normal"

    # Definir opciones base para patología
    opciones_clinicas = ["Normal", "Balance Energético Negativo (BEN)", "Estrés Calórico"]
    if species in ["Bovino", "Caprino", "Equino"]:
        opciones_clinicas.insert(2, "Cuerpo Lúteo Persistente")

    # Regla: Si "Gestación Activa" está seleccionada, bloquear BEN y CL Persistente
    if st.session_state.escenario_radio == "Gestación Activa (Con Embrión - Reconocimiento Materno)":
        opciones_clinicas = [op for op in opciones_clinicas if op not in ["Balance Energético Negativo (BEN)", "Cuerpo Lúteo Persistente"]]

    # Si la patología actual ya no es válida por el filtro, resetear a Normal
    if st.session_state.patologia_radio not in opciones_clinicas:
        st.session_state.patologia_radio = "Normal"
    
    c_mod1, c_mod2 = st.columns(2)
    with c_mod1:
        complication = st.radio(
            "Seleccione Patología:",
            opciones_clinicas,
            horizontal=True,
            key='patologia_radio'
        )
        
    # Regla: Si "BEN" o "CL Persistente", forzar Ciclo Vacío y deshabilitar Escenario
    patologias_bloqueantes = ["Balance Energético Negativo (BEN)", "Cuerpo Lúteo Persistente"]
    deshabilitar_gestacion = complication in patologias_bloqueantes
    
    if deshabilitar_gestacion:
        # Forzar estado sin gestación
        st.session_state.escenario_radio = "Ciclo Vacío (Sin Embrión - Actúa PGF2α)"

    with c_mod2:
        st.markdown("**Escenario Reproductivo:**")
        escenario = st.radio(
            "Seleccione Escenario:",
            ["Ciclo Vacío (Sin Embrión - Actúa PGF2α)", "Gestación Activa (Con Embrión - Reconocimiento Materno)"],
            label_visibility="collapsed",
            key='escenario_radio',
            disabled=deshabilitar_gestacion
        )
        pregnancy = "Gestación" in escenario
        
        if deshabilitar_gestacion:
            st.info("ℹ️ **Nota:** Gestación deshabilitada para esta patología.")
            
    # Caso Especial: Estrés Calórico + Gestación Activa
    if complication == "Estrés Calórico" and pregnancy:
        st.error("**⚠️ Alerta de Impacto Económico (Mortalidad Embrionaria Temprana):** El estrés por calor severo en zonas tropicales incrementa la temperatura uterina, deprime la viabilidad del embrión y bloquea su señal de reconocimiento antes del día 15. Esto genera una reabsorción embrionaria silenciosa, provocando el retorno de la hembra al celo. Pérdidas directas de $3.00 USD por día abierto adicional por animal.")
            
    # Mensaje informativo si se omite CL Persistente
    if species in ["Porcino", "Ovino"]:
        st.info(f"ℹ️ **Nota Clínica:** El 'Cuerpo Lúteo Persistente' no es una patología comúnmente diagnosticada ni representativa en {species.lower()}s. Ha sido deshabilitada para esta especie.")
        
    # Panel Agropecuario Dinámico de Patologías
    if complication == "Normal":
        with st.expander("📊 Diagnóstico Económico y Gestión - Normal", expanded=True):
            st.info("**✅ Diagnóstico Técnico:** Ciclicidad fisiológica óptima.")
            st.markdown("""
            <div class='texto-lectura-grande'>
                <ul>
                    <li class='item-lista-grande'><b>Métricas de Control:</b> Intervalo entre partos proyectado en 12-13 meses. Tasa de Detección de Celo (TDC) objetivo >80%.</li>
                    <li class='item-lista-grande'><b>Acción Agropecuaria:</b> Continuar con el registro zootécnico riguroso y monitoreo automatizado diario para inseminación programada.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    elif complication == "Balance Energético Negativo (BEN)":
        with st.expander("📊 Diagnóstico Económico y Gestión - BEN", expanded=True):
            st.markdown("""
            <div class="tarjeta-ben">
                <h4 style="color: #EF5350; margin-top: 0px; font-size: 20px;">⚠️ Balance Energético Negativo (BEN)</h4>
                <ul class="texto-lectura-grande">
                    <li class='item-lista-grande'><b>Diagnóstico Económico:</b> Incremento drástico de "Días Abiertos". Cada día extra por encima de los 85 días post-parto le cuesta al hato $3 USD en alimentación de mantenimiento y leche no producida. En un hato de 100 vacas, 30 días de BEN representan $9,000 USD de pérdida evitable al año.</li>
                    <li class='item-lista-grande'><b>Fisiología Productiva:</b> La alta producción de leche supera el consumo de materia seca. El cerebro detecta el déficit de energía y apaga el eje reproductivo (FSH/LH) para priorizar la supervivencia y la lactancia.</li>
                    <li class='item-lista-grande'><b>Soluciones Técnicas de Gestión:</b> Balancear raciones aumentando la densidad energética en el tercio inicial de lactancia (grasas sobrepasantes, carbohidratos fermentables). En cerdas lactantes, planificar el "Destete Sincronizado" del lote para agrupar el retorno al celo.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    elif complication == "Cuerpo Lúteo Persistente":
        with st.expander("📊 Diagnóstico Económico y Gestión - CL Persistente", expanded=True):
            st.markdown("""
            <div class="tarjeta-cl">
                <h4 style="color: #BA68C8; margin-top: 0px; font-size: 20px;">🛑 Cuerpo Lúteo Persistente</h4>
                <ul class="texto-lectura-grande">
                    <li class='item-lista-grande'><b>Diagnóstico Económico:</b> Provoca anestro prolongado (falsa preñez) que eleva los días abiertos y disminuye el índice de partos por año del hato.</li>
                    <li class='item-lista-grande'><b>Fisiología Productiva:</b> Inflamaciones o infecciones uterinas subclínicas bloquean físicamente la liberación de prostaglandina (PGF2α). El CL se mantiene intacto y la progesterona bloquea el ciclo.</li>
                    <li class='item-lista-grande'><b>Soluciones Técnicas de Gestión:</b> Reemplazar la observación visual ineficiente con protocolos de Inseminación Artificial a Tiempo Fijo (IATF, ej. Ovsynch o CIDR/DIB con progesterona) para inducir la ovulación y preñar el 100% de las hembras sincronizadas. Realizar ecografías post-parto preventivas a los 30 días.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    elif complication == "Estrés Calórico":
        with st.expander("📊 Diagnóstico Económico y Gestión - Estrés Calórico", expanded=True):
            st.markdown("""
            <div class="tarjeta-estres">
                <h4 style="color: #D4AF37; margin-top: 0px; font-size: 20px;">🥵 Estrés Calórico</h4>
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
    
    # 2. Control Slider y Auto-Play
    st.markdown("---")
    st.markdown("""
    <div class='browser-window neon-cyan' style='margin-bottom:10px;'>
        <div class='window-header'>
            <span class='dot red'></span><span class='dot yellow'></span><span class='dot green'></span>
        </div>
        <div class='window-content' style='padding:12px 20px;'>
            <h3 style='margin:0;'>⏱️ Simulador Endocrino en Tiempo Real</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_play, col_slider = st.columns([1.2, 4])
    with col_play:
        st.markdown("<br>", unsafe_allow_html=True)
    
    # ---------------------------
    # Generar HUD states (Pre-calcular)
    # ---------------------------
    df_json = df.to_dict(orient="records")
    hud_states = []
    for row in df_json:
        day_v = row["Día"]
        c_phase = get_current_phase(day_v, data["phases"])
        diag_txt, diag_typ = get_hud_diagnosis(day_v, c_phase["name"], complication, pregnancy, species)
        hud_states.append({"Día": day_v, "text": diag_txt, "type": diag_typ})
        
    export_obj = {
        "species": species,
        "complication": complication,
        "max_days": float(max_days),
        "data": df_json,
        "hud_states": hud_states
    }
    
    sim_data_json = json.dumps(export_obj, ensure_ascii=False)
    
    html_code = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
        <style>
            :root {{
                --bg: #0e1117;
                --border: #30363d;
                --text: #c9d1d9;
                --success: #2ea043;
                --error: #f85149;
                --warning: #d29922;
                --info: #58a6ff;
            }}
            body {{
                background-color: var(--bg); color: var(--text);
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                margin: 0; padding: 0;
            }}
            .controls-row {{
                display: flex; align-items: center; gap: 20px; margin-bottom: 20px; flex-wrap: wrap;
            }}
            .btn-play-pause {{
                background: #21262d; border: 1px solid var(--border); color: white;
                padding: 10px 20px; border-radius: 6px; cursor: pointer;
                font-size: 16px; font-weight: 500; transition: 0.2s; min-width: 180px;
            }}
            .btn-play-pause:hover {{ background: #30363d; border-color: #8b949e; }}
            .slider-container {{ flex-grow: 1; display: flex; flex-direction: column; min-width: 250px; }}
            .slider-container label {{ font-size: 14px; margin-bottom: 5px; color: #8b949e; }}
            input[type=range] {{ width: 100%; cursor: pointer; }}
            
            .hud-alert {{ padding: 20px; border-radius: 8px; margin-bottom: 20px; font-size: 20px; font-weight: bold; border-left-width: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); line-height: 1.4; }}
            .hud-success {{ background: rgba(46, 160, 67, 0.15); border: 1px solid var(--success); border-left-color: var(--success); color: #7ee787; }}
            .hud-error {{ background: rgba(248, 81, 73, 0.15); border: 1px solid var(--error); border-left-color: var(--error); color: #ff7b72; }}
            .hud-warning {{ background: rgba(210, 153, 34, 0.15); border: 1px solid var(--warning); border-left-color: var(--warning); color: #e3b341; }}
            .hud-info {{ background: rgba(88, 166, 255, 0.15); border: 1px solid var(--info); border-left-color: var(--info); color: #79c0ff; }}
            
            .metrics-grid {{
                display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 10px; margin-bottom: 20px; border: 1px solid var(--border);
                padding: 15px; border-radius: 8px;
            }}
            .metric {{ display: flex; flex-direction: column; }}
            .metric-label {{ font-size: 14px; color: #8b949e; margin-bottom: 5px; }}
            .metric-value {{ font-size: 28px; font-weight: bold; color: white; }}
            .plot-container {{ border: 1px solid var(--border); border-radius: 8px; padding: 10px; background: #0e1117; }}
        </style>
    </head>
    <body>
        <div class="controls-row">
            <button id="btnPlay" class="btn-play-pause">▶️ Reproducir (20s)</button>
            <div class="slider-container">
                <label>Desliza para avanzar el 'Día del Ciclo' manualmente:</label>
                <input type="range" id="timeSlider" min="0" max="100" step="0.1" value="0">
            </div>
        </div>
        
        <div id="hudBox" class="hud-alert hud-info">Inicializando simulación...</div>
        
        <div class="metrics-grid">
            <div class="metric"><span class="metric-label">🟣 FSH (%)</span><span id="met-fsh" class="metric-value">0.0%</span></div>
            <div class="metric"><span class="metric-label">🔴 LH (%)</span><span id="met-lh" class="metric-value">0.0%</span></div>
            <div class="metric"><span class="metric-label">🔵 E2 (%)</span><span id="met-e2" class="metric-value">0.0%</span></div>
            <div class="metric"><span class="metric-label">🟢 P4 (%)</span><span id="met-p4" class="metric-value">0.0%</span></div>
            <div class="metric"><span class="metric-label" id="lbl-mat">🟠 PGF2α (%)</span><span id="met-mat" class="metric-value">0.0%</span></div>
        </div>
        
        <div class="plot-container">
            <div id="plotlyChart" style="width: 100%; height: 500px;"></div>
        </div>
        
        <script>
            const simData = {sim_data_json};
            const df = simData.data;
            const hudStates = simData.hud_states;
            const maxDays = simData.max_days;
            
            document.getElementById("timeSlider").max = maxDays;
            const btnPlay = document.getElementById("btnPlay");
            const hudBox = document.getElementById("hudBox");
            const lblMat = document.getElementById("lbl-mat");
            
            let matLabel = "🟠 PGF2α (%)";
            let matKey = "PGF2α";
            if ("{str(pregnancy).lower()}" === "true") {{
                if ("{species}" === "Porcino") matLabel = "⚪ Estrógenos Emb. (%)";
                else if ("{species}" === "Equino") matLabel = "⚪ Movilidad Emb. (%)";
                else matLabel = "⚪ IFN-τ (%)";
                matKey = "Señal Materna";
            }}
            lblMat.innerText = matLabel;

            const colors = {{
                "FSH": "#BC8BFF", "LH": "#FF3366", "Estradiol (E2)": "#58A6FF",
                "Progesterona (P4)": "#00CC99", "PGF2α": "#FF4500", "Señal Materna": "#00FFFF"
            }};
            
            let isPlaying = false; let currentDay = 0.0; let animationFrameId = null; let lastTime = 0;
            const durationMs = 20000; const speedPerMs = maxDays / durationMs; 

            function initPlot() {{
                const traces = [
                    {{ x: [], y: [], mode: 'lines', name: 'FSH', line: {{color: colors['FSH'], width: 3.5}}, hoverinfo: 'skip' }},
                    {{ x: [], y: [], mode: 'lines', name: 'LH', line: {{color: colors['LH'], width: 3.5}}, hoverinfo: 'skip' }},
                    {{ x: [], y: [], mode: 'lines', name: 'Estradiol (E2)', line: {{color: colors['Estradiol (E2)'], width: 3.5}}, hoverinfo: 'skip' }},
                    {{ x: [], y: [], mode: 'lines', name: 'Progesterona (P4)', line: {{color: colors['Progesterona (P4)'], width: 3.5}}, hoverinfo: 'skip' }},
                    {{ x: [], y: [], mode: 'lines', name: matKey, line: {{color: colors[matKey], width: 3.5}}, hoverinfo: 'skip' }}
                ];
                const layout = {{
                    template: 'plotly_dark', plot_bgcolor: 'rgba(0,0,0,0)', paper_bgcolor: 'rgba(0,0,0,0)',
                    margin: {{l: 0, r: 0, t: 10, b: 0}},
                    xaxis: {{title: 'Días del Ciclo', range: [0, maxDays], gridcolor: '#30363D'}},
                    yaxis: {{title: 'Concentración (%)', range: [0, 105], gridcolor: '#30363D'}},
                    legend: {{orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1}},
                    shapes: [{{type: 'line', x0: 0, x1: 0, y0: 0, y1: 105, line: {{color: '#FFF', width: 3}}}}],
                    annotations: [{{
                        x: 0, y: 105, text: 'DÍA 0.0', showarrow: false,
                        xanchor: 'left', yanchor: 'top', 
                        font: {{color: '#FFF', size: 22}},
                        bgcolor: 'rgba(0,0,0,0.8)', bordercolor: '#FFF', borderpad: 6, borderwidth: 1, bordercolor: '#30363d'
                    }}]
                }};
                Plotly.newPlot('plotlyChart', traces, layout, {{displayModeBar: false, responsive: true}});
                updateUI(0);
            }}
            
            function updateUI(day) {{
                let idx = 0; let minDiff = Infinity;
                for(let i=0; i<df.length; i++) {{
                    let diff = Math.abs(df[i]['Día'] - day);
                    if(diff < minDiff) {{ minDiff = diff; idx = i; }}
                }}
                const row = df[idx]; const hud = hudStates[idx];
                
                document.getElementById("met-fsh").innerText = row['FSH'].toFixed(1) + '%';
                document.getElementById("met-lh").innerText = row['LH'].toFixed(1) + '%';
                document.getElementById("met-e2").innerText = row['Estradiol (E2)'].toFixed(1) + '%';
                document.getElementById("met-p4").innerText = row['Progesterona (P4)'].toFixed(1) + '%';
                document.getElementById("met-mat").innerText = row[matKey].toFixed(1) + '%';
                
                hudBox.innerText = hud.text; hudBox.className = "hud-alert hud-" + hud.type;
                
                const x = []; const fsh = []; const lh = []; const e2 = []; const p4 = []; const mat = [];
                for(let i=0; i<=idx; i++) {{
                    x.push(df[i]['Día']); fsh.push(df[i]['FSH']); lh.push(df[i]['LH']);
                    e2.push(df[i]['Estradiol (E2)']); p4.push(df[i]['Progesterona (P4)']); mat.push(df[i][matKey]);
                }}
                
                Plotly.update('plotlyChart', {{x: [x,x,x,x,x], y: [fsh,lh,e2,p4,mat]}}, {{
                    'shapes[0].x0': day, 'shapes[0].x1': day,
                    'annotations[0].x': day, 'annotations[0].text': 'DÍA ' + day.toFixed(1)
                }});
            }}
            
            function animate(time) {{
                if (!isPlaying) return;
                if (lastTime !== 0) {{
                    currentDay += (time - lastTime) * speedPerMs;
                    if (currentDay >= maxDays) {{ currentDay = maxDays; isPlaying = false; btnPlay.innerText = "▶️ Reproducir (20s)"; }}
                    document.getElementById("timeSlider").value = currentDay;
                    updateUI(currentDay);
                }}
                lastTime = time;
                if (isPlaying) requestAnimationFrame(animate); else lastTime = 0;
            }}
            
            btnPlay.addEventListener('click', () => {{
                if (isPlaying) {{ isPlaying = false; btnPlay.innerText = "▶️ Reanudar"; lastTime = 0; }}
                else {{ if (currentDay >= maxDays) currentDay = 0.0; isPlaying = true; btnPlay.innerText = "⏸️ Pausar"; requestAnimationFrame(animate); }}
            }});
            
            document.getElementById("timeSlider").addEventListener('input', (e) => {{
                currentDay = parseFloat(e.target.value); updateUI(currentDay);
                if (!isPlaying) btnPlay.innerText = currentDay < maxDays ? "▶️ Reanudar" : "▶️ Reproducir (20s)";
            }});
            initPlot();
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=850)

