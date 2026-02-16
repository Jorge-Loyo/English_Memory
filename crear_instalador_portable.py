"""
Crea un paquete portable de English Memory v1.3 para instalar en otras PCs
"""
import os
import shutil
from pathlib import Path

def crear_instalador():
    # Crear carpeta del instalador
    instalador_dir = Path("instalador_portable")
    if instalador_dir.exists():
        shutil.rmtree(instalador_dir)
    instalador_dir.mkdir()
    
    # Copiar ejecutable
    exe_source = Path("dist/English Memory.exe")
    if not exe_source.exists():
        print("Error: No se encuentra 'English Memory.exe' en la carpeta dist/")
        print("Ejecuta primero: py build_exe.py")
        return
    
    shutil.copy2(exe_source, instalador_dir / "English Memory.exe")
    
    # Crear script de instalación
    install_script = instalador_dir / "INSTALAR.bat"
    install_script.write_text('''@echo off
echo ========================================
echo   English Memory v1.0 - Instalador
echo ========================================
echo.

set "INSTALL_DIR=%LOCALAPPDATA%\\EnglishMemory"
set "DESKTOP=%USERPROFILE%\\Desktop"
set "START_MENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"

echo Instalando English Memory...
echo.

REM Crear directorio de instalacion
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copiar ejecutable
copy /Y "English Memory.exe" "%INSTALL_DIR%\\English Memory.exe" >nul

REM Crear acceso directo en escritorio
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESKTOP%\\English Memory.lnk'); $s.TargetPath = '%INSTALL_DIR%\\English Memory.exe'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Save()"

REM Crear acceso directo en menu inicio
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%START_MENU%\\English Memory.lnk'); $s.TargetPath = '%INSTALL_DIR%\\English Memory.exe'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Save()"

echo.
echo ✓ Instalacion completada exitosamente
echo.
echo   - Ejecutable: %INSTALL_DIR%
echo   - Acceso directo en Escritorio
echo   - Acceso directo en Menu Inicio
echo.
pause
''', encoding='utf-8')
    
    # Crear script de desinstalación
    uninstall_script = instalador_dir / "DESINSTALAR.bat"
    uninstall_script.write_text('''@echo off
echo ========================================
echo   English Memory - Desinstalador
echo ========================================
echo.

set "INSTALL_DIR=%LOCALAPPDATA%\\EnglishMemory"
set "DATA_DIR=%LOCALAPPDATA%\\DiccionarioPersonal"
set "DESKTOP=%USERPROFILE%\\Desktop"
set "START_MENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"

echo ATENCION: Esto eliminara English Memory de tu PC
echo.
set /p confirm="¿Deseas continuar? (S/N): "
if /i not "%confirm%"=="S" goto :end

echo.
echo Desinstalando...

REM Eliminar ejecutable
if exist "%INSTALL_DIR%" rmdir /S /Q "%INSTALL_DIR%"

REM Eliminar accesos directos
if exist "%DESKTOP%\\English Memory.lnk" del /Q "%DESKTOP%\\English Memory.lnk"
if exist "%START_MENU%\\English Memory.lnk" del /Q "%START_MENU%\\English Memory.lnk"

echo.
echo ✓ Desinstalacion completada
echo.
echo NOTA: Tus datos de vocabulario se mantienen en:
echo %DATA_DIR%
echo Si deseas eliminarlos, hazlo manualmente.
echo.

:end
pause
''', encoding='utf-8')
    
    # Crear README
    readme = instalador_dir / "LEEME.txt"
    readme.write_text('''╔════════════════════════════════════════════════════════════╗
║          ENGLISH MEMORY v1.0 - INSTALADOR PORTABLE         ║
╚════════════════════════════════════════════════════════════╝

CONTENIDO:
----------
• English Memory.exe  - Aplicación principal
• INSTALAR.bat        - Instalador automático
• DESINSTALAR.bat     - Desinstalador
• LEEME.txt           - Este archivo


INSTRUCCIONES DE INSTALACIÓN:
------------------------------
1. Copia esta carpeta completa a un pendrive
2. En la PC de destino, ejecuta "INSTALAR.bat"
3. La aplicación se instalará automáticamente y creará
   accesos directos en el Escritorio y Menú Inicio


REQUISITOS:
-----------
• Windows 7 o superior
• No requiere Python ni dependencias adicionales
• Aproximadamente 15 MB de espacio en disco


UBICACIONES:
------------
• Programa: %LOCALAPPDATA%\\EnglishMemory
• Datos: %LOCALAPPDATA%\\DiccionarioPersonal


DESINSTALACIÓN:
---------------
Ejecuta "DESINSTALAR.bat" o elimina manualmente:
• Carpeta: %LOCALAPPDATA%\\EnglishMemory
• Accesos directos del Escritorio y Menú Inicio


SOPORTE:
--------
Email: administrador@agilizesoluciones.com
Tel: +54 11 6168-2555


═══════════════════════════════════════════════════════════════
Desarrollado por Agilize Soluciones | Licencia MIT
═══════════════════════════════════════════════════════════════
''', encoding='utf-8')
    
    print("Instalador portable creado exitosamente")
    print(f"\nCarpeta: {instalador_dir.absolute()}")
    print(f"Tamanio: ~{os.path.getsize(instalador_dir / 'English Memory.exe') / 1024 / 1024:.1f} MB")
    print("\nContenido:")
    print("   - English Memory.exe")
    print("   - INSTALAR.bat")
    print("   - DESINSTALAR.bat")
    print("   - LEEME.txt")
    print("\nCopia la carpeta 'instalador_portable' completa al pendrive")

if __name__ == "__main__":
    crear_instalador()
