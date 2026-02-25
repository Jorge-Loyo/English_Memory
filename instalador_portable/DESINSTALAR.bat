@echo off
echo ==========================================
echo   English Memory v1.4.0 - Desinstalador
echo ==========================================
echo.

set "INSTALL_DIR=%LOCALAPPDATA%\EnglishMemory"
set "DESKTOP=%USERPROFILE%\Desktop"
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"

echo ADVERTENCIA: Se eliminaran los siguientes elementos:
echo   - Programa: %INSTALL_DIR%
echo   - Accesos directos
echo.
echo NOTA: Tus datos de vocabulario se mantendran en:
echo   %INSTALL_DIR%\palabras.json
echo.
set /p CONFIRM="¿Deseas continuar? (S/N): "

if /i not "%CONFIRM%"=="S" (
    echo.
    echo Desinstalacion cancelada.
    pause
    exit /b
)

echo.
echo Desinstalando English Memory...
echo.

REM Eliminar accesos directos
if exist "%DESKTOP%\English Memory.lnk" del "%DESKTOP%\English Memory.lnk"
if exist "%START_MENU%\English Memory.lnk" del "%START_MENU%\English Memory.lnk"

REM Eliminar ejecutable (mantener datos)
if exist "%INSTALL_DIR%\EnglishMemory.exe" del "%INSTALL_DIR%\EnglishMemory.exe"

echo.
echo ✓ Desinstalacion completada
echo.
echo   - Ejecutable eliminado
echo   - Accesos directos eliminados
echo   - Datos de vocabulario conservados
echo.
pause
