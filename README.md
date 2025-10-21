# 🎓 Sistema de Constancias - Jornada de Ingeniería Industrial 2025

Sistema web desarrollado en Streamlit para la generación y descarga de constancias de participación en la Jornada de Ingeniería Industrial 2025 de la Universidad del Caribe.

## 📋 Características

- ✅ Verificación automática de elegibilidad basada en asistencias
- 📝 Encuesta de satisfacción integrada
- 📄 Generación automática de constancias en PDF
- 🎨 Uso de plantillas PDF personalizadas
- ☁️ Almacenamiento persistente en Google Sheets
- 💾 Respaldo local en CSV
- 🔒 Control de encuestas completadas

## 🏗️ Estructura del Proyecto

```
constancias-jornada/
├── app.py                          # Página principal
├── pages/
│   └── 1_Constancias.py           # Página de constancias
├── utils/
│   ├── data_handler.py            # Manejo de datos
│   ├── pdf_generator.py           # Generación de PDFs
│   ├── validations.py             # Validaciones
│   └── google_sheets_handler.py   # Integración con Google Sheets
├── datos/
│   ├── participantes.csv          # Datos de participantes
│   ├── asistencias.csv            # Registro de asistencias
│   └── encuesta_respuestas.csv    # Respuestas (respaldo local)
├── assets/
│   ├── fonts/
│   │   ├── OldStandardTT-Bold.ttf
│   │   ├── OldStandardTT-Italic.ttf
│   │   └── OldStandardTT-Regular.ttf
│   ├── images/                    # Imágenes
│   └── plantillas/
│       ├── Participacion_general.pdf
│       ├── Constancia_mundialito.pdf
│       ├── W1.pdf - W6.pdf        # Plantillas de workshops
├── credentials.json               # ⚠️ NO VERSIONAR - Credenciales Google
├── requirements.txt
├── GOOGLE_SHEETS_SETUP.md         # Instrucciones de configuración
└── README.md
```

## 🚀 Instalación

### Prerrequisitos

- Python 3.10 o superior (recomendado 3.11 o 3.12)
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```powershell
   git clone https://github.com/EGarpxMaster/constancias-jornada.git
   cd constancias-jornada
   ```

2. **Crear un entorno virtual**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Instalar dependencias**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configurar Google Sheets (Opcional pero recomendado)**
   
   Para habilitar el almacenamiento persistente de respuestas:
   
   - Sigue las instrucciones detalladas en [`GOOGLE_SHEETS_SETUP.md`](GOOGLE_SHEETS_SETUP.md)
   - Crea un Service Account en Google Cloud Console
   - Descarga el archivo `credentials.json` y colócalo en la raíz del proyecto
   - **IMPORTANTE**: `credentials.json` está en `.gitignore` y NO debe subirse al repositorio
   
   Si no configuras Google Sheets, las respuestas solo se guardarán localmente en CSV (se perderán en cada reinicio en Streamlit Cloud).

## ▶️ Ejecución

Para iniciar la aplicación:

