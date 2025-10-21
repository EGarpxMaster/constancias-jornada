"""
Script para exportar datos locales (CSV) a Supabase
Migra participantes y respuestas de encuesta desde archivos CSV a la base de datos en la nube
"""

import os
import sys
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Agregar el directorio raíz al path para importar módulos
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

# Cargar variables de entorno desde .env
load_dotenv()

from utils.supabase_handler import SupabaseHandler

# Directorio de datos
DATA_DIR = ROOT_DIR / "datos"

def verificar_archivos():
    """Verifica que existan los archivos CSV necesarios"""
    archivos_requeridos = [
        "participantes.csv",
        "asistencias.csv",
        "actividades.csv",
        "equipos_concurso.csv",
        "encuesta_respuestas.csv"
    ]
    
    print("\n📂 Verificando archivos CSV...")
    archivos_encontrados = []
    for archivo in archivos_requeridos:
        ruta = DATA_DIR / archivo
        if ruta.exists():
            print(f"  ✅ {archivo} encontrado")
            archivos_encontrados.append(archivo)
        else:
            print(f"  ⚠️  {archivo} NO encontrado (se omitirá)")
    
    return len(archivos_encontrados) > 0

def exportar_tabla_generica(nombre_archivo, nombre_tabla):
    """Exporta cualquier CSV a una tabla de Supabase"""
    print(f"\n📊 EXPORTANDO {nombre_archivo.upper()} → Tabla: {nombre_tabla}")
    print("=" * 60)
    
    archivo_csv = DATA_DIR / nombre_archivo
    
    if not archivo_csv.exists():
        print(f"⚠️  Archivo {nombre_archivo} no encontrado, omitiendo...")
        return False
    
    try:
        df = pd.read_csv(archivo_csv)
        
        if df.empty:
            print("⚠️  El archivo está vacío")
            return True
        
        print(f"📝 Total de registros: {len(df)}")
        
        # Convertir DataFrame a lista de diccionarios primero
        registros = df.to_dict('records')
        
        # Reemplazar NaN por None en cada registro (JSON no acepta NaN)
        import math
        for registro in registros:
            for key, value in registro.items():
                if isinstance(value, float) and math.isnan(value):
                    registro[key] = None
        
        # Conectar a Supabase
        supabase_handler = SupabaseHandler()
        supabase_handler.connect()  # Inicializar el cliente
        
        # Eliminar datos existentes en la tabla
        print(f"🗑️  Limpiando tabla {nombre_tabla}...")
        try:
            # Intentar eliminar todos los registros
            supabase_handler.client.table(nombre_tabla).delete().neq('id', -9999).execute()
        except Exception as e:
            print(f"  ⚠️  No se pudo limpiar la tabla (puede que no exista aún): {str(e)[:80]}")
        
        # Insertar registros en lotes de 100
        batch_size = 100
        total_batches = (len(registros) + batch_size - 1) // batch_size
        
        print(f"⬆️  Insertando datos en {total_batches} lote(s)...")
        
        exitos = 0
        for i in range(0, len(registros), batch_size):
            batch = registros[i:i+batch_size]
            batch_num = (i // batch_size) + 1  # Calcular batch_num ANTES del try
            try:
                supabase_handler.client.table(nombre_tabla).insert(batch).execute()
                exitos += len(batch)
                print(f"  ✅ Lote {batch_num}/{total_batches}: {len(batch)} registros insertados")
            except Exception as e:
                print(f"  ❌ Error en lote {batch_num}/{total_batches}: {str(e)[:100]}")
        
        print(f"\n✅ Exportación completada: {exitos}/{len(registros)} registros insertados")
        return True
        
    except Exception as e:
        print(f"❌ Error al exportar {nombre_archivo}: {e}")
        import traceback
        traceback.print_exc()
        return False

def exportar_respuestas_encuesta():
    """Exporta las respuestas de la encuesta desde CSV a Supabase"""
    print("\n📊 EXPORTANDO RESPUESTAS DE ENCUESTA")
    print("=" * 60)
    
    # Cargar CSV de respuestas
    respuestas_file = DATA_DIR / "encuesta_respuestas.csv"
    
    if not respuestas_file.exists():
        print("❌ No hay archivo de respuestas para exportar")
        return False
    
    try:
        df_respuestas = pd.read_csv(respuestas_file)
        
        if df_respuestas.empty:
            print("⚠️  El archivo de respuestas está vacío")
            return True
        
        print(f"📝 Total de registros encontrados: {len(df_respuestas)}")
        
        # Obtener participantes únicos
        participantes_unicos = df_respuestas['participante_email'].unique()
        print(f"👥 Total de participantes únicos: {len(participantes_unicos)}")
        
        # Cargar participantes para obtener nombres completos
        participantes_file = DATA_DIR / "participantes.csv"
        df_participantes = pd.read_csv(participantes_file)
        
        # Conectar a Supabase
        print("\n🔗 Conectando a Supabase...")
        supabase_handler = SupabaseHandler()
        
        # Mapear pregunta_id a pregunta_texto (reconstruir desde el CSV)
        print("\n📋 Procesando respuestas por participante...")
        
        exitos = 0
        errores = 0
        
        for i, email in enumerate(participantes_unicos, 1):
            try:
                # Obtener nombre completo del participante
                participante = df_participantes[
                    df_participantes['email'].str.lower() == email.lower()
                ]
                
                if participante.empty:
                    print(f"  ⚠️  [{i}/{len(participantes_unicos)}] {email} - No encontrado en participantes.csv")
                    errores += 1
                    continue
                
                nombre_completo = participante.iloc[0]['nombre_completo']
                
                # Obtener respuestas del participante
                respuestas_participante = df_respuestas[
                    df_respuestas['participante_email'].str.lower() == email.lower()
                ]
                
                # Convertir a formato dict {pregunta_id: respuesta}
                respuestas_dict = {}
                preguntas_dict = {}
                
                for _, row in respuestas_participante.iterrows():
                    pregunta_id = int(row['pregunta_id'])
                    respuesta = row['respuesta']
                    
                    # Para preguntas_dict, usamos un texto genérico ya que no lo tenemos en el CSV
                    pregunta_texto = f"Pregunta {pregunta_id}"
                    
                    respuestas_dict[pregunta_id] = respuesta
                    preguntas_dict[pregunta_id] = pregunta_texto
                
                # Guardar en Supabase
                supabase_handler.guardar_respuestas(
                    email=email,
                    nombre_completo=nombre_completo,
                    respuestas=respuestas_dict,
                    preguntas_dict=preguntas_dict
                )
                
                print(f"  ✅ [{i}/{len(participantes_unicos)}] {nombre_completo} ({email}) - {len(respuestas_dict)} respuestas")
                exitos += 1
                
            except Exception as e:
                print(f"  ❌ [{i}/{len(participantes_unicos)}] {email} - Error: {str(e)}")
                errores += 1
        
        print("\n" + "=" * 60)
        print(f"✅ Exportación completada: {exitos} exitosos, {errores} errores")
        return True
        
    except Exception as e:
        print(f"❌ Error general al exportar respuestas: {e}")
        import traceback
        traceback.print_exc()
        return False

def verificar_exportacion():
    """Verifica que los datos se hayan exportado correctamente"""
    print("\n🔍 VERIFICANDO DATOS EN SUPABASE")
    print("=" * 60)
    
    try:
        supabase_handler = SupabaseHandler()
        estadisticas = supabase_handler.obtener_estadisticas()
        
        print(f"\n📊 Estadísticas de Supabase:")
        print(f"  Total de respuestas: {estadisticas['total_respuestas']}")
        print(f"  Total de participantes: {estadisticas['total_participantes']}")
        print(f"  Última respuesta: {estadisticas['ultima_respuesta']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar exportación: {e}")
        return False

def main():
    """Función principal"""
    print("\n" + "=" * 60)
    print("🚀 EXPORTACIÓN DE DATOS CSV A SUPABASE")
    print("=" * 60)
    
    # Verificar configuración
    print("\n🔧 Verificando configuración...")
    
    if not os.getenv('SUPABASE_URL'):
        print("❌ SUPABASE_URL no está configurado en .env")
        return
    
    if not os.getenv('SUPABASE_KEY'):
        print("❌ SUPABASE_KEY no está configurado en .env")
        return
    
    print("  ✅ Variables de entorno configuradas")
    
    # Verificar archivos
    if not verificar_archivos():
        print("\n❌ Faltan archivos necesarios. Abortando exportación.")
        return
    
    # Confirmar antes de exportar
    print("\n⚠️  ADVERTENCIA:")
    print("  - Este script eliminará los datos existentes en Supabase de cada participante")
    print("  - Los reemplazará con los datos del CSV local")
    print("  - Esta operación no se puede deshacer")
    
    respuesta = input("\n¿Deseas continuar? (escribe 'SI' para confirmar): ")
    
    if respuesta.upper() != 'SI':
        print("\n❌ Exportación cancelada por el usuario")
        return
    
    # Exportar todas las tablas
    print("\n" + "=" * 60)
    print("EXPORTANDO DATOS A SUPABASE")
    print("=" * 60)
    
    # 1. Exportar participantes
    exportar_tabla_generica("participantes.csv", "participantes")
    
    # 2. Exportar asistencias
    exportar_tabla_generica("asistencias.csv", "asistencias")
    
    # 3. Exportar actividades
    exportar_tabla_generica("actividades.csv", "actividades")
    
    # 4. Exportar equipos
    exportar_tabla_generica("equipos_concurso.csv", "equipos_concurso")
    
    # 5. Exportar respuestas de encuesta
    exportar_respuestas_encuesta()
    
    # Verificar exportación
    verificar_exportacion()
    
    print("\n" + "=" * 60)
    print("✅ PROCESO COMPLETADO")
    print("=" * 60)
    print("\n💡 Próximos pasos:")
    print("  1. Ve a Supabase Dashboard → Table Editor")
    print("  2. Verifica que los datos estén correctos en todas las tablas:")
    print("     - participantes")
    print("     - asistencias")
    print("     - actividades")
    print("     - equipos_concurso")
    print("     - encuesta_respuestas")
    print("  3. Ahora puedes desplegar tu app en Streamlit Cloud")

if __name__ == "__main__":
    main()
