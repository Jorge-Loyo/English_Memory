@echo off
cls
echo.
echo ================================================
echo   DICCIONARIO PERSONAL - Crear Ejecutable
echo ================================================
echo.
echo Preparando entorno...
echo.

echo Instalando PyInstaller...
python -m pip install pyinstaller --quiet --disable-pip-version-check
if errorlevel 1 (
    echo Error al instalar PyInstaller
    echo.
    echo Intenta manualmente:
    echo   python -m pip install pyinstaller
    pause
    exit /b 1
)
echo PyInstaller instalado correctamente
echo.

echo Generando ejecutable (esto puede tardar 1-2 minutos)...
echo.
python build_exe.py
if errorlevel 1 (
    echo.
    echo Error al crear el ejecutable
    pause
    exit /b 1
)

echo.
echo ================================================
echo            PROCESO COMPLETADO
echo ================================================
echo.
echo El ejecutable esta en: dist\Diccionario Personal.exe
echo.
echo Proximos pasos:
echo   1. Ve a la carpeta 'dist'
echo   2. Ejecuta 'Diccionario Personal.exe'
echo   3. Crea un acceso directo en tu Escritorio
echo.
pause
