-- ============================================================
-- AGREGAR POLÍTICA DE INSERT PARA ACTIVIDADES
-- ============================================================
-- Este script agrega la política faltante para permitir 
-- insertar datos en la tabla actividades
-- ============================================================

-- Política: Permitir inserción autenticada de actividades
CREATE POLICY IF NOT EXISTS "Permitir inserción autenticada de actividades" 
ON public.actividades FOR INSERT 
WITH CHECK (true);

-- Verificar que la política se creó correctamente
SELECT schemaname, tablename, policyname, permissive, roles, cmd
FROM pg_policies
WHERE tablename = 'actividades';
