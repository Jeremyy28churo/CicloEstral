"""
Modulo de Evaluacion Interactiva - Ciclo Estral Comparado
Fuente: Clase10_Ciclo_Estral_Comparado.pdf
Lenguaje academico formal. Sin emojis. Termino taxonomico: Equino.
"""
import random
import streamlit as st
import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

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
        "pregunta": 'CASO CLÍNICO INTEGRADO (BOVINOS): Usted es contratado como asesor reproductivo en una hacienda lechera especializada (Holstein de alta producción, promedio 40 L/día) ubicada en una zona con alta humedad y temperaturas constantes sobre los 32°C. El gerente de la granja reporta una Tasa de Detección de Celo (TDC) visual alarmantemente baja del 25% y una tasa de concepción del 28%. Los registros muestran que el intervalo promedio entre partos se ha extendido a 16 meses, generando pérdidas calculadas en miles de dólares por días abiertos prolongados. Al revisar el protocolo actual, nota que los operarios realizan observación visual estricta dos veces al día (6:00 AM y 5:00 PM) durante 30 minutos por sesión. Adicionalmente, el veterinario encargado ha intentado solucionar el problema implementando un protocolo Ovsynch estándar (GnRH - 7d - PGF2a - 48h - GnRH - 16h - IATF) en vacas con más de 80 días en leche, pero la tasa de preñez al primer servicio sigue estancada en un 20%. Basado en el análisis fisiológico del ciclo estral comparado y la influencia del estrés metabólico/ambiental, ¿cuál de las siguientes opciones describe el diagnóstico más preciso del fracaso reproductivo y la estrategia integral más apropiada para revertir este escenario?',
        "opciones": [
            'El fracaso se debe exclusivamente a que el estrés calórico inactiva la hormona GnRH exógena administrada en el protocolo Ovsynch, impidiendo la ovulación. La solución óptima es abandonar el Ovsynch y depender de la detección visual nocturna utilizando reflectores de luz en los corrales, sumado a la aplicación de implantes de melatonina para inducir la ciclicidad profunda.',
            'La baja TDC se explica porque las vacas Holstein de alta producción tienen un flujo sanguíneo hepático exacerbado que metaboliza el estradiol rápidamente, acortando el estro a menos de 8 horas, y reduciendo la intensidad de los signos conductuales (celos silenciosos). Además, la observación diurna pierde el 70% de los celos que ocurren de noche. El Ovsynch falla porque muchas vacas en anestro no inician el protocolo en la fase luteal temprana adecuada. La estrategia recomendada es implementar sistemas automatizados de detección (ej. collares acelerómetros 24/7) y cambiar a un protocolo Presynch-Ovsynch para pre-sincronizar los folículos, asegurando que las vacas respondan correctamente al tratamiento hormonal.',
            'El problema principal es una falla genética en la producción de interferón tau (IFN-τ) debido al cruzamiento de las vacas Holstein, provocando muertes embrionarias masivas. La observación visual a las 6:00 AM y 5:00 PM es teóricamente perfecta y debería detectar el 100% de los celos según la literatura. Se debe reemplazar inmediatamente el hato completo e implementar biotecnología de fertilización in vitro (FIV) como única solución viable a largo plazo.',
            'La tasa de detección del 25% indica que el personal está altamente capacitado pero los ovarios de las vacas Holstein en el trópico no producen progesterona. El uso de Ovsynch estándar es incorrecto porque este protocolo fue diseñado exclusivamente para yeguas y cerdas. La intervención adecuada es utilizar Altrenogest oral durante 18 días seguido de inseminación a las 72 horas para sincronizar masivamente a las vacas lecheras.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'DINÁMICA FOLICULAR COMPARADA (VACA vs CERDA): La vaca y la cerda presentan notables diferencias en su tasa ovulatoria, determinando que una sea monovulatoria (1 cría) y la otra poliovulatoria (camadas de 15-25 lechones), a pesar de que ambas especies reclutan una cantidad similar de folículos antrales (aproximadamente 20 a 30) al inicio de cada onda folicular. Imagine un escenario experimental donde un equipo de investigadores logra modificar genéticamente los folículos preovulatorios de un grupo de cerdas para que sistemáticamente produzcan niveles masivos e inmediatos de la hormona inhibina y estradiol de manera idéntica a como lo haría el folículo dominante de una vaca, tan pronto como alcanzan los 4 milímetros de diámetro. Simultáneamente, administran un antagonista de los receptores de LH sistémicos en el momento del estro. Desde el punto de vista endocrinológico estricto y analizando el mecanismo de retroalimentación en el eje hipotálamo-hipófisis-gónada, ¿cuál sería el impacto fisiológico y reproductivo directo en estas cerdas experimentales durante ese ciclo específico?',
        "opciones": [
            'La producción masiva de inhibina y estradiol por parte de un único folículo causaría una fuerte retroalimentación negativa inmediata sobre la glándula pituitaria anterior, suprimiendo de forma abrupta y total la liberación sistémica de FSH. Como el mecanismo de dominancia de la cerda (normalmente débil) se volvería extremadamente fuerte artificialmente, los demás folículos subordinados entrarían en atresia al quedarse sin soporte de FSH. En consecuencia, la cerda maduraría un solo folículo, transformándose funcionalmente en una especie monovulatoria. Sin embargo, al bloquearse los receptores de LH, ni siquiera ese folículo único lograría ovular, resultando en un ciclo anovulatorio y esterilidad temporal.',
            'La inhibina y el estradiol provocarían una hiperestimulación de la glándula pineal, la cual liberaría cantidades tóxicas de melatonina que a su vez destruirían el tejido ovárico. Esto causaría que los 20-30 folículos reclutados ovulen simultáneamente de forma prematura antes de que el óvulo madure. El bloqueo de LH no tendría efecto porque la ovulación en cerdas depende exclusivamente de la prolactina y no de la LH.',
            'Al aumentar drásticamente la inhibina, la cerda reclutaría folículos adicionales de ovarios accesorios, lo que incrementaría el tamaño de la camada a más de 40 crías. El estradiol masivo superaría el bloqueo del antagonista de LH mediante vías nerviosas directas (arco reflejo espinal), induciendo el estro conductual prolongado típico de las yeguas y permitiendo una tasa de fertilidad del 100% independientemente del tiempo de inseminación.',
            'El sistema reproductivo de la cerda ignoraría por completo la inhibina externa, ya que las hembras porcinas carecen de receptores hipofisarios para esta proteína. Los folículos continuarían creciendo bajo el estímulo exclusivo de la progesterona luteal y se daría lugar a una poliovulación normal de 20 lechones. La falla real ocurriría en el reconocimiento materno embrionario, ya que las cerdas carecen de estrógenos embrionarios.'
        ],
        "correcta": 0,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'FISIOLOGÍA Y MANEJO EN AVES (FOTOPERÍODO Y POSTURA): En un complejo avícola industrial con 500,000 gallinas de postura (Línea Hy-Line Brown) que se encuentran en su pico máximo de producción (92% de postura diaria), ocurre un fallo catastrófico en el sistema automatizado de control de iluminación y cortinas. Debido a esto, el galpón queda sometido a un régimen de apenas 8 horas de luz y 16 horas de oscuridad total (8L:16O) durante un periodo ininterrumpido de 14 días antes de que el problema técnico sea detectado y reparado. Analizando exhaustivamente el mecanismo endocrinológico que rige el ciclo ovulatorio en las aves comerciales, el cual no obedece a un ciclo estral clásico sino a un delicado equilibrio dependiente del fotoperíodo, ¿cuál será la consecuencia fisiológica sistemática observada en las aves a nivel del eje Hipotálamo-Hipófisis-Gónada (HHG), la dinámica de su jerarquía folicular ovárica (F1 a F5), y el fenotipo productivo de la parvada tras estas dos semanas?',
        "opciones": [
            'Las 16 horas prolongadas de oscuridad provocarán una hiperestimulación de la glándula pineal, la cual secretará cantidades masivas de melatonina en el torrente sanguíneo. Esta melatonina circulante ejercerá una severa inhibición sobre el hipotálamo, bloqueando drásticamente la secreción de GnRH. Sin GnRH, cesará la liberación hipofisaria de FSH y LH, causando la atresia progresiva y colapso de toda la jerarquía folicular madura en el ovario (F1 a F5). Fenotípicamente, el lote experimentará una caída vertical de la postura acercándose a cero y las gallinas probablemente iniciarán un proceso de muda forzada con pérdida masiva de plumas y regresión del oviducto.',
            'La exposición prolongada a la oscuridad actuará como un potente estímulo de bienestar animal, suprimiendo la hormona cortisol y permitiendo que la glándula pituitaria potencie sus pulsos preovulatorios de LH independientemente del hipotálamo. En el ovario, la jerarquía folicular (F1-F5) se acelerará, reduciendo el ciclo ovulatorio normal de 25 horas a menos de 12 horas. Fenotípicamente, el granjero observará que las gallinas comenzarán a poner dos huevos por día (producción >150%), aunque con cascarones más frágiles.',
            'La inversión del fotoperíodo (de 16L:8O a 8L:16O) provocará que el hipotálamo aviar empiece a secretar progesterona en lugar de GnRH. Esta progesterona activará la formación rápida de estructuras similares al cuerpo lúteo de los mamíferos en los folículos post-ovulatorios. Como resultado, las aves entrarán en un estado de seudogestación y dejarán de poner huevos por voluntad propia para iniciar el comportamiento de incubación (cloquez), pero la jerarquía folicular se mantendrá intacta y lista para ovular inmediatamente se encienda la luz.',
            'El impacto será completamente nulo en aves comerciales genéticamente modificadas, ya que las líneas modernas de alta postura han evolucionado para perder totalmente la fotosensibilidad ocular y pineal. El eje HHG de la gallina mantendrá sus pulsos circadianos de LH de forma endógena basándose en la disponibilidad de alimento y agua, manteniendo la postura estática en un 92% sin alterar la transición jerárquica del folículo F1 al F5 ni afectar el peso del huevo.'
        ],
        "correcta": 0,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'CASO INTEGRAL (RESINCRONIZACIÓN Y ULTRASONOGRAFÍA): Usted revisa un rebaño de 200 vientres cruzados (Bos taurus x Bos indicus) sometidos a un estricto protocolo de Inseminación Artificial a Tiempo Fijo (IATF) mediante la inserción de dispositivos intravaginales liberadores de progesterona (CIDR), benzoato de estradiol en el día 0, retiro y prostaglandina en el día 8, y GnRH en el día 9 con inseminación en el día 10. Exactamente 30 días posteriores a la IA masiva, el veterinario encargado realiza una sesión de ecografía transrectal para el diagnóstico temprano de gestación en todo el lote. Tras el chequeo, se identifica que un grupo de 40 vacas está definitivamente vacío (sin vesícula embrionaria y ausencia de latido cardíaco fetal). De manera alarmante, el ganadero pretendía esperar a que estas vacas mostraran celo natural para volver a inseminarlas, a pesar de que el hato se encuentra en grandes potreros de pastoreo extensivo donde la observación visual es imposible e inoperante. Fisiológicamente, ¿qué representa el estado actual de estas 40 vacas en términos de sus ovarios, y por qué la recomendación técnica innegociable debe ser la Resincronización Inmediata?',
        "opciones": [
            'A los 30 días post-IA, estas vacas vacías probablemente han reiniciado la ciclicidad, habiendo experimentado luteólisis (aprox. día 17-21 del ciclo anterior) y pueden encontrarse en distintas fases luteales o foliculares tempranas del siguiente ciclo. Esperar celo visual en un entorno extensivo garantiza celos perdidos (>60% no detectados) y alarga peligrosamente los días abiertos (pérdida de >$3 USD diarios por vaca). La resincronización inmediata reintroduce a estos animales a un nuevo control farmacológico del eje HPG (re-inserción de CIDR y reinicio del protocolo IATF), garantizando una nueva inseminación en un lapso definido de 10 días, eliminando por completo la dependencia del observador humano y maximizando el retorno productivo.',
            'Las 40 vacas vacías se encuentran obligatoriamente en un estado de anestro profundo irreversible debido al estrés del primer protocolo hormonal, por lo cual sus ovarios presentan atresia cortical total sin folículos primordiales. La recomendación de resincronización inmediata no es para lograr la preñez, sino para forzar una luteinización artificial masiva del tejido ovárico, provocando una falsa preñez que permita a las vacas entrar en periodo de secado temprano y ahorrar costos de pastoreo al ganadero.',
            'El diagnóstico de vaciedad a los 30 días mediante ecografía transrectal es inherentemente defectuoso y solo posee un 20% de sensibilidad; es altamente probable que el embrión esté oculto. La recomendación de resincronizar inmediatamente sirve para inducir un sangrado metéstrico terapéutico mediado por prostaglandinas exógenas, lo cual limpiará el endometrio y empujará al embrión oculto hacia el cuello uterino, donde podrá ser detectado con certeza en una segunda ecografía.',
            'Fisiológicamente, estas vacas han sufrido muerte embrionaria tardía exclusiva por carencia de oxitocina, lo cual retiene cuerpos lúteos quísticos gigantes. La resincronización inmediata con implantes de melatonina y eCG es indispensable para cambiar la especie de poliéstrica continua a poliéstrica estacional, forzando a que las vacas solo ovulen durante las noches de invierno, facilitando así la labor del inseminador en un clima más frío.'
        ],
        "correcta": 0,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "FARMACOLOGÍA Y MOMENTO ÓPTIMO DE IA (YEGUA): Ingresa a un centro de reproducción equina de alto valor genético una yegua Sangre Pura de Carrera (SPC). El propietario requiere que la yegua sea preñada mediante IA utilizando semen congelado importado sumamente costoso (una sola pajuela disponible). Durante el examen ecográfico reproductivo diario, usted nota el desarrollo progresivo de un gran folículo dominante, el cual alcanza un diámetro de 40 mm. Simultáneamente, la yegua muestra marcados signos de celo frente al padrillo recelador: adopta postura pasiva, lateraliza la cola, expone el clítoris rítmicamente ('guiño vulvar') y presenta micción frecuente. Considerando la fisiología del ciclo estral equino, cuyas particularidades contrastan abismalmente con los bovinos (el estro de la yegua dura de 4 a 7 días, y la ovulación fisiológica ocurre 24 a 48 horas ANTES de que finalicen los signos conductuales del estro), sumado a la limitación crítica de vida útil del semen congelado (viabilidad post-descongelación en tracto femenino extremadamente corta, menor a 12 horas), ¿cuál es la estrategia médica precisa y el fundamento fisiológico para maximizar las probabilidades de concepción utilizando esta única pajuela?",
        "opciones": [
            'Inseminar de inmediato apenas inicie el celo (día 1 del guiño vulvar), ya que los espermatozoides requieren esperar en el istmo durante 5 días completos para completar su capacitación y adquirir hipermotilidad, asegurando que estén presentes en el momento de la ovulación en el día 5.',
            "Esperar meticulosamente a que desaparezcan por completo todos los signos conductuales de celo (fin del estro y rechazo al padrillo) y entonces, aplicar la 'Regla AM-PM bovina' de manera estricta, inseminando 12 horas después para coincidir con la migración del óvulo, garantizando el éxito.",
            'Inyectar una hormona inductora de ovulación (como hCG o deslorelina - análogo de GnRH) cuando el folículo dominante alcanza un tamaño preovulatorio maduro (>35-40 mm) para programar y acelerar farmacológicamente la ruptura folicular, la cual ocurrirá aproximadamente en 36 a 48 horas. Con esto en mente, el veterinario debe realizar la IA con el semen congelado de forma ecográficamente calculada (generalmente cercano a las 36h post-inducción o mediante seguimiento seriado), logrando depositar los espermatozoides de corta vida útil justo DURANTE el estro y en un margen fisiológico de escasas horas previas a la ovulación real.',
            'Administrar dosis masivas de Prostaglandina F2a (PGF2a) directamente en el cérvix equino. Fisiológicamente, esto induce una potente luteólisis del cuerpo lúteo inexistente en el folículo de 40 mm, provocando que este último se atresie y permita el nacimiento inmediato de un folículo subordinado hiper-fértil. La pajuela única debe insertarse en este momento exacto, pues el semen congelado tiene afinidad química por las prostaglandinas.'
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'En un programa de sincronización IATF en bovinos, se administra GnRH en el día 0 y PGF2a en el día 7. ¿Cuál es el objetivo fisiológico principal de la inyección de GnRH inicial?',
        "opciones": [
            'Inducir la luteólisis del cuerpo lúteo persistente.',
            'Forzar la ovulación o luteinización del folículo dominante presente, reiniciando una nueva onda folicular.',
            'Inhibir la liberación de FSH para que no crezcan más folículos.',
            'Aumentar los niveles de progesterona directamente en el torrente sanguíneo.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'Comparando cerdas y vacas, ¿por qué la cerda desarrolla camadas grandes (poliovulatoria) mientras que la vaca normalmente gesta una sola cría (monovulatoria)?',
        "opciones": [
            'Porque la cerda recluta 50 folículos y la vaca solo 1.',
            'Debido a que el folículo dominante en la vaca produce mucha inhibina, suprimiendo la FSH y causando atresia en los folículos subordinados; en la cerda esta dominancia es mucho más débil.',
            'Porque la cerda no produce progesterona durante el estro.',
            'La vaca ovula múltiples folículos pero el útero solo permite la implantación de un embrión por falta de espacio.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "El 'Reconocimiento Materno de la Gestación' es crucial para evitar la pérdida del embrión. En los bovinos, ¿cuál es la señal y su mecanismo principal?",
        "opciones": [
            'El embrión produce estrógeno que destruye la prostaglandina F2a en el ovario.',
            'El trofoblasto secreta Interferón tau (IFN-τ), el cual bloquea la síntesis de receptores de oxitocina en el endometrio, impidiendo la liberación pulsátil de PGF2a.',
            'La hipófisis materna detecta al embrión y deja de producir hormona luteinizante.',
            'El embrión segrega melatonina, lo cual adormece la respuesta inmunitaria del útero.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": '¿Qué ocurre fisiológicamente en el ciclo reproductivo de una oveja (reproductora estacional de días cortos) durante los largos días de verano?',
        "opciones": [
            'La mayor cantidad de luz reduce la secreción de melatonina pineal, lo que disminuye la frecuencia de los pulsos de GnRH, induciendo anestro.',
            'La luz solar directa estimula la ovulación espontánea cada 5 días.',
            'Se detiene por completo la función ovárica y los ovarios se atrofian hasta el invierno.',
            'El exceso de calor inactiva los receptores uterinos de progesterona.'
        ],
        "correcta": 0,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'Al administrar un dispositivo de Altrenogest (un progestágeno sintético) a un grupo de cerdas nulíparas durante 14 días y luego retirarlo abruptamente, ¿qué respuesta fisiológica se espera?',
        "opciones": [
            'Aborto inmediato de cualquier gestación subclínica.',
            'Un bloqueo hipotalámico prolongado que las mantendrá en anestro por 2 meses.',
            'El retiro simula la luteólisis natural, provocando un aumento rebote de FSH y LH que sincroniza el estro de todo el lote en 4-5 días.',
            'Luteinización de todos los folículos presentes, formando quistes.'
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": '¿Cuál es una particularidad anatómica del oviducto de la gallina que difiere sustancialmente de los mamíferos domésticos respecto a la fertilización?',
        "opciones": [
            'No presenta infundíbulo.',
            'Posee glándulas de almacenamiento de espermatozoides que mantienen viables las células espermáticas durante semanas, permitiendo fertilizar múltiples óvulos con una sola cópula.',
            'El óvulo es fertilizado en el útero en lugar de en el tercio superior del oviducto.',
            'La gallina requiere dos cópulas con 12 horas de diferencia para capacitar al espermatozoide.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'Si un folículo dominante bovino alcanza un tamaño de 15 mm pero ocurre un pico prematuro de PGF2a en el día 10 del ciclo, ¿qué sucederá con dicho folículo?',
        "opciones": [
            'Entrará en atresia inmediatamente.',
            'Se enquistará formando un cuerpo lúteo.',
            'Ovulará, ya que la luteólisis eliminará la progesterona inhibidora, permitiendo el pico de LH y desencadenando la ovulación temprana.',
            'Se detendrá su crecimiento esperando a la segunda onda folicular.'
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'La yegua presenta un ciclo estral con un comportamiento único respecto al momento de la ovulación. ¿Cuál es esta diferencia cardinal comparada con la vaca?',
        "opciones": [
            'La yegua ovula 24-48 horas después de terminado el celo.',
            'La yegua ovula múltiples folículos simultáneamente.',
            'La yegua ovula 1 a 2 días antes de que finalicen los signos conductuales del estro (durante el celo), mientras que la vaca ovula unas 12 horas después de terminado el celo.',
            'La ovulación en yeguas es inducida exclusivamente por la cópula.'
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": "¿Cuál es el principal factor fisiológico que provoca el fenómeno de 'celo silencioso' (alta tasa de no detección) en vacas lecheras de alta producción?",
        "opciones": [
            'Incapacidad genética para producir estrógeno.',
            'El alto flujo sanguíneo hepático asociado a la ingesta masiva de alimento metaboliza y limpia el estradiol del torrente sanguíneo tan rápido que no se alcanza el umbral para mostrar signos fuertes de celo.',
            'Agotamiento de las reservas de calcio en el cerebro.',
            'El ordeño robotizado bloquea la sensibilidad táctil de la vaca.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'En aves de postura comercial, ¿cuál es el estímulo primario que regula el eje reproductivo y sostiene la jerarquía folicular ovárica activa?',
        "opciones": [
            'La presencia física del gallo reproductor.',
            'Dietas altas en calcio.',
            'El fotoperíodo (horas de luz diarias), siendo necesarias de 14 a 16 horas para mantener suprimida la melatonina y activar la secreción sostenida de GnRH.',
            'La temperatura ambiental menor a 20°C.'
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'En una granja lechera tropical (Bos taurus x Bos indicus), la tasa de detección de celo visual es del 35%. Al analizar financieramente la implementación de collares de actividad, ¿cuál es la métrica principal que justifica el ROI en menos de 6 meses según el caso de estudio?',
        "opciones": [
            'Aumento en la producción pico de leche por lactancia en un 20%.',
            'Ahorro de $150-200 USD anuales por vaca al reducir 30-40 días abiertos.',
            'Eliminación total del uso de protocolos de sincronización hormonal.',
            'Aumento del intervalo entre partos a 15 meses.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'Un ganadero decide inseminar una vaca al observar un sangrado metéstrico vaginal. Fisiológicamente, ¿por qué esta decisión resultará en una falla reproductiva?',
        "opciones": [
            'Porque el sangrado indica niveles máximos de progesterona luteal.',
            'Porque la sangre altera el pH vaginal impidiendo la capacitación.',
            'Porque el sangrado ocurre 24-48h post-ovulación, indicando que el óvulo ya envejeció.',
            'Porque es un signo primario del proestro temprano.'
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'Si aplicamos la regla AM/PM en bovinos, ¿cuál es el fundamento biológico de esperar aproximadamente 12 horas para la inseminación tras la detección del celo?',
        "opciones": [
            'El pico de LH ocurre inmediatamente con el inicio del estro y la ovulación tarda 24h.',
            'La ovulación ocurre 10-14h post-fin del estro, y los espermatozoides requieren 6-8h de capacitación.',
            'El espermatozoide bovino sobrevive menos de 4 horas en el tracto reproductor.',
            'El cérvix se abre completamente solo 12 horas después del primer signo visual.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'El protocolo Ovsynch utiliza una secuencia GnRH-PGF2α-GnRH. ¿Cuál es el propósito endocrinológico exacto de la PRIMERA dosis de GnRH en el día 0?',
        "opciones": [
            'Destruir el cuerpo lúteo presente para iniciar la luteólisis.',
            'Estimular el pico preovulatorio final para la IATF.',
            'Ovular cualquier folículo dominante presente y sincronizar el inicio de una nueva onda folicular.',
            'Bloquear la secreción endógena de PGF2α.'
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": '¿Por qué un protocolo IATF puro (Ovsynch) suele tener menor respuesta en vacas Bos indicus en el trópico comparado con vacas Holstein confinadas?',
        "opciones": [
            'Bos indicus requiere progestágenos exógenos (CIDR) y eCG para asegurar el desarrollo y ovulación del folículo.',
            'Bos indicus carece de receptores funcionales para PGF2α.',
            'El pico de LH en Bos indicus no puede ser estimulado por GnRH exógena.',
            'Los folículos de Bos indicus no producen estradiol durante el proestro.'
        ],
        "correcta": 0,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'Durante el diestro bovino, si no hay reconocimiento materno (ausencia de IFN-τ), ¿qué evento hormonal desencadena la transición hacia un nuevo ciclo?',
        "opciones": [
            'El embrión produce estrógenos que destruyen el cuerpo lúteo.',
            'El hipotálamo secreta pulsos masivos de GnRH.',
            'El endometrio libera PGF2α, causando luteólisis y caída abrupta de progesterona.',
            'El folículo dominante secreta progesterona para iniciar el estro.'
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'Analizando la dinámica folicular comparada, ¿por qué la cerda es capaz de desarrollar camadas (15-25 ovulaciones) mientras que la vaca es monovulatoria?',
        "opciones": [
            'La cerda no produce inhibina folicular en absoluto.',
            'La cerda recluta folículos que no responden a la LH.',
            'El mecanismo de dominancia en la cerda es débil; la inhibina es insuficiente para suprimir FSH completamente, madurando múltiples folículos.',
            'La vaca ovula múltiples folículos pero el útero solo permite la implantación de uno.'
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'En un sistema de producción porcina, ¿cuál es el protocolo de manejo estándar que funciona como el principal sincronizador del ciclo estral en las madres?',
        "opciones": [
            'El uso rutinario de implantes de melatonina (Melovine).',
            'El destete del lote, que elimina la supresión dopaminérgica de la prolactina.',
            'La administración secuencial de PGF2α en el día 14 post-monta.',
            'La restricción de alimento durante 72 horas.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'A diferencia de la vaca, que ovula después del estro, ¿en qué momento ocurre la ovulación de la cerda y qué implicación tiene esto en la Inseminación Artificial?',
        "opciones": [
            'DURANTE el estro (36-44h post-inicio), requiriendo IA múltiple (2-3 veces) debido al largo estro de 24-72h.',
            'ANTES del inicio del estro, obligando a inseminar a tiempo fijo obligatoriamente.',
            'A las 12h post-fin del estro, aplicando la misma regla AM/PM que en bovinos.',
            'Simultáneamente con el pico de PGF2α luteal.'
        ],
        "correcta": 0,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": '¿Cuál es el signo clínico primario en la cerda que garantiza una sensibilidad >90% en la detección del celo para IA?',
        "opciones": [
            'Flujo de moco cervical cristalino y abundante.',
            'Reflejo de inmovilidad ante la presión dorsal, especialmente en presencia de feromonas del verraco.',
            'Aumento de la temperatura vaginal superior a 0.5°C.',
            'Micción frecuente y levantamiento de la cola.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'Las ovejas son especies poliéstricas estacionales. Fisiológicamente, ¿cómo influye el fotoperíodo en la activación de su eje reproductivo?',
        "opciones": [
            'Días largos reducen la melatonina, estimulando la liberación de GnRH.',
            'Días cortos aumentan la secreción prolongada de melatonina, lo cual activa el eje HHG.',
            'La temperatura fría bloquea la dopamina independientemente de la luz.',
            'La ausencia de luz destruye el cuerpo lúteo estacional.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'Para adelantar la temporada reproductiva en ovinos simulando fisiológicamente el otoño (noches largas), ¿qué biotecnología es recomendada?',
        "opciones": [
            'Programa de luz artificial 16L:8O.',
            'Implantes subcutáneos de liberación continua de melatonina (ej. Melovine) 40-50 días pre-empadre.',
            'Inyección de prostaglandinas diarias por 15 días.',
            'Separación estricta de las hembras de cualquier macho.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'El efecto macho es una biotecnología de manejo muy útil en caprinos. ¿En qué consiste su mecanismo de acción fisiológico?',
        "opciones": [
            'La monta repetida mecánicamente rompe el folículo anovulatorio.',
            'La introducción súbita del macho libera feromonas que estimulan pulsos de GnRH y LH en hembras anovulatorias.',
            'El macho induce la liberación de progesterona luteal directamente.',
            'El olor del macho disminuye la temperatura corporal de la hembra.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'Considerando las diferencias reproductivas, ¿por qué en la yegua la inseminación artificial se debe realizar DURANTE el estro y no después como en la vaca?',
        "opciones": [
            'Porque su estro es muy corto (menos de 10 horas).',
            'Porque la ovulación en la yegua ocurre 24-48h ANTES de que termine el estro prolongado (4-7 días).',
            'Porque el espermatozoide equino requiere 48 horas de capacitación.',
            'Porque la yegua no presenta un pico ovulatorio de LH.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'La gallina comercial carece de ciclo estral pero mantiene un ciclo ovulatorio. ¿Cuál es el factor determinante que activa su eje reproductivo?',
        "opciones": [
            'Fotoperíodo largo (16L:8O) que suprime la melatonina y permite la secreción activa de GnRH.',
            'Días cortos que aumentan la melatonina.',
            'La presencia constante de un gallo maduro en el galpón.',
            'Niveles altos de progesterona luteal al finalizar la postura.'
        ],
        "correcta": 0,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": '¿Qué adaptación anatómica permite a la gallina fecundar múltiples óvulos a lo largo de 10-14 días con una única cópula?',
        "opciones": [
            'Desarrollo de múltiples cuerpos lúteos simultáneos.',
            'Túbulos de almacenamiento espermático (SST) en la unión útero-vaginal con liberación gradual.',
            'Un oviducto extremadamente corto que capacita el semen instantáneamente.',
            'Doble ovario funcional y sincronizado.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'En un protocolo Ovsynch bovino (Día 0 GnRH, Día 7 PGF2α, Día 9 GnRH), ¿qué pasaría si omitimos la dosis de PGF2α del día 7?',
        "opciones": [
            'La vaca ovularía normalmente porque la segunda GnRH es suficiente.',
            'El cuerpo lúteo no se destruiría (no luteólisis), la progesterona se mantendría alta y bloquearía la ovulación del folículo dominante.',
            'Se induciría una poliovulación y riesgo de gestación gemelar.',
            'El útero rechazaría la implantación por exceso de prostaglandina endógena.'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": '¿Cuál es la justificación principal para añadir una fase de Presynch (2 dosis de PGF2α previas) a un protocolo Ovsynch en vacas lecheras?',
        "opciones": [
            'Inducir súperovulación temprana.',
            'Destruir folículos atrésicos del parto anterior.',
            'Asegurar que la gran mayoría del lote se encuentre en la fase luteal temprana al iniciar el Ovsynch, mejorando las tasas de preñez en 5-10%.',
            'Reducir los costos operativos de las hormonas sintéticas.'
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'El Herd Navigator permite medir niveles de progesterona en la leche de forma automatizada. Clínicamente, ¿qué indica una caída sostenida a menos de 5 ng/mL en una vaca?',
        "opciones": [
            'Gestación confirmada.',
            'Presencia de un quiste luteal persistente.',
            'Luteólisis exitosa y entrada a la fase folicular (posible celo inminente).',
            'Ausencia absoluta de actividad ovárica (Anestro profundo).'
        ],
        "correcta": 2,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'Una revisión de registros indica una tasa de preñez a 3 meses del 20% en un hato bovino tropical con detección visual de celos. Si la tasa de concepción es del 50%, ¿cuál es la tasa de detección de celo (TDC)?',
        "opciones": [
            '20%',
            '40%',
            '50%',
            '70%'
        ],
        "correcta": 1,
        "tipo": "opcion_multiple"
    },
    {
        "pregunta": 'Empareje la estructura ovárica anatómica con su función principal y hormona predominante.',
        "opciones": [
            'Reserva ovárica en reposo',
            'Secreta grandes cantidades de Estradiol e Inhibina',
            'Secreta Progesterona para mantener la gestación',
            'Cicatriz fibrosa inactiva'
        ],
        "pares": [
            'Folículo Primordial',
            'Folículo Dominante',
            'Cuerpo Lúteo',
            'Cuerpo Albicans'
        ],
        "correcta": {'Folículo Primordial': 'Reserva ovárica en reposo', 'Folículo Dominante': 'Secreta grandes cantidades de Estradiol e Inhibina', 'Cuerpo Lúteo': 'Secreta Progesterona para mantener la gestación', 'Cuerpo Albicans': 'Cicatriz fibrosa inactiva'},
        "tipo": "emparejar"
    },
    {
        "pregunta": 'Empareje la hormona con la glándula endocrina que la sintetiza y secreta.',
        "opciones": [
            'Hipotálamo',
            'Hipófisis Anterior (Adenohipófisis)',
            'Endometrio uterino',
            'Glándula Pineal'
        ],
        "pares": [
            'GnRH (Hormona Liberadora de Gonadotropinas)',
            'FSH (Hormona Foliculoestimulante)',
            'Prostaglandina F2a (PGF2a)',
            'Melatonina'
        ],
        "correcta": {'GnRH (Hormona Liberadora de Gonadotropinas)': 'Hipotálamo', 'FSH (Hormona Foliculoestimulante)': 'Hipófisis Anterior (Adenohipófisis)', 'Prostaglandina F2a (PGF2a)': 'Endometrio uterino', 'Melatonina': 'Glándula Pineal'},
        "tipo": "emparejar"
    },
    {
        "pregunta": 'Asocie a cada especie con la característica principal que define su ciclo reproductivo estral.',
        "opciones": [
            'Poliéstrica continua, monovulatoria',
            'Poliéstrica estacional de días largos, estro prolongado',
            'Poliéstrica estacional de días cortos',
            'Poliéstrica continua, poliovulatoria (camadas)'
        ],
        "pares": [
            'Bovino',
            'Equino',
            'Ovino',
            'Porcino'
        ],
        "correcta": {'Bovino': 'Poliéstrica continua, monovulatoria', 'Equino': 'Poliéstrica estacional de días largos, estro prolongado', 'Ovino': 'Poliéstrica estacional de días cortos', 'Porcino': 'Poliéstrica continua, poliovulatoria (camadas)'},
        "tipo": "emparejar"
    },
    {
        "pregunta": 'Empareje la fase del ciclo estral con el evento predominante que ocurre en ella.',
        "opciones": [
            'Crecimiento folicular acelerado post-luteólisis',
            'Receptividad sexual y pico de LH',
            'Formación del cuerpo hemorrágico/lúteo temprano',
            'Dominancia absoluta de la Progesterona'
        ],
        "pares": [
            'Proestro',
            'Estro',
            'Metaestro',
            'Diestro'
        ],
        "correcta": {'Proestro': 'Crecimiento folicular acelerado post-luteólisis', 'Estro': 'Receptividad sexual y pico de LH', 'Metaestro': 'Formación del cuerpo hemorrágico/lúteo temprano', 'Diestro': 'Dominancia absoluta de la Progesterona'},
        "tipo": "emparejar"
    },
    {
        "pregunta": 'Relacione el protocolo de sincronización o biotecnología con su función principal en campo.',
        "opciones": [
            'Sincronización de ovulación mediante GnRH-PGF2a-GnRH',
            'Dispositivo intravaginal liberador de Progesterona',
            'Progestágeno oral usado comúnmente en cerdas y yeguas',
            'Adelanto de la temporada reproductiva en ovejas'
        ],
        "pares": [
            'Ovsynch',
            'CIDR',
            'Altrenogest',
            'Implante de Melatonina'
        ],
        "correcta": {'Ovsynch': 'Sincronización de ovulación mediante GnRH-PGF2a-GnRH', 'CIDR': 'Dispositivo intravaginal liberador de Progesterona', 'Altrenogest': 'Progestágeno oral usado comúnmente en cerdas y yeguas', 'Implante de Melatonina': 'Adelanto de la temporada reproductiva en ovejas'},
        "tipo": "emparejar"
    },
    {
        "pregunta": 'Asocie cada segmento del tracto reproductivo de la gallina con su función fisiológica en la formación del huevo.',
        "opciones": [
            'Lugar exacto de la fertilización',
            'Secreción de la albúmina (clara) densa',
            'Formación de las membranas testáceas',
            'Depósito masivo de carbonato de calcio para el cascarón'
        ],
        "pares": [
            'Infundíbulo',
            'Magno',
            'Istmo',
            'Útero (Glándula cascarógena)'
        ],
        "correcta": {'Infundíbulo': 'Lugar exacto de la fertilización', 'Magno': 'Secreción de la albúmina (clara) densa', 'Istmo': 'Formación de las membranas testáceas', 'Útero (Glándula cascarógena)': 'Depósito masivo de carbonato de calcio para el cascarón'},
        "tipo": "emparejar"
    },
    {
        "pregunta": 'Empareje el evento del desarrollo folicular bovino con la hormona gonadotropina que lo estimula principalmente.',
        "opciones": [
            'Altos niveles de FSH sinérgicos con baja LH',
            'Transición de dependencia de FSH hacia LH',
            'Dependencia exclusiva de pulsos altos de LH',
            'Pico preovulatorio masivo de LH'
        ],
        "pares": [
            'Reclutamiento',
            'Selección',
            'Dominancia',
            'Ovulación'
        ],
        "correcta": {'Reclutamiento': 'Altos niveles de FSH sinérgicos con baja LH', 'Selección': 'Transición de dependencia de FSH hacia LH', 'Dominancia': 'Dependencia exclusiva de pulsos altos de LH', 'Ovulación': 'Pico preovulatorio masivo de LH'},
        "tipo": "emparejar"
    },
    {
        "pregunta": 'Relacione el fallo reproductivo con su causa metabólica más probable según los casos de estudio.',
        "opciones": [
            'Rápido metabolismo hepático del estradiol en alta producción',
            'Falta de un folículo responsivo en la primera inyección de GnRH',
            'Déficit en la producción de Interferón tau por estrés térmico',
            'Fotoperíodo mantenido en días artificialmente largos'
        ],
        "pares": [
            'Celo silencioso',
            'Fallo de Ovsynch',
            'Muerte embrionaria temprana',
            'Anestro estacional ovino prolongado'
        ],
        "correcta": {'Celo silencioso': 'Rápido metabolismo hepático del estradiol en alta producción', 'Fallo de Ovsynch': 'Falta de un folículo responsivo en la primera inyección de GnRH', 'Muerte embrionaria temprana': 'Déficit en la producción de Interferón tau por estrés térmico', 'Anestro estacional ovino prolongado': 'Fotoperíodo mantenido en días artificialmente largos'},
        "tipo": "emparejar"
    },
    {
        "pregunta": 'Empareje la herramienta de detección de estros con su fundamento de funcionamiento biológico.',
        "opciones": [
            'Miden la aceptación pasiva de la monta (fricción)',
            'Miden la hiperactividad motriz asociada a la fase estrogénica',
            'Cuantifican la caída bioquímica de progesterona en leche',
            'Visualizan la dinámica del crecimiento y ruptura del folículo preovulatorio'
        ],
        "pares": [
            'Parches KaMar / Pintura',
            'Collares acelerómetros',
            'Herd Navigator',
            'Ecografía transrectal seriada'
        ],
        "correcta": {'Parches KaMar / Pintura': 'Miden la aceptación pasiva de la monta (fricción)', 'Collares acelerómetros': 'Miden la hiperactividad motriz asociada a la fase estrogénica', 'Herd Navigator': 'Cuantifican la caída bioquímica de progesterona en leche', 'Ecografía transrectal seriada': 'Visualizan la dinámica del crecimiento y ruptura del folículo preovulatorio'},
        "tipo": "emparejar"
    },
    {
        "pregunta": "Relacione cada especie con el mecanismo de 'Reconocimiento Materno de la Gestación'.",
        "opciones": [
            'Interferón tau (IFN-t) inhibe los receptores de oxitocina',
            'Estrógenos embrionarios redirigen la PGF2a hacia el lumen uterino',
            'Movimiento continuo del concepto esférico por toda la cavidad uterina',
            'No requieren señal química especial; el cuerpo lúteo dura lo mismo que una gestación natural'
        ],
        "pares": [
            'Bovinos / Ovinos',
            'Porcinos',
            'Equinos',
            'Caninos'
        ],
        "correcta": {'Bovinos / Ovinos': 'Interferón tau (IFN-t) inhibe los receptores de oxitocina', 'Porcinos': 'Estrógenos embrionarios redirigen la PGF2a hacia el lumen uterino', 'Equinos': 'Movimiento continuo del concepto esférico por toda la cavidad uterina', 'Caninos': 'No requieren señal química especial; el cuerpo lúteo dura lo mismo que una gestación natural'},
        "tipo": "emparejar"
    },
    {
        "pregunta": 'La secreción de la hormona [1] es controlada por el hipotálamo y viaja a la hipófisis para estimular la liberación de FSH y LH. A su vez, la [2] es producida por el folículo para inhibir selectivamente a la FSH y asegurar la dominancia.',
        "opciones": {
            '1': [
                'GnRH',
                'Oxitocina',
                'Progesterona',
                'Prolactina'
            ],
            '2': [
                'Inhibina',
                'PGF2a',
                'Melatonina',
                'Adrenalina'
            ]
        },
        "correcta": {'1': 'GnRH', '2': 'Inhibina'},
        "tipo": "completar_espacios"
    },
    {
        "pregunta": 'Durante el protocolo Ovsynch bovino, la inyección de GnRH en el día 0 busca inducir una [1], mientras que la inyección de PGF2a en el día 7 tiene como objetivo causar [2].',
        "opciones": {
            '1': [
                'Nueva onda folicular',
                'Luteólisis total',
                'Gestación inmediata',
                'Atrofia ovárica'
            ],
            '2': [
                'Luteólisis',
                'Ovulación',
                'Formación de quistes',
                'Fecundación'
            ]
        },
        "correcta": {'1': 'Nueva onda folicular', '2': 'Luteólisis'},
        "tipo": "completar_espacios"
    },
    {
        "pregunta": 'La vaca es clasificada como poliéstrica [1], lo que significa que cicla todo el año. En contraste, la yegua es poliéstrica estacional de días [2], lo que significa que su actividad ovárica se reactiva en primavera.',
        "opciones": {
            '1': [
                'Continua',
                'Estacional',
                'Anual',
                'Invertida'
            ],
            '2': [
                'Largos',
                'Cortos',
                'Lluviosos',
                'Oscuros'
            ]
        },
        "correcta": {'1': 'Continua', '2': 'Largos'},
        "tipo": "completar_espacios"
    },
    {
        "pregunta": 'La luteólisis es el proceso fisiológico que destruye al [1] para permitir un nuevo ciclo estral. En los rumiantes y porcinos, la hormona que causa este evento es la [2], producida por el útero en ausencia de gestación.',
        "opciones": {
            '1': [
                'Cuerpo Lúteo',
                'Folículo Primario',
                'Endometrio',
                'Trofoblasto'
            ],
            '2': [
                'Prostaglandina F2a',
                'Oxitocina',
                'GnRH',
                'Progesterona'
            ]
        },
        "correcta": {'1': 'Cuerpo Lúteo', '2': 'Prostaglandina F2a'},
        "tipo": "completar_espacios"
    },
    {
        "pregunta": 'El Reconocimiento Materno de la Gestación en cerdos es dependiente de los [1] secretados por el embrión, lo cual evita que la PGF2a destruya a los [2] necesarios para mantener la preñez.',
        "opciones": {
            '1': [
                'Estrógenos',
                'Interferones',
                'Andrógenos',
                'Mineralocorticoides'
            ],
            '2': [
                'Cuerpos Lúteos',
                'Folículos Antrales',
                'Ovocitos',
                'Receptores de GnRH'
            ]
        },
        "correcta": {'1': 'Estrógenos', '2': 'Cuerpos Lúteos'},
        "tipo": "completar_espacios"
    },
    {
        "pregunta": 'En las aves reproductoras, la [1] de los espermatozoides se da en criptas especializadas de la unión útero-vaginal, permitiendo que la fertilización ocurra repetidamente sin necesidad del gallo hasta por [2] semanas.',
        "opciones": {
            '1': [
                'Almacenamiento (Supervivencia prolongada)',
                'Capacitación fulminante',
                'Destrucción ácida',
                'Replicación genética'
            ],
            '2': [
                '2 a 4',
                'Menos de 1',
                'Más de 10',
                'Aproximadamente 40'
            ]
        },
        "correcta": {'1': 'Almacenamiento (Supervivencia prolongada)', '2': '2 a 4'},
        "tipo": "completar_espacios"
    },
    {
        "pregunta": 'En yeguas, el fotoperíodo controla la estacionalidad a través de la glándula [1]. Cuando los días son largos, la producción de melatonina [2], lo que retira el freno inhibitorio sobre el hipotálamo y permite el inicio de la ciclicidad.',
        "opciones": {
            '1': [
                'Pineal',
                'Pituitaria',
                'Tiroides',
                'Suprarrenal'
            ],
            '2': [
                'Disminuye',
                'Aumenta al máximo',
                'Se cristaliza',
                'Inicia su producción'
            ]
        },
        "correcta": {'1': 'Pineal', '2': 'Disminuye'},
        "tipo": "completar_espacios"
    },
    {
        "pregunta": 'Durante la detección de estros con parches (KaMar), se identifica a las vacas que aceptan el [1]. Sin embargo, en hatos robotizados, es mucho más eficaz el monitoreo hormonal mediante [2].',
        "opciones": {
            '1': [
                'Monta (fricción dorso-lumbar)',
                'Ordeño',
                'Consumo de alimento',
                'Olor del toro'
            ],
            '2': [
                'Biosensores de Progesterona en leche (ej. Herd Navigator)',
                'Ecografía manual diaria',
                'Visualización nocturna',
                'Collares acústicos'
            ]
        },
        "correcta": {'1': 'Monta (fricción dorso-lumbar)', '2': 'Biosensores de Progesterona en leche (ej. Herd Navigator)'},
        "tipo": "completar_espacios"
    },
    {
        "pregunta": "Una causa frecuente de fallo en protocolos IATF es no respetar la regla 'AM-PM', la cual indica inseminar [1] horas después de detectado el estro. Esto se debe a que la ovulación bovina ocurre unas [2] horas posteriores a la culminación de los signos de celo.",
        "opciones": {
            '1': [
                '12',
                '0',
                '48',
                '72'
            ],
            '2': [
                '10 a 14',
                '2 a 4',
                '24 a 30',
                '40 a 50'
            ]
        },
        "correcta": {'1': '12', '2': '10 a 14'},
        "tipo": "completar_espacios"
    },
    {
        "pregunta": 'El metabolismo de las vacas lecheras de altísima producción genera un alto flujo [1], que elimina velozmente los estrógenos circulantes. Esto se traduce fisiológicamente en [2], dificultando severamente la observación visual.',
        "opciones": {
            '1': [
                'Sanguíneo Hepático (Hígado)',
                'Linfático mamario',
                'Respiratorio',
                'Digestivo ruminal'
            ],
            '2': [
                'Celos silenciosos o muy cortos',
                'Aceptación de montas continuas',
                'Prolapso vaginal',
                'Ninfomanía prolongada'
            ]
        },
        "correcta": {'1': 'Sanguíneo Hepático (Hígado)', '2': 'Celos silenciosos o muy cortos'},
        "tipo": "completar_espacios"
    }
]

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
                long_question = random.sample(BANCO_PREGUNTAS[:5], 1)
                other_questions = random.sample(BANCO_PREGUNTAS[5:], 19)
                selected_questions = long_question + other_questions
                random.shuffle(selected_questions)
                st.session_state.eval_preguntas = selected_questions
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
                if q["tipo"] == "opcion_multiple":
                    val = st.session_state.get(f"radio_q_{idx}")
                    if val is not None:
                        st.session_state.eval_seleccion_actual = q["opciones"].index(val)
                        completo = True
                elif q["tipo"] == "emparejar":
                    selecciones = {}
                    completo = True
                    for par in q["pares"]:
                        val = st.session_state.get(f"emp_q_{idx}_{par}")
                        if val == "Seleccionar..." or not val:
                            completo = False
                            break
                        selecciones[par] = val
                    if completo:
                        st.session_state.eval_seleccion_actual = selecciones
                elif q["tipo"] == "completar_espacios":
                    selecciones = {}
                    completo = True
                    for esp_num in q["opciones"].keys():
                        val = st.session_state.get(f"comp_q_{idx}_{esp_num}")
                        if val == "Seleccionar..." or not val:
                            completo = False
                            break
                        selecciones[esp_num] = val
                    if completo:
                        st.session_state.eval_seleccion_actual = selecciones

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
            
            gs = get_global_exam_state()
            duracion_total = 1200
            if gs.get("hora_inicio") and gs.get("hora_fin"):
                duracion_total = (gs["hora_fin"] - gs["hora_inicio"]).total_seconds()
                
            end_time = st.session_state.get("eval_global_end_time", datetime.datetime.now())
            tiempo_tardado = duracion_total - max(0, (end_time - datetime.datetime.now()).total_seconds())
            
            tiempo_minutos = round(tiempo_tardado / 60, 2)
            registro = {
                "key": est_key,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nombre": nombre,
                "carrera": carrera,
                "curso": curso,
                "nota": f"{puntaje}/20",
                "tiempo": f"{tiempo_minutos} min"
            }
            if "registros" in gs:
                gs["registros"].append(registro)
            st.session_state.eval_guardado_global = True
            
            # --- INTEGRACIÓN GOOGLE SHEETS ---
            
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                data = pd.DataFrame([registro])
                
                existing_data = conn.read(worksheet="Calificaciones", ttl=5)
                # Si la hoja está totalmente vacía, 'existing_data' puede no tener columnas
                if existing_data.empty:
                    updated_data = data
                else:
                    updated_data = pd.concat([existing_data, data], ignore_index=True)
                    
                conn.update(worksheet="Calificaciones", data=updated_data)
            except Exception as e:
                print("Error GSheets:", e)
        
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
