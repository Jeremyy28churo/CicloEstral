"""
Modulo de Evaluacion Interactiva - Ciclo Estral Comparado
Fuente: Clase10_Ciclo_Estral_Comparado.pdf
Lenguaje academico formal. Sin emojis. Termino taxonomico: Equino.
"""
import random
import streamlit as st
import datetime

import json
import os

@st.cache_resource
def get_global_exam_state():
    state = {
        "activo": False,
        "hora_inicio": None,
        "registros": []
    }
    if os.path.exists("evaluaciones_registros.json"):
        try:
            with open("evaluaciones_registros.json", "r", encoding="utf-8") as f:
                state["registros"] = json.load(f)
        except Exception:
            pass
    return state

def save_global_exam_state(state):
    try:
        with open("evaluaciones_registros.json", "w", encoding="utf-8") as f:
            json.dump(state["registros"], f, ensure_ascii=False, indent=4)
    except Exception:
        pass

# =============================================================================
# BANCO DE 50 PREGUNTAS DE OPCION MULTIPLE
# Basadas estrictamente en: Clase10_Ciclo_Estral_Comparado.pdf
# Formato: {"pregunta": str, "opciones": [4 str], "correcta": int (0-indexed)}
# =============================================================================

BANCO_PREGUNTAS = [
    {
        "tipo": "emparejar",
        "pregunta": "Empareja cada especie con la duración promedio de su ciclo estral:",
        "pares": [
            "Vaca",
            "Cerda",
            "Oveja"
        ],
        "opciones": [
            "21 días (Poliovulatoria)",
            "21 días (rango 18-24)",
            "17 días (Estacional)"
        ],
        "correcta": {
            "Vaca": "21 días (rango 18-24)",
            "Cerda": "21 días (Poliovulatoria)",
            "Oveja": "17 días (Estacional)"
        }
    },
    {
        "tipo": "emparejar",
        "pregunta": "Clasifica la ciclicidad reproductiva según la especie:",
        "pares": [
            "Yegua",
            "Oveja",
            "Cabra (trópico)",
            "Gallina"
        ],
        "opciones": [
            "Poliéstrica estacional leve / continua",
            "Poliéstrica estacional (días cortos)",
            "Ciclo ovulatorio por fotoperíodo",
            "Poliéstrica estacional (días largos)"
        ],
        "correcta": {
            "Yegua": "Poliéstrica estacional (días largos)",
            "Oveja": "Poliéstrica estacional (días cortos)",
            "Cabra (trópico)": "Poliéstrica estacional leve / continua",
            "Gallina": "Ciclo ovulatorio por fotoperíodo"
        }
    },
    {
        "tipo": "completar_espacios",
        "pregunta": "En el protocolo Ovsynch, la primera {1} (Día 0) sincroniza una nueva onda folicular, luego la {2} (Día 7) destruye el cuerpo lúteo, y finalmente la segunda GnRH (Día 9) programa la {3} para realizar la IATF.",
        "opciones": {
            "1": [
                "GnRH",
                "PGF2alfa",
                "Progesterona"
            ],
            "2": [
                "PGF2alfa",
                "eCG",
                "Inhibina"
            ],
            "3": [
                "Ovulación",
                "Luteólisis",
                "Atresia"
            ]
        },
        "correcta": {
            "1": "GnRH",
            "2": "PGF2alfa",
            "3": "Ovulación"
        }
    },
    {
        "tipo": "completar_espacios",
        "pregunta": "Según la regla AM/PM bovina, si se detecta el celo a las 7:00 AM, la inseminación debe realizarse a las {1}, ya que la ovulación ocurrirá aproximadamente a las {2}.",
        "opciones": {
            "1": [
                "3:00 PM (misma tarde)",
                "7:00 AM (día siguiente)",
                "10:00 PM"
            ],
            "2": [
                "7:00 PM (12h post-detección)",
                "12:00 PM (5h post-detección)",
                "7:00 AM (24h post-detección)"
            ]
        },
        "correcta": {
            "1": "3:00 PM (misma tarde)",
            "2": "7:00 PM (12h post-detección)"
        }
    },
    {
        "tipo": "emparejar",
        "pregunta": "Asocia cada fase del ciclo estral bovino con su evento principal:",
        "pares": [
            "Proestro",
            "Estro",
            "Metaestro",
            "Diestro"
        ],
        "opciones": [
            "Formación del Cuerpo Lúteo",
            "Pico de LH y receptividad",
            "Producción máxima de Progesterona",
            "Crecimiento folicular rápido"
        ],
        "correcta": {
            "Proestro": "Crecimiento folicular rápido",
            "Estro": "Pico de LH y receptividad",
            "Metaestro": "Formación del Cuerpo Lúteo",
            "Diestro": "Producción máxima de Progesterona"
        }
    },
    {
        "tipo": "completar_espacios",
        "pregunta": "El signo primario de celo en bovinos es la {1}, la cual es exhibida por solo el {2} de las vacas y ocurre mayoritariamente en horario {3}.",
        "opciones": {
            "1": [
                "Monta aceptada",
                "Vulva edematosa",
                "Moco cervical filante"
            ],
            "2": [
                "50%",
                "10%",
                "95%"
            ],
            "3": [
                "Nocturno (60-70%)",
                "Diurno (80%)",
                "Madrugada (100%)"
            ]
        },
        "correcta": {
            "1": "Monta aceptada",
            "2": "50%",
            "3": "Nocturno (60-70%)"
        }
    },
    {
        "tipo": "emparejar",
        "pregunta": "Selecciona la sensibilidad de detección esperada para cada tecnología en ganado lechero:",
        "pares": [
            "Observación visual (2x/día)",
            "Parches de monta",
            "Collares acelerómetros",
            "Monitoreo P4 en leche"
        ],
        "opciones": [
            "85-95%",
            "60-80%",
            ">95%",
            "40-60%"
        ],
        "correcta": {
            "Observación visual (2x/día)": "40-60%",
            "Parches de monta": "60-80%",
            "Collares acelerómetros": "85-95%",
            "Monitoreo P4 en leche": ">95%"
        }
    },
    {
        "tipo": "completar_espacios",
        "pregunta": "El reconocimiento materno en la vaca se logra cuando el embrión produce {1}, el cual bloquea la liberación endometrial de {2}, permitiendo que el cuerpo lúteo mantenga niveles altos de {3}.",
        "opciones": {
            "1": [
                "IFN-tau",
                "Estrógenos",
                "hCG"
            ],
            "2": [
                "PGF2alfa",
                "GnRH",
                "FSH"
            ],
            "3": [
                "Progesterona",
                "Oxitocina",
                "Prolactina"
            ]
        },
        "correcta": {
            "1": "IFN-tau",
            "2": "PGF2alfa",
            "3": "Progesterona"
        }
    },
    {
        "tipo": "emparejar",
        "pregunta": "Asigna el momento de la ovulación para cada especie reproductiva:",
        "pares": [
            "Vaca",
            "Cerda",
            "Gallina",
            "Yegua"
        ],
        "opciones": [
            "6-8h post-oviposición",
            "36-44h post-inicio del estro",
            "24-48h ANTES del fin del estro",
            "10-14h post-fin del estro"
        ],
        "correcta": {
            "Vaca": "10-14h post-fin del estro",
            "Cerda": "36-44h post-inicio del estro",
            "Gallina": "6-8h post-oviposición",
            "Yegua": "24-48h ANTES del fin del estro"
        }
    },
    {
        "tipo": "completar_espacios",
        "pregunta": "En cerdas, la técnica principal de sincronización es el {1}, ya que al eliminar la succión se retira la inhibición de la {2}, permitiendo la reactivación del eje HHG y el retorno al celo en {3} días.",
        "opciones": {
            "1": [
                "Destete del lote",
                "Ovsynch",
                "Implante de progesterona"
            ],
            "2": [
                "Prolactina",
                "Oxitocina",
                "Melatonina"
            ],
            "3": [
                "4-7",
                "1-2",
                "14-21"
            ]
        },
        "correcta": {
            "1": "Destete del lote",
            "2": "Prolactina",
            "3": "4-7"
        }
    },
    {
        "tipo": "emparejar",
        "pregunta": "Asocia el problema reproductivo bovino con su causa principal de muerte embrionaria (días 8-30):",
        "pares": [
            "Insuficiente IFN-tau",
            "Balance Energético Negativo (BEN)",
            "Estrés calórico"
        ],
        "opciones": [
            "Ambiente uterino pobre por baja P4",
            "No se bloquea la luteólisis",
            "Daño oocitario y embrión deficiente"
        ],
        "correcta": {
            "Insuficiente IFN-tau": "No se bloquea la luteólisis",
            "Balance Energético Negativo (BEN)": "Ambiente uterino pobre por baja P4",
            "Estrés calórico": "Daño oocitario y embrión deficiente"
        }
    },
    {
        "tipo": "completar_espacios",
        "pregunta": "En gallinas comerciales, el programa de iluminación óptimo es de {1} horas de luz. Si las horas de luz caen por debajo de {2}, se produce un aumento de {3}, lo que suprime el eje reproductor causando cese de postura.",
        "opciones": {
            "1": [
                "16",
                "12",
                "24"
            ],
            "2": [
                "14",
                "18",
                "8"
            ],
            "3": [
                "Melatonina",
                "Adrenalina",
                "Corticosterona"
            ]
        },
        "correcta": {
            "1": "16",
            "2": "14",
            "3": "Melatonina"
        }
    },
    {
        "tipo": "emparejar",
        "pregunta": "Diferencia el manejo reproductivo de los pequeños rumiantes estacionales:",
        "pares": [
            "Oveja (Melatonina)",
            "Cabra (Efecto macho)"
        ],
        "opciones": [
            "Induce ciclicidad en hembras anovulatorias por feromonas",
            "Activa el eje HHG simulando noches largas de otoño"
        ],
        "correcta": {
            "Oveja (Melatonina)": "Activa el eje HHG simulando noches largas de otoño",
            "Cabra (Efecto macho)": "Induce ciclicidad en hembras anovulatorias por feromonas"
        }
    },
    {
        "tipo": "completar_espacios",
        "pregunta": "En ganado Bos indicus tropical, el protocolo Ovsynch tradicional tiene baja respuesta. Por ello se utilizan dispositivos intravaginales de {1} combinados con {2} y eCG para lograr tasas de preñez del {3}.",
        "opciones": {
            "1": [
                "Progesterona (CIDR/DIB)",
                "Prostaglandina F2a",
                "Oxitocina"
            ],
            "2": [
                "Estradiol",
                "Testosterona",
                "Inhibina"
            ],
            "3": [
                "50-60%",
                "20-30%",
                "90-100%"
            ]
        },
        "correcta": {
            "1": "Progesterona (CIDR/DIB)",
            "2": "Estradiol",
            "3": "50-60%"
        }
    },
    {
        "tipo": "emparejar",
        "pregunta": "Empareja la señal de alarma reproductiva con su posible investigación diagnóstica:",
        "pares": [
            "Tasa de Detección de Celo < 50%",
            "Tasa de Concepción < 30%",
            "Anestro > 60 días post-parto"
        ],
        "opciones": [
            "Evaluar calidad de semen y momento de la IA",
            "Revisar protocolo visual y considerar collares IA",
            "Evaluar Balance Energético Negativo mediante ecografía"
        ],
        "correcta": {
            "Tasa de Detección de Celo < 50%": "Revisar protocolo visual y considerar collares IA",
            "Tasa de Concepción < 30%": "Evaluar calidad de semen y momento de la IA",
            "Anestro > 60 días post-parto": "Evaluar Balance Energético Negativo mediante ecografía"
        }
    },
    {
        "tipo": "completar_espacios",
        "pregunta": "En la vaca, un único folículo produce {1} para suprimir la FSH y volverse monovulatoria. En la cerda, el mecanismo de dominancia es {2}, lo que permite que la FSH no caiga abruptamente y resulten en {3} ovulaciones.",
        "opciones": {
            "1": [
                "Inhibina y Estradiol",
                "Testosterona",
                "Progesterona"
            ],
            "2": [
                "Débil",
                "Muy Fuerte",
                "Inexistente"
            ],
            "3": [
                "15-25",
                "1-2",
                "50-60"
            ]
        },
        "correcta": {
            "1": "Inhibina y Estradiol",
            "2": "Débil",
            "3": "15-25"
        }
    },
    {
        "tipo": "emparejar",
        "pregunta": "Asocia la especie con su estrategia de almacenamiento o capacitación espermática:",
        "pares": [
            "Vaca",
            "Gallina",
            "Cerda"
        ],
        "opciones": [
            "Almacena esperma en SST de unión útero-vaginal por 10-14 días",
            "Capacitación requiere 6-8 horas en el tracto femenino",
            "Inseminación masiva con 3-4 mil millones de espermatozoides"
        ],
        "correcta": {
            "Vaca": "Capacitación requiere 6-8 horas en el tracto femenino",
            "Gallina": "Almacena esperma en SST de unión útero-vaginal por 10-14 días",
            "Cerda": "Inseminación masiva con 3-4 mil millones de espermatozoides"
        }
    },
    {
        "tipo": "completar_espacios",
        "pregunta": "Cada día abierto por encima de los {1} días post-parto cuesta aproximadamente {2} USD por vaca al día, lo que hace que mejorar la tasa de {3} tenga un impacto directo en la rentabilidad.",
        "opciones": {
            "1": [
                "85",
                "30",
                "150"
            ],
            "2": [
                "$3",
                "$10",
                "$0.50"
            ],
            "3": [
                "Preñez",
                "Mortalidad",
                "Lactancia"
            ]
        },
        "correcta": {
            "1": "85",
            "2": "$3",
            "3": "Preñez"
        }
    },
    {
        "tipo": "emparejar",
        "pregunta": "Relaciona el signo secundario del celo bovino con su manifestación:",
        "pares": [
            "Moco cervical",
            "Actividad locomotora",
            "Producción de leche",
            "Temperatura vaginal"
        ],
        "opciones": [
            "Cae un 5-10% por estrés",
            "Aumenta un 200-400% (medible por collar)",
            "Aumenta entre 0.3 y 0.5°C",
            "Transparente, filante y elástico"
        ],
        "correcta": {
            "Moco cervical": "Transparente, filante y elástico",
            "Actividad locomotora": "Aumenta un 200-400% (medible por collar)",
            "Producción de leche": "Cae un 5-10% por estrés",
            "Temperatura vaginal": "Aumenta entre 0.3 y 0.5°C"
        }
    },
    {
        "tipo": "completar_espacios",
        "pregunta": "La observación de sangrado metéstrico en una vaca indica que la ovulación {1} ocurrió. Por lo tanto, en ese momento es {2} realizar la inseminación y se debe esperar al {3}.",
        "opciones": {
            "1": [
                "YA",
                "AÚN NO",
                "NUNCA"
            ],
            "2": [
                "Demasiado tarde para",
                "El momento óptimo para",
                "Peligroso pero posible"
            ],
            "3": [
                "Próximo ciclo (21 días)",
                "Día siguiente",
                "Diagnóstico de preñez"
            ]
        },
        "correcta": {
            "1": "YA",
            "2": "Demasiado tarde para",
            "3": "Próximo ciclo (21 días)"
        }
    },
    {
        "pregunta": "En un hato con una TDC del 40% y una tasa de concepción del 50%, ¿cuál es la tasa de preñez resultante por ciclo?",
        "opciones": [
            "40%",
            "30%",
            "20%",
            "10%"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿Qué nivel de Tasa de Detección de Celo (TDC) se alcanza al implementar collares acelerómetros en el hato?",
        "opciones": [
            "40-60%",
            "60-70%",
            "85-95%",
            "Mayor al 99%"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿Qué porcentaje de los eventos estrales bovinos ocurren en horario nocturno (18:00 - 06:00) en vacas de alta producción?",
        "opciones": [
            "30-40%",
            "50-60%",
            "60-70%",
            "80-90%"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿Qué establece el protocolo AM/PM para optimizar el momento de la inseminación artificial bovina?",
        "opciones": [
            "Celo AM: inseminar la mañana siguiente; Celo PM: inseminar esa tarde",
            "Celo AM: inseminar esa tarde; Celo PM: inseminar la mañana siguiente",
            "Inseminar siempre a las 6:00 AM",
            "Inseminar 36 horas después de cualquier celo"
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "Posterior al inicio del comportamiento estral bovino, ¿cuál es la ventana temporal óptima para realizar la inseminación artificial?",
        "opciones": [
            "0-6 horas",
            "6-16 horas",
            "18-24 horas",
            "24-36 horas"
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿Cuánto tiempo requieren los espermatozoides bovinos para completar su capacitación en el tracto reproductivo de la hembra?",
        "opciones": [
            "1-2 horas",
            "6-8 horas",
            "12-14 horas",
            "24 horas"
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "Al utilizar el sistema Herd Navigator basado en monitoreo de progesterona láctea, ¿qué sensibilidad se logra en la detección del estro?",
        "opciones": [
            "60-70%",
            "75-85%",
            "Mayor al 95%",
            "40-60%"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿Qué implicancia fisiológica tiene la observación de sangrado metéstrico vaginal 24 a 48 horas post-ovulación en la hembra bovina?",
        "opciones": [
            "Que la vaca está en pleno estro lista para inseminar",
            "Que la vaca padece metritis",
            "Que la vaca ya ovuló; NO debe inseminarse en ese momento",
            "Que inició el proestro del siguiente ciclo"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "En el ámbito de la biotecnología reproductiva, ¿qué significan las siglas IATF?",
        "opciones": [
            "Inseminación Asistida por Tecnología Folicular",
            "Indicador de Actividad y Temperatura Fisiológica",
            "Inseminación Artificial a Tiempo Fijo",
            "Índice de Acceso a la Tecnología de Fertilización"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿Cuál es la secuencia farmacológica correcta del protocolo de sincronización Ovsynch?",
        "opciones": [
            "PGF2alfa (Día 0) - GnRH (Día 7) - PGF2alfa (Día 9) - IATF (Día 10)",
            "GnRH (Día 0) - PGF2alfa (Día 7) - GnRH (Día 9) - IATF (Día 10)",
            "CIDR (Día 0) - PGF2alfa (Día 8) - GnRH (Día 9) - IATF (Día 10)",
            "GnRH (Día 0) - GnRH (Día 7) - PGF2alfa (Día 9) - IATF (Día 10)"
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "En el protocolo Ovsynch, ¿cuál es el objetivo fisiológico de la administración inicial de GnRH (Día 0)?",
        "opciones": [
            "Destruir el cuerpo lúteo existente",
            "Ovular el folículo dominante presente y sincronizar el inicio de una nueva onda folicular",
            "Inducir el pico de LH para la IATF",
            "Estimular la liberación de progesterona luteal"
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿Qué efecto farmacodinámico ejerce la administración de PGF2alfa en el día 7 del protocolo Ovsynch?",
        "opciones": [
            "Sincronizar la onda folicular",
            "Inducir el surge de LH",
            "Destruir el cuerpo lúteo causando la caída abrupta de P4",
            "Estimular la producción de FSH hipofisiaria"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "En el esquema Ovsynch, ¿cuántas horas posteriores a la segunda dosis de GnRH debe ejecutarse la Inseminación Artificial a Tiempo Fijo?",
        "opciones": [
            "6-8 horas",
            "12-14 horas",
            "16-20 horas",
            "24-30 horas"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿Qué tasa de preñez por servicio se espera al aplicar el protocolo Ovsynch en vacas lecheras Bos taurus?",
        "opciones": [
            "20-30%",
            "35-40%",
            "45-55%",
            "65-75%"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿En qué subpoblación bovina se indica preferentemente el protocolo compuesto por CIDR + Benzoato de Estradiol + PGF2alfa + eCG?",
        "opciones": [
            "Vacas lecheras Holstein en clima frío",
            "Bos indicus y cruzas en condiciones tropicales",
            "Novillas de primer servicio en sistemas intensivos",
            "Vacas de alta producción con BEN severo"
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "Al implementar IATF en bovinos Bos indicus bajo condiciones tropicales, ¿cuál es la tasa de preñez esperada?",
        "opciones": [
            "25-35%",
            "40-45%",
            "50-60%",
            "70-80%"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "En el manejo reproductivo porcino, ¿cuál es el método fisiológico utilizado para sincronizar el retorno al estro de un lote de cerdas?",
        "opciones": [
            "Con implantes de melatonina",
            "Con el destete del lote, que elimina la inhibición dopaminérgica y permite el retorno al celo en 4-7 días",
            "Con protocolo Ovsynch adaptado para porcinos",
            "Con machos marcadores de arnés"
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿Qué beneficio fisiológico aporta la pre-sincronización con dos dosis de PGF2alfa previo al inicio del protocolo Ovsynch?",
        "opciones": [
            "Reduce el costo del protocolo",
            "Aumenta el número de ovulaciones por ciclo",
            "Asegura que más vacas tengan CL funcional al inicio del Ovsynch, mejorando la preñez en 5-10%",
            "Sustituye la segunda GnRH del protocolo"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "Fisiológicamente, ¿por qué la hembra bovina es monovulatoria mientras que la cerda desarrolla dominancia folicular múltiple?",
        "opciones": [
            "Porque la vaca no posee onda folicular",
            "Porque en la vaca el folículo dominante produce inhibina + E2 que suprimen los demás; en la cerda la dominancia es débil y múltiples folículos maduran",
            "Porque el útero bovino no puede sostener más de un embrión",
            "Porque la cerda ovula folículo dominante de la primera onda"
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿Qué porcentaje de gestaciones bovinas se interrumpe debido a muerte embrionaria temprana entre los días 8 y 30?",
        "opciones": [
            "5-10%",
            "10-15%",
            "20-30%",
            "40-50%"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "En términos económicos, ¿cuál es el costo estimado por cada día abierto adicional (superados los 85 días post-parto) en ganadería lechera?",
        "opciones": [
            "$0.50 USD/día",
            "$1.00 USD/día",
            "$3.00 USD/día",
            "$10.00 USD/día"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿En qué biomarcador se fundamenta el sistema automatizado Herd Navigator para el monitoreo del ciclo estral?",
        "opciones": [
            "Acelerómetro de actividad locomotora",
            "Cámara con inteligencia artificial",
            "Medición automatizada de progesterona en leche en cada ordeño",
            "Bolo intravaginal de temperatura"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "En la producción avícola comercial, ¿cuál es el fotoperiodo óptimo para estimular la actividad reproductiva de la gallina?",
        "opciones": [
            "8 horas de luz : 16 horas de oscuridad",
            "12 horas de luz : 12 horas de oscuridad",
            "16 horas de luz : 8 horas de oscuridad",
            "24 horas de luz continua"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "Gracias al almacenamiento espermático en los túbulos espermáticos (SST), ¿por cuántos días puede una gallina fertilizar óvulos tras una cópula?",
        "opciones": [
            "1-2 días",
            "3-5 días",
            "10-14 días",
            "21 días"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "En la especie ovina, ¿qué intervención biotecnológica se emplea para inducir el inicio anticipado de la temporada reproductiva?",
        "opciones": [
            "Implante de estradiol",
            "Implante de melatonina (Melovine)",
            "Dispositivo CIDR intravaginal",
            "Protocolo Ovsynch adaptado para ovinos"
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "Según el análisis de caso de estudio, al incrementar la TDC del 42% al 88% mediante collares SCR en un hato de 200 vacas, ¿cuál fue el ahorro anual proyectado?",
        "opciones": [
            "$5,000 USD",
            "$19,000 USD",
            "$45,000 USD",
            "$100,000 USD"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "Para hatos lecheros que superan las 200 vacas en ordeño, ¿qué nivel de tecnificación recomienda la pirámide de decisión reproductiva?",
        "opciones": [
            "Solo observación visual con registros",
            "Parches de monta más observación visual",
            "Collares de actividad",
            "Cámaras con IA o monitoreo de P4 en leche"
        ],
        "correcta": 3,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "En la comunicación química porcina, ¿cuáles son las feromonas del verraco responsables de desencadenar el reflejo de inmovilidad en la cerda?",
        "opciones": [
            "Estradiol y progesterona",
            "Androstenona y androstenol",
            "GnRH y melatonina",
            "FSH y LH"
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "Para optimizar la rentabilidad en sistemas de lechería especializada, ¿cuál es el intervalo entre partos objetivo?",
        "opciones": [
            "10-11 meses",
            "12-13 meses",
            "14-15 meses",
            "16-18 meses"
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "Como indicador de alarma reproductiva, ¿qué hallazgo clínico sugiere la necesidad inmediata de evaluar el Balance Energético Negativo (BEN) y la funcionalidad lútea por ecografía?",
        "opciones": [
            "TDC menor al 50%",
            "Tasa de concepción menor al 30%",
            "Anestro mayor a 60 días post-parto",
            "Intervalo interestro irregular"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "En el ciclo reproductivo de las aves (gallina), ¿cuál es el tiempo aproximado que tarda un óvulo desde la ovulación hasta la oviposición?",
        "opciones": [
            "12-14 horas",
            "24-26 horas",
            "36-40 horas",
            "48 horas"
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿Qué hormona es la principal responsable de inducir la ovulación del folículo maduro F1 en las aves?",
        "opciones": [
            "Estradiol (E2)",
            "Progesterona (P4)",
            "Hormona Luteinizante (LH)",
            "Hormona Foliculoestimulante (FSH)"
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "En el tracto reproductivo aviar, ¿en qué segmento ocurre la calcificación de la cáscara del huevo?",
        "opciones": [
            "Magno",
            "Istmo",
            "Infundíbulo",
            "Útero (glándula cascarógena)"
        ],
        "correcta": 3,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿Cómo se organiza el desarrollo folicular ovárico en las aves maduras de postura activa?",
        "opciones": [
            "Oleadas foliculares sincrónicas cada 21 días",
            "Jerarquía folicular asimétrica (F1, F2, F3...)",
            "Desarrollo bilateral de múltiples folículos de Graaf",
            "Cuerpos lúteos secuenciales"
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿Qué factor ambiental es el principal sincronizador endocrino que estimula el eje reproductivo (HHG) en las aves?",
        "opciones": [
            "La humedad relativa ambiental",
            "El fotoperíodo (horas luz)",
            "La temperatura nocturna",
            "La concentración de amoníaco"
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
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


    # Verificar tiempo de la evaluación sincronizado con el estado global
    if st.session_state.get("eval_fase") == "activo":
        end_time = st.session_state.get("eval_global_end_time")
        if end_time and datetime.datetime.now() >= end_time:
            st.session_state.eval_fase = "finalizado"
            preguntas = st.session_state.get("eval_preguntas", [])
            puntaje = sum(
                1 for i, p in enumerate(preguntas)
                if st.session_state.eval_respuestas.get(i) == p["correcta"]
            )
            st.session_state.eval_puntaje = puntaje
            st.warning(" El tiempo límite global ha expirado. Evaluación finalizada automáticamente.")
            st.rerun()

    # =========================================================================
    # EL ENCABEZADO FUE REMOVIDO PARA EVITAR DUPLICADOS CON MAIN.PY
    # =========================================================================

    # =========================================================================
    # PANTALLA 1: INICIO — Instrucciones y arranque del examen
    # =========================================================================
    if st.session_state.eval_fase == "inicio":
        import streamlit.components.v1 as components
        components.html("""
            <script>
                const parent = window.parent.document;
                const timerDiv = parent.getElementById('floating-timer-estral');
                if (timerDiv) timerDiv.remove();
            </script>
        """, height=0)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(22,33,25,0.7), rgba(10,18,12,0.9)); 
                    padding:35px 40px; border-radius:16px; border:1px solid rgba(76, 175, 80, 0.3);
                    box-shadow: 0 10px 40px rgba(0,0,0,0.5); margin-bottom:30px; position: relative; overflow: hidden;'>
            <div style='position:absolute; top:-50%; left:-50%; width:200%; height:200%; background: radial-gradient(circle, rgba(76,175,80,0.05) 0%, transparent 60%); pointer-events:none;'></div>
            <h3 style='color:#F8FAFC; margin:0 0 20px 0; font-weight:700; font-size:1.6rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom:15px; display:flex; align-items:center;'>
                Reglamento de la Evaluación
            </h3>
            <ul style='color:#CBD5E1; font-size:1.05rem; line-height:2.2; margin:0; padding-left:25px; list-style-type: square;'>
                <li>El examen consta de <b style="color:#4CAF50;">20 preguntas de opción múltiple y emparejamiento</b>.</li>
                <li>Las preguntas se presentan <b style="color:#4CAF50;">una por una</b>. No es posible retroceder a modificar respuestas.</li>
                <li>El límite de tiempo (20 minutos) es estrictamente medido y validado por el servidor.</li>
                <li>Para aprobar con éxito se requiere un mínimo de <b style="color:#34D399;">16 respuestas correctas (Nota mínima: 16/20).</b></li>
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

        # --- Temporizador Javascript Flotante ---
        import streamlit.components.v1 as components
        end_time = st.session_state.get("eval_global_end_time")
        if end_time:
            remaining = max(0, (end_time - datetime.datetime.now()).total_seconds())
        else:
            remaining = 0
        
        components.html(f"""
            <script>
                const parent = window.parent.document;
                let timerDiv = parent.getElementById('floating-timer-estral');
                if (!timerDiv) {{
                    timerDiv = parent.createElement('div');
                    timerDiv.id = 'floating-timer-estral';
                    timerDiv.style.position = 'fixed';
                    timerDiv.style.top = '25px';
                    timerDiv.style.right = '35px';
                    timerDiv.style.zIndex = '999999';
                    timerDiv.style.backgroundColor = 'rgba(25, 15, 15, 0.95)';
                    timerDiv.style.border = '1px solid rgba(239, 83, 80, 0.5)';
                    timerDiv.style.borderRadius = '8px';
                    timerDiv.style.padding = '8px 18px';
                    timerDiv.style.color = '#EF5350';
                    timerDiv.style.fontFamily = '"Inter", sans-serif';
                    timerDiv.style.fontSize = '1.3rem';
                    timerDiv.style.fontWeight = '800';
                    timerDiv.style.boxShadow = '0 6px 25px rgba(239, 83, 80, 0.3)';
                    timerDiv.style.backdropFilter = 'blur(10px)';
                    timerDiv.style.display = 'flex';
                    timerDiv.style.alignItems = 'center';
                    timerDiv.style.gap = '12px';
                    
                    timerDiv.innerHTML = `
                        <span style="font-size: 0.75rem; color: #8B949E; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px;">Tiempo</span>
                        <span id="timer-val" style="font-variant-numeric: tabular-nums;">--:--</span>
                    `;
                    parent.body.appendChild(timerDiv);
                }}
                
                var timeLeft = {int(remaining)};
                const valSpan = parent.getElementById('timer-val');
                
                if (timeLeft <= 0) {{
                    window.parent.location.reload();
                }} else {{
                    setTimeout(function() {{
                        window.parent.location.reload();
                    }}, timeLeft * 1000);
                    
                    setInterval(function() {{
                        if (timeLeft > 0) timeLeft--;
                        var m = Math.floor(timeLeft / 60);
                        var s = timeLeft % 60;
                        if (valSpan) {{
                            valSpan.innerText = m + ":" + (s < 10 ? "0" : "") + s;
                            if (timeLeft < 120) {{
                                timerDiv.style.color = '#EF5350';
                                timerDiv.style.borderColor = 'rgba(239, 83, 80, 0.5)';
                            }}
                        }}
                    }}, 1000);
                }}
            </script>
        """, height=0)

        # --- Barra de progreso ---
        progreso = idx / total
        st.markdown(f"""
        <style>
            [data-testid="stProgress"] > div > div > div > div {{
                background-color: #EF5350 !important;
            }}
        </style>
        <div style='margin-bottom:10px; display:flex; justify-content:space-between;
                    font-size:0.9rem; color:#94A3B8; font-weight:600; text-transform:uppercase; letter-spacing:1px;'>
            <span style='color:#EF5350;'>Pregunta {num} de {total}</span>
            <span>{idx} completadas / {total - idx} pendientes</span>
        </div>
        """, unsafe_allow_html=True)
        st.progress(progreso)
        st.markdown("<br>", unsafe_allow_html=True)

        # --- Enunciado de la pregunta ---
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, rgba(25,15,15,0.8), rgba(18,10,10,0.9));
                    border: 1px solid rgba(239, 83, 80, 0.4); border-left: 6px solid #EF5350;
                    padding: 30px 35px; border-radius: 16px;
                    box-shadow: 0 0 25px rgba(239, 83, 80, 0.2); margin-bottom: 30px; backdrop-filter: blur(15px); position:relative; overflow:hidden;'>
            <div style='position:absolute; top:-20px; right:-20px; width:100px; height:100px; background:radial-gradient(circle, rgba(239,83,80,0.15) 0%, transparent 70%); border-radius:50%;'></div>
            <h3 style='margin:0; color:#F8FAFC; font-size:1.35rem; font-weight:600; line-height:1.7; position:relative; z-index:2;'>
                <span style='color:#EF5350; font-size:1.6rem; font-weight:800; margin-right:12px; display:inline-block; transform:translateY(2px);'>{num}.</span> {q["pregunta"]}
            </h3>
        </div>
        """, unsafe_allow_html=True)

        # --- Renderizado por tipo de pregunta y callbacks ---
        if st.session_state.eval_seleccion_actual is None and q["tipo"] in ["emparejar", "completar_espacios"]:
            st.session_state.eval_seleccion_actual = {}

        if q["tipo"] == "opcion_multiple":
            widget_key = f"radio_q_{idx}"

            def _registrar_seleccion():
                valor = st.session_state.get(widget_key)
                if valor is not None:
                    st.session_state.eval_seleccion_actual = q["opciones"].index(valor)
                st.session_state.eval_advertencia = False

            idx_inicial = st.session_state.eval_seleccion_actual if isinstance(st.session_state.eval_seleccion_actual, int) else None

            st.radio(
                label="Seleccione una opcion de respuesta:",
                options=q["opciones"],
                index=idx_inicial,
                key=widget_key,
                on_change=_registrar_seleccion,
                label_visibility="collapsed"
            )

        elif q["tipo"] == "emparejar":
            st.markdown("<h4 style='color:#B0BEC5; margin-bottom:15px; font-weight:500;'>Selecciona la correspondencia correcta para cada concepto:</h4>", unsafe_allow_html=True)
            
            def _registrar_emparejamiento(par):
                def _callback():
                    valor = st.session_state.get(f"emp_q_{idx}_{par}")
                    if not isinstance(st.session_state.eval_seleccion_actual, dict):
                        st.session_state.eval_seleccion_actual = {}
                    if valor != "Seleccionar...":
                        st.session_state.eval_seleccion_actual[par] = valor
                    else:
                        st.session_state.eval_seleccion_actual.pop(par, None)
                    st.session_state.eval_advertencia = False
                return _callback

            for par in q["pares"]:
                c1, c2 = st.columns([1, 1.2])
                with c1:
                    st.markdown(f"<div style='background:rgba(255,255,255,0.03); padding:12px 18px; border-radius:8px; border-left:4px solid #4CAF50; height: 100%; display:flex; align-items:center;'><p style='margin:0; font-weight:500; font-size:1.05rem; color:#E8F5E9;'>{par}</p></div>", unsafe_allow_html=True)
                with c2:
                    current_val = st.session_state.eval_seleccion_actual.get(par) if isinstance(st.session_state.eval_seleccion_actual, dict) else None
                    opts = ["Seleccionar..."] + q["opciones"]
                    idx_opt = opts.index(current_val) if current_val in opts else 0
                    st.selectbox(
                        label=f"Match for {par}", 
                        options=opts, 
                        index=idx_opt, 
                        key=f"emp_q_{idx}_{par}", 
                        on_change=_registrar_emparejamiento(par),
                        label_visibility="collapsed"
                    )
                st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)

        elif q["tipo"] == "completar_espacios":
            st.markdown("<h4 style='color:#B0BEC5; margin-bottom:15px; font-weight:500;'>Selecciona la palabra adecuada para completar el texto:</h4>", unsafe_allow_html=True)
            
            def _registrar_completar(espacio):
                def _callback():
                    valor = st.session_state.get(f"comp_q_{idx}_{espacio}")
                    if not isinstance(st.session_state.eval_seleccion_actual, dict):
                        st.session_state.eval_seleccion_actual = {}
                    if valor != "Seleccionar...":
                        st.session_state.eval_seleccion_actual[espacio] = valor
                    else:
                        st.session_state.eval_seleccion_actual.pop(espacio, None)
                    st.session_state.eval_advertencia = False
                return _callback

            cols = st.columns(len(q["opciones"]))
            for col_idx, (espacio_num, opciones_espacio) in enumerate(q["opciones"].items()):
                with cols[col_idx]:
                    st.markdown(f"<p style='color:#4CAF50; font-weight:700; margin-bottom:5px;'>Espacio [{espacio_num}]:</p>", unsafe_allow_html=True)
                    current_val = st.session_state.eval_seleccion_actual.get(espacio_num) if isinstance(st.session_state.eval_seleccion_actual, dict) else None
                    opts = ["Seleccionar..."] + opciones_espacio
                    idx_opt = opts.index(current_val) if current_val in opts else 0
                    st.selectbox(
                        label=f"Espacio {espacio_num}", 
                        options=opts, 
                        index=idx_opt, 
                        key=f"comp_q_{idx}_{espacio_num}", 
                        on_change=_registrar_completar(espacio_num),
                        label_visibility="collapsed"
                    )
            st.markdown("<br/>", unsafe_allow_html=True)

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
                completo = False
                if q["tipo"] == "opcion_multiple" and st.session_state.eval_seleccion_actual is not None:
                    completo = True
                elif q["tipo"] == "emparejar" and isinstance(st.session_state.eval_seleccion_actual, dict) and len(st.session_state.eval_seleccion_actual) == len(q["pares"]):
                    completo = True
                elif q["tipo"] == "completar_espacios" and isinstance(st.session_state.eval_seleccion_actual, dict) and len(st.session_state.eval_seleccion_actual) == len(q["opciones"]):
                    completo = True

                if not completo:
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
        import streamlit.components.v1 as components
        components.html("""
            <script>
                const parent = window.parent.document;
                const timerDiv = parent.getElementById('floating-timer-estral');
                if (timerDiv) timerDiv.remove();
            </script>
        """, height=0)
        
        puntaje = st.session_state.eval_puntaje
        total = 20
        
        # GUARDAR EN ESTADO GLOBAL SOLO UNA VEZ
        if not st.session_state.get("eval_guardado_global", False):
            import sys
            # Soporte de namespace al importar
            gs = get_global_exam_state()
            estudiante = st.session_state.get("eval_estudiante", {})
            nombre = estudiante.get("nombre", "No registrado")
            carrera = estudiante.get("carrera", "No registrada")
            curso = estudiante.get("curso", "No registrado")
            est_key = f"{nombre}_{carrera}_{curso}"
            
            preguntas = st.session_state.eval_preguntas
            fallos = []
            for i, p in enumerate(preguntas):
                if st.session_state.eval_respuestas.get(i) != p["correcta"]:
                    fallos.append(i + 1)
            
            end_time = st.session_state.get("eval_global_end_time", datetime.datetime.now())
            tiempo_tardado = 1200 - max(0, (end_time - datetime.datetime.now()).total_seconds())
            
            registro = {
                "key": est_key,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nombre": nombre,
                "carrera": carrera,
                "curso": curso,
                "nota": puntaje,
                "fallos": fallos,
                "tiempo": round(tiempo_tardado, 1)
            }
            if "registros" in gs:
                gs["registros"].append(registro)
            st.session_state.eval_guardado_global = True
            
            # --- INTEGRACIÓN GOOGLE SHEETS (Descomentar al configurar secrets.toml) ---
            # from streamlit_gsheets import GSheetsConnection
            # import pandas as pd
            # conn = st.connection("gsheets", type=GSheetsConnection)
            # data = pd.DataFrame([registro])
            # try:
            #     existing_data = conn.read(worksheet="Calificaciones", ttl=5)
            #     updated_data = pd.concat([existing_data, data], ignore_index=True)
            #     conn.update(worksheet="Calificaciones", data=updated_data)
            # except Exception as e:
            #     print("Error GSheets:", e)
        
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

        estudiante = st.session_state.get("eval_estudiante", {})
        nombre = estudiante.get("nombre", "No registrado")
        carrera = estudiante.get("carrera", "No registrada")
        curso = estudiante.get("curso", "No registrado")

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(22,33,25,0.95), rgba(12,22,16,0.98));
                    padding: 40px 50px; border-radius: 16px;
                    border-top: 5px solid {color_res};
                    border: 1px solid rgba(255,255,255,0.07);
                    text-align: center; margin: 20px 0;'>
            <h2 style='color:{color_res}; font-weight:800; letter-spacing:2px; margin:0 0 8px 0;'>{titulo_res}</h2>
            <div style='background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; margin: 15px 0; text-align: left; display: inline-block;'>
                <p style='margin: 0; color: #E0E0E0; font-size: 1rem;'><b>Estudiante:</b> {nombre}</p>
                <p style='margin: 5px 0 0 0; color: #E0E0E0; font-size: 1rem;'><b>Carrera:</b> {carrera}</p>
                <p style='margin: 5px 0 0 0; color: #E0E0E0; font-size: 1rem;'><b>Curso:</b> {curso}</p>
            </div>
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
                
                if q.get("tipo", "opcion_multiple") == "opcion_multiple":
                    texto_respuesta = q["opciones"][resp] if resp is not None else "Sin responder"
                    correct_text = q["opciones"][q["correcta"]]
                elif q["tipo"] == "emparejar":
                    correct_text = "<br/>" + "<br/>".join([f"• <b style='color:#58A6FF;'>{k}</b>: {v}" for k, v in q['correcta'].items()])
                    if resp is not None and isinstance(resp, dict):
                        texto_respuesta = "<br/>" + "<br/>".join([f"• <b>{k}</b>: {v}" for k, v in resp.items()])
                    else:
                        texto_respuesta = "Sin responder"
                else:
                    correct_text = "<br/>" + "<br/>".join([f"• <b>Espacio [{k}]</b>: {v}" for k, v in q['correcta'].items()])
                    if resp is not None and isinstance(resp, dict):
                        texto_respuesta = "<br/>" + "<br/>".join([f"• <b>Espacio [{k}]</b>: {v}" for k, v in resp.items()])
                    else:
                        texto_respuesta = "Sin responder"

                bloque_usuario = (
                    ""
                    if es_correcta
                    else f" <br> <span style='color:#EF5350;'>Su respuesta: {texto_respuesta}</span>"
                )
                st.markdown(f"""
                <div style='border-left: 3px solid {color_icon}; padding: 10px 16px;
                            margin-bottom: 12px; background: rgba(255,255,255,0.02);
                            border-radius: 0 8px 8px 0;'>
                    <p style='margin:0 0 4px 0; font-size:0.85rem; color:{color_icon};
                              font-weight:700; letter-spacing:1px;'>{i + 1}. {indicador}</p>
                    <p style='margin:0 0 6px 0; color:#E8F5E9; font-size:0.9rem;'>{q["pregunta"]}</p>
                    <p style='margin:0; color:#90A4AE; font-size:0.82rem;'>
                        Respuesta correcta: <b style="color:#4CAF50;">{correct_text}</b>
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
