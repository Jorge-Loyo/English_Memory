# 📚 English Memory v1.4.0

Aplicación educativa multiplataforma para aprender y organizar vocabulario en inglés.

![Version](https://img.shields.io/badge/version-1.4.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-Educational-orange)

---

## ✨ Características Principales

### 📖 Gestión de Vocabulario
- Agregar, editar y eliminar palabras
- Búsqueda rápida y filtrado
- Pronunciación fonética opcional
- Notas personalizadas por palabra
- Exportar/Importar CSV

### 🎯 Modos de Práctica
- Quiz Inglés ↔ Español
- Práctica de caligrafía con repetición espaciada
- Seguimiento de palabras erróneas
- Estadísticas de progreso

### 📚 Recursos Educativos
- **Preposiciones**: 47 preposiciones con traducciones
- **Días/Meses**: 58 términos relacionados con tiempo
- **Números**: Conversor + reglas de ordinales, decimales y fracciones
- **Gramática**: Pronombres, verbos auxiliares, artículos, demostrativos
- **Contracciones**: 93 contracciones formales e informales
- **Verbos**: 368 verbos (124 irregulares + 239 regulares + 5 modales)
- **Verbos Frasales**: Verbos frasales comunes con significados
- **Conjugación**: 6 tiempos verbales + Modal Verbs

### 🌐 Herramientas Integradas
- **Traductor**: Bidireccional Inglés ↔ Español con MyMemory API
- **Diccionario**: Definiciones completas con sinónimos y ejemplos
- **Pronunciación TTS**: Text-to-Speech integrado (pyttsx3)

### 💾 Sistema de Respaldo
- Backups automáticos antes de cada guardado
- Mantiene últimos 10 backups
- Validación centralizada de datos
- Almacenamiento híbrido (JSON + SQLite)

---

## 🚀 Instalación

### 🪟 Windows - Instalador Portable (Recomendado)

1. **Descarga** el instalador desde [Releases](https://github.com/Jorge-Loyo/English_Memory/releases/latest)
2. **Descomprime** el archivo `EnglishMemory_v1.4.0_Portable.zip`
3. **Ejecuta** `INSTALAR.bat`
4. ¡Listo! Se creará un acceso directo en tu escritorio

**Características:**
- ✅ No requiere Python instalado
- ✅ Instalación automática en `%LOCALAPPDATA%\EnglishMemory`
- ✅ Accesos directos en Escritorio y Menú Inicio
- ✅ Desinstalador incluido (`DESINSTALAR.bat`)

**Requisitos:** Windows 7 o superior

---

### 🐧 Linux - Compilar desde Código

```bash
# 1. Clonar repositorio
git clone https://github.com/Jorge-Loyo/English_Memory.git
cd English_Memory

# 2. Dar permisos de ejecución
chmod +x build_linux.sh

# 3. Compilar ejecutable
./build_linux.sh

# 4. Ejecutar
./dist/EnglishMemory
```

**Requisitos:** Python 3.8+, pip3

**Datos guardados en:** `~/.local/share/EnglishMemory/data`

---

### 🍎 macOS - Desde Código Fuente

```bash
# 1. Clonar repositorio
git clone https://github.com/Jorge-Loyo/English_Memory.git
cd English_Memory

# 2. Instalar dependencias
pip3 install -r requirements.txt

# 3. Ejecutar aplicación
python3 app_modular.py
```

**Requisitos:** Python 3.8+, pip3

**Datos guardados en:** `~/Library/Application Support/EnglishMemory/data`

---

### 💻 Ejecutar desde Código (Todas las plataformas)

```bash
# Clonar repositorio
git clone https://github.com/Jorge-Loyo/English_Memory.git
cd English_Memory

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app_modular.py
```

---

## 📦 Dependencias

```
pyttsx3>=2.90          # Text-to-Speech
requests>=2.31.0       # API calls
beautifulsoup4>=4.12.0 # Web scraping
```

---

## 🎨 Capturas de Pantalla

### Vocabulario
Gestiona tu vocabulario personal con búsqueda rápida y edición intuitiva.

### Práctica
Modo quiz interactivo para reforzar el aprendizaje.

### Recursos Educativos
Acceso rápido a verbos, preposiciones, gramática y más.

---

## 📂 Estructura del Proyecto

```
English_Memory/
├── app_modular.py              # Punto de entrada principal
├── requirements.txt            # Dependencias
├── EnglishMemory.spec         # Configuración PyInstaller
├── src/
│   ├── controllers/           # Lógica de negocio
│   ├── models/                # Modelos de datos
│   ├── views/                 # Interfaces de usuario
│   ├── data/                  # Datos estáticos
│   ├── integrations/          # APIs externas
│   └── utils/                 # Utilidades
├── docs/                      # Documentación
└── dist/                      # Ejecutables compilados
```

---

## 🛠️ Compilar Ejecutable

```bash
# Instalar PyInstaller
pip install pyinstaller

# Compilar
pyinstaller EnglishMemory.spec

# El ejecutable estará en dist/EnglishMemory_Modular.exe
```

---

## 💡 Uso

### Agregar Palabras
1. Ve a la pestaña **Vocabulario**
2. Clic en **➕ Agregar**
3. Completa los campos (palabra, significado, pronunciación, notas)
4. Clic en **💾 Guardar**

### Practicar
1. Ve a la pestaña **Práctica**
2. Selecciona modo (Inglés→Español o Español→Inglés)
3. Responde las preguntas
4. Revisa tus estadísticas

### Consultar Recursos
- Navega por las pestañas: Verbos, Preposiciones, Gramática, etc.
- Usa el botón **🔊 Pronunciar** para escuchar
- Usa la búsqueda para filtrar contenido

---

## 📊 Almacenamiento de Datos

### Windows
```
%LOCALAPPDATA%\EnglishMemory\
├── palabras.json          # Vocabulario
├── statistics.db          # Estadísticas
└── palabras.json.backup_* # Backups automáticos
```

### Linux/macOS
```
~/.local/share/EnglishMemory/
├── palabras.json
├── statistics.db
└── palabras.json.backup_*
```

---

## 🤝 Contribuir

¿Tienes ideas para mejorar la aplicación? ¡Nos encantaría escucharlas!

### Reportar Errores o Sugerencias
Envía un email a: **Jorgenayati@gmail.com**

Incluye:
- Descripción del problema o sugerencia
- Pasos para reproducir (si es un error)
- Capturas de pantalla (opcional)
- Versión de la aplicación

---

## 📝 Changelog

### v1.4.0 (2025-01-28)
- ✅ Validación centralizada de datos
- ✅ Sistema de backups automáticos
- ✅ Pronunciación TTS mejorada (funciona múltiples veces)
- ✅ Diccionario con definiciones completas
- ✅ Traductor con MyMemory API
- ✅ Números ordinales y reglas completas
- ✅ Pronunciación en contracciones
- ✅ Pestaña de Ayuda completa

### v1.3.2
- Agregados 368 verbos totales
- Backup automático cada 5 minutos
- Pronunciación TTS integrada

---

## 📄 Licencia

Software de uso libre para fines educativos personales.

**Términos:**
- ✅ Uso educativo gratuito
- ✅ Datos almacenados localmente
- ✅ Sin recopilación de información personal
- ❌ No redistribuir con fines comerciales

---

## 👨‍💻 Desarrollado por

**Agilize Soluciones**

📧 Contacto: Jorgenayati@gmail.com  
📱 Teléfono: +54 11 6168-2555

---

## 🙏 Agradecimientos

- **pyttsx3**: Text-to-Speech engine
- **MyMemory API**: Servicio de traducción
- **DictionaryAPI.dev**: Diccionario en inglés
- Comunidad de Python por las excelentes librerías

---

## ⭐ ¿Te gusta el proyecto?

Si encuentras útil esta aplicación, considera:
- Darle una estrella ⭐ al repositorio
- Compartirla con otros estudiantes de inglés
- Enviar tus sugerencias para mejorarla

---

**English Memory** - Aprende inglés de forma organizada y efectiva 📚✨
