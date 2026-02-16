# 🚀 English Memory v1.3.0 - Release Notes

## 📅 Fecha: 2024-01-23

## ✨ Nuevas Características

### 🔊 Pronunciación TTS (Text-to-Speech)
- **Integración con pyttsx3**: Escucha la pronunciación de palabras en inglés
- **Botón en Vocabulario**: Selecciona una palabra y presiona "🔊 TTS"
- **Botón en Práctica**: Escucha la palabra actual mientras practicas
- **Instalación opcional**: Funciona si pyttsx3 está instalado (`pip install pyttsx3`)

### 🌓 Toggle Tema Claro/Oscuro
- **Botón 🌓 en header**: Cambia entre tema oscuro y claro
- **Colores optimizados**: Paleta de colores para cada tema
- **Requiere reinicio**: Reinicia la app para aplicar el nuevo tema

### 💾 Backup Automático
- **Cada 5 minutos**: Respaldo automático de tu vocabulario
- **Ubicación**: `%LOCALAPPDATA%\DiccionarioPersonal\backups\`
- **Retención inteligente**: Mantiene solo los últimos 10 backups
- **Sin intervención**: Funciona en segundo plano

### 📘 Pestaña de Verbos
- **100 verbos irregulares**: Los más comunes en inglés
- **4 columnas**: Infinitivo, Pasado, Participio, Español
- **Búsqueda en tiempo real**: Encuentra verbos rápidamente
- **Ejemplos**: be/was/been, go/went/gone, make/made/made, etc.

### ⏰ Pestaña de Conjugación
- **6 tiempos verbales**:
  1. Simple Present (Presente Simple)
  2. Present Continuous (Presente Continuo)
  3. Simple Past (Pasado Simple)
  4. Present Perfect (Presente Perfecto)
  5. Future Simple (Futuro Simple)
  6. Modal Verbs (Verbos Modales)
- **Formas completas**: Afirmativo, Negativo, Interrogativo
- **Ejemplos prácticos**: Para cada tiempo verbal

### 📊 Estadísticas Mejoradas
- **Nueva métrica**: "💾 Backups guardados"
- **Contador en tiempo real**: Muestra cuántos backups tienes
- **Información útil**: Monitorea tu progreso y seguridad de datos

## 🛠️ Mejoras

### Interfaz
- Header reorganizado con botón de tema
- 11 pestañas totales (antes 9)
- Sección de novedades en pestaña Ayuda

### Funcionalidad
- Detección automática de pyttsx3
- Sistema de backups robusto con manejo de errores
- Preparación para temas personalizables

## 📊 Resumen de Cambios

- **Pestañas totales**: 11 (antes 9)
- **Verbos irregulares**: 100
- **Tiempos verbales**: 6
- **Backup automático**: Cada 5 minutos
- **TTS**: Opcional con pyttsx3

## 🎯 Características Completas v1.3

| Característica | Descripción |
|----------------|-------------|
| 📖 Vocabulario | CRUD completo + búsqueda + CSV |
| 🎯 Práctica | Quiz con validación + TTS |
| ✍️ Caligrafía | Repetición espaciada |
| 📍 Preposiciones | 47 preposiciones |
| 📅 Días/Meses | 58 términos |
| 🔢 Números | Conversor + reglas |
| 📝 Gramática | Pronombres, verbos, artículos |
| 📘 Verbos | 100 verbos irregulares |
| ⏰ Conjugación | 6 tiempos verbales |
| 📊 Estadísticas | Métricas + backups |
| ❓ Ayuda | Soporte + manual |

## 📥 Instalación

### Requisitos
```bash
pip install pyttsx3  # Opcional para TTS
```

### Ejecutar
```bash
python diccionario_gui.py
```

### Crear Ejecutable
```bash
# Windows
python build_exe.py

# Linux
chmod +x build_linux.sh
./build_linux.sh
```

## 🔄 Actualización desde v1.2

1. Cierra la aplicación actual
2. Reemplaza el ejecutable o actualiza el código
3. Instala pyttsx3 (opcional): `pip install pyttsx3`
4. Tus datos se mantienen intactos

## 📁 Ubicación de Archivos

- **Datos**: `%LOCALAPPDATA%\DiccionarioPersonal\palabras.json`
- **Backups**: `%LOCALAPPDATA%\DiccionarioPersonal\backups\`
- **Frecuencia**: Backup cada 5 minutos
- **Retención**: Últimos 10 backups

## 🐛 Problemas Conocidos

- El cambio de tema requiere reiniciar la aplicación
- TTS solo funciona si pyttsx3 está instalado
- En Linux, puede requerir dependencias adicionales para TTS

## 📞 Soporte

- 📧 Email: administrador@agilizesoluciones.com
- 📱 Teléfono: +54 11 6168-2555

## 🙏 Agradecimientos

Gracias a todos los usuarios por sus sugerencias que hicieron posible esta actualización.

---

**English Memory v1.3.0** - Aprende inglés de manera más efectiva 🚀

Desarrollado por [Agilize Soluciones](https://agilizesoluciones.com)
