# 🎓 Sistema de Constancias - Jornada de Ingeniería Industrial 2025

Sistema web desarrollado en Streamlit para la generación y descarga de constancias de participación en la Jornada de Ingeniería Industrial 2025 de la Universidad del Caribe.

## 📋 Características

- ✅ Verificación automática de elegibilidad basada en asistencias
- 📝 Encuesta de satisfacción integrada
- 📄 Generación automática de constancias en PDF
- 🎨 Uso de plantillas PDF personalizadas
- 💾 Almacenamiento de respuestas en CSV
- 🔒 Control de encuestas completadas

## 🏗️ Estructura del Proyecto

```
constancias-jornada/
├── app.py                          # Página principal
├── pages/
│   └── 1_📝_Constancias.py        # Página de constancias
├── Multipage App/
│   └── datos/
│       ├── participantes.csv       # Datos de participantes
│       ├── asistencias.csv         # Registro de asistencias
│       └── encuesta_respuestas.csv # Respuestas de encuestas
├── assets/
│   ├── fonts/
│   │   ├── OldStandardTT-Bold.ttf
│   │   ├── OldStandardTT-Italic.ttf
│   │   └── OldStandardTT-Regular.ttf
│   └── plantillas/
│       ├── Participacion_general.pdf
│       ├── Constancia_mundialito.pdf
│       ├── W1.pdf
│       ├── W2.pdf
│       ├── W3.pdf
│       ├── W4.pdf
│       ├── W5.pdf
│       └── W6.pdf
├── requirements.txt
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

### encuesta_respuestas.csv (generado automáticamente)

```csv
participante_email,pregunta_id,respuesta,fecha
ejemplo@ucaribe.edu.mx,1,5,2025-10-20 15:30:00
```

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

## 📝 Notas de Despliegue

### Despliegue en Streamlit Cloud

1. Sube el repositorio a GitHub
2. Conecta tu cuenta de Streamlit Cloud
3. Selecciona el repositorio y la rama
4. Especifica `app.py` como archivo principal
5. Despliega

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
