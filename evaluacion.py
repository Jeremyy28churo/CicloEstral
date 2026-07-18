"""
Modulo de Evaluacion Interactiva - Ciclo Estral Comparado
Fuente: Clase10_Ciclo_Estral_Comparado.pdf
Lenguaje academico formal. Sin emojis. Termino taxonomico: Equino.
"""
import random
import streamlit as st

# =============================================================================
# BANCO DE 50 PREGUNTAS DE OPCION MULTIPLE
# Basadas estrictamente en: Clase10_Ciclo_Estral_Comparado.pdf
# Formato: {"pregunta": str, "opciones": [4 str], "correcta": int (0-indexed)}
# =============================================================================

BANCO_PREGUNTAS = [
    {
        "pregunta": "¿Cuál es la secuencia cronológica correcta de las fases del ciclo estral bovino?",
        "opciones": [
            "Estro, Proestro, Diestro, Metaestro",
            "Proestro, Estro, Metaestro, Diestro",
            "Diestro, Proestro, Metaestro, Estro",
            "Metaestro, Estro, Diestro, Proestro"
        ],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuál es la duración fisiológica total del ciclo estral bovino promedio?",
        "opciones": [
            "17 días",
            "21 días",
            "21-22 días",
            "25 días"
        ],
        "correcta": 1
    },
    {
        "pregunta": "Durante el proestro bovino, ¿qué dimensiones alcanza el folículo dominante en su fase de crecimiento preovulatorio?",
        "opciones": [
            "De 1 mm a 5 mm",
            "De 4 mm a 12-18 mm",
            "De 10 mm a 30 mm",
            "De 2 mm a 8 mm"
        ],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuál es la duración promedio del estro clínico en una hembra bovina de raza Holstein de alta producción?",
        "opciones": [
            "18-24 horas",
            "12-18 horas",
            "Menos de 10 horas",
            "24-36 horas"
        ],
        "correcta": 2
    },
    {
        "pregunta": "¿Qué signo primario indica la receptividad estral en bovinos y cuál es su especificidad diagnóstica?",
        "opciones": [
            "Moco cervical filante, especificidad 70%",
            "Aumento de actividad locomotora, especificidad 80%",
            "Monta aceptada, especificidad mayor al 95%",
            "Alza de temperatura vaginal, especificidad 85%"
        ],
        "correcta": 2
    },
    {
        "pregunta": "¿En qué ventana temporal ocurre la ovulación bovina respecto a la finalización del estro?",
        "opciones": [
            "Al inicio del estro",
            "36-44 horas post-inicio",
            "10-14 horas post-fin del estro",
            "24-48 horas antes del fin del estro"
        ],
        "correcta": 2
    },
    {
        "pregunta": "¿Qué molécula secretada por el embrión bovino actúa como señal de reconocimiento materno para bloquear la luteólisis?",
        "opciones": [
            "Progesterona (P4)",
            "Estradiol (E2)",
            "Interferón tau (IFN-t)",
            "Prostaglandina F2alfa"
        ],
        "correcta": 2
    },
    {
        "pregunta": "En un ciclo bovino no gestacional, ¿qué evento endocrino desencadena la regresión del cuerpo lúteo?",
        "opciones": [
            "El pico preovulatorio de LH",
            "La liberación de PGF2alfa por el endometrio en los días 17-18",
            "La caída del estradiol al inicio del proestro",
            "La producción de inhibina por el folículo dominante"
        ],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuál es la extensión temporal de la fase de diestro en el ciclo estral bovino?",
        "opciones": [
            "3-4 días",
            "2-3 días",
            "12-18 horas",
            "12-14 días"
        ],
        "correcta": 3
    },
    {
        "pregunta": "¿Qué función endocrina primaria cumple la progesterona (P4) durante el diestro bovino?",
        "opciones": [
            "Estimular el surge preovulatorio de LH",
            "Inhibir GnRH, impedir nueva ovulación y preparar el útero para la gestación",
            "Causar luteólisis endometrial",
            "Inducir el crecimiento del folículo dominante"
        ],
        "correcta": 1
    },
    {
        "pregunta": "Desde el punto de vista reproductivo, ¿qué patrón de ciclicidad presenta la especie del Equino?",
        "opciones": [
            "Poliéstrica continua",
            "Monoéstrica estacional",
            "Poliéstrica estacional de días largos",
            "Poliéstrica estacional de días cortos"
        ],
        "correcta": 2
    },
    {
        "pregunta": "¿Qué particularidad fisiológica distingue el momento de la ovulación en el Equino en comparación con la especie bovina?",
        "opciones": [
            "La ovulación ocurre 10-14 horas después del fin del estro",
            "La ovulación ocurre 24-48 horas ANTES del fin del estro",
            "La ovulación ocurre al inicio del estro",
            "La ovulación ocurre 36-44 horas post-inicio del estro"
        ],
        "correcta": 1
    },
    {
        "pregunta": "¿En qué momento estratégico se recomienda realizar la inseminación artificial en el Equino?",
        "opciones": [
            "10-14 horas después del fin del estro",
            "Durante el estro, no después de su finalización",
            "36 horas post-inicio del estro",
            "24 horas antes del inicio del estro"
        ],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuál es la duración del periodo de estro en la hembra del Equino?",
        "opciones": [
            "12-18 horas",
            "24-72 horas",
            "4-7 días",
            "24-36 horas"
        ],
        "correcta": 2
    },
    {
        "pregunta": "¿Qué signo clínico específico manifiesta la hembra del Equino en estro ante la presencia del reproductor macho?",
        "opciones": [
            "Aumento de actividad locomotora del 200-400%",
            "Moco cervical filante y cristalino",
            "Guiño vulvar rítmico, vulva relajada y postura de monta con cola levantada",
            "Monta aceptada con especificidad mayor al 95%"
        ],
        "correcta": 2
    },
    {
        "pregunta": "En la fisiología reproductiva porcina, ¿cuál es la tasa ovulatoria característica por ciclo?",
        "opciones": [
            "1 ovulación",
            "1-3 ovulaciones",
            "5-8 ovulaciones",
            "15-25 ovulaciones"
        ],
        "correcta": 3
    },
    {
        "pregunta": "¿Cuál es el signo clínico primario para la detección de celo en la cerda y qué sensibilidad presenta ante la presencia del verraco?",
        "opciones": [
            "Monta aceptada, especificidad mayor al 95%",
            "Reflejo de inmovilidad ante presión dorsal, sensibilidad mayor al 90%",
            "Moco cervical filante, sensibilidad del 70%",
            "Efecto macho, sensibilidad del 60%"
        ],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué patrón de ciclicidad presenta la especie ovina y qué hormona actúa como regulador fotoperiódico principal?",
        "opciones": [
            "Días largos, regulada por estradiol",
            "Días cortos (otoño), regulada por melatonina",
            "Días largos, regulada por melatonina",
            "Continua, regulada por progesterona"
        ],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuál es la duración fisiológica del ciclo estral en la oveja?",
        "opciones": [
            "21 días",
            "17 días",
            "21-22 días",
            "25-27 horas"
        ],
        "correcta": 1
    },
    {
        "pregunta": "¿En qué difiere el mecanismo de reconocimiento materno de la cerda respecto al de la especie bovina?",
        "opciones": [
            "La cerda produce IFN-t igual que el bovino",
            "La cerda produce estrógenos embrionarios como molécula de reconocimiento materno",
            "La cerda no posee reconocimiento materno",
            "La cerda produce progesterona embrionaria"
        ],
        "correcta": 1
    },
    {
        "pregunta": "En sistemas de ganadería tropical, ¿cuál es la Tasa de Detección de Celo (TDC) promedio lograda mediante observación visual?",
        "opciones": [
            "70-80%",
            "85-95%",
            "30-40%",
            "55-65%"
        ],
        "correcta": 2
    },
    {
        "pregunta": "¿Cuál es la fórmula epidemiológica para calcular la Tasa de Preñez por ciclo (Pregnancy Rate)?",
        "opciones": [
            "TDC + Tasa de Concepción",
            "TDC x Tasa de Concepción",
            "Tasa de Concepción / TDC",
            "TDC - Tasa de Concepción"
        ],
        "correcta": 1
    },
    {
        "pregunta": "En un hato con una TDC del 40% y una tasa de concepción del 50%, ¿cuál es la tasa de preñez resultante por ciclo?",
        "opciones": [
            "40%",
            "30%",
            "20%",
            "10%"
        ],
        "correcta": 2
    },
    {
        "pregunta": "¿Qué nivel de Tasa de Detección de Celo (TDC) se alcanza al implementar collares acelerómetros en el hato?",
        "opciones": [
            "40-60%",
            "60-70%",
            "85-95%",
            "Mayor al 99%"
        ],
        "correcta": 2
    },
    {
        "pregunta": "¿Qué porcentaje de los eventos estrales bovinos ocurren en horario nocturno (18:00 - 06:00) en vacas de alta producción?",
        "opciones": [
            "30-40%",
            "50-60%",
            "60-70%",
            "80-90%"
        ],
        "correcta": 2
    },
    {
        "pregunta": "¿Qué establece el protocolo AM/PM para optimizar el momento de la inseminación artificial bovina?",
        "opciones": [
            "Celo AM: inseminar la mañana siguiente; Celo PM: inseminar esa tarde",
            "Celo AM: inseminar esa tarde; Celo PM: inseminar la mañana siguiente",
            "Inseminar siempre a las 6:00 AM",
            "Inseminar 36 horas después de cualquier celo"
        ],
        "correcta": 1
    },
    {
        "pregunta": "Posterior al inicio del comportamiento estral bovino, ¿cuál es la ventana temporal óptima para realizar la inseminación artificial?",
        "opciones": [
            "0-6 horas",
            "6-16 horas",
            "18-24 horas",
            "24-36 horas"
        ],
        "correcta": 1
    },
    {
        "pregunta": "¿Cuánto tiempo requieren los espermatozoides bovinos para completar su capacitación en el tracto reproductivo de la hembra?",
        "opciones": [
            "1-2 horas",
            "6-8 horas",
            "12-14 horas",
            "24 horas"
        ],
        "correcta": 1
    },
    {
        "pregunta": "Al utilizar el sistema Herd Navigator basado en monitoreo de progesterona láctea, ¿qué sensibilidad se logra en la detección del estro?",
        "opciones": [
            "60-70%",
            "75-85%",
            "Mayor al 95%",
            "40-60%"
        ],
        "correcta": 2
    },
    {
        "pregunta": "¿Qué implicancia fisiológica tiene la observación de sangrado metéstrico vaginal 24 a 48 horas post-ovulación en la hembra bovina?",
        "opciones": [
            "Que la vaca está en pleno estro lista para inseminar",
            "Que la vaca padece metritis",
            "Que la vaca ya ovuló; NO debe inseminarse en ese momento",
            "Que inició el proestro del siguiente ciclo"
        ],
        "correcta": 2
    },
    {
        "pregunta": "En el ámbito de la biotecnología reproductiva, ¿qué significan las siglas IATF?",
        "opciones": [
            "Inseminación Asistida por Tecnología Folicular",
            "Indicador de Actividad y Temperatura Fisiológica",
            "Inseminación Artificial a Tiempo Fijo",
            "Índice de Acceso a la Tecnología de Fertilización"
        ],
        "correcta": 2
    },
    {
        "pregunta": "¿Cuál es la secuencia farmacológica correcta del protocolo de sincronización Ovsynch?",
        "opciones": [
            "PGF2alfa (Día 0) - GnRH (Día 7) - PGF2alfa (Día 9) - IATF (Día 10)",
            "GnRH (Día 0) - PGF2alfa (Día 7) - GnRH (Día 9) - IATF (Día 10)",
            "CIDR (Día 0) - PGF2alfa (Día 8) - GnRH (Día 9) - IATF (Día 10)",
            "GnRH (Día 0) - GnRH (Día 7) - PGF2alfa (Día 9) - IATF (Día 10)"
        ],
        "correcta": 1
    },
    {
        "pregunta": "En el protocolo Ovsynch, ¿cuál es el objetivo fisiológico de la administración inicial de GnRH (Día 0)?",
        "opciones": [
            "Destruir el cuerpo lúteo existente",
            "Ovular el folículo dominante presente y sincronizar el inicio de una nueva onda folicular",
            "Inducir el pico de LH para la IATF",
            "Estimular la liberación de progesterona luteal"
        ],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué efecto farmacodinámico ejerce la administración de PGF2alfa en el día 7 del protocolo Ovsynch?",
        "opciones": [
            "Sincronizar la onda folicular",
            "Inducir el surge de LH",
            "Destruir el cuerpo lúteo causando la caída abrupta de P4",
            "Estimular la producción de FSH hipofisiaria"
        ],
        "correcta": 2
    },
    {
        "pregunta": "En el esquema Ovsynch, ¿cuántas horas posteriores a la segunda dosis de GnRH debe ejecutarse la Inseminación Artificial a Tiempo Fijo?",
        "opciones": [
            "6-8 horas",
            "12-14 horas",
            "16-20 horas",
            "24-30 horas"
        ],
        "correcta": 2
    },
    {
        "pregunta": "¿Qué tasa de preñez por servicio se espera al aplicar el protocolo Ovsynch en vacas lecheras Bos taurus?",
        "opciones": [
            "20-30%",
            "35-40%",
            "45-55%",
            "65-75%"
        ],
        "correcta": 2
    },
    {
        "pregunta": "¿En qué subpoblación bovina se indica preferentemente el protocolo compuesto por CIDR + Benzoato de Estradiol + PGF2alfa + eCG?",
        "opciones": [
            "Vacas lecheras Holstein en clima frío",
            "Bos indicus y cruzas en condiciones tropicales",
            "Novillas de primer servicio en sistemas intensivos",
            "Vacas de alta producción con BEN severo"
        ],
        "correcta": 1
    },
    {
        "pregunta": "Al implementar IATF en bovinos Bos indicus bajo condiciones tropicales, ¿cuál es la tasa de preñez esperada?",
        "opciones": [
            "25-35%",
            "40-45%",
            "50-60%",
            "70-80%"
        ],
        "correcta": 2
    },
    {
        "pregunta": "En el manejo reproductivo porcino, ¿cuál es el método fisiológico utilizado para sincronizar el retorno al estro de un lote de cerdas?",
        "opciones": [
            "Con implantes de melatonina",
            "Con el destete del lote, que elimina la inhibición dopaminérgica y permite el retorno al celo en 4-7 días",
            "Con protocolo Ovsynch adaptado para porcinos",
            "Con machos marcadores de arnés"
        ],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué beneficio fisiológico aporta la pre-sincronización con dos dosis de PGF2alfa previo al inicio del protocolo Ovsynch?",
        "opciones": [
            "Reduce el costo del protocolo",
            "Aumenta el número de ovulaciones por ciclo",
            "Asegura que más vacas tengan CL funcional al inicio del Ovsynch, mejorando la preñez en 5-10%",
            "Sustituye la segunda GnRH del protocolo"
        ],
        "correcta": 2
    },
    {
        "pregunta": "Fisiológicamente, ¿por qué la hembra bovina es monovulatoria mientras que la cerda desarrolla dominancia folicular múltiple?",
        "opciones": [
            "Porque la vaca no posee onda folicular",
            "Porque en la vaca el folículo dominante produce inhibina + E2 que suprimen los demás; en la cerda la dominancia es débil y múltiples folículos maduran",
            "Porque el útero bovino no puede sostener más de un embrión",
            "Porque la cerda ovula folículo dominante de la primera onda"
        ],
        "correcta": 1
    },
    {
        "pregunta": "¿Qué porcentaje de gestaciones bovinas se interrumpe debido a muerte embrionaria temprana entre los días 8 y 30?",
        "opciones": [
            "5-10%",
            "10-15%",
            "20-30%",
            "40-50%"
        ],
        "correcta": 2
    },
    {
        "pregunta": "En términos económicos, ¿cuál es el costo estimado por cada día abierto adicional (superados los 85 días post-parto) en ganadería lechera?",
        "opciones": [
            "$0.50 USD/día",
            "$1.00 USD/día",
            "$3.00 USD/día",
            "$10.00 USD/día"
        ],
        "correcta": 2
    },
    {
        "pregunta": "¿En qué biomarcador se fundamenta el sistema automatizado Herd Navigator para el monitoreo del ciclo estral?",
        "opciones": [
            "Acelerómetro de actividad locomotora",
            "Cámara con inteligencia artificial",
            "Medición automatizada de progesterona en leche en cada ordeño",
            "Bolo intravaginal de temperatura"
        ],
        "correcta": 2
    },
    {
        "pregunta": "En la producción avícola comercial, ¿cuál es el fotoperiodo óptimo para estimular la actividad reproductiva de la gallina?",
        "opciones": [
            "8 horas de luz : 16 horas de oscuridad",
            "12 horas de luz : 12 horas de oscuridad",
            "16 horas de luz : 8 horas de oscuridad",
            "24 horas de luz continua"
        ],
        "correcta": 2
    },
    {
        "pregunta": "Gracias al almacenamiento espermático en los túbulos espermáticos (SST), ¿por cuántos días puede una gallina fertilizar óvulos tras una cópula?",
        "opciones": [
            "1-2 días",
            "3-5 días",
            "10-14 días",
            "21 días"
        ],
        "correcta": 2
    },
    {
        "pregunta": "En la especie ovina, ¿qué intervención biotecnológica se emplea para inducir el inicio anticipado de la temporada reproductiva?",
        "opciones": [
            "Implante de estradiol",
            "Implante de melatonina (Melovine)",
            "Dispositivo CIDR intravaginal",
            "Protocolo Ovsynch adaptado para ovinos"
        ],
        "correcta": 1
    },
    {
        "pregunta": "Según el análisis de caso de estudio, al incrementar la TDC del 42% al 88% mediante collares SCR en un hato de 200 vacas, ¿cuál fue el ahorro anual proyectado?",
        "opciones": [
            "$5,000 USD",
            "$19,000 USD",
            "$45,000 USD",
            "$100,000 USD"
        ],
        "correcta": 2
    },
    {
        "pregunta": "Para hatos lecheros que superan las 200 vacas en ordeño, ¿qué nivel de tecnificación recomienda la pirámide de decisión reproductiva?",
        "opciones": [
            "Solo observación visual con registros",
            "Parches de monta más observación visual",
            "Collares de actividad",
            "Cámaras con IA o monitoreo de P4 en leche"
        ],
        "correcta": 3
    },
    {
        "pregunta": "En la comunicación química porcina, ¿cuáles son las feromonas del verraco responsables de desencadenar el reflejo de inmovilidad en la cerda?",
        "opciones": [
            "Estradiol y progesterona",
            "Androstenona y androstenol",
            "GnRH y melatonina",
            "FSH y LH"
        ],
        "correcta": 1
    },
    {
        "pregunta": "Para optimizar la rentabilidad en sistemas de lechería especializada, ¿cuál es el intervalo entre partos objetivo?",
        "opciones": [
            "10-11 meses",
            "12-13 meses",
            "14-15 meses",
            "16-18 meses"
        ],
        "correcta": 1
    },
    {
        "pregunta": "Como indicador de alarma reproductiva, ¿qué hallazgo clínico sugiere la necesidad inmediata de evaluar el Balance Energético Negativo (BEN) y la funcionalidad lútea por ecografía?",
        "opciones": [
            "TDC menor al 50%",
            "Tasa de concepción menor al 30%",
            "Anestro mayor a 60 días post-parto",
            "Intervalo interestro irregular"
        ],
        "correcta": 2
    }
]

