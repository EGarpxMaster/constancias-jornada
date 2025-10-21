# 🚀 Guía de Despliegue en Streamlit Cloud

Esta guía te ayudará a desplegar tu aplicación de constancias en Streamlit Cloud con almacenamiento persistente en Supabase.

## 📋 Requisitos Previos

✅ Código subido a GitHub  
✅ Cuenta en Supabase configurada (ver `OPCION_SIMPLE_SUPABASE.md`)  
✅ Tabla `encuesta_respuestas` creada en Supabase  
✅ Valores de `SUPABASE_URL` y `SUPABASE_KEY` guardados

## 🔧 Paso 1: Preparar el Repositorio

1. **Asegúrate de que el código esté en GitHub**:
   ```powershell
   git add .
   git commit -m "Preparar para despliegue en Streamlit Cloud con Supabase"
   git push origin main
   ```

2. **Verifica que NO hayas subido el archivo `.env`** (debe estar en `.gitignore`):
   ```powershell
   git status
   # No debería aparecer .env en la lista
   ```

## ☁️ Paso 2: Desplegar en Streamlit Cloud

1. **Ve a [share.streamlit.io](https://share.streamlit.io)** e inicia sesión con GitHub

2. **Haz clic en "New app"**

3. **Configura tu aplicación**:
   - **Repository**: `constancias-jornada`
   - **Branch**: `main` (o la rama que uses)
   - **Main file path**: `app.py`
   - **App URL**: Elige un nombre personalizado (opcional)

4. **NO hagas clic en "Deploy" todavía** - primero configuraremos los secretos

## 🔐 Paso 3: Configurar Secretos de Supabase

1. **Antes de desplegar**, haz clic en **"Advanced settings"**

2. En la sección **"Secrets"**, copia y pega exactamente lo siguiente:

```toml
SUPABASE_URL = "https://inpduodbcorajrvbftrf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlucGR1b2RiY29yYWpydmJmdHJmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA5OTEwMzksImV4cCI6MjA3NjU2NzAzOX0.CkiwLxkjbXmDujoNDIpT2tjfdXtrao3Dfr-tSmsNLt8"
```

> **⚠️ IMPORTANTE**: 
> - Copia TODO el bloque de arriba (ambas líneas)
> - NO agregues comentarios (líneas con #)
> - NO agregues espacios extra antes o después de las comillas
> - Las comillas son obligatorias

3. **Verifica el formato**:
   - Debe haber exactamente 2 líneas
   - Cada línea debe seguir el formato: `NOMBRE = "valor"`
   - Sin comentarios ni líneas vacías al inicio

4. **Guarda** haciendo clic en "Save"

## 🎯 Paso 4: Desplegar

1. Ahora sí, haz clic en **"Deploy!"**

2. Streamlit Cloud comenzará a instalar las dependencias y desplegar tu app

3. Espera 2-5 minutos mientras se completa el despliegue

4. Una vez que veas "Your app is live!" 🎉, tu aplicación estará disponible

## ✅ Paso 5: Verificar el Funcionamiento

1. **Abre tu aplicación** en el navegador

2. **Completa la encuesta de prueba** con tu email de UCaribe

3. **Verifica en Supabase** que los datos se guardaron:
   - Ve a tu proyecto en Supabase
   - **Table Editor** → `encuesta_respuestas`
   - Deberías ver tus respuestas guardadas

4. **Reinicia la aplicación** en Streamlit Cloud:
   - Menú (☰) → "Reboot app"
   - Espera a que reinicie
   - Verifica que tus respuestas siguen ahí en Supabase

## 🔄 Actualizar la Aplicación

Cuando hagas cambios en tu código:

```powershell
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

Streamlit Cloud detectará automáticamente los cambios y redesplegará la app.

## 🔧 Actualizar los Secretos

Si necesitas cambiar `SUPABASE_URL` o `SUPABASE_KEY`:

1. Ve a tu app en Streamlit Cloud
2. **Settings** (⚙️) → **Secrets**
3. Edita los valores
4. **Save**
5. La app se reiniciará automáticamente

## ❌ Solución de Problemas

### Error: "Invalid API key"

**Causa**: La clave de Supabase no está configurada correctamente

**Solución**:
1. Verifica que copiaste el **anon public** key (no el service role key)
2. Asegúrate de que no haya espacios al inicio o final
3. Ve a Settings → Secrets y verifica la configuración

### Error: "Module 'supabase' not found"

**Causa**: `requirements.txt` no está en el repositorio

**Solución**:
```powershell
git add requirements.txt
git commit -m "Agregar requirements.txt"
git push origin main
```

### La app se queda "Spinning up"

**Causa**: Puede haber un error en el código o en las dependencias

**Solución**:
1. Haz clic en "Manage app" → "Logs"
2. Revisa los errores en los logs
3. Corrige el código y haz push de nuevo

### Los datos no se guardan

**Causa**: Secretos no configurados o tabla no creada

**Solución**:
1. Verifica que los secretos estén configurados correctamente
2. Asegúrate de que la tabla `encuesta_respuestas` existe en Supabase
3. Revisa los logs de la app para ver errores específicos

## 📊 Monitoreo

Para ver las respuestas guardadas:

1. Ve a [supabase.com](https://supabase.com)
2. Selecciona tu proyecto
3. **Table Editor** → `encuesta_respuestas`
4. Ahí verás todas las respuestas en tiempo real

## 🎓 Recursos Adicionales

- [Documentación de Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Secrets Management en Streamlit](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Documentación de Supabase](https://supabase.com/docs)

---

✅ **¡Listo!** Tu aplicación ahora está desplegada en Streamlit Cloud con almacenamiento persistente en Supabase.
