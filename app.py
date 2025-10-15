#!/usr/bin/env python3
"""
🌿 ASISTENTE EMOCIONAL ULTRA - STREAMLIT VERSION COMPLETA
Versión: 4.0 - "Detección Multi-Emocional Avanzada"
Interfaz completa adaptada a Streamlit
"""

import streamlit as st
import json
import random
import datetime
import os
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

# ==================== CONFIGURACIÓN STREAMLIT ====================
st.set_page_config(
    page_title="Asistente Emocional ULTRA",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CONFIGURACIÓN AVANZADA ====================
CONFIG = {
    "usuario": {
        "nombre": "Jorge",
        "edad": 19,
        "preferencias": {
            "tono": "psicólogo-amigo-poeta",
            "profundidad_reflexiones": "media",
            "incluir_tecnicas": True,
            "incluir_poesia": True,
            "deteccion_multiple": True
        }
    },
    "ia": {
        "confianza_minima": 0.65,
        "umbral_conflicto": 0.3
    },
    "sistema": {
        "backup_automatico": True,
        "max_historial": 1000,
        "auto_limpieza": True
    }
}

# ==================== SABIDURÍA COMPLETA (MANTENIENDO TODO EL CONTENIDO) ====================
SABIDURIA = {
    "validacion": {
        "universal": [
            "Todo lo que sientes es válido y merece ser escuchado con compasión.",
            "Tu emoción no es un error del sistema, es una característica del diseño humano.",
            "No estás roto por sentir esto - estás vivo y respondiendo a la vida.",
            "Cada emoción tiene su geografía interna; explorarla con curiosidad es sanador.",
            "Lo que sientes ahora es un capítulo, no toda la historia.",
            "Incluso la sombra necesita ser abrazada para revelar su forma completa.",
            "Cada sentimiento trae un mensaje: escúchalo antes de juzgarlo.",
            "Eres humano, y eso significa sentir, equivocarte, volver a intentar.",
            "No necesitas justificar tu emoción; sentir ya es suficiente.",
            "La vulnerabilidad no es debilidad: es el lenguaje de la autenticidad."
        ],
        "conflicto": [
            "Es completamente humano sentir emociones contradictorias al mismo tiempo.",
            "Tu conflicto interno es señal de que estás procesando algo complejo y significativo.",
            "Las emociones mezcladas son como colores que se encuentran - crean nuevos matices.",
            "No tienes que elegir una sola emoción; todas pueden coexistir en tu experiencia.",
            "Esta ambivalencia revela la riqueza de tu mundo interior.",
            "Sentir opuestos simultáneamente es evidencia de tu capacidad para contener complejidad.",
            "Tu corazón puede albergar múltiples verdades emocionales a la vez.",
            "Este conflicto no es caos, es el tejido mismo de la experiencia humana auténtica.",
            "Las emociones contradictorias son como instrumentos en una orquesta - cada una aporta su sonido único.",
            "Honra todas las partes de ti que están hablando a través de estas emociones."
        ],
        "tristeza": [
            "La tristeza es el corazón diciendo 'esto me importa profundamente'.",
            "Detrás de cada lágrima hay una historia de amor que merece ser honrada.",
            "Permitirse estar triste en un mundo que exige felicidad constante es un acto de valentía.",
            "Tu tristeza no es un peso, es un maestro silencioso.",
            "El dolor que sientes es la medida de tu capacidad para amar.",
            "Está bien no estar bien; incluso las estrellas tienen noches sin brillo.",
            "No te avergüences de tu melancolía, es la prueba de que tu alma siente profundamente.",
            "Lo que ahora pesa, mañana será enseñanza.",
            "La tristeza no es un callejón sin salida, sino un camino hacia tu interior.",
            "Cada lágrima contiene una verdad que merece ser escuchada.",
            "Permanece con tu pena; a veces la atención suave la transforma en entendimiento.",
            "No tienes que arreglar todo ahora; el tiempo y la ternura harán su parte.",
            "La melancolía también es una forma de sabiduría que habla despacio.",
            "Hay poemas y días que nacen solo porque permitiste sentir.",
            "Cada noche cerrada prepara el alba de una nueva claridad.",
            "Tu cuidado hoy será la memoria que te sostenga mañana.",
            "La tristeza no borra tu valor; lo revela desde otra dimensión.",
            "Está bien pedir calma, compañía o silencio: tu deseo importa.",
            "No apures el duelo; algunas cosas necesitan tiempo y ternura.",
            "Siéntela, nómbrala y deja que pase con respeto hacia ti."
        ],
        "alegria": [
            "¡Qué hermoso que permits que la alegría te habite! Disfruta este regalo plenamente.",
            "Tu felicidad es un faro que ilumina no solo tu camino sino también el de otros.",
            "Estos momentos de alegría son depósitos en tu banco emocional para días más difíciles.",
            "La alegría auténtica nace desde dentro y se expande sin condiciones.",
            "Celebra esta emoción - es evidencia de que estás vivo y presente.",
            "Tu risa es un pequeño milagro que desafía la gravedad del mundo.",
            "A veces la felicidad no se explica, solo se habita.",
            "Qué hermoso verte florecer en tu propio tiempo.",
            "La alegría que sientes hoy es semilla para mañanas más oscuros.",
            "Comparte tu alegría - es un recurso que crece al darse.",
            "Disfrutar sin culpa es un acto de justicia contigo mismo.",
            "Registra este momento: la memoria es un aliado en días grises.",
            "Permítete celebrar en pequeño y en grande: ambos cuentan.",
            "La alegría fortalece y suaviza, como un entramado que sostiene.",
            "Deja que esa luz te recuerde quién eres cuando la sombra vuelva.",
            "La gratitud convierte pequeños instantes en tesoros duraderos.",
            "Ser feliz hoy es preparar equipaje emocional para el mañana.",
            "Cuando compartes alegría, la multiplicas sin perder nada.",
            "Canta en silencio si quieres: la alegría no siempre necesita público.",
            "Agradece el cuerpo que posibilita la sonrisa; él también merece cuidado."
        ],
        "ansiedad": [
            "Tu ansiedad es un sistema ancestral de protección, no un enemigo.",
            "La mente está haciendo su trabajo: anticipar para protegerte.",
            "Esta sensación pasará - como todas las olas emocionales, tiene principio y fin.",
            "Respirar conscientemente es tu ancla en este mar de incertidumbre.",
            "No necesitas resolver todo ahora. Basta con el siguiente pequeño paso.",
            "No necesitas controlar el mar, solo aprender a flotar en él.",
            "Respira. No estás en peligro, solo en pensamientos que exageran.",
            "Tu mente corre rápido porque quiere protegerte; agradécele y dile que puede descansar.",
            "La ansiedad es el eco de futuros que aún no han decidido llegar.",
            "Ancla tu atención en este momento - es el único que realmente existe.",
            "No eres tu ritmo acelerado; eres quien puede observarlo con ternura.",
            "Una pausa breve puede cambiar el curso de una hora ansiosa.",
            "El oxígeno que entra ahora calma circuitos antiguos: confía en ello.",
            "Es válido pedir ayuda cuando la mente pesa más de lo habitual.",
            "Reducir la velocidad no es renuncia, es estrategia de supervivencia emocional.",
            "Repetir una frase amable (" + '"estoy aquí"' + ") suaviza la tormenta interna.",
            "Un gesto corporal sencillo (poner la mano en el pecho) te conecta con el presente.",
            "Acepta la incomodidad como visitante, no como huésped permanente.",
            "Hacer una cosa pequeña ahora puede devolver sensación de control.",
            "Recuerda: sentir temor no te hace débil; te hace humano y sensible."
        ],
        "enojo": [
            "Tu enojo es energía pura que señala límites importantes.",
            "Detrás de esta ira hay necesidades no escuchadas que claman atención.",
            "El enojo bien canalizado puede ser el motor de cambios necesarios.",
            "Esta emoción te está mostrando lo que realmente valoras y quieres proteger.",
            "Tu frustración es evidencia de que aún te importa, aún tienes esperanza.",
            "Tu enojo es la voz de algo que ya no cabe en silencio.",
            "A veces gritar internamente es la única forma de decir 'esto me importa'.",
            "No es debilidad enfadarte; es señal de que algo dentro de ti exige respeto.",
            "El fuego de tu enojo puede forjar herramientas de cambio positivo.",
            "Tu rabia contiene información crucial sobre tus valores más profundos.",
            "Respirar antes de actuar da sabiduría a la reacción.",
            "La ira puede ser brújula: ¿hacia dónde te dirige exactamente?",
            "No confundas sentir rabia con dañarte a ti mismo o a otros.",
            "En ocasiones, convertir enojo en límites claros es la mejor respuesta.",
            "Permitir la expresión contenida evita que el fuego te consuma.",
            "La ira sirve como termómetro: te indica dónde poner energía reparadora.",
            "Puedes usar esa intensidad para crear, no solo para destruir.",
            "Agradece la señal; ahora decide con frialdad qué hacer con ella.",
            "Hablar la verdad desde calma es más potente que gritar desde el daño.",
            "La asertividad es la forma adulta de transformar la rabia en cambio."
        ],
        "esperanza": [
            "La esperanza es el oxígeno del alma en momentos de oscuridad.",
            "Cada amanecer trae nuevas posibilidades aún no imaginadas.", 
            "Tu resiliencia se construye día a día, como un músculo invisible.",
            "Los momentos difíciles son el suelo donde crece la esperanza.",
            "Confía en el proceso, incluso cuando no veas el camino completo.",
            "La esperanza no consiste en negar lo absurdo, sino en abrazarlo sin temor.",
            "Cuando todo carece de sentido, la esperanza se convierte en acto de rebeldía.",
            "El hombre absurdo halla esperanza en la aceptación plena de su destino.",
            "Sísifo sonríe, y en su sonrisa nace una esperanza que no promete nada.",
            "No hay futuro garantizado, pero sí presente elegido: ahí reside la esperanza.",
            "La esperanza nace cuando el hombre se descubre como posibilidad inacabada.",
            "No se espera lo que se tiene, sino lo que aún puede ser creado.",
            "El hombre se hace a sí mismo, y en ese hacerse habita la esperanza.",
            "La libertad es la raíz de toda esperanza auténtica.",
            "Esperar es comprometerse con el futuro desde el presente.",
            "Incluso en la oscuridad del sufrimiento, el sentido puede iluminar el alma.",
            "La esperanza es la fuerza que convierte el dolor en propósito.",
            "Quien tiene un porqué puede soportar casi cualquier cómo.",
            "La desesperación es sufrimiento sin sentido; la esperanza es darle dirección.",
            "Hasta en el infierno humano puede hallarse una chispa de sentido."
        ],
    },

    "reflexion": {
        "tristeza": [
            """La tristeza, cuando es abrazada con compasión, revela dimensiones profundas del ser:

• Enseña humildad al recordarnos nuestra vulnerabilidad compartida
• Abre espacio para el autoconocimiento y la introspección verdadera  
• Purifica el alma, como la lluvia limpia el aire después de la tormenta
• Conecta con la belleza de lo efímero y la profundidad de lo humano
• Prepara el terreno para nuevas semillas de significado y propósito

Esta emoción no es un callejón sin salida, sino un camino hacia tu interior más auténtico.""",
            """Desde la neurociencia y la sabiduría ancestral:

La tristeza activa redes cerebrales de reflexión y autoconciencia
Estimula la producción de lágrimas que liberan hormonas del estrés
En muchas tradiciones, el llanto es considerado una limpieza del alma
Los poetas encuentran en la melancolía su fuente más profunda de creatividad
La tristeza bien transitada fortalece la resiliencia emocional

Honra este proceso - tu sistema completo está trabajando para tu evolución.""",
            """La pena no es un error; es una respuesta a lo que importa. Al recibirla con cuidado,
ella se vuelve guía: te señala qué necesita reparación, atención o reconocimiento.
Déjala hablar y aprenderás qué valora tu corazón."""
        ],
        "alegria": [
            """La alegría auténtica es mucho más que emoción pasajera:

Es práctica espiritual que conecta con la abundancia del presente
Es acto de resistencia contra el cinismo y la desesperanza contemporáneos  
Es lenguaje universal que trasciende barreras y une corazones
Es recurso renovable que crece exponencialmente cuando se comparte
Es ancla que mantiene conectado a lo esencial cuando todo se complica

Tu alegría hoy es recordatorio de que la vida, a pesar de todo, merece celebración.""",
            """La ciencia detrás del bienestar:

La alegría libera endorfinas, dopamina y serotonina - el cóctel natural de bienestar
Fortalece el sistema inmunológico y promueve la salud cardiovascular
Crea nuevas conexiones neuronales que facilitan el aprendizaje y creatividad
Genera coherencia cardiaca que armoniza todo el organismo
Se almacena en memoria implícita como recurso para momentos desafiantes"""
        ],
        "ansiedad": [
            """La ansiedad moderna es often exilio del presente:

Vivimos en memoria del dolor pasado o anticipación del futuro temido
Perdemos contacto con el único momento donde existe la paz: AHORA
La respiración consciente es el puente de regreso a casa
El cuerpo nunca está ansioso en el presente absoluto - solo cuando la mente viaja en el tiempo
La práctica de anclarse en los sentidos (5-4-3-2-1) reconecta con la realidad inmediata

Tu respiración en este instante es tu mayor aliado.""",
            """El sistema nervioso no está roto - está haciendo su trabajo evolutivo:

Por millones de años, este sistema mantuvo vivos a nuestros ancestros
Hoy reacciona a emails, fechas límite y opiniones como si fueran tigres
La amígdala no distingue entre depredadores reales y amenazas modernas
Reentrenar esta respuesta es el trabajo espiritual de nuestra era
Mindfulness, respiración y terapia son formas de actualizar software ancestral"""
        ],
        "enojo": [
            """El enojo transformado conscientemente se convierte en fuerza creativa:

La misma energía que destruye puentes puede construir nuevos caminos
El fuego que quema también purifica y permite renacer desde cenizas
La indignación que paraliza puede movilizar hacia acción significativa
La frustración que envenena puede convertirse en determinación sanadora
El límite que se defiende con rabia puede protegerse después con asertividad"""
        ],
        "esperanza": [
            """La esperanza es una brújula interna que funciona incluso en la oscuridad:

• No es optimismo ciego, sino la convicción de que existen caminos por descubrir
• Se alimenta de pequeños logros y gestos de bondad hacia uno mismo  
• Es un músculo que se fortalece con cada desafío superado
• Permite ver posibilidades donde otros solo ven obstáculos

La esperanza realista es el combustible del cambio significativo.""",

            """Desde Camus, Sartre y Frankl:

ESPERANZA ABSURDA (Camus): 
- Abrazar el sinsentido sin ilusiones
- Encontrar dignidad en la lucha misma
- Sonreír mientras se empuja la roca

ESPERANZA COMO PROYECTO (Sartre):
- Crearse a uno mismo desde la libertad
- El hombre como posibilidad inacabada
- Actuar sin garantías pero con propósito

ESPERANZA TRASCENDENTE (Frankl):
- Hallar significado incluso en el sufrimiento
- Transformar el dolor en propósito
- La libertad interior como último refugio

Tres filosofías, una verdad: la esperanza es elección activa, no pasiva.""",

            """El hombre que sabe que su destino es rodar la roca es, paradójicamente, libre y esperanzado.

Sísifo nos enseña que la esperanza no está en alcanzar la cima, 
sino en encontrar dignidad en cada ascenso, significado en cada esfuerzo.

Como dice Frankl: "El hombre no solo sobrevive por instinto, sino por significado."
La esperanza es ese significado que transforma el sufrimiento en propósito.

Y Sartre añade: "El hombre está condenado a ser libre" - condenado a elegir, 
a proyectarse hacia futuros posibles, a crear esperanza donde no la hay."""
        ],
        "conflicto": [
            """Los conflictos emocionales son el terreno fértil del crecimiento:

• Indican que estás procesando experiencias complejas y multidimensionales
• Revelan la riqueza de tu mundo interior y tu capacidad para contener contradicciones
• Son oportunidades para desarrollar tolerancia a la ambigüedad emocional
• Facilitan la integración de partes aparentemente opuestas de tu ser
• Fortalecen tu capacidad para navegar la complejidad de la experiencia humana

Este conflicto no es problema a resolver, sino proceso a honrar.""",

            """Desde la psicología de la complejidad emocional:

Las emociones contradictorias activan redes cerebrales más integradas
La ambivalencia emocional correlaciona con mayor inteligencia emocional
La capacidad de contener opuestos es signo de madurez psicológica
Los conflictos emocionales bien transitados expanden tu rango de experiencia
La integración de emociones mixtas fortalece la resiliencia emocional

Estás desarrollando musculatura emocional avanzada.""",

            """Tu conflicto interno es como un río con múltiples corrientes:

Cada emoción lleva su propia verdad y su propia necesidad
No necesitas elegir una corriente sobre las otras
Puedes aprender a navegar las aguas mezcladas
La sabiduría está en honrar todas las voces internas
La integración surge del diálogo, no de la eliminación

Este es el arte de contener la complejidad humana."""
        ],
        "soledad": [
            """La soledad puede ser maestra o castigo; la diferencia está en la compañía que te ofreces.
Aprende a dialogar desde la ternura interna y verás que la soledad se vuelve fertile espacio creativo."""
        ],
        "calma": [
            "La calma no es ausencia de movimiento sino un lugar interior hacia el que puedes volver. Practicar volver es el arte."
        ]
    },

    "fragmentos": {
        "tristeza": [
            "«La herida es el lugar por donde entra la luz.» — Rumi",
            "«Quien tiene un porqué para vivir puede soportar casi cualquier cómo.» — Viktor Frankl", 
            "«La tristeza da profundidad; deja que te enseñe.» — Adaptado"
        ],
        "alegria": [
            "«De vez en cuando es bueno parar de buscar la felicidad y simplemente ser feliz.» — Guillaume Apollinaire",
            "«La alegría no está en las cosas; está en nosotros.» — Richard Wagner",
            "«Ríe y el mundo reirá contigo.» — Proverbio"
        ],
        "ansiedad": [
            "«Respira. Este momento es todo lo que tienes realmente.» — Eckhart Tolle", 
            "«La mente que se preocupa por el futuro olvida vivir el presente.» — Jon Kabat-Zinn",
            "«Un paso pequeño ahora vale más que mil planes en la cabeza.» — Adaptado"
        ],
        "enojo": [
            "«Cuando estés enojado, calla; cuando estés calmado, decide.» — Séneca",
            "«El que domina su ira domina un poderoso enemigo.» — Adaptado", 
            "«Transforma el fuego en luz para ver con claridad.» — Adaptado"
        ],
        "esperanza": [
            "«La esperanza es el oxígeno del alma en momentos de oscuridad.» — Adaptado de Desmond Tutu",
            "«Quien tiene un porqué para vivir puede soportar casi cualquier cómo.» — Viktor Frankl", 
            "«El hombre está condenado a ser libre.» — Jean-Paul Sartre",
            "«Debo imaginar a Sísifo feliz.» — Albert Camus",
            "«La libertad es lo que haces con lo que te han hecho.» — Jean-Paul Sartre"
        ],
        "soledad": [
            "«Ame su soledad y soporte con dulce melodía el dolor que ella le cause.» — Rilke",
            "«La soledad es también una forma de libertad que enseña a escucharte.» — Adaptado"
        ],
        "calma": [
            "«El silencio es una respuesta que a veces cura más que mil palabras.» — Dalai Lama", 
            "«Nada es tan malo como parece cuando se lo contempla con serenidad.» — Marco Aurelio"
        ],
        "conflicto": [
            "«El corazón humano tiene la capacidad de contener emociones contradictorias sin romperse.» — Adaptado",
            "«En el conflicto interno reside la semilla de la integración.» — Desconocido",
            "«No tengas miedo de tus contradicciones; son signo de que estás vivo.» — Adaptado", 
            "«La ambivalencia es el lenguaje del alma compleja.» — Desconocido"
        ]
    },

    "tecnicas": {
        "tristeza": [
            "💧 **Permitirse llorar**: Las lágrimas liberan hormonas del estrés y endorfinas naturales que ayudan a procesar el dolor emocional.",
            "📝 **Escritura expresiva**: 20 minutos escribiendo lo más profundo sin filtros ni juicios - permite liberar y comprender.",
            "🌳 **Baño de naturaleza**: Caminar 15 minutos en parque o zona verde, conectando conscientemente con los sentidos.",
            "🎵 **Musicoterapia emocional**: Crear playlist que acompañe tu estado actual y permita la catarsis emocional.",
            "🧘 **Meditación de autocompasión**: 10 minutos de bondad amorosa hacia ti mismo: 'Que yo esté libre de sufrimiento...'",
            "☕ **Ritual de cuidado**: Preparar una bebida caliente y hacerla atención plena durante 5 minutos.",
            "📩 **Escribe a tu yo futuro**: narrar qué te ayudaría leer en seis meses.",
            "📦 **Caja de consuelo**: recolectar objetos que te calman y tenerlos a mano.",
            "📞 **Contacto seguro**: ten una lista corta de 2-3 personas a quienes llamar cuando lo necesites.",
            "🧵 **Pequeña tarea creativa**: coser, dibujar o armar algo simple para recuperar sensación de logro."
        ],
        "alegria": [
            "🌟 **Multiplicar alegría**: Compartir tu estado con alguien que aprecies - la alegría crece al ser compartida.",
            "📸 **Fotografía mental**: Crear imagen mental vívida de este momento para memoria futura en días difíciles.", 
            "🎉 **Ritual de celebración**: Hacer algo especial para honrar este estado (comida favorita, actividad placentera).",
            "💝 **Acto de bondad**: Usar tu energía positiva para hacer algo bueno por otro - efecto multiplicador garantizado.",
            "📓 **Diario de gratitud**: Anotar 3 cosas específicas que generan esta alegría para reforzar patrones positivos.",
            "🎈 **Regala una sonrisa**: iniciar con un gesto pequeño para contagiar bienestar.",
            "🎵 **Lista de triunfo**: escribe 5 cosas que lograste este mes y léelas en voz alta.",
            "🧩 **Proyecta tu alegría**: planifica una pequeña actividad que celebre esta sensación.",
            "🍽️ **Comida ritual**: preparar un plato que te guste conscientemente como acto de celebración.",
            "📣 **Compartir positivo**: enviar un mensaje de agradecimiento a alguien que formó parte de tu alegría."
        ],
        "ansiedad": [
            "🌬️ **Respiración 4-7-8**: Inhala 4 segundos, mantén 7, exhala 8. Repite 4 ciclos - activa sistema parasimpático.",
            "🎯 **Anclaje sensorial**: 5 cosas que ves, 4 que tocas, 3 que oyes, 2 que hueles, 1 que saboreas - reconecta con presente.",
            "⏰ **Técnica 5-5-5**: ¿Importará en 5 días? ¿5 meses? ¿5 años? Esto da perspectiva y reduce catastrófización.",
            "🛑 **Parada de pensamiento**: Decir 'BASTA' en voz alta cuando rumiación se dispara - interrumpe ciclo ansioso.", 
            "🏃 **Liberación física**: 10 minutos de ejercicio intenso para metabolizar cortisol y adrenalina acumulados.",
            "🗒️ **Lista 'pequeños pasos'**: escribir tres acciones posibles y elegir la más simple.",
            "⏳ **Caja de tiempo**: dedicar 20 minutos a preocuparte (timer) y luego seguir con otra actividad.",
            "📦 **Desglosar problema**: dividir en pasos concretos para reducir abrumo.",
            "🧸 **Objeto ancla**: tocar un objeto cálido o texturado para calmar el sistema.",
            "📚 **Lectura corta**: leer un texto breve y amable para distraer la mente no productiva."
        ],
        "enojo": [
            "💥 **Descarga física segura**: Golpear almohada, hacer ejercicio intenso, gritar en lugar privado - libera energía acumulada.",
            "🕒 **Regla 10 minutos**: Esperar 10 minutos antes de actuar o hablar - permite que amígdala se calme y corteza prefrontal actúe.",
            "🎨 **Expresión creativa**: Dibujar, escribir, bailar la rabia hasta transformarla en algo constructivo.",
            "📋 **Análisis de necesidades**: ¿Qué necesidad hay detrás de este enojo? Escribirla claramente para entender origen.",
            "🔄 **Reencuadre cognitivo**: ¿Cómo vería esta situación mi 'yo futuro' más sabio? Cambia perspectiva inmediatamente.",
            "🛠️ **Acción constructiva**: convertir la energía en una tarea concreta de mejora.",
            "📐 **Establecer límites claros**: redactar una frase asertiva para futuras interacciones.",
            "🧭 **Mapa de ira**: identificar desencadenantes y patrones para anticiparlos.",
            "🧊 **Técnica de enfriamiento**: beber agua fría o abrir una ventana para bajar la intensidad física.",
            "🎭 **Role-play seguro**: ensayar respuesta con muñeco o en la mente antes de hablar."
        ],
        "esperanza": [
            "🎯 **Visualización de futuro deseado**: 10 minutos imaginando detalladamente cómo quieres que sean las cosas.",
            "📈 **Lista de pequeños logros**: Anota cada progreso, por mínimo que sea.",
            "🌱 **Metas escalonadas**: Divide objetivos grandes en pasos alcanzables de 15 minutos.", 
            "🪨 **Práctica sísifa**: Encuentra significado en tareas repetitivas o desafiantes.",
            "💫 **Ejercicio de proyección existencial**: ¿Qué versión futura de ti merece tu esperanza actual?",
            "📝 **Diario de sentido**: Cada noche escribe: 'Hoy encontré significado en...'",
            "🎭 **Role-play filosófico**: Actúa como si fueras Sísifo sonriendo con su roca"
        ],
        "conflicto": [
            "🎭 **Diálogo de partes internas**: Escribe un diálogo donde cada emoción tenga voz y pueda expresar su necesidad.",
            "🌈 **Mapeo emocional múltiple**: Dibuja un mapa con todas tus emociones actuales y cómo se relacionan entre sí.",
            "⚖️ **Técnica de la balanza**: Para cada emoción conflictiva, identifica qué te da y qué te quita.",
            "🕊️ **Meditación de aceptación múltiple**: 10 minutos aceptando conscientemente todas las emociones sin juzgar ninguna.", 
            "📖 **Narrativa integradora**: Escribe una historia que incluya todas tus emociones como personajes que colaboran.",
            "🎨 **Expresión artística mixta**: Usa diferentes colores/texturas para representar cada emoción en una misma obra.",
            "🧩 **Técnica del rompecabezas**: Visualiza cada emoción como una pieza que contribuye al panorama completo."
        ]
    },

    "citas": {
        "tristeza": [
            "«Las lágrimas derramadas son amargas, pero más amargas son las que no se derraman.» - Proverbio irlandés",
            "«La herida es el lugar por donde entra la luz.» - Rumi", 
            "«No hay nada más valiente que llorar cuando el alma lo necesita.» - Anónimo",
            "«La tristeza da profundidad. La felicidad, altura. La tristeza da raíces. La felicidad, ramas.» - Rabindranath Tagore",
            "«El dolor es inevitable; el sufrimiento es opcional.» - Buda",
            "«No hay noche que dure para siempre.» - Anónimo", 
            "«En las cenizas también habita la promesa de la llama.» - Adaptado"
        ],
        "alegria": [
            "«La felicidad no es algo hecho. Viene de tus propias acciones.» - Dalai Lama",
            "«Disfruta de los pequeños momentos, porque en realidad son los grandes.» - Desconocido", 
            "«La alegría es la piedra filosofal que todo lo convierte en oro.» - Benjamin Franklin",
            "«La felicidad es interior, no exterior; por lo tanto, no depende de lo que tenemos, sino de lo que somos.» - Henry Van Dyke",
            "«La alegría compartida es doble felicidad.» - Proverbio",
            "«El optimismo es la fe que conduce al logro.» - Helen Keller"
        ],
        "ansiedad": [
            "«La calma no llega cuando el mundo se detiene, sino cuando decides respirar.» - Desconocido", 
            "«No creas todo lo que piensas.» - Allan Lokos",
            "«La ansiedad es el vértigo de la libertad.» - Søren Kierkegaard",
            "«Hoy me evitaré dos males: la ansiedad por el futuro y los lamentos por el pasado.» - Marco Aurelio", 
            "«No dejes que la imaginación te robe la paz del presente.» - Adaptado",
            "«Respira: la vida ocurre en el aliento siguiente.» - Adaptado"
        ],
        "enojo": [
            "«El enojo es un ácido que puede hacer más daño al recipiente en la que se almacena que a cualquier cosa sobre la que se vierte.» - Séneca",
            "«Guardar enfado es como tomar veneno y esperar que otra persona muera.» - Buda", 
            "«La mejor cura para la ira es la demora.» - Séneca",
            "«El hombre superior comprende la equidad; el hombre inferior comprende el interés.» - Confucio",
            "«Aprende a escuchar la ira antes de responderla.» - Adaptado", 
            "«La serenidad se gana cuando no reaccionas al primer impulso.» - Adaptado"
        ],
        "esperanza": [
            "«La esperanza es ser capaz de ver que hay luz a pesar de toda la oscuridad.» - Desmond Tutu",
            "«Mantén tus sueños vivos. Entiende que para lograr cualquier cosa requiere fe y creencia en ti mismo.» - Les Brown", 
            "«La esperanza no consiste en negar lo absurdo, sino en abrazarlo sin temor.» - Albert Camus",
            "«Esperar lo imposible es el modo humano de no rendirse ante la nada.» - Albert Camus", 
            "«El absurdo no destruja la esperanza; la redefine sin ilusiones.» - Albert Camus",
            "«La esperanza nace cuando el hombre se descubre como posibilidad inacabada.» - Jean-Paul Sartre",
            "«El hombre que actúa sin garantías encarna la esperanza de la existencia.» - Jean-Paul Sartre", 
            "«La esperanza no es refugio, es tarea.» - Jean-Paul Sartre",
            "«Quien tiene un porqué puede soportar casi cualquier cómo.» - Viktor Frankl",
            "«Incluso en el infierno humano puede hallarse una chispa de sentido.» - Viktor Frankl", 
            "«El hombre que sufre con propósito es invencible.» - Viktor Frankl"
        ],
        "conflicto": [
            "«La capacidad de contener emociones contradictorias es signo de fortaleza emocional.» — Daniel Goleman", 
            "«El conflicto interno no es patología, es el terreno del crecimiento.» — Carl Jung",
            "«En la tensión de los opuestos encontramos nuestra profundidad.» — Adaptado",
            "«La sabiduría comienza cuando aceptamos nuestra complejidad interna.» — Desconocido"
        ]
    },

    "haikus": {
        "tristeza": [
            "Llueve en el alma,\npero el río sigue,\ncantando despacio.",
            "Noche en el pecho,\nla luna sigue brillando,\ntras la tormenta.", 
            "Hojas que caen,\nraíces que se afirman,\nrenacer vendrá.",
            "Silencio y sal,\nla luna recoge todo,\nvuelve la calma."
        ],
        "alegria": [
            "Brilla tu risa,\ncomo un sol sin permiso,\nrompiendo el invierno.",
            "Alegría pura,\nflorece sin razones,\nregalo del ser.", 
            "Rayo de luz clara,\nen el jardín del alma,\nflorece la paz.",
            "Manos al cielo,\nun pequeño milagro,\ncorazón canta."
        ],
        "ansiedad": [
            "Mil pensamientos,\nvuelan sin dirección,\nvuelve a tu centro.",
            "Mente en tormenta,\nrespiración es ancla,\npaz en el ahora.", 
            "Olas de inquietud,\nla playa sigue firme,\nrespira y confía.",
            "Pulso apremia,\nun respiro lo calma,\nla orilla espera."
        ],
        "enojo": [
            "Fuego que grita,\nlimpia los cimientos,\nnace nueva calma.",
            "Tormenta interna,\npurifica la tierra,\ncrece lo nuevo.", 
            "Furia que arde,\nforja herramientas nuevas,\ncambios que sanan.",
            "Grito contenido,\nresuena y se convierte\nen voz que construye."
        ],
        "esperanza": [
            "Amanecer llega,\naún en noche cerrada,\nla luz siempre gana.",
            "Semilla en tierra,\nconfía en tiempo y sol,\nflor nacerá.", 
            "Roca que sube,\nsonrisa en la pendiente,\ncorazón libre.",
            "Hombre que elige,\ncrea su propio camino,\nesperanza nace.",
            "Dolor con sentido,\nse transforma en fuerza pura,\nalma que resiste.", 
            "Vacío grita,\npero el ser se proyecta,\nfuturo nace.",
            "Sin garantías,\nactúa con valor puro,\nesperanza vive."
        ],
        "conflicto": [
            "Dos corrientes,\nun mismo río fluye,\nmar al final.",
            "Lluvia y sol,\nel arcoíris nace,\nde opuestos unidos.", 
            "Voces internas,\ncoro que se encuentra,\nmelodía nueva.",
            "Invierno y verano,\nen un solo día,\nriqueza del ser."
        ],
        "universal": [
            "Siente y respira,\nTodo se mueve,\ntodo renace.",
            "Emoción fluye,\ncomo río eterno,\nsiempre cambiante.", 
            "Aquí y ahora,\núnico momento real,\nrespira profundo."
        ]
    }
}

# ==================== SISTEMA DE ARCHIVOS MEJORADO ====================
class SistemaArchivos:
    def __init__(self):
        self.directorio = Path("datos_emocionales")
        self.directorio.mkdir(exist_ok=True)
        self.historial_file = self.directorio / "historial_emocional.json"
        self.estadisticas_file = self.directorio / "estadisticas_avanzadas.json"
        self.config_file = self.directorio / "configuracion_usuario.json"
        
    def guardar_historial(self, datos):
        historial = self.cargar_historial()
        historial.append(datos)
        
        # Auto-limpieza si excede máximo
        if len(historial) > CONFIG["sistema"]["max_historial"]:
            historial = historial[-CONFIG["sistema"]["max_historial"]:]
            
        with open(self.historial_file, 'w', encoding='utf-8') as f:
            json.dump(historial, f, ensure_ascii=False, indent=2)
            
    def cargar_historial(self):
        if not self.historial_file.exists():
            return []
        try:
            with open(self.historial_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
            
    def guardar_estadisticas(self, estadisticas):
        with open(self.estadisticas_file, 'w', encoding='utf-8') as f:
            json.dump(estadisticas, f, ensure_ascii=False, indent=2)
            
    def cargar_estadisticas(self):
        if not self.estadisticas_file.exists():
            return {}
        try:
            with open(self.estadisticas_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

# ==================== MOTOR EMOCIONAL COMPLETO ====================
class MotorEmocional:
    def __init__(self):
        self.archivos = SistemaArchivos()
        self.emociones_base = ["tristeza", "alegria", "ansiedad", "enojo", "gratitud", "esperanza", "confusion", "paz", "motivacion"]
        
        # Precompilar patrones regex para búsqueda rápida
        self._compilar_patrones()
        
    def _compilar_patrones(self):
        """Precompila patrones regex para búsqueda ultra rápida"""
        palabras_emociones = {
            "tristeza": ["triste", "tristeza", "deprimido", "desanimado", "melancol", "llorar", "solo", "vacío", "desesperanzado", "apenado"],
            "alegria": ["feliz", "alegre", "contento", "emocionado", "optimista", "increíble", "maravilloso", "genial", "eufórico", "radiante"],
            "ansiedad": ["ansioso", "ansiedad", "nervioso", "preocupado", "estresado", "miedo", "agobiado", "pánico", "tenso", "inquieto"],
            "enojo": ["enojado", "enojo", "enfadado", "molesto", "frustrado", "rabia", "furioso", "irritado", "indignado", "colérico"],
            "esperanza": ["esperanza", "esperanzado", "optimista", "confío", "fe", "creer", "confianza", "posibilidad", "futuro", "sentido", "propósito", "resistir", "renacer", "posible", "horizonte", "amanecer", "florecer", "creer", "confiar", "proyecto", "libertad", "elección", "significado"]
        }
        
        # Compilar patrones regex una sola vez
        self.patrones_emociones = {}
        for emocion, palabras in palabras_emociones.items():
            # Crear patrón que busque cualquiera de las palabras
            patron = r'\b(?:' + '|'.join(palabras) + r')\b'
            self.patrones_emociones[emocion] = re.compile(patron, re.IGNORECASE)
            
        # Patrones de negación
        self.patron_negacion = re.compile(r'\b(?:no estoy|no me siento|no estoy sintiendo)\b', re.IGNORECASE)
        
    def analizar_texto_avanzado(self, texto):
        """ANÁLISIS MEJORADO: Detección múltiple de emociones y conflictos"""
        texto_limpio = self._limpiar_texto_avanzado(texto)
        
        # 1. Análisis por palabras clave optimizado con regex (múltiple)
        emociones_keywords = self._analizar_multiple_por_palabras(texto_limpio)
        if emociones_keywords:
            emocion_principal, tipo_caso = self._determinar_caso_complejidad(emociones_keywords, {e: 0.7 for e in emociones_keywords})
            return emocion_principal, 0.75, "keywords_multiple", emociones_keywords, tipo_caso
            
        # 2. Análisis de sentimiento básico
        emocion_sentimiento = self._analizar_sentimiento(texto_limpio)
        if emocion_sentimiento:
            return emocion_sentimiento, 0.6, "sentimiento", [emocion_sentimiento], "simple"
            
        return "indefinida", 0.5, "basico", ["indefinida"], "simple"
    
    def _analizar_multiple_por_palabras(self, texto):
        """Detección múltiple por palabras clave"""
        if self.patron_negacion.search(texto):
            return []
            
        emociones_detectadas = []
        for emocion, patron in self.patrones_emociones.items():
            if patron.search(texto):
                emociones_detectadas.append(emocion)
                
        return emociones_detectadas
    
    def _determinar_caso_complejidad(self, emociones, confianzas):
        """Determina si es caso simple o complejo con conflicto"""
        if not emociones or len(emociones) == 0:
            return "indefinida", "simple"
            
        if len(emociones) == 1:
            return emociones[0], "simple"
        
        # DETECCIÓN DE CONFLICTOS EMOCIONALES
        emociones_principales = emociones[:2]
        confianza_principal = 0.7
        confianza_secundaria = 0.6
        
        # Detectar si hay conflicto entre emociones opuestas
        conflictos_detectados = self._detectar_conflictos(emociones_principales)
        
        if conflictos_detectados and confianza_secundaria >= CONFIG["ia"]["umbral_conflicto"]:
            return "conflicto", "complejo"
        else:
            return emociones_principales[0], "multiple"
    
    def _detectar_conflictos(self, emociones):
        """Detecta conflictos entre emociones opuestas"""
        pares_opuestos = [
            {"tristeza", "alegria"},
            {"ansiedad", "paz"},
            {"enojo", "calma"},
            {"miedo", "esperanza"},
            {"desesperanza", "esperanza"}
        ]
        
        emociones_set = set(emociones)
        
        for par in pares_opuestos:
            if par.issubset(emociones_set):
                return True
                
        return False
        
    def _analizar_sentimiento(self, texto):
        try:
            # Análisis básico de sentimiento
            palabras_positivas = ["bien", "feliz", "contento", "genial", "maravilloso", "increíble", "optimista"]
            palabras_negativas = ["mal", "triste", "deprimido", "enojado", "ansioso", "preocupado", "estresado"]
            
            conteo_positivo = sum(1 for palabra in palabras_positivas if palabra in texto.lower())
            conteo_negativo = sum(1 for palabra in palabras_negativas if palabra in texto.lower())
            
            if conteo_positivo > conteo_negativo:
                return "alegria"
            elif conteo_negativo > conteo_positivo:
                return "tristeza"
        except:
            pass
            
        return None
        
    def _limpiar_texto_avanzado(self, texto):
        """Normalización lingüística avanzada"""
        # Convertir a minúsculas y limpiar espacios
        texto = texto.lower().strip()
        
        # Normalizar caracteres Unicode (eliminar tildes pero mantener ñ)
        texto = unicodedata.normalize('NFD', texto)
        texto = ''.join(c for c in texto if not unicodedata.combining(c))
        
        # Limpiar caracteres especiales pero mantener letras, números y espacios
        texto = re.sub(r'[^a-z0-9\sñ]', '', texto)
        
        return texto

# ==================== GENERADOR DE RESPUESTAS COMPLETO ====================
class GeneradorRespuestas:
    def __init__(self):
        self.motor = MotorEmocional()
        
    def generar_respuesta_completa(self, texto_usuario, emocion_principal, confianza, fuente, emociones_detectadas=None, tipo_caso="simple"):
        """Genera respuesta adaptada a casos simples vs complejos"""
        
        respuesta = {
            "timestamp": datetime.datetime.now().isoformat(),
            "emocion_principal": emocion_principal,
            "confianza": confianza,
            "fuente_deteccion": fuente,
            "tipo_caso": tipo_caso,
            "emociones_detectadas": emociones_detectadas or [emocion_principal],
            "componentes": {}
        }
        
        try:
            # RESPUESTAS DIFERENCIADAS SEGÚN COMPLEJIDAD
            if tipo_caso == "complejo":
                respuesta["componentes"] = self._generar_respuesta_compleja(texto_usuario, emociones_detectadas)
            elif tipo_caso == "multiple":
                respuesta["componentes"] = self._generar_respuesta_multiple(texto_usuario, emociones_detectadas)
            else:
                respuesta["componentes"] = self._generar_respuesta_simple(texto_usuario, emocion_principal)
                
        except Exception as e:
            # Respuesta de emergencia
            respuesta["componentes"] = {
                "validacion": "Estoy aquí contigo en este momento complejo.",
                "reflexion": "Todos los sentimientos merecen ser escuchados con compasión.",
                "cita": "«Lo esencial es invisible a los ojos.» - El Principito",
                "tecnicas": ["🌬️ Respiración consciente para calmar el sistema"],
                "haiku": "En este momento,\nrespira profundamente,\nla calma regresa.",
                "fragmento_diario": f'"{texto_usuario[:50]}..." — Un momento de honestidad emocional.'
            }
            
        return respuesta

    def _generar_respuesta_simple(self, texto_usuario, emocion):
        """Respuesta para casos de una sola emoción"""
        componentes = {}
        
        if emocion in self.motor.emociones_base:
            # 1. Validación emocional
            componentes["validacion"] = random.choice(
                SABIDURIA["validacion"].get(emocion, SABIDURIA["validacion"]["universal"])
            )
            
            # 2. Reflexión profunda
            if emocion in SABIDURIA["reflexion"]:
                componentes["reflexion"] = random.choice(SABIDURIA["reflexion"][emocion])
            else:
                componentes["reflexion"] = "Reflexión no disponible para esta emoción."
            
            # 3. Técnicas específicas
            if CONFIG["usuario"]["preferencias"]["incluir_tecnicas"]:
                if emocion in SABIDURIA["tecnicas"]:
                    componentes["tecnicas"] = random.sample(SABIDURIA["tecnicas"][emocion], min(3, len(SABIDURIA["tecnicas"][emocion])))
                else:
                    componentes["tecnicas"] = ["Técnicas no disponibles para esta emoción."]
                    
            # 4. Cita inspiradora
            if emocion in SABIDURIA["citas"]:
                componentes["cita"] = random.choice(SABIDURIA["citas"][emocion])
            else:
                componentes["cita"] = "Cita no disponible para esta emoción."
            
            # 5. Fragmento diario poético
            componentes["fragmento_diario"] = self._generar_fragmento_diario(texto_usuario, emocion)
            
            # 6. Haiku emocional
            if CONFIG["usuario"]["preferencias"]["incluir_poesia"]:
                if emocion in SABIDURIA["haikus"]:
                    componentes["haiku"] = random.choice(SABIDURIA["haikus"][emocion])
                else:
                    componentes["haiku"] = random.choice(SABIDURIA["haikus"]["universal"])
                    
        else:
            # Respuesta para emociones indefinidas
            componentes = self._generar_respuesta_universal(texto_usuario)
            
        return componentes

    def _generar_respuesta_multiple(self, texto_usuario, emociones):
        """Respuesta para múltiples emociones sin conflicto"""
        emocion_principal = emociones[0] if isinstance(emociones, list) else list(emociones.keys())[0]
        
        componentes = {
            "validacion": f"Estás experimentando una mezcla de emociones: {', '.join(emociones[:3])}. Todas son válidas y merecen atención.",
            "reflexion": self._generar_reflexion_multiple(emociones),
            "tecnicas": self._generar_tecnicas_multiple(emociones),
            "cita": random.choice(SABIDURIA["citas"].get("universal", SABIDURIA["citas"]["alegria"])),
            "fragmento_diario": self._generar_fragmento_multiple(texto_usuario, emociones),
            "haiku": self._generar_haiku_multiple(emociones)
        }
        
        return componentes

    def _generar_respuesta_compleja(self, texto_usuario, emociones):
        """Respuesta para conflictos emocionales"""
        componentes = {
            "validacion": random.choice(SABIDURIA["validacion"]["conflicto"]),
            "reflexion": random.choice(SABIDURIA["reflexion"]["conflicto"]),
            "tecnicas": random.sample(SABIDURIA["tecnicas"]["conflicto"], min(3, len(SABIDURIA["tecnicas"]["conflicto"]))),
            "cita": random.choice(SABIDURIA["citas"]["conflicto"]),
            "fragmento_diario": self._generar_fragmento_conflicto(texto_usuario, emociones),
            "haiku": random.choice(SABIDURIA["haikus"]["conflicto"])
        }
        
        return componentes

    def _generar_reflexion_multiple(self, emociones):
        """Reflexión para múltiples emociones"""
        base = "Experimentar múltiples emociones simultáneamente es signo de un mundo interior rico y complejo. "
        
        if "alegria" in emociones and "tristeza" in emociones:
            base += "La alegría y la tristeza pueden coexistir, mostrando tu capacidad para contener la plenitud de la experiencia humana."
        elif "enojo" in emociones and "esperanza" in emociones:
            base += "El enojo te muestra lo que importa, la esperanza te guía hacia el cambio posible."
        else:
            base += "Cada emoción aporta su propia sabiduría al conjunto de tu experiencia."
            
        return base

    def _generar_tecnicas_multiple(self, emociones):
        """Técnicas para múltiples emociones"""
        tecnicas = []
        
        # Tomar una técnica de cada emoción detectada (máximo 3)
        for emocion in emociones[:3]:
            if emocion in SABIDURIA["tecnicas"]:
                tecnicas.append(random.choice(SABIDURIA["tecnicas"][emocion]))
        
        if not tecnicas:
            tecnicas = ["🌬️ Respiración consciente para calmar el sistema", "📝 Escritura libre para explorar todas las emociones"]
            
        return tecnicas

    def _generar_fragmento_multiple(self, texto, emociones):
        """Fragmento para múltiples emociones"""
        emociones_str = ", ".join(emociones[:3])
        return f'"{texto[:60]}..." — Un momento donde conviven {emociones_str} en tu paisaje interior.'

    def _generar_fragmento_conflicto(self, texto, emociones):
        """Fragmento para conflictos emocionales"""
        emociones_opuestas = [e for e in emociones if e in ["tristeza", "alegria", "enojo", "paz", "ansiedad", "esperanza"]]
        emociones_str = " y ".join(emociones_opuestas[:2])
        return f'"{texto[:60]}..." — En la tensión entre {emociones_str} se revela tu profundidad emocional.'

    def _generar_haiku_multiple(self, emociones):
        """Haiku para múltiples emociones"""
        haikus_multiple = [
            "Múltiples voces,\nun solo corazón late,\nriqueza del ser.",
            "Colores mezclados,\nforman nuevo paisaje,\nalma que se expande.",
            "Diferentes notas,\nuna misma melodía,\ncorazón sabio."
        ]
        return random.choice(haikus_multiple)

    def _generar_fragmento_diario(self, texto, emocion):
        """Genera fragmento poético para el diario"""
        fragmentos_poeticos = {
            "tristeza": [
                "En el jardín del alma, incluso la tristeza tiene sus flores nocturnas.",
                "El río de las lágrimas también alimenta la tierra del crecimiento.",
                "Bajo el peso de esta emoción, se forja la profundidad del carácter."
            ],
            "alegria": [
                "La alegría es el sol interior que ilumina hasta los rincones más oscuros.",
                "Este momento de luz se guarda en el cofre de los recuerdos que sanan.",
                "La felicidad auténtica deja huellas en el alma que el tiempo no borra."
            ],
            "ansiedad": [
                "La ansiedad es el eco de futuros que aún no deciden llegar.",
                "En el mar de la incertidumbre, cada respiración es un ancla.",
                "Las olas del miedo retroceden ante la costa firme del presente."
            ],
            "enojo": [
                "El fuego del enojo, bien dirigido, forja herramientas de cambio.",
                "En la energía de la ira duerme el poder de la transformación.",
                "Los límites que defiende la rabia son los cimientos del respeto."
            ],
            "esperanza": [
                "La esperanza es el amanecer interno que disipa las sombras del alma.",
                "Cada semilla de esperanza contiene el bosque completo de posibilidades.",
                "En el horizonte de la esperanza, los imposibles se vuelven caminos por recorrer."
            ],
            "conflicto": [
                "En el crisol del conflicto emocional se forja la sabiduría del corazón.",
                "Las emociones opuestas son los polos que generan el campo magnético del crecimiento.",
                "En la tensión entre contrarios encontramos nuestra auténtica profundidad."
            ],
            "universal": [
                "Este momento merece ser recordado con compasión.",
                "Cada emoción es un mensajero que merece ser escuchado.",
                "En la honestidad de sentir reside la verdadera fortaleza."
            ]
        }
        
        if emocion in fragmentos_poeticos:
            base = random.choice(fragmentos_poeticos[emocion])
        else:
            base = random.choice(fragmentos_poeticos["universal"])
        
        return f'"{texto[:60]}..." — {base}'

    def _generar_respuesta_universal(self, texto_usuario):
        """Respuesta cuando no se detecta emoción clara"""
        return {
            "validacion": "Todos los sentimientos son válidos, incluso cuando no tienen nombre claro.",
            "reflexion": "El simple hecho de preguntarte '¿cómo me siento?' ya es un acto profundo de autocuidado.",
            "tecnicas": [
                "🌬️ Respiración consciente: 5 ciclos de inhalación y exhalación profundas",
                "📝 Escritura libre: 5 minutos escribiendo lo primero que venga a la mente"
            ],
            "cita": "«El único camino hacia adelante es a través.» — Robert Frost",
            "fragmento_diario": f'"{texto_usuario[:50]}..." — Un momento de honestidad emocional.',
            "haiku": random.choice(SABIDURIA["haikus"]["universal"])
        }

# ==================== INTERFAZ STREAMLIT COMPLETA ====================
def inicializar_sistema():
    """Inicializa los componentes del sistema en session_state"""
    if 'motor_emocional' not in st.session_state:
        st.session_state.motor_emocional = MotorEmocional()
    if 'generador_respuestas' not in st.session_state:
        st.session_state.generador_respuestas = GeneradorRespuestas()
    if 'historial' not in st.session_state:
        st.session_state.historial = []
    if 'mostrar_estadisticas' not in st.session_state:
        st.session_state.mostrar_estadisticas = False

def mostrar_bienvenida():
    """Muestra la pantalla de bienvenida"""
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem; color: white;'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem;'>🌿 ASISTENTE EMOCIONAL ULTRA</h1>
        <p style='color: white; font-size: 1.3rem; margin: 0.5rem 0;'>v4.0 - "Detección Multi-Emocional Avanzada"</p>
        <p style='color: white; opacity: 0.9; font-size: 1.1rem;'>Hola <strong>Jorge</strong>, estoy aquí para acompañarte en tu viaje emocional</p>
    </div>
    """, unsafe_allow_html=True)

def procesar_entrada_usuario(texto):
    """Procesa la entrada del usuario y genera respuesta"""
    if not texto.strip():
        return None
        
    motor = st.session_state.motor_emocional
    generador = st.session_state.generador_respuestas
    
    emocion_principal, confianza, fuente, emociones_detectadas, tipo_caso = motor.analizar_texto_avanzado(texto)
    respuesta = generador.generar_respuesta_completa(texto, emocion_principal, confianza, fuente, emociones_detectadas, tipo_caso)
    
    # Guardar en historial
    registro = {
        "timestamp": respuesta["timestamp"],
        "texto_usuario": texto,
        "emocion_principal": emocion_principal,
        "emociones_detectadas": emociones_detectadas,
        "tipo_caso": tipo_caso,
        "confianza": confianza,
        "fuente_deteccion": fuente,
        "componentes": respuesta["componentes"]
    }
    
    st.session_state.historial.append(registro)
    motor.archivos.guardar_historial(registro)
    
    return respuesta

def mostrar_respuesta(respuesta):
    """Muestra la respuesta formateada en Streamlit"""
    componentes = respuesta["componentes"]
    emocion_principal = respuesta["emocion_principal"]
    tipo_caso = respuesta["tipo_caso"]
    emociones_detectadas = respuesta.get("emociones_detectadas", [emocion_principal])
    
    # Colores según emoción
    colores_emocion = {
        "tristeza": "#4A90E2",
        "alegria": "#F5A623", 
        "ansiedad": "#BD10E0",
        "enojo": "#D0021B",
        "esperanza": "#7ED321",
        "conflicto": "#50E3C2",
        "indefinida": "#9B9B9B"
    }
    
    color = colores_emocion.get(emocion_principal, "#9B9B9B")
    
    # Header de la respuesta
    with st.container():
        st.markdown(f"""
        <div style='background-color: {color}20; padding: 1.5rem; border-radius: 10px; border-left: 4px solid {color}; margin: 1rem 0;'>
            <h3 style='color: {color}; margin: 0;'>🎭 Análisis Emocional: {tipo_caso.upper()}</h3>
            <p style='color: {color}; margin: 0.5rem 0 0 0;'>
                <strong>Emoción principal:</strong> {emocion_principal.capitalize()} | 
                <strong>Confianza:</strong> {respuesta['confianza']:.1%} |
                <strong>Fuente:</strong> {respuesta['fuente_deteccion']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar múltiples emociones si las hay
        if len(emociones_detectadas) > 1:
            emociones_str = ", ".join([e.capitalize() for e in emociones_detectadas[:3]])
            st.info(f"🌈 **Emociones detectadas:** {emociones_str}")

    # Componentes de la respuesta en columnas
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Validación Emocional
        with st.expander("💬 Validación Emocional", expanded=True):
            st.write(componentes["validacion"])
        
        # Reflexión Profunda
        with st.expander("🧠 Reflexión Profunda", expanded=True):
            # Dividir la reflexión en líneas para mejor formato
            lineas = componentes["reflexion"].split('\n')
            for linea in lineas:
                if linea.strip():
                    if linea.startswith('•') or linea.startswith('-'):
                        st.write(f"• {linea[1:].strip()}")
                    else:
                        st.write(linea)
        
        # Fragmento para el Diario
        with st.expander("✍️ Fragmento para tu Diario", expanded=True):
            st.success(componentes["fragmento_diario"])
    
    with col2:
        # Técnicas
        with st.expander("🛠️ Técnicas de Regulación", expanded=True):
            for tecnica in componentes.get("tecnicas", []):
                st.write(f"• {tecnica}")
        
        # Cita Inspiradora
        with st.expander("📖 Cita Inspiradora", expanded=True):
            st.markdown(f"*{componentes['cita']}*")
        
        # Haiku Emocional
        if "haiku" in componentes and CONFIG["usuario"]["preferencias"]["incluir_poesia"]:
            with st.expander("🎭 Haiku Emocional", expanded=True):
                st.code(componentes["haiku"])

def mostrar_historial_completo():
    """Muestra el historial completo de conversaciones"""
    st.markdown("## 📖 Tu Historial Emocional Completo")
    
    if not st.session_state.historial:
        st.info("Aún no hay registros en tu historial emocional.")
        return
        
    # Estadísticas rápidas
    total_registros = len(st.session_state.historial)
    emociones_count = {}
    for registro in st.session_state.historial:
        emocion = registro['emocion_principal']
        emociones_count[emocion] = emociones_count.get(emocion, 0) + 1
    
    if emociones_count:
        emocion_mas_comun = max(emociones_count, key=emociones_count.get)
        st.metric("Registros totales", total_registros)
        st.metric("Emoción más común", emocion_mas_comun.capitalize())
    
    # Mostrar últimos 15 registros
    for i, registro in enumerate(reversed(st.session_state.historial[-15:]), 1):
        with st.expander(f"Conversación {i} - {registro['emocion_principal'].capitalize()} ({registro['tipo_caso']})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Tu mensaje:** {registro['texto_usuario']}")
                st.write(f"**Fragmento del diario:** {registro['componentes']['fragmento_diario']}")
                
            with col2:
                st.write(f"**Emoción:** {registro['emocion_principal']}")
                st.write(f"**Tipo de caso:** {registro['tipo_caso']}")
                st.write(f"**Confianza:** {registro['confianza']:.1%}")
                if registro['emociones_detectadas']:
                    st.write(f"**Todas las emociones:** {', '.join(registro['emociones_detectadas'])}")

def analizar_tendencias_streamlit():
    """Versión adaptada del análisis de tendencias para Streamlit"""
    archivos = SistemaArchivos()
    historial = archivos.cargar_historial()
    
    if not historial or len(historial) < 3:
        st.warning("📊 Aún no hay suficientes datos para analizar tendencias.")
        st.info("💡 Usa más la conversación emocional para generar insights valiosos.")
        return
    
    st.markdown("## 📈 Análisis Avanzado de Tendencias Emocionales")
    
    # Análisis básico
    emociones_count = {}
    complejidad_count = {}
    
    for registro in historial:
        emocion = registro.get('emocion_principal', 'indefinida')
        emociones_count[emocion] = emociones_count.get(emocion, 0) + 1
        
        tipo_caso = registro.get('tipo_caso', 'simple')
        complejidad_count[tipo_caso] = complejidad_count.get(tipo_caso, 0) + 1
    
    total_registros = len(historial)
    
    # Mostrar estadísticas en columnas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de registros", total_registros)
    
    with col2:
        emocion_principal = max(emociones_count, key=emociones_count.get)
        st.metric("Emoción principal", emocion_principal.capitalize())
    
    with col3:
        st.metric("Registros únicos", len(emociones_count))
    
    # Gráfico de distribución de emociones
    st.markdown("### 🎭 Distribución de Emociones")
    emociones_ordenadas = sorted(emociones_count.items(), key=lambda x: x[1], reverse=True)
    
    for emocion, count in emociones_ordenadas:
        porcentaje = (count / total_registros) * 100
        progress = int(porcentaje / 2)  # Barra de progreso simplificada
        barras = "█" * progress + "░" * (50 - progress)
        
        emoji = {
            "tristeza": "💧", "alegria": "✨", "ansiedad": "🌪️", 
            "enojo": "🔥", "esperanza": "🌅", "conflicto": "⚡", "indefinida": "❓"
        }.get(emocion, "🎭")
        
        st.write(f"{emoji} **{emocion.capitalize()}:** {barras} {porcentaje:.1f}% ({count} veces)")
    
    # Análisis de complejidad
    st.markdown("### 🎯 Complejidad Emocional Detectada")
    for tipo_caso, count in complejidad_count.items():
        porcentaje = (count / total_registros) * 100
        icono = {
            "simple": "🎯",
            "multiple": "🌈",
            "complejo": "⚡"
        }.get(tipo_caso, "❓")
        
        st.write(f"{icono} **{tipo_caso.capitalize()}:** {count} veces ({porcentaje:.1f}%)")
    
    # Recomendación personalizada
    st.markdown("### 💡 Recomendación Personalizada")
    if emocion_principal in ["tristeza", "ansiedad"]:
        st.success("""
        **Sugerencia:** Considera incorporar una práctica diaria de gratitud y mindfulness. 
        Pequeños momentos de atención plena pueden transformar tu panorama emocional.
        """)
    elif emocion_principal == "alegria":
        st.success("""
        **Sugerencia:** ¡Excelente! Aprovecha esta energía positiva para establecer nuevos hábitos 
        y proyectos que te apasionen. La alegría es un gran combustible para el crecimiento.
        """)
    else:
        st.info("""
        **Sugerencia:** Continúa explorando y registrando tus emociones. El autoconocimiento 
        emocional es un viaje continuo de descubrimiento y crecimiento personal.
        """)

def frase_del_dia_emocional():
    """Frase del día emocional"""
    todas_las_frases = []
    for grupo in SABIDURIA["validacion"].values():
        todas_las_frases.extend(grupo)
    return random.choice(todas_las_frases)

def main():
    """Función principal de Streamlit"""
    inicializar_sistema()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🌿 Asistente Emocional ULTRA")
        st.markdown("---")
        
        st.markdown("### ⚙️ Configuración")
        st.write(f"**Usuario:** {CONFIG['usuario']['nombre']}")
        st.write(f"**Edad:** {CONFIG['usuario']['edad']}")
        st.write(f"**Tono:** {CONFIG['usuario']['preferencias']['tono']}")
        
        # Frase del día
        st.markdown("---")
        st.markdown("### 🌞 Frase del Día")
        st.info(frase_del_dia_emocional())
        
        st.markdown("---")
        # Acciones rápidas
        if st.button("🧹 Limpiar Historial Temporal", use_container_width=True):
            st.session_state.historial = []
            st.rerun()
            
        if st.button("📊 Ver Análisis Avanzado", use_container_width=True):
            st.session_state.mostrar_estadisticas = True
            
        if st.button("💬 Volver al Chat", use_container_width=True):
            st.session_state.mostrar_estadisticas = False

    # Contenido principal
    mostrar_bienvenida()
    
    # Navegación principal
    if st.session_state.mostrar_estadisticas:
        analizar_tendencias_streamlit()
    else:
        # Pestañas para las diferentes funcionalidades
        tab1, tab2, tab3 = st.tabs(["💬 Conversación Emocional", "📖 Historial Completo", "ℹ️ Acerca del Sistema"])
        
        with tab1:
            st.markdown("### Comparte cómo te sientes...")
            
            # Input de chat mejorado
            texto_usuario = st.chat_input("Escribe lo que estás sintiendo en este momento...")
            
            if texto_usuario:
                # Mostrar mensaje del usuario
                with st.chat_message("user"):
                    st.write(texto_usuario)
                
                # Procesar y mostrar respuesta
                with st.chat_message("assistant"):
                    with st.spinner("🔍 Analizando tus emociones..."):
                        respuesta = procesar_entrada_usuario(texto_usuario)
                        if respuesta:
                            mostrar_respuesta(respuesta)
            
            # Sugerencias rápidas
            st.markdown("---")
            st.markdown("### 💡 ¿No sabes por dónde empezar?")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("😔 Me siento triste"):
                    st.rerun()
            with col2:
                if st.button("😊 Estoy contento"):
                    st.rerun()
            with col3:
                if st.button("😰 Siento ansiedad"):
                    st.rerun()
        
        with tab2:
            mostrar_historial_completo()
        
        with tab3:
            st.markdown("## ℹ️ Acerca del Sistema")
            st.markdown("""
            ### 🌿 Asistente Emocional ULTRA v4.0
            
            **Características principales:**
            - 🎯 **Detección Multi-Emocional Avanzada**
            - ⚡ **Identificación de Conflictos Internos**
            - 🌈 **Respuestas Diferenciadas (Simples vs Complejas)**
            - 🧠 **Manejo Profesional de Complejidad Emocional**
            - 📊 **Análisis de Tendencias y Patrones**
            
            **Tecnologías utilizadas:**
            - Motor de análisis emocional con Regex optimizado
            - Base de datos de sabiduría emocional extensa
            - Sistema de archivos persistente
            - Interfaz Streamlit moderna y responsive
            
            **Desarrollado con:** Python, Streamlit, y mucha psicología humana 💫
            """)

if __name__ == "__main__":
    main()