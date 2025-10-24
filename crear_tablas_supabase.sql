-- ============================================================
-- SCRIPT PARA CREAR TABLAS EN SUPABASE
-- ============================================================
-- Ejecuta este script en: Supabase Dashboard → SQL Editor → New query
-- Copia y pega todo el contenido, luego presiona "Run"
-- ============================================================

-- 1. TABLA: participantes
-- Almacena información de los participantes del evento
-- ============================================================
CREATE TABLE IF NOT EXISTS public.participantes (
    id BIGINT PRIMARY KEY,
    nombre_completo TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    telefono TEXT,
    categoria TEXT,
    programa TEXT,
    brazalete TEXT,
    encuesta_completada BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para mejorar rendimiento de búsquedas
CREATE INDEX IF NOT EXISTS idx_participantes_email ON public.participantes(email);
CREATE INDEX IF NOT EXISTS idx_participantes_categoria ON public.participantes(categoria);

-- Comentarios para documentación
COMMENT ON TABLE public.participantes IS 'Registro de participantes del evento';
COMMENT ON COLUMN public.participantes.email IS 'Email único del participante';
COMMENT ON COLUMN public.participantes.encuesta_completada IS 'Indica si completó la encuesta post-evento';

-- ============================================================
-- 2. TABLA: actividades
-- Almacena las actividades/conferencias del evento
-- ============================================================
CREATE TABLE IF NOT EXISTS public.actividades (
    id BIGINT PRIMARY KEY,
    codigo TEXT UNIQUE NOT NULL,
    titulo TEXT NOT NULL,
    ponente TEXT,
    institucion TEXT,
    bio_ponente TEXT,
    descripcion TEXT,
    imagen_ponente TEXT,
    banner TEXT,
    fecha_inicio TIMESTAMPTZ,
    fecha_fin TIMESTAMPTZ,
    lugar TEXT,
    tipo TEXT,
    cupo_maximo INTEGER,
    activa BOOLEAN DEFAULT TRUE,
    creado TIMESTAMPTZ DEFAULT NOW(),
    actualizado TIMESTAMPTZ DEFAULT NOW()
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_actividades_codigo ON public.actividades(codigo);
CREATE INDEX IF NOT EXISTS idx_actividades_tipo ON public.actividades(tipo);
CREATE INDEX IF NOT EXISTS idx_actividades_fecha_inicio ON public.actividades(fecha_inicio);

-- Comentarios
COMMENT ON TABLE public.actividades IS 'Conferencias, talleres y actividades del evento';
COMMENT ON COLUMN public.actividades.codigo IS 'Código único de la actividad (ej: C1, T1)';
COMMENT ON COLUMN public.actividades.cupo_maximo IS 'Capacidad máxima de asistentes';

-- ============================================================
-- 3. TABLA: asistencias
-- Registra la asistencia de participantes a actividades
-- ============================================================
CREATE TABLE IF NOT EXISTS public.asistencias (
    id BIGINT PRIMARY KEY,
    participante_email TEXT NOT NULL,
    actividad_codigo TEXT NOT NULL,
    estado TEXT NOT NULL,
    modo_asistencia TEXT,
    fecha_asistencia TIMESTAMPTZ DEFAULT NOW(),
    notas TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para consultas frecuentes
CREATE INDEX IF NOT EXISTS idx_asistencias_participante ON public.asistencias(participante_email);
CREATE INDEX IF NOT EXISTS idx_asistencias_actividad ON public.asistencias(actividad_codigo);
CREATE INDEX IF NOT EXISTS idx_asistencias_estado ON public.asistencias(estado);
CREATE INDEX IF NOT EXISTS idx_asistencias_fecha ON public.asistencias(fecha_asistencia);

-- Índice compuesto para validar asistencia única
CREATE UNIQUE INDEX IF NOT EXISTS idx_asistencias_unique 
ON public.asistencias(participante_email, actividad_codigo);

-- Comentarios
COMMENT ON TABLE public.asistencias IS 'Registro de asistencia de participantes a actividades';
COMMENT ON COLUMN public.asistencias.estado IS 'Estado: registrado, asistió, no asistió';
COMMENT ON COLUMN public.asistencias.modo_asistencia IS 'Cómo registró: self, admin, qr';

-- ============================================================
-- 4. TABLA: equipos_concurso
-- Almacena equipos registrados para el concurso
-- ============================================================
CREATE TABLE IF NOT EXISTS public.equipos_concurso (
    id BIGINT PRIMARY KEY,
    nombre_equipo TEXT NOT NULL,
    estado_id INTEGER,
    email_capitan TEXT NOT NULL,
    nombre_capitan TEXT NOT NULL,
    telefono_capitan TEXT,
    email_miembro_1 TEXT,
    email_miembro_2 TEXT,
    email_miembro_3 TEXT,
    email_miembro_4 TEXT,
    email_miembro_5 TEXT,
    estado_registro TEXT DEFAULT 'pendiente',
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMPTZ DEFAULT NOW(),
    fecha_confirmacion TIMESTAMPTZ
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_equipos_capitan ON public.equipos_concurso(email_capitan);
CREATE INDEX IF NOT EXISTS idx_equipos_estado_registro ON public.equipos_concurso(estado_registro);
CREATE INDEX IF NOT EXISTS idx_equipos_activo ON public.equipos_concurso(activo);

-- Comentarios
COMMENT ON TABLE public.equipos_concurso IS 'Equipos registrados para el concurso del evento';
COMMENT ON COLUMN public.equipos_concurso.estado_registro IS 'Estado: pendiente, confirmado, rechazado';
COMMENT ON COLUMN public.equipos_concurso.estado_id IS 'ID del estado de México que representa';

-- ============================================================
-- 5. TABLA: encuesta_respuestas
-- Almacena respuestas individuales de la encuesta post-evento
-- ============================================================
CREATE TABLE IF NOT EXISTS public.encuesta_respuestas (
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

-- Índices
CREATE INDEX IF NOT EXISTS idx_encuesta_participante ON public.encuesta_respuestas(participante_email);
CREATE INDEX IF NOT EXISTS idx_encuesta_pregunta ON public.encuesta_respuestas(pregunta_id);
CREATE INDEX IF NOT EXISTS idx_encuesta_timestamp ON public.encuesta_respuestas(timestamp);

-- Índice compuesto para evitar respuestas duplicadas
CREATE UNIQUE INDEX IF NOT EXISTS idx_encuesta_unique 
ON public.encuesta_respuestas(participante_email, pregunta_id);

-- Comentarios
COMMENT ON TABLE public.encuesta_respuestas IS 'Respuestas individuales de encuesta post-evento';
COMMENT ON COLUMN public.encuesta_respuestas.pregunta_id IS 'ID de la pregunta (1-17)';
COMMENT ON COLUMN public.encuesta_respuestas.pregunta_texto IS 'Texto de la pregunta';
COMMENT ON COLUMN public.encuesta_respuestas.fecha IS 'Fecha de respuesta en formato legible';
COMMENT ON COLUMN public.encuesta_respuestas.timestamp IS 'Timestamp Unix de la respuesta';

-- ============================================================
-- POLÍTICAS DE SEGURIDAD (Row Level Security)
-- ============================================================

-- Habilitar RLS en todas las tablas
ALTER TABLE public.participantes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.actividades ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.asistencias ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.equipos_concurso ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.encuesta_respuestas ENABLE ROW LEVEL SECURITY;

-- Políticas: Permitir lectura pública (para la app)
CREATE POLICY "Permitir lectura pública de participantes" 
ON public.participantes FOR SELECT 
USING (true);

CREATE POLICY "Permitir lectura pública de actividades" 
ON public.actividades FOR SELECT 
USING (true);

CREATE POLICY "Permitir lectura pública de asistencias" 
ON public.asistencias FOR SELECT 
USING (true);

CREATE POLICY "Permitir lectura pública de equipos" 
ON public.equipos_concurso FOR SELECT 
USING (true);

CREATE POLICY "Permitir lectura pública de encuestas" 
ON public.encuesta_respuestas FOR SELECT 
USING (true);

-- Políticas: Permitir escritura con autenticación (para la app)
CREATE POLICY "Permitir inserción autenticada de participantes" 
ON public.participantes FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Permitir inserción autenticada de asistencias" 
ON public.asistencias FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Permitir inserción autenticada de equipos" 
ON public.equipos_concurso FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Permitir inserción autenticada de encuestas" 
ON public.encuesta_respuestas FOR INSERT 
WITH CHECK (true);

-- Políticas: Permitir actualización autenticada
CREATE POLICY "Permitir actualización autenticada de participantes" 
ON public.participantes FOR UPDATE 
USING (true);

CREATE POLICY "Permitir actualización autenticada de asistencias" 
ON public.asistencias FOR UPDATE 
USING (true);

-- Políticas: Permitir eliminación autenticada (para importación)
CREATE POLICY "Permitir eliminación autenticada de participantes" 
ON public.participantes FOR DELETE 
USING (true);

CREATE POLICY "Permitir eliminación autenticada de asistencias" 
ON public.asistencias FOR DELETE 
USING (true);

CREATE POLICY "Permitir eliminación autenticada de actividades" 
ON public.actividades FOR DELETE 
USING (true);

CREATE POLICY "Permitir eliminación autenticada de equipos" 
ON public.equipos_concurso FOR DELETE 
USING (true);

CREATE POLICY "Permitir eliminación autenticada de encuestas" 
ON public.encuesta_respuestas FOR DELETE 
USING (true);

-- ============================================================
-- TRIGGERS PARA ACTUALIZAR TIMESTAMPS
-- ============================================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para participantes
CREATE TRIGGER update_participantes_updated_at 
BEFORE UPDATE ON public.participantes 
FOR EACH ROW 
EXECUTE FUNCTION update_updated_at_column();

-- Trigger para actividades
CREATE TRIGGER update_actividades_updated_at 
BEFORE UPDATE ON public.actividades 
FOR EACH ROW 
EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- VISTAS ÚTILES
-- ============================================================

-- Vista: Estadísticas de asistencia por actividad
CREATE OR REPLACE VIEW public.vista_estadisticas_actividades AS
SELECT 
    a.codigo,
    a.titulo,
    a.tipo,
    a.cupo_maximo,
    COUNT(asi.id) as total_asistencias,
    COUNT(CASE WHEN asi.estado = 'asistió' THEN 1 END) as asistencias_confirmadas,
    ROUND(COUNT(CASE WHEN asi.estado = 'asistió' THEN 1 END)::NUMERIC / 
          NULLIF(a.cupo_maximo, 0) * 100, 2) as porcentaje_ocupacion
FROM public.actividades a
LEFT JOIN public.asistencias asi ON a.codigo = asi.actividad_codigo
GROUP BY a.id, a.codigo, a.titulo, a.tipo, a.cupo_maximo;

-- Vista: Participantes con estadísticas de asistencia
CREATE OR REPLACE VIEW public.vista_participantes_completa AS
SELECT 
    p.id,
    p.nombre_completo,
    p.email,
    p.categoria,
    p.programa,
    p.encuesta_completada,
    COUNT(a.id) as total_asistencias,
    COUNT(CASE WHEN a.estado = 'asistió' THEN 1 END) as asistencias_confirmadas
FROM public.participantes p
LEFT JOIN public.asistencias a ON LOWER(p.email) = LOWER(a.participante_email)
GROUP BY p.id, p.nombre_completo, p.email, p.categoria, p.programa, p.encuesta_completada;

-- ============================================================
-- VERIFICACIÓN FINAL
-- ============================================================

-- Consulta para verificar que las tablas se crearon correctamente
SELECT 
    schemaname,
    tablename,
    tableowner
FROM pg_tables
WHERE schemaname = 'public'
    AND tablename IN ('participantes', 'actividades', 'asistencias', 'equipos_concurso', 'encuesta_respuestas')
ORDER BY tablename;

-- ============================================================
-- ✅ SCRIPT COMPLETADO
-- ============================================================
-- Después de ejecutar este script:
-- 1. Verifica que las 5 tablas aparezcan en Table Editor
-- 2. Ejecuta el script: python exportar_datos_supabase.py
-- 3. Verifica que los datos se hayan importado correctamente
-- ============================================================
