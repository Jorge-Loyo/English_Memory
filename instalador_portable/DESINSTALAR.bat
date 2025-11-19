@echo off
echo ========================================
echo   English Memory - Desinstalador
echo ========================================
echo.

set "INSTALL_DIR=%LOCALAPPDATA%\EnglishMemory"
set "DATA_DIR=%LOCALAPPDATA%\DiccionarioPersonal"
set "DESKTOP=%USERPROFILE%\Desktop"
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"

echo ATENCION: Esto eliminara English Memory de tu PC
echo.
set /p confirm="¿Deseas continuar? (S/N): "
if /i not "%confirm%"=="S" goto :end

echo.
echo Desinstalando...

REM Eliminar ejecutable
if exist "%INSTALL_DIR%" rmdir /S /Q "%INSTALL_DIR%"

REM Eliminar accesos directos
if exist "%DESKTOP%\English Memory.lnk" del /Q "%DESKTOP%\English Memory.lnk"
if exist "%START_MENU%\English Memory.lnk" del /Q "%START_MENU%\English Memory.lnk"

echo.
echo ✓ Desinstalacion completada
echo.
echo NOTA: Tus datos de vocabulario se mantienen en:
echo %DATA_DIR%
echo Si deseas eliminarlos, hazlo manualmente.
echo.

:end
pause
