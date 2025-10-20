"""
Página de Constancias - Sistema JII 2025
"""
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfReader, PdfWriter

# Configuración
st.set_page_config(page_title="Constancias - JII 2025", page_icon="📝", layout="wide")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "datos"
ASSETS_DIR = ROOT / "assets"
FONT_DIR = ASSETS_DIR / "fonts"
PLANTILLAS_DIR = ASSETS_DIR / "plantillas"

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

# Funciones auxiliares
@st.cache_data
def cargar_datos():
    """Carga los datos de participantes, asistencias y actividades"""
    try:
        # Debug: mostrar rutas que se están usando
        participantes_path = DATA_DIR / "participantes.csv"
        asistencias_path = DATA_DIR / "asistencias.csv"
        actividades_path = DATA_DIR / "actividades.csv"
        
        # Verificar que los archivos existen
        if not participantes_path.exists():
            st.error(f"❌ No se encuentra el archivo: {participantes_path}")
            return None, None, None
        if not asistencias_path.exists():
            st.error(f"❌ No se encuentra el archivo: {asistencias_path}")
            return None, None, None
        if not actividades_path.exists():
            st.error(f"❌ No se encuentra el archivo: {actividades_path}")
            return None, None, None
            
        participantes = pd.read_csv(participantes_path)
        asistencias = pd.read_csv(asistencias_path)
        actividades = pd.read_csv(actividades_path)
        
        # Agregar columna encuesta_completada si no existe
        if 'encuesta_completada' not in participantes.columns:
            participantes['encuesta_completada'] = False
            
        return participantes, asistencias, actividades
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {e}")
        st.error(f"📁 DATA_DIR configurado como: {DATA_DIR}")
        return None, None, None

def verificar_elegibilidad(email, participantes, asistencias):
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
    
    # Verificar participación en mundialito (necesitamos verificar en equipos_concurso.csv)
    # Por ahora, asumimos que no participó
    participo_mundialito = False
    
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
    """Guarda las respuestas de la encuesta"""
    try:
        # Crear archivo CSV de respuestas si no existe
        respuestas_file = DATA_DIR / "encuesta_respuestas.csv"
        
        # Preparar datos para guardar
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
        
        # Guardar o actualizar respuestas
        if respuestas_file.exists():
            df_existente = pd.read_csv(respuestas_file)
            # Eliminar respuestas previas del mismo participante
            df_existente = df_existente[df_existente['participante_email'].str.lower() != email.lower()]
            df_respuestas = pd.concat([df_existente, df_respuestas], ignore_index=True)
        
        df_respuestas.to_csv(respuestas_file, index=False)
        
        # Actualizar participantes.csv
        participantes_df.loc[participantes_df['email'].str.lower() == email.lower(), 'encuesta_completada'] = True
        participantes_df.to_csv(DATA_DIR / "participantes.csv", index=False)
        
        return True
    except Exception as e:
        st.error(f"Error al guardar respuestas: {e}")
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
            
            # Crear overlay con el nombre
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            
            # Configurar fuente
            try:
                can.setFont("OldStandardTT-Bold", 24)
            except:
                can.setFont("Helvetica-Bold", 24)
            
            # Nombre completo (nombres primero)
            nombre_partes = participante['nombre_completo'].split()
            if len(nombre_partes) >= 2:
                # Asumiendo formato: Apellido1 Apellido2 Nombre1 Nombre2
                nombres = ' '.join(nombre_partes[2:]) if len(nombre_partes) > 2 else nombre_partes[-1]
                apellidos = ' '.join(nombre_partes[:2]) if len(nombre_partes) > 2 else nombre_partes[0]
                nombre_completo = f"{nombres} {apellidos}"
            else:
                nombre_completo = participante['nombre_completo']
            
            # Centrar el texto (ajustar coordenadas según plantilla)
            text_width = can.stringWidth(nombre_completo, "OldStandardTT-Bold", 24)
            x = (letter[0] - text_width) / 2
            y = letter[1] / 2  # Ajustar según necesidad
            
            can.drawString(x, y, nombre_completo)
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
            
            # Nombre
            try:
                can.setFont("OldStandardTT-Bold", 24)
            except:
                can.setFont("Helvetica-Bold", 24)
            
            nombre_partes = participante['nombre_completo'].split()
            if len(nombre_partes) >= 2:
                nombres = ' '.join(nombre_partes[2:]) if len(nombre_partes) > 2 else nombre_partes[-1]
                apellidos = ' '.join(nombre_partes[:2]) if len(nombre_partes) > 2 else nombre_partes[0]
                nombre_completo = f"{nombres} {apellidos}"
            else:
                nombre_completo = participante['nombre_completo']
            
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
st.markdown("---")

# Cargar datos
participantes_df, asistencias_df, actividades_df = cargar_datos()

if participantes_df is None or asistencias_df is None or actividades_df is None:
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
    elegibilidad, error = verificar_elegibilidad(email, participantes_df, asistencias_df)
    
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
                    if st.button("📥 Descargar", key="btn_general", use_container_width=True):
                        pdf_buffer = generar_constancia_pdf(participante, 'general')
                        if pdf_buffer:
                            st.download_button(
                                label="💾 Guardar PDF",
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
                    if st.button("📥 Descargar", key="btn_workshop", use_container_width=True):
                        pdf_buffer = generar_constancia_pdf(participante, 'workshop')
                        if pdf_buffer:
                            st.download_button(
                                label="💾 Guardar PDF",
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
                    if st.button("📥 Descargar", key="btn_mundialito", use_container_width=True):
                        pdf_buffer = generar_constancia_pdf(participante, 'mundialito')
                        if pdf_buffer:
                            st.download_button(
                                label="💾 Guardar PDF",
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
