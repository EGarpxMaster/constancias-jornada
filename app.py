"""
Aplicación Principal - Sistema de Constancias JII 2025
"""
import streamlit as st
from pathlib import Path

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Constancias - JII 2025",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Directorio raíz
ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT / "assets"
IMAGES_DIR = ASSETS_DIR / "images"

# Estilo CSS personalizado con paleta de colores
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
    
    .stApp {
        background-color: var(--light-color) !important;
        color: var(--text-color) !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary-color) !important;
        font-family: var(--font-family);
    }
    
    p, span, div, label, li {
        color: var(--text-color) !important;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--primary-color) !important;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: var(--secondary-color) !important;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .info-box {
        background-color: white !important;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid var(--secondary-color);
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        color: var(--text-color) !important;
    }
    
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
    
    /* Info boxes */
    .stInfo {
        background-color: rgba(30, 206, 202, 0.08) !important;
        color: var(--text-color) !important;
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
