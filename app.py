"""
Aplicación Principal - Sistema de Constancias JII 2025
"""
import streamlit as st
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Constancias - JII 2025",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Directorio raíz
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "Multipage App" / "datos"
ASSETS_DIR = ROOT / "assets"

# Estilo CSS personalizado
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header principal
st.markdown('<div class="main-header">🎓 Sistema de Constancias</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Jornada de Ingeniería Industrial 2025</div>', unsafe_allow_html=True)

# Información principal
with st.container():
    st.markdown("### 📋 Bienvenido al Sistema de Constancias")
    st.write("Este sistema te permite obtener tus constancias de participación en la Jornada de Ingeniería Industrial 2025.")
    
    st.markdown("#### 📍 Para obtener tu constancia necesitas:")
    st.markdown("""
    - ✅ Haber asistido a **2 o más actividades** del evento
    - ✅ Haber participado en un **workshop** (opcional, para constancia específica)
    - ✅ Haber participado en el **Mundialito Mexicano** (opcional, para constancia específica)
    - ✅ Contestar una **breve encuesta** de satisfacción
    """)
    
    st.markdown("#### 🎯 Tipos de constancias disponibles:")
    st.markdown("""
    - 🏆 **Constancia de Participación General** - Por asistir al evento
    - 🔧 **Constancia de Workshop** - Por participar en un taller específico
    - ⚽ **Constancia del Mundialito Mexicano** - Por participar en el torneo
    """)

st.markdown("---")

# Instrucciones
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 1️⃣ Verifica tu correo
    Ingresa tu correo electrónico institucional para verificar tu participación.
    """)

with col2:
    st.markdown("""
    ### 2️⃣ Contesta la encuesta
    Responde una breve encuesta de satisfacción sobre el evento.
    """)

with col3:
    st.markdown("""
    ### 3️⃣ Descarga tus constancias
    Una vez completada la encuesta, descarga tus constancias en PDF.
    """)

st.markdown("---")

# Botón para comenzar
st.markdown("### 🚀 ¿Listo para comenzar?")
st.info("👈 **Utiliza el menú lateral para navegar** hacia la sección de Constancias.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>Jornada de Ingeniería Industrial 2025</strong></p>
    <p>Universidad del Caribe</p>
    <p style="font-size: 0.9rem;">Para cualquier duda o aclaración, contacta al equipo organizador.</p>
</div>
""", unsafe_allow_html=True)
