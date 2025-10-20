import streamlit as st
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.utils.pdf_generator import PDFGenerator

def render_constancias_page():
    st.header("📜 Obtener Constancias")
    
    data_handler = st.session_state.data_handler
    
    # Inicializar estado de sesión
    if 'email_verified' not in st.session_state:
        st.session_state.email_verified = False
    if 'participante_data' not in st.session_state:
        st.session_state.participante_data = None
    if 'survey_completed' not in st.session_state:
        st.session_state.survey_completed = False
    
    # Paso 1: Verificación de correo
    if not st.session_state.email_verified:
        render_email_verification(data_handler)
    
    # Paso 2: Mostrar elegibilidad y encuesta
    elif not st.session_state.survey_completed:
        render_eligibility_and_survey(data_handler)
    
    # Paso 3: Generar y descargar constancias
    else:
        render_download_section(data_handler)


def render_email_verification(data_handler):
    st.subheader("Paso 1: Verificación de Identidad")
    
    st.info("Por favor, ingresa tu correo electrónico registrado para verificar tu elegibilidad.")
    
    email = st.text_input(
        "Correo Electrónico",
        placeholder="ejemplo@correo.com",
        key="email_input"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        verificar_btn = st.button("🔍 Verificar Elegibilidad", use_container_width=True)
    
    if verificar_btn:
        if not email:
            st.error("Por favor ingresa tu correo electrónico.")
            return
        
        with st.spinner("Verificando información..."):
            elegibilidad = data_handler.check_eligibility(email)
            
            if not elegibilidad['found']:
                st.error(f"❌ {elegibilidad['message']}")
                st.info("Verifica que hayas ingresado el correo correcto con el que te registraste.")
            else:
                st.session_state.email_verified = True
                st.session_state.participante_data = elegibilidad
                st.rerun()


def render_eligibility_and_survey(data_handler):
    elegibilidad = st.session_state.participante_data
    participante = elegibilidad['participante']
    
    st.success(f"✅ ¡Bienvenido/a {participante['nombres']} {participante['apellidos']}!")
    
    st.subheader("Tu Estado de Elegibilidad")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Asistencias Registradas", elegibilidad['asistencias'])
        if elegibilidad['asistencias'] >= 2:
            st.success("✅ Cumple requisito")
        else:
            st.warning("⚠️ Necesitas 2 asistencias")
    
    with col2:
        st.metric("Workshop", "Sí" if elegibilidad['workshop_attended'] else "No")
        if elegibilidad['workshop_attended']:
            st.success(f"✅ {elegibilidad['workshop_name']}")
        else:
            st.info("Sin participación")
    
    with col3:
        st.metric("Mundialito", "Sí" if elegibilidad['mundialito_attended'] else "No")
        if elegibilidad['mundialito_attended']:
            st.success("✅ Participó")
        else:
            st.info("Sin participación")
    
    st.markdown("---")
    
    # Mostrar constancias disponibles
    constancias = elegibilidad['constancias_disponibles']
    
    if len(constancias) == 0:
        st.warning("⚠️ No cumples con los requisitos mínimos para obtener constancias.")
        st.info("Necesitas al menos 2 asistencias registradas para la constancia de participación general.")
        return
    
    st.subheader("📋 Constancias Disponibles")
    
    for constancia in constancias:
        st.write(f"✅ {constancia['nombre']}")
    
    st.markdown("---")
    
    # Verificar si ya completó la encuesta
    if elegibilidad['encuesta_completada']:
        st.info("✅ Ya has completado la encuesta anteriormente.")
        st.session_state.survey_completed = True
        st.rerun()
    else:
        st.subheader("Paso 2: Completa la Encuesta de Satisfacción")
        st.write("Para poder descargar tus constancias, por favor completa la siguiente encuesta.")
        
        render_survey_form(data_handler, participante, elegibilidad)


def render_survey_form(data_handler, participante, elegibilidad):
    preguntas = data_handler.get_preguntas_encuesta()
    
    with st.form("encuesta_form"):
        st.markdown("### Encuesta General")
        
        respuestas = {}
        
        # Preguntas generales
        for pregunta in preguntas['general']:
            st.markdown(f"**{pregunta['texto']}**")
            
            if pregunta['tipo'] == 'calificacion_1_5':
                respuestas[pregunta['id']] = st.radio(
                    "Selecciona tu respuesta:",
                    options=[1, 2, 3, 4, 5],
                    format_func=lambda x: f"{x} - {'Muy Malo' if x==1 else 'Malo' if x==2 else 'Regular' if x==3 else 'Bueno' if x==4 else 'Excelente'}",
                    key=f"pregunta_{pregunta['id']}",
                    horizontal=True
                )
            elif pregunta['tipo'] == 'texto_corto':
                respuestas[pregunta['id']] = st.text_input(
                    "Tu respuesta:",
                    key=f"pregunta_{pregunta['id']}"
                )
            elif pregunta['tipo'] == 'texto_largo':
                respuestas[pregunta['id']] = st.text_area(
                    "Tu respuesta:",
                    key=f"pregunta_{pregunta['id']}",
                    height=100
                )
            
            st.markdown("---")
        
        # Preguntas de workshop si aplica
        if elegibilidad['workshop_attended']:
            st.markdown("### Encuesta de Workshop")
            st.info(f"Sobre el workshop: {elegibilidad['workshop_name']}")
            
            for pregunta in preguntas['workshop']:
                st.markdown(f"**{pregunta['texto']}**")
                
                if pregunta['tipo'] == 'calificacion_1_5':
                    respuestas[pregunta['id']] = st.radio(
                        "Selecciona tu respuesta:",
                        options=[1, 2, 3, 4, 5],
                        format_func=lambda x: f"{x} - {'Muy Malo' if x==1 else 'Malo' if x==2 else 'Regular' if x==3 else 'Bueno' if x==4 else 'Excelente'}",
                        key=f"pregunta_{pregunta['id']}",
                        horizontal=True
                    )
                elif pregunta['tipo'] == 'texto_largo':
                    respuestas[pregunta['id']] = st.text_area(
                        "Tu respuesta:",
                        key=f"pregunta_{pregunta['id']}",
                        height=100
                    )
                
                st.markdown("---")
        
        # Preguntas de mundialito si aplica
        if elegibilidad['mundialito_attended']:
            st.markdown("### Encuesta de Mundialito Mexicano")
            
            for pregunta in preguntas['mundialito']:
                st.markdown(f"**{pregunta['texto']}**")
                
                if pregunta['tipo'] == 'calificacion_1_5':
                    respuestas[pregunta['id']] = st.radio(
                        "Selecciona tu respuesta:",
                        options=[1, 2, 3, 4, 5],
                        format_func=lambda x: f"{x} - {'Muy Malo' if x==1 else 'Malo' if x==2 else 'Regular' if x==3 else 'Bueno' if x==4 else 'Excelente'}",
                        key=f"pregunta_{pregunta['id']}",
                        horizontal=True
                    )
                elif pregunta['tipo'] == 'texto_largo':
                    respuestas[pregunta['id']] = st.text_area(
                        "Tu respuesta:",
                        key=f"pregunta_{pregunta['id']}",
                        height=100
                    )
                
                st.markdown("---")
        
        # Botón de envío
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submitted = st.form_submit_button("📤 Enviar Encuesta", use_container_width=True)
        
        if submitted:
            # Validar que todas las preguntas requeridas estén respondidas
            preguntas_vacias = []
            for pregunta_id, respuesta in respuestas.items():
                if respuesta == "" or respuesta is None:
                    preguntas_vacias.append(pregunta_id)
            
            if len(preguntas_vacias) > 0:
                st.error("Por favor completa todas las preguntas antes de enviar.")
            else:
                with st.spinner("Guardando tus respuestas..."):
                    success = data_handler.save_survey_responses(
                        participante['id'],
                        respuestas
                    )
                    
                    if success:
                        st.success("✅ ¡Encuesta completada exitosamente!")
                        st.balloons()
                        st.session_state.survey_completed = True
                        st.rerun()
                    else:
                        st.error("Hubo un error al guardar tus respuestas. Intenta nuevamente.")


def render_download_section(data_handler):
    elegibilidad = st.session_state.participante_data
    participante = elegibilidad['participante']
    
    st.success("✅ ¡Encuesta completada! Ahora puedes descargar tus constancias.")
    
    st.subheader("Descarga tus Constancias")
    
    # Nombre completo (nombres primero)
    nombre_completo = f"{participante['nombres']} {participante['apellidos']}"
    
    st.info(f"**Nombre en constancia:** {nombre_completo}")
    
    # Inicializar generador de PDF
    pdf_generator = PDFGenerator(ROOT / "assets")
    
    constancias = elegibilidad['constancias_disponibles']
    
    st.markdown("---")
    
    for idx, constancia in enumerate(constancias):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"### {constancia['nombre']}")
            st.write(f"Tipo: {constancia['tipo'].replace('_', ' ').title()}")
        
        with col2:
            # Botón de descarga
            if st.button(f"⬇️ Descargar", key=f"download_{idx}"):
                try:
                    with st.spinner("Generando constancia..."):
                        pdf_bytes = pdf_generator.generate_constancia(
                            constancia['plantilla'],
                            nombre_completo
                        )
                        
                        filename = f"Constancia_{constancia['tipo']}_{nombre_completo.replace(' ', '_')}.pdf"
                        
                        st.download_button(
                            label="💾 Guardar PDF",
                            data=pdf_bytes,
                            file_name=filename,
                            mime="application/pdf",
                            key=f"save_{idx}"
                        )
                        
                        st.success("✅ Constancia generada correctamente")
                
                except Exception as e:
                    st.error(f"Error al generar la constancia: {str(e)}")
                    st.info("Por favor contacta al equipo técnico si el problema persiste.")
        
        st.markdown("---")
    
    # Opción para volver a empezar
    st.markdown("---")
    if st.button("🔄 Verificar otro participante"):
        st.session_state.email_verified = False
        st.session_state.participante_data = None
        st.session_state.survey_completed = False
        st.rerun()