"""
Script de prueba para verificar la conexión con Supabase
Ejecuta este script para verificar que todo esté configurado correctamente
"""

from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

print("=" * 60)
print("🔍 VERIFICACIÓN DE CONFIGURACIÓN DE SUPABASE")
print("=" * 60)

# Verificar que las variables estén definidas
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

print("\n1. Variables de entorno:")
print(f"   SUPABASE_URL: {'✅ Configurada' if supabase_url else '❌ NO configurada'}")
if supabase_url:
    print(f"   Valor: {supabase_url}")

print(f"   SUPABASE_KEY: {'✅ Configurada' if supabase_key else '❌ NO configurada'}")
if supabase_key:
    # Mostrar solo los primeros 20 caracteres por seguridad
    print(f"   Valor: {supabase_key[:20]}...")

# Intentar conectar con Supabase
if supabase_url and supabase_key:
    print("\n2. Intentando conectar con Supabase...")
    try:
        from supabase import create_client, Client
        
        supabase: Client = create_client(supabase_url, supabase_key)
        print("   ✅ Cliente de Supabase creado exitosamente")
        
        # Intentar hacer una consulta simple
        print("\n3. Verificando tabla 'encuesta_respuestas'...")
        try:
            # Intentar contar registros (debería funcionar aunque esté vacía)
            response = supabase.table('encuesta_respuestas').select('*', count='exact').limit(1).execute()
            count = response.count if hasattr(response, 'count') else 0
            print(f"   ✅ Tabla encontrada. Registros actuales: {count}")
            
            print("\n" + "=" * 60)
            print("✅ CONFIGURACIÓN CORRECTA - TODO FUNCIONA")
            print("=" * 60)
            print("\n💡 Siguiente paso:")
            print("   1. Ejecuta: streamlit run app.py")
            print("   2. Completa la encuesta de prueba")
            print("   3. Ve a Supabase Dashboard → Table Editor")
            print("   4. Verifica que los datos aparezcan en la tabla")
            
        except Exception as e:
            error_str = str(e)
            if "relation" in error_str.lower() or "does not exist" in error_str.lower():
                print("   ⚠️  La tabla 'encuesta_respuestas' NO existe")
                print("\n📝 Debes crear la tabla en Supabase:")
                print("   1. Ve a: https://supabase.com/dashboard")
                print("   2. Abre tu proyecto")
                print("   3. Ve a: SQL Editor")
                print("   4. Ejecuta el SQL de OPCION_SIMPLE_SUPABASE.md")
            else:
                print(f"   ❌ Error al consultar tabla: {e}")
        
    except ImportError:
        print("   ❌ La librería 'supabase' no está instalada")
        print("\n📦 Ejecuta: pip install supabase")
    except Exception as e:
        print(f"   ❌ Error al conectar: {e}")
        print("\n🔧 Verifica que:")
        print("   - SUPABASE_URL sea correcta (debe empezar con https://)")
        print("   - SUPABASE_KEY sea la 'anon public' key (no la service_role)")
else:
    print("\n" + "=" * 60)
    print("❌ CONFIGURACIÓN INCOMPLETA")
    print("=" * 60)
    print("\n📝 Para configurar Supabase:")
    print("   1. Ve a: https://supabase.com/dashboard")
    print("   2. Abre tu proyecto (o créalo si no existe)")
    print("   3. Ve a: Settings → API")
    print("   4. Copia:")
    print("      - Project URL → SUPABASE_URL en .env")
    print("      - anon public → SUPABASE_KEY en .env")
    print("\n💡 Consulta OPCION_SIMPLE_SUPABASE.md para más detalles")

print("\n" + "=" * 60)
