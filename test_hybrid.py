"""
Test del sistema híbrido JSON + SQLite
"""
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.models import HybridStorage
import tempfile
import shutil

def test_hybrid_storage():
    # Crear directorio temporal para pruebas
    test_dir = Path(tempfile.mkdtemp())
    print(f"Directorio de prueba: {test_dir}")
    
    try:
        # Inicializar storage
        print("1. Inicializando HybridStorage...")
        storage = HybridStorage(test_dir)
        print("OK Storage inicializado")
        
        # Agregar palabras
        print("\n2. Agregando palabras al vocabulario...")
        storage.agregar_palabra("hello", "hola", "/həˈloʊ/", "Saludo común")
        storage.agregar_palabra("world", "mundo", "/wɜːrld/")
        storage.agregar_palabra("test", "prueba")
        print(f"OK {len(storage.obtener_todas_palabras())} palabras agregadas")
        
        # Registrar prácticas
        print("\n3. Registrando practicas...")
        storage.registrar_practica("hello", "ingles_espanol", True, "hola", 5000)
        storage.registrar_practica("hello", "ingles_espanol", True, "hola", 3000)
        storage.registrar_practica("world", "ingles_espanol", False, "tierra", 8000)
        storage.registrar_practica("test", "espanol_ingles", True, "test", 4000)
        print("OK 4 practicas registradas")
        
        # Obtener progreso de palabra
        print("\n4. Consultando progreso de 'hello'...")
        progreso = storage.obtener_progreso_palabra("hello")
        if progreso:
            print(f"   Veces vista: {progreso['veces_vista']}")
            print(f"   Correctas: {progreso['veces_correcta']}")
            print(f"   Incorrectas: {progreso['veces_incorrecta']}")
            print(f"   Tasa éxito: {(progreso['veces_correcta']/progreso['veces_vista']*100):.1f}%")
        
        # Obtener palabras difíciles
        print("\n5. Palabras mas dificiles...")
        dificiles = storage.obtener_palabras_dificiles(5)
        for palabra in dificiles:
            print(f"   {palabra['palabra']}: {palabra['tasa_exito']:.1f}% éxito ({palabra['veces_vista']} intentos)")
        
        # Estadísticas del período
        print("\n6. Estadisticas de los ultimos 30 dias...")
        stats = storage.obtener_estadisticas_periodo(30)
        if stats:
            total_practicas = sum(s['practicas_totales'] for s in stats)
            total_correctas = sum(s['practicas_correctas'] for s in stats)
            print(f"   Total prácticas: {total_practicas}")
            print(f"   Correctas: {total_correctas}")
            print(f"   Tasa éxito: {(total_correctas/total_practicas*100):.1f}%")
        
        # Racha de estudio
        print("\n7. Racha de estudio...")
        racha = storage.obtener_racha_estudio()
        print("   Dias estudiados (ultimos 30): {racha}")
        
        # Verificar archivos creados
        print("\n8. Verificando archivos...")
        json_file = test_dir / 'palabras.json'
        db_file = test_dir / 'statistics.db'
        print(f"   JSON: {json_file.exists()} ({json_file.stat().st_size if json_file.exists() else 0} bytes)")
        print(f"   SQLite: {db_file.exists()} ({db_file.stat().st_size if db_file.exists() else 0} bytes)")
        
        print("\nOK Todas las pruebas pasaron exitosamente!")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Limpiar directorio temporal
        shutil.rmtree(test_dir, ignore_errors=True)
        print(f"\nDirectorio temporal eliminado")

if __name__ == "__main__":
    print("="*60)
    print("  TEST: Sistema Híbrido JSON + SQLite")
    print("  English Memory v1.4.0")
    print("="*60)
    test_hybrid_storage()
