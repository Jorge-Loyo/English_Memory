@echo off
echo ========================================
echo   English Memory v1.1 - Instalador
echo ========================================
echo.

set "INSTALL_DIR=%LOCALAPPDATA%\EnglishMemory"
set "DESKTOP=%USERPROFILE%\Desktop"
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"

echo Instalando English Memory...
echo.

REM Crear directorio de instalacion
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copiar ejecutable
copy /Y "English Memory.exe" "%INSTALL_DIR%\English Memory.exe" >nul

REM Crear acceso directo en escritorio
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%DESKTOP%\English Memory.lnk'); $s.TargetPath = '%INSTALL_DIR%\English Memory.exe'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Save()"

REM Crear acceso directo en menu inicio
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%START_MENU%\English Memory.lnk'); $s.TargetPath = '%INSTALL_DIR%\English Memory.exe'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Save()"

echo.
echo ✓ Instalacion completada exitosamente
echo.
echo   - Ejecutable: %INSTALL_DIR%
echo   - Acceso directo en Escritorio
echo   - Acceso directo en Menu Inicio
echo.
pause
