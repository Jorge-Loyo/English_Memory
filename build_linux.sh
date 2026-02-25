#!/bin/bash

echo "=================================================="
echo "  Creando English Memory v1.4.0 para Linux"
echo "=================================================="
echo ""

# Instalar dependencias
echo "Instalando dependencias..."
pip3 install -r requirements.txt
pip3 install pyinstaller

echo ""
echo "Creando ejecutable..."

# Crear ejecutable usando el spec file
pyinstaller EnglishMemory.spec --clean

# Renombrar ejecutable para Linux
mv dist/EnglishMemory_Modular dist/EnglishMemory

echo ""
echo "=================================================="
echo "  Ejecutable creado exitosamente"
echo "=================================================="
echo ""
echo "Ubicación: ./dist/EnglishMemory"
echo ""
echo "Próximos pasos:"
echo "   1. Ve a la carpeta 'dist'"
echo "   2. Ejecuta './EnglishMemory'"
echo "   3. O crea un acceso directo en tu escritorio"
echo ""
echo "Tus datos se guardan en:"
echo "   ~/.local/share/EnglishMemory/data"
echo ""
echo "Contacto: Jorgenayati@gmail.com"
echo ""
