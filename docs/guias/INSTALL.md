# 🚀 Guía de Instalación - English Memory v1.0

## 📋 Requisitos Previos

### Windows
- Python 3.7 o superior
- Windows 10/11

### Linux
- Python 3.7 o superior
- tkinter (python3-tk)

## 💻 Instalación

### Opción 1: Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/english-memory.git
cd english-memory
```

### Opción 2: Descargar ZIP

1. Click en "Code" → "Download ZIP"
2. Extraer el archivo
3. Abrir terminal en la carpeta extraída

## 🔧 Configuración

### Windows

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Ejecutar la aplicación:**
```bash
python diccionario_gui.py
```

3. **Crear ejecutable (opcional):**
```bash
python build_exe.py
```
El ejecutable estará en `dist/English Memory.exe`

### Linux

1. **Instalar tkinter:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

2. **Instalar dependencias:**
```bash
pip3 install -r requirements.txt
```

3. **Ejecutar la aplicación:**
```bash
python3 diccionario_gui.py
```

4. **Crear ejecutable (opcional):**
```bash
chmod +x build_linux.sh
./build_linux.sh
```
El ejecutable estará en `dist/English Memory`

## 📁 Ubicación de Datos

Los datos se guardan automáticamente en:

- **Windows:** `%LOCALAPPDATA%\DiccionarioPersonal\palabras.json`
- **Linux:** `~/.local/share/DiccionarioPersonal/palabras.json`

## ✅ Verificar Instalación

Ejecuta la aplicación y verifica que:
- La ventana se abre correctamente
- Puedes agregar una palabra de prueba
- Los datos se guardan correctamente

## 🐛 Solución de Problemas

### Error: "No module named tkinter"
```bash
# Linux
sudo apt-get install python3-tk
```

### Error: "No se encuentra Python"
Instala Python desde [python.org](https://www.python.org/downloads/)

### Error de permisos en Linux
```bash
chmod +x build_linux.sh
chmod +x diccionario_gui.py
```

## 📞 Soporte

- 📧 Email: administrador@agilizesoluciones.com
- 📱 Teléfono: +54 11 6168-2555

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.
