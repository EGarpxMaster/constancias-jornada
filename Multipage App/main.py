import streamlit as st
from pathlib import Path
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="JII 2025 - Sistema de Constancias",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar paths
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "datos"

# Función para cargar datos
@st.cache_data
def cargar_datos():
    """Carga los datos de participantes y asistencias"""
    try:
        participantes = pd.read_csv(DATA_DIR / "participantes.csv")
        asistencias = pd.read_csv(DATA_DIR / "asistencias.csv")
        equipos = pd.read_csv(DATA_DIR / "equipos_concurso.csv") if (DATA_DIR / "equipos_concurso.csv").exists() else pd.DataFrame()
        return participantes, asistencias, equipos
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# Cargar datos
participantes_df, asistencias_df, equipos_df = cargar_datos()

# CSS personalizado
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        padding: 20px;
        font-size: 2.5em;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
    }
    .success-box {
        padding: 20px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        margin: 20px 0;
    }
    .info-box {
        padding: 15px;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-title">🎓 Jornada de Ingeniería Industrial 2025</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Sistema de Generación de Constancias</p>', unsafe_allow_html=True)

# Menú principal
menu = st.sidebar.radio(
    "Navegación",
    ["🏠 Inicio", "📜 Obtener Constancias", "📊 Información"]
)

if menu == "🏠 Inicio":
    st.header("Bienvenido al Sistema de Constancias JII 2025")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Requisitos para obtener constancias")
        st.write("Para poder generar tus constancias, debes cumplir con:")
        st.markdown("""
- ✅ **Asistencia General**: Mínimo 2 asistencias registradas
- ✅ **Workshop**: Haber participado en al menos un workshop
- ✅ **Mundialito Mexicano**: Participación registrada
- ✅ **Encuesta**: Completar la encuesta de satisfacción
        """)
    
    with col2:
        st.markdown("### 🎯 ¿Cómo obtener mi constancia?")
        st.write("")
        st.markdown("""
1. Ve a la sección **"Obtener Constancias"**
2. Ingresa tu correo electrónico registrado
3. Verifica tu elegibilidad
4. Completa la encuesta de satisfacción
5. Descarga tus constancias disponibles
        """)
    
    st.info("💡 **Importante**: Asegúrate de usar el mismo correo electrónico con el que te registraste al evento.")

elif menu == "📜 Obtener Constancias":
    st.info("👉 Por favor, usa el menú de **páginas** en la barra lateral izquierda para acceder a la sección de Constancias.")
    st.write("O puedes ir directamente a la aplicación principal:")
    st.page_link("app.py", label="🏠 Ir a la página principal", icon="🏠")

elif menu == "📊 Información":
    st.header("Información del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Participantes", len(participantes_df))
    
    with col2:
        st.metric("Total Asistencias", len(asistencias_df))
    
    with col3:
        st.metric("Equipos Mundialito", len(equipos_df))
    
    st.markdown("---")
    
    st.subheader("Contacto y Soporte")
    st.write("Para dudas o problemas técnicos, contacta al equipo organizador de la JII.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Jornada de Ingeniería Industrial 2025</p>
        <p>Desarrollado con ❤️ para la comunidad de Ingeniería Industrial</p>
    </div>
    """,
    unsafe_allow_html=True
)