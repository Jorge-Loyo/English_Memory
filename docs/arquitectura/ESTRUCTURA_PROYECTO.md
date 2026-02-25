# 📁 Estructura del Proyecto - English Memory

```
english-memory/
│
├── 📄 diccionario_gui.py          # Aplicación principal con interfaz gráfica
├── 📄 diccionario.py               # Versión de consola (CLI)
├── 📄 build_exe.py                 # Script para crear ejecutable Windows
├── 📄 build_linux.sh               # Script para crear ejecutable Linux
├── 📄 setup.py                     # Configuración de instalación
├── 📄 requirements.txt             # Dependencias del proyecto
│
├── 📚 Documentación
│   ├── README.md                   # Documentación principal
│   ├── QUICK_START.md              # Inicio rápido
│   ├── INSTALL.md                  # Guía de instalación
│   ├── CONTRIBUTING.md             # Guía de contribución
│   ├── CHANGELOG.md                # Historial de cambios
│   ├── ESTRUCTURA_PROYECTO.md      # Este archivo
│   └── git_commands.txt            # Comandos Git útiles
│
├── ⚙️ Configuración
│   ├── .gitignore                  # Archivos ignorados por Git
│   ├── LICENSE                     # Licencia MIT
│   └── README_MULTIPLATAFORMA.md   # Info multiplataforma
│
├── 📦 Build (generados, no en Git)
│   ├── build/                      # Archivos temporales de build
│   ├── dist/                       # Ejecutables generados
│   │   ├── English Memory.exe      # Ejecutable Windows
│   │   └── English Memory          # Ejecutable Linux
│   └── *.spec                      # Archivos de configuración PyInstaller
│
└── 💾 Datos (locales, no en Git)
    └── palabras.json               # Vocabulario del usuario
```

## 📋 Descripción de Archivos

### Archivos Principales

**diccionario_gui.py**
- Aplicación principal con interfaz gráfica Tkinter
- 9 pestañas: Vocabulario, Pronunciación, Práctica, Caligrafía, Preposiciones, Días/Meses, Números, Estadísticas, Ayuda
- ~1200 líneas de código
- Multiplataforma (Windows/Linux)

**diccionario.py**
- Versión de consola (CLI)
- Funcionalidad básica de vocabulario
- Útil para testing y uso en terminal

### Scripts de Build

**build_exe.py**
- Crea ejecutable para Windows
- Usa PyInstaller
- Genera `English Memory.exe` en carpeta `dist/`

**build_linux.sh**
- Crea ejecutable para Linux
- Usa PyInstaller
- Genera `English Memory` en carpeta `dist/`

### Documentación

**README.md**
- Documentación principal del proyecto
- Características, instalación, uso
- Badges y enlaces importantes

**QUICK_START.md**
- Guía de inicio rápido
- 3 pasos para instalar y ejecutar
- Uso básico

**INSTALL.md**
- Guía detallada de instalación
- Instrucciones para Windows y Linux
- Solución de problemas

**CONTRIBUTING.md**
- Cómo contribuir al proyecto
- Estándares de código
- Proceso de Pull Request

**CHANGELOG.md**
- Historial de versiones
- Cambios en cada release
- Funcionalidades planeadas

### Configuración

**.gitignore**
- Excluye archivos innecesarios de Git
- Build artifacts, cache, datos locales

**LICENSE**
- Licencia MIT
- Permisos y limitaciones

**requirements.txt**
- Dependencias del proyecto
- PyInstaller 5.13.2+

**setup.py**
- Configuración para distribución
- Metadata del paquete

## 🗂️ Archivos NO incluidos en Git

```
# Generados por build
build/
dist/
*.spec

# Datos del usuario
palabras.json

# Cache de Python
__pycache__/
*.pyc

# IDEs
.vscode/
.idea/
```

## 📊 Estadísticas del Proyecto

- **Líneas de código:** ~1,500
- **Archivos Python:** 2
- **Archivos de documentación:** 7
- **Pestañas en la app:** 9
- **Funcionalidades:** 15+
- **Idiomas soportados:** Español/Inglés
- **Plataformas:** Windows, Linux

## 🔄 Flujo de Trabajo

1. **Desarrollo:** Editar `diccionario_gui.py`
2. **Testing:** Ejecutar `python diccionario_gui.py`
3. **Build:** Ejecutar `build_exe.py` o `build_linux.sh`
4. **Distribución:** Compartir ejecutable de `dist/`
5. **Git:** Commit y push cambios

## 📦 Distribución

### Para Usuarios
- Descargar ejecutable de `dist/`
- No requiere Python instalado
- Portable y standalone

### Para Desarrolladores
- Clonar repositorio
- Instalar dependencias
- Ejecutar desde código fuente

## 🔐 Datos del Usuario

Los datos se guardan en:
- **Windows:** `%LOCALAPPDATA%\DiccionarioPersonal\palabras.json`
- **Linux:** `~/.local/share/DiccionarioPersonal/palabras.json`

Estos archivos NO se incluyen en el repositorio Git.

## 🚀 Próximos Pasos

1. Subir a GitHub
2. Crear releases
3. Agregar screenshots
4. Configurar GitHub Actions para CI/CD
5. Crear wiki con documentación extendida
