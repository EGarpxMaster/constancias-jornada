"""
Script de inicialización del sistema
Crea las carpetas necesarias y verifica la estructura
"""
from pathlib import Path

def crear_estructura():
    """Crea la estructura de carpetas necesaria"""
    
    ROOT = Path(__file__).resolve().parent
    
    # Carpetas a crear
    carpetas = [
        ROOT / "Multipage App" / "datos",
        ROOT / "assets" / "fonts",
        ROOT / "assets" / "plantillas",
        ROOT / "pages",
    ]
    
    for carpeta in carpetas:
        carpeta.mkdir(parents=True, exist_ok=True)
        print(f"✅ Carpeta creada/verificada: {carpeta}")
    
    # Verificar archivos requeridos
    archivos_requeridos = [
        ROOT / "Multipage App" / "datos" / "participantes.csv",
        ROOT / "Multipage App" / "datos" / "asistencias.csv",
    ]
    
    for archivo in archivos_requeridos:
        if archivo.exists():
            print(f"✅ Archivo encontrado: {archivo.name}")
        else:
            print(f"⚠️  Archivo faltante: {archivo.name}")
    
    # Verificar fuentes
    fuentes = [
        ROOT / "assets" / "fonts" / "OldStandardTT-Bold.ttf",
        ROOT / "assets" / "fonts" / "OldStandardTT-Italic.ttf",
        ROOT / "assets" / "fonts" / "OldStandardTT-Regular.ttf",
    ]
    
    for fuente in fuentes:
        if fuente.exists():
            print(f"✅ Fuente encontrada: {fuente.name}")
        else:
            print(f"⚠️  Fuente faltante: {fuente.name}")
    
    # Verificar plantillas
    plantillas = [
        "Participacion_general.pdf",
        "Constancia_mundialito.pdf",
        "W1.pdf", "W2.pdf", "W3.pdf", "W4.pdf", "W5.pdf", "W6.pdf"
    ]
    
    for plantilla in plantillas:
        archivo_plantilla = ROOT / "assets" / "plantillas" / plantilla
        if archivo_plantilla.exists():
            print(f"✅ Plantilla encontrada: {plantilla}")
        else:
            print(f"ℹ️  Plantilla opcional faltante: {plantilla}")
    
    print("\n" + "="*60)
    print("✨ Verificación completada")
    print("="*60)

if __name__ == "__main__":
    crear_estructura()
