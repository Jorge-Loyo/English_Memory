#!/bin/bash

echo "=================================================="
echo "  Creando English Memory v1.3.2 para Linux"
echo "=================================================="
echo ""

# Instalar pyinstaller si no está instalado
pip3 install pyinstaller

# Crear ejecutable
pyinstaller diccionario_gui.py \
    --name="English Memory" \
    --onefile \
    --windowed \
    --clean

echo ""
echo "=================================================="
echo "  Ejecutable creado exitosamente"
echo "=================================================="
echo ""
echo "Ubicación: ./dist/English Memory"
echo ""
echo "Próximos pasos:"
echo "   1. Ve a la carpeta 'dist'"
echo "   2. Ejecuta './English Memory'"
echo "   3. O crea un acceso directo en tu escritorio"
echo ""
echo "Tus datos se guardan en:"
echo "   ~/.local/share/DiccionarioPersonal"
echo ""
echo "Soporte: administrador@agilizesoluciones.com | +54 11 6168-2555"
echo ""