# =============================================================================
# FUNCION PRINCIPAL DEL MODULO DE EVALUACION
# Arquitectura anti-Ghost Rerun basada en st.session_state centralizado.
# =============================================================================

def renderizar_evaluacion():
    """
    Modulo interactivo de evaluacion formal.
    Selecciona 20 preguntas aleatorias del banco de 50.
    Umbral de aprobacion: 16/20 correctas (80%).

    Variables de estado gestionadas:
      eval_fase            : str  — "inicio" | "activo" | "finalizado"
      eval_preguntas       : list — 20 preguntas sorteadas aleatoriamente
      eval_respuestas      : dict — {idx_pregunta (int): idx_opcion (int)}
      eval_pregunta_actual : int  — indice 0-19 de la pregunta en pantalla
      eval_seleccion_actual: int|None — indice de la opcion marcada; persiste
                             entre reruns gracias al callback on_change del radio
      eval_puntaje         : int  — numero de respuestas correctas (resultado)
      eval_advertencia     : bool — activa el aviso de seleccion obligatoria
    """

    # =========================================================================
    # INICIALIZACION ROBUSTA — evita KeyError en cualquier orden de carga
    # =========================================================================
    defaults = {
        "eval_fase": "inicio",
        "eval_preguntas": [],
        "eval_respuestas": {},
        "eval_pregunta_actual": 0,
        "eval_seleccion_actual": None,
        "eval_puntaje": 0,
        "eval_advertencia": False,
    }
    for clave, valor_inicial in defaults.items():
        if clave not in st.session_state:
            st.session_state[clave] = valor_inicial

    # =========================================================================
    # CABECERA — visible en las tres pantallas del modulo
    # =========================================================================
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(22,33,25,0.9), rgba(12,22,16,0.95));
                padding: 30px 40px; border-radius: 14px;
                border-top: 4px solid #4CAF50;
                border: 1px solid rgba(76,175,80,0.2);
                margin-bottom: 30px;'>
        <h2 style='margin:0 0 8px 0; color:#4CAF50; font-weight:700; letter-spacing:1px;'>
            MODULO DE EVALUACION FORMAL
        </h2>
        <p style='margin:0; color:#B0BEC5; font-size:0.95rem;'>
            Ciclo Estral Comparado - Fisiologia Animal Aplicada | Clase 10
        </p>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================================
    # PANTALLA 1: INICIO — Instrucciones y arranque del examen
    # =========================================================================
    if st.session_state.eval_fase == "inicio":
        st.markdown("""
        <div style='background: rgba(255,255,255,0.03); padding:24px 30px;
                    border-radius:12px; border:1px solid rgba(255,255,255,0.07);
                    margin-bottom:24px;'>
            <h4 style='color:#E8F5E9; margin:0 0 12px 0; font-weight:600;'>Instrucciones del Examen</h4>
            <ul style='color:#B0BEC5; font-size:0.92rem; line-height:1.9; margin:0; padding-left:20px;'>
                <li>Se seleccionaran <b style="color:#4CAF50;">20 preguntas aleatorias</b> del banco de 50 preguntas.</li>
                <li>Las preguntas se presentaran <b style="color:#4CAF50;">una por una</b>. No podra retroceder a preguntas anteriores.</li>
                <li>Cada pregunta tiene <b style="color:#4CAF50;">4 opciones de respuesta</b>, de las cuales una es correcta.</li>
                <li>Para aprobar se requiere un minimo de <b style="color:#4CAF50;">16 respuestas correctas (80%).</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            if st.button("INICIAR EVALUACION", use_container_width=True, key="btn_iniciar_eval"):
                st.session_state.eval_preguntas = random.sample(BANCO_PREGUNTAS, 20)
                st.session_state.eval_respuestas = {}
                st.session_state.eval_pregunta_actual = 0
                st.session_state.eval_seleccion_actual = None
                st.session_state.eval_puntaje = 0
                st.session_state.eval_advertencia = False
                st.session_state.eval_fase = "activo"
                st.rerun()

    # =========================================================================
    # PANTALLA 2: CUESTIONARIO ACTIVO — Una pregunta por pantalla, sin retroceso
    # =========================================================================
    elif st.session_state.eval_fase == "activo":
        preguntas = st.session_state.eval_preguntas
        total = len(preguntas)
        idx = st.session_state.eval_pregunta_actual
        q = preguntas[idx]
        num = idx + 1

        # --- Barra de progreso ---
        progreso = idx / total
        st.markdown(f"""
        <div style='margin-bottom:6px; display:flex; justify-content:space-between;
                    font-size:0.82rem; color:#90A4AE;'>
            <span>Pregunta {num} de {total}</span>
            <span>{idx} respondidas &mdash; {total - idx} restantes</span>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progreso)
        st.markdown("<br>", unsafe_allow_html=True)

        # --- Enunciado de la pregunta ---
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.03); padding:22px 28px;
                    border-radius:10px; border:1px solid rgba(255,255,255,0.06);
                    margin-bottom:20px;'>
            <p style='margin:0; color:#E8F5E9; font-size:1.1rem; font-weight:500; line-height:1.5;'>
                <span style='color:#4CAF50; font-weight:800; font-size:1.2rem;'>{num}.</span> {q["pregunta"]}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # --- Callback: captura y persiste la seleccion del usuario ---
        # El callback se ejecuta ANTES de que el cuerpo principal del script
        # continue, por lo tanto eval_seleccion_actual siempre refleja el ultimo
        # valor elegido por el usuario, incluso ante reruns intermedios. Esto
        # elimina el Ghost Rerun: la seleccion no puede perderse.
        widget_key = f"radio_q_{idx}"

        def _registrar_seleccion():
            valor = st.session_state.get(widget_key)
            if valor is not None:
                st.session_state.eval_seleccion_actual = q["opciones"].index(valor)
            st.session_state.eval_advertencia = False

        # El indice inicial del radio se obtiene del estado persistido,
        # no de una variable local que se perderia en cada rerun.
        idx_inicial = st.session_state.eval_seleccion_actual

        st.radio(
            label="Seleccione una opcion de respuesta:",
            options=q["opciones"],
            index=idx_inicial,
            key=widget_key,
            on_change=_registrar_seleccion,
            label_visibility="collapsed"
        )

        # --- Aviso de seleccion obligatoria ---
        # Se renderiza directamente desde session_state, sin causar reruns
        # adicionales que borren la seleccion del usuario.
        if st.session_state.eval_advertencia:
            st.markdown("""
            <div style='background: rgba(239,83,80,0.08); border-left: 3px solid #EF5350;
                        padding: 10px 16px; border-radius: 0 8px 8px 0; margin-bottom: 12px;'>
                <p style='margin:0; color:#EF5350; font-size:0.9rem; font-weight:500;'>
                    Debe seleccionar una respuesta para continuar.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Boton de avance ---
        # Lee EXCLUSIVAMENTE desde session_state. Nunca lee el valor del widget
        # en tiempo real, lo que garantiza inmunidad total al Ghost Rerun.
        texto_boton = "SIGUIENTE PREGUNTA" if idx < total - 1 else "FINALIZAR EVALUACION"
        col_a, col_b, col_c = st.columns([1, 1.5, 1])
        with col_b:
            if st.button(texto_boton, use_container_width=True, key=f"btn_sig_{idx}"):
                if st.session_state.eval_seleccion_actual is None:
                    # Bloquear avance sin seleccion
                    st.session_state.eval_advertencia = True
                    st.rerun()
                else:
                    # Guardar la respuesta confirmada de esta pregunta
                    st.session_state.eval_respuestas[idx] = st.session_state.eval_seleccion_actual
                    st.session_state.eval_advertencia = False

                    if idx < total - 1:
                        # Avanzar: limpiar seleccion temporal e incrementar indice
                        st.session_state.eval_pregunta_actual += 1
                        st.session_state.eval_seleccion_actual = None
                        st.rerun()
                    else:
                        # Pregunta 20 confirmada: calcular puntaje y cerrar examen
                        puntaje = sum(
                            1 for i, p in enumerate(preguntas)
                            if st.session_state.eval_respuestas.get(i) == p["correcta"]
                        )
                        st.session_state.eval_puntaje = puntaje
                        st.session_state.eval_fase = "finalizado"
                        st.rerun()

    # =========================================================================
    # PANTALLA 3: RESULTADOS — Puntaje final y revision detallada de respuestas
    # =========================================================================
    elif st.session_state.eval_fase == "finalizado":
        puntaje = st.session_state.eval_puntaje
        total = 20
        porcentaje = (puntaje / total) * 100
        aprobado = puntaje >= 16
        color_res = "#4CAF50" if aprobado else "#EF5350"
        titulo_res = "EVALUACION APROBADA" if aprobado else "EVALUACION REPROBADA"
        mensaje = (
            "Rendimiento academico satisfactorio. El evaluado demuestra dominio de los contenidos "
            "del ciclo estral comparado, deteccion de celo y protocolos de sincronizacion."
            if aprobado else
            "Rendimiento insuficiente. Se recomienda repasar los temas de fisiologia hormonal, "
            "deteccion de celo y protocolos de sincronizacion antes de una nueva evaluacion."
        )

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(22,33,25,0.95), rgba(12,22,16,0.98));
                    padding: 40px 50px; border-radius: 16px;
                    border-top: 5px solid {color_res};
                    border: 1px solid rgba(255,255,255,0.07);
                    text-align: center; margin: 20px 0;'>
            <h2 style='color:{color_res}; font-weight:800; letter-spacing:2px; margin:0 0 8px 0;'>{titulo_res}</h2>
            <p style='font-size:3.5rem; font-weight:900; color:{color_res}; margin:20px 0 5px 0;'>{puntaje} / {total}</p>
            <p style='font-size:1.2rem; color:#B0BEC5; margin:0 0 20px 0;'>{porcentaje:.1f}% &mdash; Umbral de aprobacion: 80% (16 correctas)</p>
            <hr style='border-color:rgba(255,255,255,0.08); margin:20px 0;'>
            <p style='color:#90A4AE; font-size:0.9rem; margin:0;'>{mensaje}</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Revision detallada de respuestas", expanded=False):
            for i, q in enumerate(st.session_state.eval_preguntas):
                resp = st.session_state.eval_respuestas.get(i)
                es_correcta = resp == q["correcta"]
                color_icon = "#4CAF50" if es_correcta else "#EF5350"
                indicador = "CORRECTO" if es_correcta else "INCORRECTO"
                texto_respuesta = q["opciones"][resp] if resp is not None else "Sin responder"
                bloque_usuario = (
                    ""
                    if es_correcta
                    else f" | Su respuesta: <span style='color:#EF5350;'>{texto_respuesta}</span>"
                )
                st.markdown(f"""
                <div style='border-left: 3px solid {color_icon}; padding: 10px 16px;
                            margin-bottom: 12px; background: rgba(255,255,255,0.02);
                            border-radius: 0 8px 8px 0;'>
                    <p style='margin:0 0 4px 0; font-size:0.85rem; color:{color_icon};
                              font-weight:700; letter-spacing:1px;'>{i + 1}. {indicador}</p>
                    <p style='margin:0 0 6px 0; color:#E8F5E9; font-size:0.9rem;'>{q["pregunta"]}</p>
                    <p style='margin:0; color:#90A4AE; font-size:0.82rem;'>
                        Respuesta correcta: <b style="color:#4CAF50;">{q["opciones"][q["correcta"]]}</b>
                        {bloque_usuario}
                    </p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_x, col_y, col_z = st.columns([1, 1.5, 1])
        with col_y:
            if st.button("NUEVA EVALUACION", use_container_width=True, key="btn_nueva_eval"):
                claves_a_limpiar = [
                    "eval_fase",
                    "eval_preguntas",
                    "eval_respuestas",
                    "eval_pregunta_actual",
                    "eval_seleccion_actual",
                    "eval_puntaje",
                    "eval_advertencia",
                ]
                for k in claves_a_limpiar:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()
