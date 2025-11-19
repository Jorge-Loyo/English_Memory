"""
Script de verificación del proyecto English Memory
Verifica que todos los archivos necesarios estén presentes y correctos
"""

import os
from pathlib import Path

def verificar_archivos():
    """Verifica que todos los archivos necesarios existan"""
    archivos_requeridos = [
        'diccionario_gui.py',
        'diccionario.py',
        'build_exe.py',
        'build_linux.sh',
        'requirements.txt',
        'README.md',
        'LICENSE',
        '.gitignore',
        'INSTALL.md',
        'CONTRIBUTING.md',
        'CHANGELOG.md',
        'QUICK_START.md',
        'setup.py',
        'ESTRUCTURA_PROYECTO.md',
        'git_commands.txt'
    ]
    
    print("[*] Verificando archivos del proyecto...\n")
    
    faltantes = []
    presentes = []
    
    for archivo in archivos_requeridos:
        if Path(archivo).exists():
            presentes.append(archivo)
            print(f"[OK] {archivo}")
        else:
            faltantes.append(archivo)
            print(f"[FALTA] {archivo}")
    
    print(f"\n[RESUMEN]")
    print(f"   Presentes: {len(presentes)}/{len(archivos_requeridos)}")
    print(f"   Faltantes: {len(faltantes)}/{len(archivos_requeridos)}")
    
    if faltantes:
        print(f"\n[ADVERTENCIA] Archivos faltantes:")
        for archivo in faltantes:
            print(f"   - {archivo}")
        return False
    else:
        print(f"\n[EXITO] Todos los archivos estan presentes!")
        return True

def verificar_contenido():
    """Verifica el contenido básico de archivos importantes"""
    print("\n[*] Verificando contenido de archivos...\n")
    
    verificaciones = []
    
    # Verificar README
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            contenido = f.read()
            if 'English Memory' in contenido and 'v1.0' in contenido:
                print("[OK] README.md contiene informacion correcta")
                verificaciones.append(True)
            else:
                print("[ERROR] README.md no contiene informacion esperada")
                verificaciones.append(False)
    except:
        print("[ERROR] Error al leer README.md")
        verificaciones.append(False)
    
    # Verificar requirements.txt
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            contenido = f.read()
            if 'pyinstaller' in contenido.lower():
                print("[OK] requirements.txt contiene dependencias")
                verificaciones.append(True)
            else:
                print("[ERROR] requirements.txt no contiene pyinstaller")
                verificaciones.append(False)
    except:
        print("[ERROR] Error al leer requirements.txt")
        verificaciones.append(False)
    
    # Verificar LICENSE
    try:
        with open('LICENSE', 'r', encoding='utf-8') as f:
            contenido = f.read()
            if 'MIT' in contenido:
                print("[OK] LICENSE contiene licencia MIT")
                verificaciones.append(True)
            else:
                print("[ERROR] LICENSE no contiene licencia MIT")
                verificaciones.append(False)
    except:
        print("[ERROR] Error al leer LICENSE")
        verificaciones.append(False)
    
    return all(verificaciones)

def verificar_gitignore():
    """Verifica que .gitignore esté configurado correctamente"""
    print("\n[*] Verificando .gitignore...\n")
    
    try:
        with open('.gitignore', 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        patrones_importantes = [
            ('__pycache__', ['__pycache__']),
            ('*.pyc', ['*.pyc', '*.py[cod]']),
            ('dist/', ['dist/']),
            ('build/', ['build/']),
            ('palabras.json', ['palabras.json'])
        ]
        
        todos_presentes = True
        for nombre, variantes in patrones_importantes:
            encontrado = any(v in contenido for v in variantes)
            if encontrado:
                print(f"[OK] {nombre}")
            else:
                print(f"[FALTA] {nombre}")
                todos_presentes = False
        
        return todos_presentes
    except:
        print("[ERROR] Error al leer .gitignore")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("  VERIFICACIÓN DEL PROYECTO ENGLISH MEMORY v1.0")
    print("=" * 60)
    print()
    
    # Verificar archivos
    archivos_ok = verificar_archivos()
    
    # Verificar contenido
    contenido_ok = verificar_contenido()
    
    # Verificar gitignore
    gitignore_ok = verificar_gitignore()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("  RESUMEN FINAL")
    print("=" * 60)
    
    if archivos_ok and contenido_ok and gitignore_ok:
        print("\n[EXITO] PROYECTO LISTO PARA SUBIR A GIT!")
        print("\nProximos pasos:")
        print("   1. git init")
        print("   2. git add .")
        print("   3. git commit -m 'feat: Initial release v1.0.0'")
        print("   4. git remote add origin <tu-repo-url>")
        print("   5. git push -u origin main")
        print("\nVer git_commands.txt para mas detalles")
    else:
        print("\n[ADVERTENCIA] HAY PROBLEMAS QUE CORREGIR")
        print("\nRevisa los errores arriba y corrígelos antes de subir a Git")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
