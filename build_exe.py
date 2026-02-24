import PyInstaller.__main__
from pathlib import Path

# Obtener el directorio actual
current_dir = Path(__file__).parent

print("="*50)
print("  Creando English Memory v1.3.2")
print("="*50)
print()

PyInstaller.__main__.run([
    'diccionario_gui.py',
    '--name=English Memory',
    '--onefile',
    '--windowed',
    '--noconsole',
    '--hidden-import=pyttsx3',
    '--hidden-import=pyttsx3.drivers',
    '--hidden-import=pyttsx3.drivers.sapi5',
    '--collect-all=pyttsx3',
    '--clean',
    f'--distpath={current_dir / "dist"}',
    f'--workpath={current_dir / "build"}',
    f'--specpath={current_dir}',
])

print()
print("="*50)
print("  Ejecutable creado exitosamente")
print("="*50)
print()
print(f"Ubicacion: {current_dir / 'dist' / 'English Memory.exe'}")
print()
print("Proximos pasos:")
print("   1. Ve a la carpeta 'dist'")
print("   2. Ejecuta 'English Memory.exe'")
print("   3. Crea un acceso directo en tu Escritorio")
print()
print("Tus datos se guardan en:")
print("   %LOCALAPPDATA%\\DiccionarioPersonal")
print()
print("Soporte: administrador@agilizesoluciones.com | +54 11 6168-2555")
print()