```powershell
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📊 Estructura de Datos

### participantes.csv

```csv
id,nombre_completo,email,telefono,categoria,programa,brazalete,encuesta_completada
456,Mario Alberto Estrada Contreras,ejemplo@ucaribe.edu.mx,9982127686,Estudiante,Ingeniería Industrial,,False
```

**Columnas:**
- `id`: Identificador único del participante
- `nombre_completo`: Nombre completo (formato: Apellidos Nombres)
- `email`: Correo electrónico
- `telefono`: Número de teléfono
- `categoria`: Tipo de participante (Estudiante, Docente, Ponente, etc.)
- `programa`: Programa académico
- `brazalete`: Número de brazalete
- `encuesta_completada`: Indica si completó la encuesta (True/False)

### asistencias.csv

```csv
id,participante_email,actividad_codigo,estado,modo_asistencia,fecha_asistencia,notas
1051,ejemplo@ucaribe.edu.mx,CL1,registrado,self,2025-09-26 15:17:01,
```

**Columnas:**
- `id`: Identificador único de asistencia
- `participante_email`: Email del participante
- `actividad_codigo`: Código de la actividad (CL1, C1, W1, F1, etc.)
- `estado`: Estado de la asistencia
- `modo_asistencia`: Modo de registro
- `fecha_asistencia`: Fecha y hora de registro
- `notas`: Notas adicionales

### encuesta_respuestas.csv (generado automáticamente - respaldo local)

```csv
participante_email,pregunta_id,respuesta,fecha
ejemplo@ucaribe.edu.mx,1,5,2025-10-20 15:30:00
```

**Nota**: Este archivo es un respaldo local. Las respuestas principales se almacenan en Google Sheets (hoja "JII2025_Encuestas" → worksheet "Respuestas") con las siguientes columnas:
- `participante_email`: Email del participante
- `nombre_completo`: Nombre completo del participante
- `pregunta_id`: ID de la pregunta
- `pregunta_texto`: Texto completo de la pregunta
- `respuesta`: Respuesta del participante
- `fecha`: Fecha en formato legible (YYYY-MM-DD HH:MM:SS)
- `timestamp`: Unix timestamp para ordenamiento

## 🎯 Lógica de Negocio

### Elegibilidad para Constancias

1. **Constancia General**: Requiere 2 o más asistencias al evento
2. **Constancia de Workshop**: Requiere asistencia a un workshop (código W1-W6)
3. **Constancia de Mundialito**: Requiere participación en el mundialito

### Preguntas de la Encuesta

#### Preguntas Generales (1-16)
- Calificación de organización, horarios, duración
- Razón de asistencia
- Expectativas y utilidad del contenido
- Nivel profesional
- Conferencias y actividades relevantes
- Puntos fuertes y áreas de mejora
- Sugerencias para 2026
- Calificación general
- Comentarios adicionales

#### Preguntas de Workshop (17-18)
- Valoración del workshop (1-5)
- Comentarios sobre el workshop

#### Preguntas de Mundialito (19-20)
- Valoración del mundialito (1-5)
- Comentarios sobre el mundialito

## 🎨 Personalización de Constancias

Las constancias se generan utilizando:

1. **Plantillas PDF**: Ubicadas en `assets/plantillas/`
2. **Fuente personalizada**: OldStandardTT-Bold
3. **Overlay de nombre**: El nombre se agrega sobre la plantilla
4. **Formato de nombre**: Nombres + Apellidos (invertido del formato de almacenamiento)

### Agregar Nuevas Plantillas

1. Coloca el archivo PDF en `assets/plantillas/`
2. Nombra el archivo según el tipo:
   - `Participacion_general.pdf` para constancia general
   - `W1.pdf` a `W6.pdf` para workshops
   - `Constancia_mundialito.pdf` para mundialito

## 🔧 Configuración

### Ajustar Posición del Nombre

En `pages/1_📝_Constancias.py`, modifica las coordenadas en la función `generar_constancia_pdf()`:

```python
x = (letter[0] - text_width) / 2  # Posición horizontal
y = letter[1] / 2  # Posición vertical (ajustar según plantilla)
```

### Modificar Preguntas de la Encuesta

Edita las listas `PREGUNTAS_GENERALES`, `PREGUNTAS_WORKSHOP`, y `PREGUNTAS_MUNDIALITO` en `pages/1_📝_Constancias.py`

## 📦 Dependencias Principales

- **streamlit**: Framework web para Python
- **pandas**: Manipulación de datos
- **reportlab**: Generación de PDFs
- **PyPDF2**: Manipulación de PDFs
- **Pillow**: Procesamiento de imágenes
- **gspread**: Integración con Google Sheets API
- **oauth2client**: Autenticación con Google Cloud

## 🐛 Solución de Problemas

### Error al instalar pandas en Python 3.13

**Problema**: pandas 2.1.4 no es compatible con Python 3.13

**Solución**: Usa Python 3.11 o 3.12, o actualiza pandas a la versión 2.2.0+

```powershell
pip install pandas>=2.2.0
```

### Error al cargar la fuente

**Problema**: No se encuentra OldStandardTT-Bold.ttf

**Solución**: Verifica que los archivos de fuente estén en `assets/fonts/`

### Plantillas no encontradas

**Problema**: Las constancias se generan sin plantilla

**Solución**: Asegúrate de que las plantillas PDF estén en `assets/plantillas/`

### Google Sheets no funciona

**Problema**: Las respuestas no se guardan en Google Sheets

**Solución**:
1. Verifica que `credentials.json` esté en la raíz del proyecto
2. Verifica que hayas habilitado Google Sheets API y Google Drive API en Google Cloud Console
3. Asegúrate de que el Service Account tenga permisos de Editor
4. Consulta `GOOGLE_SHEETS_SETUP.md` para instrucciones completas

### Error "SpreadsheetNotFound"

**Problema**: La aplicación no puede crear la hoja de cálculo

**Solución**: Verifica que hayas dado permisos de Editor al Service Account y que Google Drive API esté habilitado

## 📝 Notas de Despliegue

### Despliegue en Streamlit Cloud

1. Sube el repositorio a GitHub (**sin incluir credentials.json**)
2. Conecta tu cuenta de Streamlit Cloud
3. Selecciona el repositorio y la rama
4. Especifica `app.py` como archivo principal
5. **Configura los Secrets**:
   - Ve a Settings → Secrets
   - Copia el contenido de `credentials.json` en formato TOML:
   ```toml
   [gcp_service_account]
   type = "service_account"
   project_id = "tu-project-id"
   private_key_id = "tu-private-key-id"
   private_key = "-----BEGIN PRIVATE KEY-----\ntu-private-key\n-----END PRIVATE KEY-----\n"
   client_email = "tu-service-account@tu-project.iam.gserviceaccount.com"
   client_id = "tu-client-id"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/tu-service-account%40tu-project.iam.gserviceaccount.com"
   ```
6. Despliega

**Importante**: 
- Sin Google Sheets configurado, las respuestas se perderán en cada reinicio
- Google Sheets es **esencial** para producción en Streamlit Cloud
- Consulta `GOOGLE_SHEETS_SETUP.md` para el formato completo de secrets

**Nota**: GitHub Pages no es compatible con Streamlit ya que requiere ejecución de Python en el servidor.

### Alternativas de Despliegue

- **Streamlit Cloud**: Gratuito, ideal para proyectos pequeños
- **Heroku**: Requiere configuración adicional
- **AWS/Azure/GCP**: Para aplicaciones de producción
- **Servidor propio**: Usando Docker o instalación directa

## 👥 Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto fue desarrollado para la Universidad del Caribe - Jornada de Ingeniería Industrial 2025.

## 📞 Contacto

Para dudas o soporte técnico, contacta al equipo organizador de la JII 2025.

---

**Universidad del Caribe**  
*Jornada de Ingeniería Industrial 2025*
