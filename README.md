# 📚 English Memory v1.2

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey.svg)](https://github.com/tu-usuario/english-memory)
[![Version](https://img.shields.io/badge/version-1.2.0-green.svg)](https://github.com/tu-usuario/english-memory/releases)

Aplicación educativa multiplataforma para aprender y organizar vocabulario en inglés.

![English Memory](https://via.placeholder.com/800x400/1a1625/a78bfa?text=English+Memory+v1.2)

## 🌟 Características Destacadas

- 🎯 **Modo Práctica Interactivo** - Quiz con validación de respuestas y seguimiento de errores
- 📚 **Gestión Completa** - Agrega, edita y organiza tu vocabulario
- 🔊 **Pronunciación Fonética** - Aprende la pronunciación correcta
- ✍️ **Práctica de Caligrafía** - Método de repetición espaciada con palabras erróneas
- 📝 **Gramática Esencial** - Pronombres, verbos auxiliares, artículos y más
- 📊 **Estadísticas** - Monitorea tu progreso
- 💾 **Datos Seguros** - Almacenamiento local automático
- 🌐 **Multiplataforma** - Windows y Linux

## ✨ Características

### 📖 Gestión de Vocabulario
- ➕ Agregar palabras con significado, pronunciación y notas
- ✏️ Editar palabras (doble clic en la tabla)
- 🗑️ Eliminar palabras
- 🔍 Búsqueda en tiempo real
- 📊 Ordenar por columnas
- 📤 Exportar a CSV
- 📥 Importar desde CSV

### 🎓 Herramientas de Aprendizaje
- 🔊 **Pronunciación**: Gestiona la pronunciación fonética de palabras
- 🎯 **Práctica**: Modo quiz (Inglés ↔ Español)
- ✍️ **Caligrafía**: Practica escritura con oraciones de ejemplo
- 📍 **Preposiciones**: 47 preposiciones con traducciones
- 📅 **Días/Meses**: 58 términos relacionados con tiempo
- 🔢 **Números**: Conversor + reglas importantes
- 📝 **Gramática**: Pronombres, verbos auxiliares, artículos, demostrativos, cuantificadores
- 📊 **Estadísticas**: Métricas de tu vocabulario

## 🖥️ Compatibilidad

- ✅ Windows 10/11
- ✅ Linux (Ubuntu, Debian, Fedora, Arch, etc.)
- ✅ macOS (compatible)

## 📋 Tabla de Contenidos

- [Inicio Rápido](#-inicio-rápido)
- [Características](#-características)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Documentación](#-documentación)
- [Contribuir](#-contribuir)
- [Soporte](#-soporte)
- [Licencia](#-licencia)

## ⚡ Inicio Rápido

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/english-memory.git
cd english-memory

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python diccionario_gui.py
```

📖 Ver [QUICK_START.md](QUICK_START.md) para más detalles.

## 🚀 Instalación

### Opción 1: Ejecutable (Recomendado)

#### Windows
1. Ejecuta `crear_ejecutable.bat`
2. El ejecutable estará en la carpeta `dist`
3. Copia `English Memory.exe` donde quieras
4. Crea un acceso directo en el escritorio

#### Linux
```bash
chmod +x build_linux.sh
./build_linux.sh
cd dist
./English\ Memory
```

### Opción 2: Ejecutar con Python

#### Requisitos
- Python 3.7 o superior
- tkinter (incluido en Python)

#### Windows
```bash
python diccionario_gui.py
```

#### Linux
```bash
# Instalar tkinter si es necesario
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora
sudo pacman -S tk                 # Arch Linux

# Ejecutar
python3 diccionario_gui.py
```

## 📁 Ubicación de Datos

Los datos se guardan automáticamente en:

- **Windows**: `C:\Users\TuUsuario\AppData\Local\DiccionarioPersonal\palabras.json`
- **Linux**: `~/.local/share/DiccionarioPersonal/palabras.json`
- **macOS**: `~/.local/share/DiccionarioPersonal/palabras.json`

## 📖 Manual de Usuario

### Vocabulario
1. **Agregar**: Click en "➕ Agregar", completa los campos y guarda
2. **Editar**: Doble clic en cualquier palabra de la tabla
3. **Eliminar**: Selecciona una palabra y click en "🗑️ Eliminar"
4. **Buscar**: Escribe en el campo de búsqueda (busca en inglés y español)
5. **Ordenar**: Click en los encabezados de columna

### Pronunciación
1. Escribe la palabra en inglés
2. Escribe la pronunciación fonética
3. Click en "💾 Guardar Pronunciación"

### Práctica
1. Selecciona el modo (Inglés→Español o Español→Inglés)
2. Click en "🔄 Nueva Palabra" para practicar
3. Click en "👁️ Ver Respuesta" para verificar

### Caligrafía
1. Selecciona una palabra del menú desplegable
2. Practica escribiendo en las líneas
3. Copia las oraciones de ejemplo

### Exportar/Importar
- **Exportar**: Click en "📤 Exportar" y elige ubicación
- **Importar**: Click en "📥 Importar" y selecciona archivo CSV

## 🔧 Respaldos

### Método 1: Copiar carpeta de datos
Copia la carpeta completa (ver ubicación arriba)

### Método 2: Exportar CSV
Usa la función "📤 Exportar" en la pestaña Vocabulario

## 📞 Soporte Técnico

¿Necesitas ayuda? Contáctanos:

- 📧 **Email**: administrador@agilizesoluciones.com
- 📱 **Teléfono**: +54 11 6168-2555

Horario de atención: Lunes a Viernes, 9:00 - 18:00 (GMT-3)

## 📋 Términos y Condiciones

1. **Uso Educativo**: Aplicación gratuita con fines educativos
2. **Privacidad**: Todos los datos se almacenan localmente
3. **Respaldos**: Responsabilidad del usuario
4. **Garantía**: Software proporcionado "tal cual"
5. **Soporte**: Disponible por email/teléfono
6. **Licencia**: Uso libre para fines educativos personales

## 🐛 Solución de Problemas

### Windows: "No se encuentra Python"
Instala Python desde [python.org](https://www.python.org/downloads/)

### Linux: "No module named tkinter"
```bash
sudo apt-get install python3-tk
```

### Linux: "Permission denied"
```bash
chmod +x "dist/English Memory"
```

### Los datos no se guardan
Verifica permisos de escritura en la carpeta de datos

## 🎨 Personalización

La aplicación usa:
- **Tema**: Oscuro (morado/violeta)
- **Fuente Windows**: Segoe UI
- **Fuente Linux**: Sans

## 📦 Dependencias

- Python 3.7+
- tkinter (incluido en Python)
- PyInstaller 5.13.2+ (solo para crear ejecutable)

## 🔄 Actualizaciones

**Versión 1.2** (2024)
- Validación de respuestas en práctica
- Caligrafía con repetición espaciada
- Columna de Notas en vocabulario
- Pestaña de Pronunciación eliminada (integrada)

**Versión 1.0** (2024)
- Lanzamiento inicial
- Gestión completa de vocabulario
- 9 pestañas de herramientas
- Soporte multiplataforma
- Exportar/Importar CSV

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor lee [CONTRIBUTING.md](CONTRIBUTING.md) para detalles.

### 👥 Contribuidores

Gracias a todos los que han contribuido a este proyecto.

## 📚 Documentación

- 📖 [README](README.md) - Documentación principal
- ⚡ [QUICK_START](QUICK_START.md) - Inicio rápido
- 📦 [INSTALL](INSTALL.md) - Guía de instalación
- 🤝 [CONTRIBUTING](CONTRIBUTING.md) - Cómo contribuir
- 📝 [CHANGELOG](CHANGELOG.md) - Historial de cambios

## 👨‍💻 Desarrollador

**Agilize Soluciones**
- 🌐 Website: [agilizesoluciones.com](https://agilizesoluciones.com)
- 📧 Email: administrador@agilizesoluciones.com
- 📱 Teléfono: +54 11 6168-2555

## ⭐ Agradecimientos

Gracias a todos los usuarios y contribuidores que hacen posible este proyecto.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.

```
MIT License - Copyright (c) 2024 Agilize Soluciones
```

## 📊 Estado del Proyecto

✅ **Versión Estable:** 1.2.0  
🚧 **En Desarrollo:** Nuevas funcionalidades planeadas  
🐛 **Bugs Conocidos:** Ninguno reportado  

---

<div align="center">

**English Memory v1.0** - Aprende inglés de manera efectiva 🚀

Hecho con ❤️ por [Agilize Soluciones](https://agilizesoluciones.com)

[Reportar Bug](https://github.com/tu-usuario/english-memory/issues) · [Solicitar Funcionalidad](https://github.com/tu-usuario/english-memory/issues) · [Documentación](https://github.com/tu-usuario/english-memory/wiki)

</div>
