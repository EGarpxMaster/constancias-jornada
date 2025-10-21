"""
Página de Constancias - Sistema JII 2025
"""
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import io
import time
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfReader, PdfWriter

# Importar handler de almacenamiento persistente (Supabase)
try:
    from utils.supabase_handler import SupabaseHandler
    SUPABASE_AVAILABLE = True
except:
    SUPABASE_AVAILABLE = False

# Configuración
st.set_page_config(page_title="Constancias - JII 2025", page_icon="📝", layout="wide")

# CSS personalizado con paleta de colores
st.markdown("""
<style>
    :root {
        --primary-color: #1b1c39;
        --secondary-color: #1ECECA;
        --text-color: #2d3e50;
        --light-color: #f9f9f9;
        --font-family: "Montserrat", sans-serif;
        --transition-speed: 0.3s;
    }
    
    /* Forzar tema claro */
    [data-testid="stAppViewContainer"] {
        background-color: #f9f9f9 !important;
    }
    
    [data-testid="stHeader"] {
        background-color: #f9f9f9 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
    }
    
    /* Estilos generales */
    .stApp {
        background-color: var(--light-color) !important;
        color: var(--text-color) !important;
    }
    
    /* Títulos */
    h1, h2, h3 {
        color: var(--primary-color) !important;
        font-family: var(--font-family);
    }
    
    /* Texto general */
    p, span, div, label {
        color: var(--text-color) !important;
    }
    
    /* Botones */
    .stButton > button {
        background-color: var(--secondary-color) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        transition: all var(--transition-speed) ease !important;
    }
    
    .stButton > button:hover {
        background-color: #18b3af !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 206, 202, 0.3);
    }
    
    /* Botón de enviar formulario - usar paleta original */
    .stFormSubmitButton > button {
        background-color: var(--secondary-color) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all var(--transition-speed) ease !important;
        width: 100%;
    }
    
    .stFormSubmitButton > button:hover {
        background-color: #18b3af !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(30, 206, 202, 0.4);
    }
    
    /* Botones de descarga - usar paleta de colores */
    .stDownloadButton > button {
        background-color: var(--secondary-color) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        transition: all var(--transition-speed) ease !important;
    }
    
    .stDownloadButton > button:hover {
        background-color: #18b3af !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 206, 202, 0.3);
    }
    
    /* Inputs y selectbox */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stSelectbox [data-baseweb="select"] > div,
    .stSelectbox [data-baseweb="select"] input {
        border-color: var(--secondary-color) !important;
        border-radius: 8px !important;
        background-color: white !important;
        color: var(--text-color) !important;
    }
    
    /* Selectbox específico - forzar fondo blanco */
    [data-baseweb="select"] {
        background-color: white !important;
    }
    
    [data-baseweb="select"] > div {
        background-color: white !important;
        color: var(--text-color) !important;
    }
    
    /* Opciones del selectbox */
    [role="option"] {
        background-color: white !important;
        color: var(--text-color) !important;
    }
    
    [role="option"]:hover {
        background-color: rgba(30, 206, 202, 0.1) !important;
    }
    
    /* Text areas */
    .stTextArea > div > div > textarea {
        border-color: var(--secondary-color) !important;
        border-radius: 8px !important;
        background-color: white !important;
        color: var(--text-color) !important;
    }
    
    /* Success, info, warning boxes */
    .stSuccess {
        background-color: rgba(30, 206, 202, 0.1) !important;
        border-left: 4px solid var(--secondary-color) !important;
        color: var(--text-color) !important;
    }
    
    .stInfo {
        background-color: rgba(30, 206, 202, 0.08) !important;
        color: var(--text-color) !important;
    }
    
    .stWarning {
        background-color: rgba(255, 193, 7, 0.1) !important;
        color: var(--text-color) !important;
    }
    
    .stError {
        background-color: rgba(244, 67, 54, 0.1) !important;
        color: var(--text-color) !important;
    }
    
    /* Containers */
    .element-container {
        transition: all var(--transition-speed) ease;
    }
    
    /* Formularios */
    [data-testid="stForm"] {
        background-color: white !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 12px !important;
        padding: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "datos"
ASSETS_DIR = ROOT / "assets"
FONT_DIR = ASSETS_DIR / "fonts"
PLANTILLAS_DIR = ASSETS_DIR / "plantillas"
IMAGES_DIR = ASSETS_DIR / "images"

# Registrar fuente
try:
    pdfmetrics.registerFont(TTFont('OldStandardTT-Bold', str(FONT_DIR / 'OldStandardTT-Bold.ttf')))
except:
    st.warning("⚠️ No se pudo cargar la fuente OldStandardTT-Bold. Se usará la fuente predeterminada.")

# Preguntas de la encuesta
PREGUNTAS_GENERALES = [
    {"id": 1, "texto": "¿Cómo calificas la organización de la JII?", "tipo": "calificacion_1_5"},
    {"id": 2, "texto": "¿Cómo calificas los horarios de la JII?", "tipo": "calificacion_1_5"},
    {"id": 3, "texto": "¿Cómo calificas la duración de las actividades?", "tipo": "calificacion_1_5"},
    {"id": 4, "texto": "Especifica la razón principal por la que asististe a la JII:", "tipo": "texto_corto"},
    {"id": 5, "texto": "¿Cumplieron tus expectativas las actividades en las que participaste?", "tipo": "calificacion_1_5"},
    {"id": 6, "texto": "¿Los contenidos desarrollados resultaron útiles?", "tipo": "calificacion_1_5"},
    {"id": 7, "texto": "¿Qué tan relevante consideras que fue el nivel profesional de la JII?", "tipo": "calificacion_1_5"},
    {"id": 8, "texto": "¿Qué conferencia magistral te pareció la más relevante?", "tipo": "select_conferencia"},
    {"id": 10, "texto": "¿Qué actividad consideras que fue la de mayor relevancia?", "tipo": "select_tipo_actividad"},
    {"id": 11, "texto": "¿Cuáles fueron para ti los puntos fuertes de la JII? ¿Por qué?", "tipo": "texto_largo"},
    {"id": 12, "texto": "¿Qué parte te gustó menos? ¿Por qué?", "tipo": "texto_largo"},
    {"id": 13, "texto": "Propón tres temas de tu interés para la edición 2026 de la JII.", "tipo": "texto_largo"},
    {"id": 14, "texto": "¿Qué sugerencias podrías aportar para mejorar la próxima edición de la JII?", "tipo": "texto_largo"},
    {"id": 15, "texto": "En términos generales, ¿Cómo calificaría la Jornada de Ingeniería Industrial 2025?", "tipo": "calificacion_1_5"},
    {"id": 16, "texto": "Comentarios adicionales:", "tipo": "texto_largo"},
]

PREGUNTAS_WORKSHOP = [
    {"id": 17, "texto": "Valora el workshop al que asististe (1=Muy Malo, 5=Excelente)", "tipo": "calificacion_1_5"},
    {"id": 18, "texto": "Comentarios sobre el workshop", "tipo": "texto_largo"},
]

PREGUNTAS_MUNDIALITO = [
    {"id": 19, "texto": "Valora el Mundialito Mexicano", "tipo": "calificacion_1_5"},
    {"id": 20, "texto": "Comentarios sobre el Mundialito Mexicano", "tipo": "texto_largo"},
]

# Crear diccionario de preguntas para Google Sheets
PREGUNTAS_DICT = {}
for pregunta in PREGUNTAS_GENERALES + PREGUNTAS_WORKSHOP + PREGUNTAS_MUNDIALITO:
    PREGUNTAS_DICT[pregunta['id']] = pregunta['texto']

# Funciones auxiliares
@st.cache_data
def cargar_datos():
    """Carga los datos de participantes, asistencias, actividades y equipos"""
    try:
        # Debug: mostrar rutas que se están usando
        participantes_path = DATA_DIR / "participantes.csv"
        asistencias_path = DATA_DIR / "asistencias.csv"
        actividades_path = DATA_DIR / "actividades.csv"
        equipos_path = DATA_DIR / "equipos_concurso.csv"
        
        # Verificar que los archivos existen
        if not participantes_path.exists():
            st.error(f"❌ No se encuentra el archivo: {participantes_path}")
            return None, None, None, None
        if not asistencias_path.exists():
            st.error(f"❌ No se encuentra el archivo: {asistencias_path}")
            return None, None, None, None
        if not actividades_path.exists():
            st.error(f"❌ No se encuentra el archivo: {actividades_path}")
            return None, None, None, None
        if not equipos_path.exists():
            st.error(f"❌ No se encuentra el archivo: {equipos_path}")
            return None, None, None, None
            
        participantes = pd.read_csv(participantes_path)
        asistencias = pd.read_csv(asistencias_path)
        actividades = pd.read_csv(actividades_path)
        equipos = pd.read_csv(equipos_path)
        
        # Agregar columna encuesta_completada si no existe
        if 'encuesta_completada' not in participantes.columns:
            participantes['encuesta_completada'] = False
            
        return participantes, asistencias, actividades, equipos
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {e}")
        st.error(f"📁 DATA_DIR configurado como: {DATA_DIR}")
        return None, None, None, None

def verificar_elegibilidad(email, participantes, asistencias, equipos):
    """Verifica si el participante es elegible para constancias"""
    # Buscar participante
    participante = participantes[participantes['email'].str.lower() == email.lower()]
    
    if participante.empty:
        return None, "❌ No se encontró tu correo electrónico en la base de datos."
    
    participante = participante.iloc[0]
    
    # Contar asistencias
    num_asistencias = len(asistencias[asistencias['participante_email'].str.lower() == email.lower()])
    
    # Verificar participación en workshops (códigos W1-W6)
    asistencias_participante = asistencias[asistencias['participante_email'].str.lower() == email.lower()]
    participo_workshop = any(asistencias_participante['actividad_codigo'].str.startswith('W'))
    
    # Verificar participación en mundialito - buscar email en captain o cualquiera de los 5 miembros
    participo_mundialito = False
    email_lower = email.lower()
    
    # Verificar si el email aparece como capitán o miembro del equipo
    if not equipos.empty:
        es_capitan = equipos['email_capitan'].str.lower() == email_lower
        es_miembro_1 = equipos['email_miembro_1'].str.lower() == email_lower
        es_miembro_2 = equipos['email_miembro_2'].str.lower() == email_lower
        es_miembro_3 = equipos['email_miembro_3'].str.lower() == email_lower
        es_miembro_4 = equipos['email_miembro_4'].str.lower() == email_lower
        es_miembro_5 = equipos['email_miembro_5'].str.lower() == email_lower
        
        participo_mundialito = any([
            es_capitan.any(), es_miembro_1.any(), es_miembro_2.any(),
            es_miembro_3.any(), es_miembro_4.any(), es_miembro_5.any()
        ])
    
    elegibilidad = {
        'participante': participante,
        'num_asistencias': num_asistencias,
        'participo_workshop': participo_workshop,
        'participo_mundialito': participo_mundialito,
        'elegible_general': num_asistencias >= 2,
        'encuesta_completada': participante.get('encuesta_completada', False)
    }
    
    return elegibilidad, None

def guardar_respuestas_encuesta(email, respuestas, participantes_df):
    """Guarda las respuestas de la encuesta en Supabase y como respaldo en CSV"""
    try:
        # Obtener nombre completo del participante
        participante = participantes_df[participantes_df['email'].str.lower() == email.lower()]
        if participante.empty:
            st.error("No se encontró el participante")
            return False
        nombre_completo = participante.iloc[0]['nombre_completo']
        
        # 1. Intentar guardar en Supabase (almacenamiento persistente)
        cloud_storage_success = False
        
        if SUPABASE_AVAILABLE:
            try:
                supabase_handler = SupabaseHandler()
                supabase_handler.guardar_respuestas(email, nombre_completo, respuestas, PREGUNTAS_DICT)
                cloud_storage_success = True
                st.success("✅ Respuestas guardadas")
            except Exception as e:
                st.warning(f"⚠️ Base de datos no disponible: {str(e)[:80]}...")
        
        # Si Supabase no funcionó, mostrar advertencia
        if not cloud_storage_success:
            st.warning("⚠️ Almacenamiento en la nube no configurado")
            st.info("💡 Las respuestas se guardarán solo localmente. Configura Supabase para almacenamiento persistente. Ver OPCION_SIMPLE_SUPABASE.md")
        
        # 2. Guardar en CSV local como respaldo (siempre)
        respuestas_file = DATA_DIR / "encuesta_respuestas.csv"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        respuestas_data = []
        
        for pregunta_id, respuesta in respuestas.items():
            respuestas_data.append({
                'participante_email': email,
                'pregunta_id': pregunta_id,
                'respuesta': respuesta,
                'fecha': timestamp
            })
        
        df_respuestas = pd.DataFrame(respuestas_data)
        
        # Guardar o actualizar respuestas en CSV
        if respuestas_file.exists():
            df_existente = pd.read_csv(respuestas_file)
            if not df_existente.empty and 'participante_email' in df_existente.columns:
                df_existente = df_existente[df_existente['participante_email'].str.lower() != email.lower()]
                df_respuestas = pd.concat([df_existente, df_respuestas], ignore_index=True)
        
        df_respuestas.to_csv(respuestas_file, index=False)
        
        # 3. Actualizar participantes.csv
        participantes_df.loc[participantes_df['email'].str.lower() == email.lower(), 'encuesta_completada'] = True
        participantes_df.to_csv(DATA_DIR / "participantes.csv", index=False)
        
        if not cloud_storage_success:
            st.info("💾 Respuestas guardadas localmente como respaldo.")
        
        return True
    except Exception as e:
        st.error(f"❌ Error al guardar respuestas: {e}")
        return False

def generar_constancia_pdf(participante, tipo_constancia):
    """Genera una constancia en PDF"""
    buffer = io.BytesIO()
    
    # Determinar qué plantilla usar
    plantillas_map = {
        'general': 'Participacion_general.pdf',
        'workshop': f'W{participante.get("workshop_numero", "1")}.pdf',
        'mundialito': 'Constancia_mundialito.pdf'
    }
    
    plantilla_path = PLANTILLAS_DIR / plantillas_map.get(tipo_constancia, 'Participacion_general.pdf')
    
    try:
        if plantilla_path.exists():
            # Usar plantilla existente
            pdf_reader = PdfReader(str(plantilla_path))
            pdf_writer = PdfWriter()
            
            # Obtener dimensiones de la página de la plantilla
            page = pdf_reader.pages[0]
            media_box = page.mediabox
            page_width = float(media_box.width)
            page_height = float(media_box.height)
            
            # Crear overlay con el nombre usando las dimensiones correctas de la plantilla
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=(page_width, page_height))
            
            # Configurar fuente con tamaño más grande
            font_size = 32
            try:
                can.setFont("OldStandardTT-Bold", font_size)
            except:
                can.setFont("Helvetica-Bold", font_size)
            
            # Configurar color del texto: rgba(4, 68, 153) -> RGB en escala 0-1
            can.setFillColorRGB(4/255, 68/255, 153/255)
            
            # Usar el nombre completo tal como está en el CSV (ya está en formato correcto)
            nombre_completo = participante['nombre_completo']
            
            # Centrar el texto horizontalmente usando drawCentredString
            # La posición X será el centro de la página automáticamente
            x_center = page_width / 2
            
            # Posición vertical: aproximadamente en el centro vertical de la plantilla
            # Para una plantilla horizontal de ~612pt de alto, el centro está alrededor de 306pt
            y = page_height / 1.80
            
            # Usar drawCentredString para centrado automático
            can.drawCentredString(x_center, y, nombre_completo)
            can.save()
            
            # Combinar
            packet.seek(0)
            overlay_pdf = PdfReader(packet)
            page = pdf_reader.pages[0]
            page.merge_page(overlay_pdf.pages[0])
            pdf_writer.add_page(page)
            
            # Guardar en buffer
            pdf_writer.write(buffer)
        else:
            # Crear constancia desde cero
            can = canvas.Canvas(buffer, pagesize=A4)
            width, height = A4
            
            # Título
            can.setFont("Helvetica-Bold", 28)
            can.drawCentredString(width/2, height - 100, "CONSTANCIA")
            
            # Subtítulo
            can.setFont("Helvetica", 16)
            can.drawCentredString(width/2, height - 150, "Jornada de Ingeniería Industrial 2025")
            
            # Cuerpo
            can.setFont("Helvetica", 14)
            can.drawCentredString(width/2, height - 250, "Se otorga la presente constancia a:")
            
            # Nombre con tamaño más grande
            font_size = 32
            try:
                can.setFont("OldStandardTT-Bold", font_size)
            except:
                can.setFont("Helvetica-Bold", font_size)
            
            # Usar el nombre completo en MAYÚSCULAS para homogeneidad
            nombre_completo = participante['nombre_completo'].upper()
            
            can.drawCentredString(width/2, height - 300, nombre_completo)
            
            # Descripción según tipo
            can.setFont("Helvetica", 12)
            if tipo_constancia == 'general':
                texto = "Por su destacada participación en la Jornada de Ingeniería Industrial 2025"
            elif tipo_constancia == 'workshop':
                texto = f"Por su participación en el Workshop de la Jornada de Ingeniería Industrial 2025"
            else:
                texto = "Por su participación en el Mundialito Mexicano - JII 2025"
            
            can.drawCentredString(width/2, height - 380, texto)
            
            # Fecha
            can.drawCentredString(width/2, height - 450, "Cancún, Quintana Roo - Octubre 2025")
            
            # Footer
            can.setFont("Helvetica", 10)
            can.drawCentredString(width/2, 50, "Universidad del Caribe")
            
            can.save()
    
        buffer.seek(0)
        return buffer
    
    except Exception as e:
        st.error(f"Error al generar constancia: {e}")
        return None

# Header
st.title("📝 Obtén tus Constancias")
st.markdown("**Jornada de Ingeniería Industrial 2025**")

st.markdown("---")

# Cargar datos
participantes_df, asistencias_df, actividades_df, equipos_df = cargar_datos()

if participantes_df is None or asistencias_df is None or actividades_df is None or equipos_df is None:
    st.error("No se pudieron cargar los datos. Por favor, contacta al administrador.")
    st.stop()

# Preparar listas de actividades para los selectbox
# Solo conferencias con código C1, C2, C3, etc.
conferencias = actividades_df[actividades_df['codigo'].str.match(r'^C\d+$', na=False)]['titulo'].tolist()

# Tipos de actividades genéricas
tipos_actividades = [
    "Conferencia",
    "Workshop",
    "Panel de Egresados",
    "Mundialito mexicano",
    "Conversatorio",
    "Estancia de movilidad de Posgrado"
]

# Paso 1: Verificar correo electrónico
st.header("1️⃣ Verificación de Participación")

email = st.text_input("📧 Ingresa tu correo electrónico:", placeholder="Correo electrónico")

if email:
    elegibilidad, error = verificar_elegibilidad(email, participantes_df, asistencias_df, equipos_df)
    
    if error:
        st.error(error)
    elif elegibilidad:
        participante = elegibilidad['participante']
        
        # Mostrar información del participante
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"✅ **Participante encontrado:** {participante['nombre_completo']}")
            st.info(f"📊 **Asistencias registradas:** {elegibilidad['num_asistencias']}")
        
        with col2:
            if elegibilidad['participo_workshop']:
                st.success("✅ Participaste en un Workshop")
            else:
                st.info("ℹ️ No se encontró registro de participación en Workshops")
            
            if elegibilidad['participo_mundialito']:
                st.success("✅ Participaste en el Mundialito")
            else:
                st.info("ℹ️ No se encontró registro de participación en el Mundialito")
        
        # Verificar elegibilidad
        if not elegibilidad['elegible_general']:
            st.warning(f"⚠️ Necesitas al menos 2 asistencias para obtener constancias. Actualmente tienes {elegibilidad['num_asistencias']}.")
            st.stop()
        
        st.markdown("---")
        
        # Paso 2: Encuesta
        if not elegibilidad['encuesta_completada']:
            st.header("2️⃣ Encuesta de Satisfacción")
            st.info("📋 Por favor, completa esta breve encuesta para poder generar tus constancias.")
            
            with st.form("encuesta_form"):
                respuestas = {}
                
                # Preguntas generales
                st.subheader("📊 Preguntas Generales")
                for pregunta in PREGUNTAS_GENERALES:
                    if pregunta['tipo'] == 'calificacion_1_5':
                        respuestas[pregunta['id']] = st.selectbox(
                            f"**{pregunta['texto']}**",
                            options=[1, 2, 3, 4, 5],
                            index=4,  # Valor por defecto: 5
                            key=f"preg_{pregunta['id']}"
                        )
                    elif pregunta['tipo'] == 'select_conferencia':
                        respuestas[pregunta['id']] = st.selectbox(
                            f"**{pregunta['texto']}**",
                            options=conferencias,
                            key=f"preg_{pregunta['id']}"
                        )
                    elif pregunta['tipo'] == 'select_tipo_actividad':
                        respuestas[pregunta['id']] = st.selectbox(
                            f"**{pregunta['texto']}**",
                            options=tipos_actividades,
                            key=f"preg_{pregunta['id']}"
                        )
                    elif pregunta['tipo'] == 'texto_corto':
                        respuestas[pregunta['id']] = st.text_input(
                            f"**{pregunta['texto']}**",
                            key=f"preg_{pregunta['id']}"
                        )
                    elif pregunta['tipo'] == 'texto_largo':
                        respuestas[pregunta['id']] = st.text_area(
                            f"**{pregunta['texto']}**",
                            key=f"preg_{pregunta['id']}",
                            height=100
                        )
                
                # Preguntas de workshop
                if elegibilidad['participo_workshop']:
                    st.subheader("🔧 Preguntas sobre el Workshop")
                    for pregunta in PREGUNTAS_WORKSHOP:
                        if pregunta['tipo'] == 'calificacion_1_5':
                            respuestas[pregunta['id']] = st.selectbox(
                                f"**{pregunta['texto']}**",
                                options=[1, 2, 3, 4, 5],
                                index=4,  # Valor por defecto: 5
                                key=f"preg_{pregunta['id']}"
                            )
                        elif pregunta['tipo'] == 'texto_largo':
                            respuestas[pregunta['id']] = st.text_area(
                                f"**{pregunta['texto']}**",
                                key=f"preg_{pregunta['id']}",
                                height=100
                            )
                
                # Preguntas de mundialito
                if elegibilidad['participo_mundialito']:
                    st.subheader("⚽ Preguntas sobre el Mundialito")
                    for pregunta in PREGUNTAS_MUNDIALITO:
                        if pregunta['tipo'] == 'calificacion_1_5':
                            respuestas[pregunta['id']] = st.selectbox(
                                f"**{pregunta['texto']}**",
                                options=[1, 2, 3, 4, 5],
                                index=4,  # Valor por defecto: 5
                                key=f"preg_{pregunta['id']}"
                            )
                        elif pregunta['tipo'] == 'texto_largo':
                            respuestas[pregunta['id']] = st.text_area(
                                f"**{pregunta['texto']}**",
                                key=f"preg_{pregunta['id']}",
                                height=100
                            )
                
                submitted = st.form_submit_button("✅ Enviar Encuesta", type="primary", use_container_width=True)
                
                if submitted:
                    # Validar respuestas obligatorias
                    respuestas_vacias = [p['texto'] for p in PREGUNTAS_GENERALES[:8] if not respuestas.get(p['id'])]
                    
                    if respuestas_vacias:
                        st.error("⚠️ Por favor, completa todas las preguntas obligatorias.")
                    else:
                        if guardar_respuestas_encuesta(email, respuestas, participantes_df):
                            st.success("✅ ¡Encuesta enviada exitosamente!")
                            st.balloons()
                            # Limpiar cache para forzar recarga de datos
                            cargar_datos.clear()
                            # Pequeño delay para que el usuario vea el mensaje de éxito
                            time.sleep(1)
                            st.rerun()
        
        else:
            # Paso 3: Descargar constancias
            st.header("3️⃣ Descarga tus Constancias")
            st.success("✅ Ya completaste la encuesta. ¡Gracias por tu participación!")
            
            st.markdown("### 📄 Selecciona las constancias que deseas descargar:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if elegibilidad['elegible_general']:
                    st.markdown("#### 🏆 Participación General")
                    st.info("Constancia por asistir a la JII 2025")
                    pdf_buffer = generar_constancia_pdf(participante, 'general')
                    if pdf_buffer:
                        st.download_button(
                            label="Descargar PDF",
                            data=pdf_buffer,
                            file_name=f"Constancia_JII2025_{participante['nombre_completo'].replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            key="download_general",
                            use_container_width=True
                        )
            
            with col2:
                if elegibilidad['participo_workshop']:
                    st.markdown("#### 🔧 Workshop")
                    st.info("Constancia por participar en Workshop")
                    pdf_buffer = generar_constancia_pdf(participante, 'workshop')
                    if pdf_buffer:
                        st.download_button(
                            label="Descargar PDF",
                            data=pdf_buffer,
                            file_name=f"Constancia_Workshop_JII2025_{participante['nombre_completo'].replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            key="download_workshop",
                            use_container_width=True
                        )
                else:
                    st.markdown("#### 🔧 Workshop")
                    st.warning("No elegible")
            
            with col3:
                if elegibilidad['participo_mundialito']:
                    st.markdown("#### ⚽ Mundialito")
                    st.info("Constancia por participar en Mundialito")
                    pdf_buffer = generar_constancia_pdf(participante, 'mundialito')
                    if pdf_buffer:
                        st.download_button(
                            label="Descargar PDF",
                            data=pdf_buffer,
                            file_name=f"Constancia_Mundialito_JII2025_{participante['nombre_completo'].replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            key="download_mundialito",
                            use_container_width=True
                        )
                else:
                    st.markdown("#### ⚽ Mundialito")
                    st.warning("No elegible")

# Footer
st.markdown("---")
st.info("💡 **Nota:** Las constancias se generan automáticamente con tu nombre completo y están listas para imprimir.")
