import json
from pathlib import Path

ARCHIVO_DATOS = Path('palabras.json')

# Límites de validación
MAX_PALABRA = 100
MAX_SIGNIFICADO = 500
MAX_PRONUNCIACION = 200

def cargar_datos():
    if ARCHIVO_DATOS.exists():
        try:
            with open(ARCHIVO_DATOS, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError, PermissionError) as e:
            print(f"Error al cargar datos: {e}")
            return {}
    return {}

def guardar_datos(datos):
    try:
        with open(ARCHIVO_DATOS, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    except (IOError, PermissionError) as e:
        print(f"Error al guardar datos: {e}")
        return False
    return True

def agregar_palabra(datos):
    palabra = input("Palabra en inglés: ").strip()
    if not palabra or len(palabra) > MAX_PALABRA:
        print(f"Palabra inválida (máximo {MAX_PALABRA} caracteres)")
        return
    
    significado = input("Significado en español: ").strip()
    if not significado or len(significado) > MAX_SIGNIFICADO:
        print(f"Significado inválido (máximo {MAX_SIGNIFICADO} caracteres)")
        return
    
    if palabra in datos:
        print(f"'{palabra}' ya está en el vocabulario")
        return
    
    datos[palabra] = {'significado': significado}
    
    if guardar_datos(datos):
        print(f"✓ Palabra '{palabra}' guardada")
    else:
        print(f"✗ Error al guardar '{palabra}'")

def consultar_vocabulario(datos):
    if not datos:
        print("No hay palabras en el vocabulario")
        return
    
    print("\n1. Ver todas las palabras")
    print("2. Buscar palabra específica")
    opcion = input("Opción: ").strip()
    
    if opcion == '1':
        print(f"\n{'INGLÉS':<20} {'ESPAÑOL':<30} {'PRONUNCIACIÓN':<20}")
        print("-" * 70)
        for palabra in sorted(datos.keys()):
            significado = datos[palabra].get('significado', '')
            pronunciacion = datos[palabra].get('pronunciacion', '-')
            print(f"{palabra:<20} {significado:<30} {pronunciacion:<20}")
    elif opcion == '2':
        palabra = input("Palabra a buscar: ").strip()
        if palabra in datos:
            print(f"\nPalabra: {palabra}")
            print(f"Significado: {datos[palabra].get('significado', '-')}")
            print(f"Pronunciación: {datos[palabra].get('pronunciacion', '-')}")
        else:
            print(f"'{palabra}' no encontrada")

def gestionar_pronunciacion(datos):
    if not datos:
        print("No hay palabras en el vocabulario")
        return
    
    print("\n1. Agregar/actualizar pronunciación")
    print("2. Ver pronunciaciones")
    opcion = input("Opción: ").strip()
    
    if opcion == '1':
        palabra = input("Palabra en inglés: ").strip()
        if palabra not in datos:
            print(f"'{palabra}' no existe en el vocabulario")
            return
        
        pronunciacion = input("Pronunciación: ").strip()
        if not pronunciacion or len(pronunciacion) > MAX_PRONUNCIACION:
            print(f"Pronunciación inválida (máximo {MAX_PRONUNCIACION} caracteres)")
            return
        
        datos[palabra]['pronunciacion'] = pronunciacion
        if guardar_datos(datos):
            print(f"✓ Pronunciación de '{palabra}' guardada")
        else:
            print(f"✗ Error al guardar pronunciación de '{palabra}'")
    
    elif opcion == '2':
        print(f"\n{'INGLÉS':<20} {'PRONUNCIACIÓN':<30}")
        print("-" * 50)
        for palabra in sorted(datos.keys()):
            pronunciacion = datos[palabra].get('pronunciacion', '-')
            print(f"{palabra:<20} {pronunciacion:<30}")

def main():
    datos = cargar_datos()
    
    while True:
        print("\n=== DICCIONARIO PERSONAL ===")
        print("1. Agregar palabra")
        print("2. Consultar vocabulario")
        print("3. Pronunciación")
        print("4. Salir")
        
        opcion = input("\nOpción: ").strip()
        
        if opcion == '1':
            agregar_palabra(datos)
        elif opcion == '2':
            consultar_vocabulario(datos)
        elif opcion == '3':
            gestionar_pronunciacion(datos)
        elif opcion == '4':
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida")

if __name__ == '__main__':
    main()
