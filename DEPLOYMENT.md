# 🚀 Guía de Despliegue - Streamlit Cloud

## ⚠️ Nota Importante sobre GitHub Pages

**GitHub Pages NO es compatible con aplicaciones Streamlit** porque:
- GitHub Pages solo sirve archivos estáticos (HTML, CSS, JS)
- Streamlit requiere Python ejecutándose en un servidor
- GitHub Pages no ejecuta código del lado del servidor

Para desplegar esta aplicación, debes usar **Streamlit Cloud** (recomendado) u otras alternativas.

---

## 📦 Opción 1: Streamlit Cloud (Recomendado - GRATIS)

### Paso 1: Preparar el Repositorio

1. **Asegúrate de que todos los archivos estén en GitHub:**
   ```powershell
   git add .
   git commit -m "Preparar aplicación para despliegue"
   git push origin main
   ```

2. **Verifica que estos archivos estén en el repositorio:**
   - ✅ `app.py` (archivo principal)
   - ✅ `requirements.txt`
   - ✅ `pages/1_📝_Constancias.py`
   - ✅ `Multipage App/datos/` (con los CSV)
   - ✅ `assets/fonts/` (con las fuentes)
   - ✅ `assets/plantillas/` (con las plantillas PDF)

### Paso 2: Registrarse en Streamlit Cloud

1. Ve a https://streamlit.io/cloud
2. Haz clic en **"Sign up"** o **"Sign in"**
3. Usa tu cuenta de GitHub para registrarte
4. Autoriza a Streamlit Cloud para acceder a tus repositorios

### Paso 3: Crear una Nueva App

1. En el dashboard de Streamlit Cloud, haz clic en **"New app"**
2. Selecciona:
   - **Repository**: `EGarpxMaster/constancias-jornada`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Haz clic en **"Deploy!"**

### Paso 4: Esperar el Despliegue

- El proceso toma 2-5 minutos
- Streamlit Cloud instalará automáticamente las dependencias
- Una vez completado, obtendrás una URL pública como:
  `https://constancias-jornada-xxx.streamlit.app`

### Paso 5: Compartir la URL

Comparte la URL generada con los participantes de la JII 2025.

---

## 🔧 Opción 2: Heroku

### Requisitos Adicionales

Crea un archivo `Procfile` en la raíz:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Crea un archivo `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

### Pasos de Despliegue

1. Instala Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Login en Heroku:
   ```powershell
   heroku login
   ```
3. Crea una nueva app:
   ```powershell
   heroku create nombre-de-tu-app
   ```
4. Despliega:
   ```powershell
   git push heroku main
   ```

---

## 🐳 Opción 3: Docker + Servidor Propio

### Dockerfile

Crea un `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Construir y Ejecutar

```powershell
# Construir imagen
docker build -t constancias-jii .

# Ejecutar contenedor
docker run -p 8501:8501 constancias-jii
```

---

## 🔐 Configuración de Seguridad

### Variables de Entorno (Streamlit Cloud)

Si necesitas agregar variables de entorno sensibles:

1. Ve a tu app en Streamlit Cloud
2. Haz clic en **"⋮"** (menú) → **"Settings"**
3. En la sección **"Secrets"**, agrega:
   ```toml
   # Ejemplo de secretos
   [passwords]
   admin_password = "tu_password_seguro"
   ```

### Acceso en el Código

```python
import streamlit as st

# Acceder a secretos
if "passwords" in st.secrets:
    admin_pass = st.secrets["passwords"]["admin_password"]
```

---

## 📊 Monitoreo y Mantenimiento

### Logs en Streamlit Cloud

1. Abre tu app en Streamlit Cloud
2. Haz clic en **"⋮"** → **"Logs"**
3. Aquí puedes ver:
   - Errores de la aplicación
   - Tiempo de carga
   - Uso de recursos

### Actualizar la Aplicación

Simplemente haz push a tu repositorio:
```powershell
git add .
git commit -m "Actualización"
git push origin main
```

Streamlit Cloud detectará los cambios y redesplegará automáticamente.

---

## 🎯 Optimización para Producción

### 1. Caché de Datos

El código ya usa `@st.cache_data` para optimizar la carga de datos.

### 2. Limitar Tamaño de Archivos

Streamlit Cloud tiene límites:
- **Repositorio**: 1 GB
- **RAM**: 1 GB (plan gratuito)
- **CPU**: Compartida

### 3. Comprimir Archivos

Si los PDFs de plantillas son muy grandes:
```python
# Usar compresión en PDFs
from PyPDF2 import PdfWriter

writer = PdfWriter()
writer.add_page(page)
writer.compress_content_streams()
```

---

## ❓ Solución de Problemas

### Error: "ModuleNotFoundError"

**Causa**: Falta una dependencia en `requirements.txt`

**Solución**: Agrega el módulo faltante y haz push.

### Error: "File not found"

**Causa**: Rutas de archivos incorrectas

**Solución**: Verifica que todas las rutas usen `Path` correctamente y que los archivos estén en el repositorio.

### La app es muy lenta

**Causas posibles**:
- Archivos CSV muy grandes
- Plantillas PDF pesadas
- Falta de caché

**Soluciones**:
- Optimiza los CSV (elimina columnas innecesarias)
- Comprime las plantillas PDF
- Agrega más `@st.cache_data`

---

## 📞 Recursos y Ayuda

- **Documentación de Streamlit**: https://docs.streamlit.io
- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Foro de Streamlit**: https://discuss.streamlit.io
- **GitHub Issues**: Reporta problemas en el repositorio

---

## 🎉 ¡Listo!

Tu aplicación estará disponible 24/7 en la URL de Streamlit Cloud para que los participantes de la JII 2025 puedan obtener sus constancias.

**URL de ejemplo**: `https://constancias-jornada-jii2025.streamlit.app`
