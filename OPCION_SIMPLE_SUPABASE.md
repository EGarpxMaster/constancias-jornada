# 🚀 Opción MÁS SIMPLE: Supabase (5 minutos)

## ¿Por qué Supabase?

- ✅ **Setup en 5 minutos**: Sin instalar nada, todo en el navegador
- ✅ **100% Gratis**: 500 MB de base de datos + 1 GB de transferencia
- ✅ **Sin CLI**: Todo desde la web
- ✅ **PostgreSQL**: Base de datos profesional
- ✅ **2 valores**: URL + API Key (como Turso)

## 🔧 Setup (5 minutos)

### 1. Crear cuenta (2 minutos)

1. Ve a https://supabase.com/
2. Haz clic en "Start your project"
3. Inicia sesión con GitHub (más rápido)

### 2. Crear proyecto (1 minuto)

1. Haz clic en "New Project"
2. Nombre: `jii2025-encuestas`
3. Database Password: (guárdala, la necesitarás)
4. Región: `South America (São Paulo)` (más cerca de México)
5. Haz clic en "Create new project"
6. Espera 1-2 minutos mientras se crea

### 3. Crear tabla (2 minutos)

1. En el menú izquierdo, haz clic en **Table Editor**
2. Haz clic en **New Table**
3. Copia y pega este SQL:

```sql
CREATE TABLE encuesta_respuestas (
    id BIGSERIAL PRIMARY KEY,
    participante_email TEXT NOT NULL,
    nombre_completo TEXT NOT NULL,
    pregunta_id INTEGER NOT NULL,
    pregunta_texto TEXT NOT NULL,
    respuesta TEXT NOT NULL,
    fecha TEXT NOT NULL,
    timestamp BIGINT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Crear índices para búsquedas rápidas
CREATE INDEX idx_email ON encuesta_respuestas(participante_email);
CREATE INDEX idx_pregunta ON encuesta_respuestas(pregunta_id);
CREATE INDEX idx_timestamp ON encuesta_respuestas(timestamp);
```

O usa la interfaz visual:
- Table name: `encuesta_respuestas`
- Agrega las columnas manualmente

4. Haz clic en "Save"

### 4. Obtener credenciales (30 segundos)

1. Ve a **Settings** → **API**
2. Copia estos 2 valores:

   - **Project URL**: `https://tuproject.supabase.co`
   - **anon public key**: `eyJhbG...` (es largo, cópialo completo)

¡Listo! Ya tienes todo configurado.

## 📦 Instalación de librería

```powershell
pip install supabase
```

## 🔧 Configuración

### Local (.env)

Crea un archivo `.env` en la raíz del proyecto:

```env
SUPABASE_URL=https://tuproject.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Streamlit Cloud (Secrets)

Settings → Secrets:

```toml
SUPABASE_URL = "https://tuproject.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 📊 Ver tus datos

### Opción 1: Dashboard Web (más fácil)

1. Ve a **Table Editor** en Supabase
2. Haz clic en `encuesta_respuestas`
3. ¡Ves todos los datos en tiempo real!

### Opción 2: SQL Editor

1. Ve a **SQL Editor**
2. Escribe queries:

```sql
-- Ver últimas 10 respuestas
SELECT * FROM encuesta_respuestas 
ORDER BY timestamp DESC 
LIMIT 10;

-- Contar respuestas por participante
SELECT participante_email, COUNT(*) as total
FROM encuesta_respuestas
GROUP BY participante_email;

-- Respuestas de una pregunta específica
SELECT nombre_completo, respuesta
FROM encuesta_respuestas
WHERE pregunta_id = 1;
```

### Opción 3: Exportar a CSV

1. En Table Editor, selecciona la tabla
2. Haz clic en los 3 puntos (⋮)
3. **Export data** → **CSV**

## 🔐 Seguridad

- La `anon public key` es segura para el frontend
- Supabase tiene Row Level Security (RLS) automático
- Los datos están encriptados en tránsito y en reposo

## 💰 Límites Gratuitos

- ✅ 500 MB de base de datos
- ✅ 1 GB de transferencia/mes
- ✅ 50,000 usuarios autenticados
- ✅ Backups automáticos

**Para 1000 participantes con 20 respuestas cada uno** = ~2 MB
→ Tienes espacio para **250,000 participantes** 🚀

## 🆘 Solución de problemas

### No puedo crear la tabla

**Opción A**: Usa el editor SQL:
1. SQL Editor → New Query
2. Pega el CREATE TABLE
3. Run

**Opción B**: Interfaz visual:
1. Table Editor → New Table
2. Agrega columnas una por una

### Error de conexión

- Verifica que la URL empiece con `https://`
- Verifica que la API Key esté completa (es muy larga)
- Intenta regenerar la API Key en Settings → API

### Ver logs de errores

Settings → Database → Logs

## 🎨 Bonus: Dashboard automático

Supabase genera automáticamente un dashboard con:
- Gráficas de uso
- Logs de queries
- Métricas de rendimiento
- Backups automáticos

## 🔄 Migrar datos existentes

Si ya tienes datos en CSV:

```python
import pandas as pd
from supabase import create_client, Client

url = "tu-url"
key = "tu-key"
supabase: Client = create_client(url, key)

# Leer CSV
df = pd.read_csv("datos/encuesta_respuestas.csv")

# Insertar en Supabase
data = df.to_dict('records')
supabase.table('encuesta_respuestas').insert(data).execute()
```

## 📚 Documentación

- Docs: https://supabase.com/docs
- Python Client: https://supabase.com/docs/reference/python/introduction
- Ejemplos: https://github.com/supabase/supabase/tree/master/examples

---

**Supabase es la opción más simple**: interfaz web, sin instalaciones, gratis para siempre, y más potente que Google Sheets.
