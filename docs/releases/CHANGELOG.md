# 📝 Changelog

Todos los cambios notables en este proyecto serán documentados aquí.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.3.2] - 2025-01-27

### ✨ Agregado
- 368 verbos totales (124 irregulares + 239 regulares + 5 modales)
- Verbo modal CAN y otros modales (may, must, shall, will)
- Más de 200 verbos regulares nuevos
- 68 verbos irregulares adicionales

### 🔧 Mejorado
- Lista de verbos ampliada significativamente
- Mejor cobertura de verbos comunes en inglés
- Documentación actualizada con nuevos totales

## [1.3.1] - 2024-01-24

### ✨ Agregado
- Pestaña de Contracciones con 93 contracciones en inglés
- Contracciones formales (I'm, you're, he's, etc.)
- Contracciones negativas (isn't, don't, can't, etc.)
- Contracciones informales (gonna, wanna, gotta, etc.)
- Búsqueda en tiempo real de contracciones

### 🔧 Mejorado
- Total de 12 pestañas funcionales
- Documentación actualizada

## [1.3.0] - 2024-01-23

### ✨ Agregado
- Pronunciación TTS con pyttsx3 (botón en Vocabulario, Práctica y Caligrafía)
- Botón toggle para cambiar entre tema claro/oscuro (en desarrollo)
- Backup automático cada 5 minutos
- Sistema de backups con retención de últimos 10 archivos
- Pestaña de Verbos con 100 verbos irregulares
- Pestaña de Conjugación con 6 tiempos verbales
- **Pestaña de Contracciones con 93 contracciones en inglés**
- Contador de backups en Estadísticas
- Botones Exportar/Importar CSV movidos a Estadísticas
- Modo de práctica en Caligrafía: Palabras Erróneas o Todo el Vocabulario
- Sección de novedades en Ayuda

### 🔧 Mejorado
- TTS ahora se reinicializa en cada uso (corregido bug de uso único)
- Estadísticas ahora muestran cantidad de backups guardados
- Caligrafía mejorada con selector de modo (erróneas/todas)
- Botón de pronunciación en Caligrafía para reforzar aprendizaje
- Interfaz preparada para temas claro/oscuro
- **Total de 12 pestañas funcionales**
- Mejor organización de botones en Vocabulario

### 🐛 Corregido
- TTS funcionaba solo una vez, ahora funciona múltiples veces
- Error de variable 'container' no definida en Estadísticas
- Botones de Exportar/Importar mejor ubicados

### 📚 Documentación
- README actualizado con nuevas características
- CHANGELOG actualizado
- Versión actualizada en todos los archivos
- Plan v2.0 creado con arquitectura MVC

## [1.2.0] - 2024-01-22

### ✨ Agregado
- Tabla de vocabulario ahora incluye columna de Notas
- Campo de pronunciación al agregar/editar palabras
- Sistema de validación de respuestas en modo práctica
- Guardado automático de palabras erróneas
- Nuevo modelo de caligrafía con repetición espaciada
- Caligrafía enfocada solo en palabras erróneas
- Navegación entre palabras en caligrafía

### 🛠️ Mejorado
- Práctica ahora requiere escribir la respuesta
- Feedback visual inmediato (correcto/incorrecto)
- Caligrafía con método científico de 7 pasos
- Interfaz más limpia y moderna en caligrafía

### 🗑️ Eliminado
- Pestaña de Pronunciación (integrada en Vocabulario)

## [1.1.0] - 2024-01-20

### ✨ Agregado
- Nueva pestaña 📝 Gramática con contenido esencial
- Tabla completa de pronombres (sujeto, objeto, posesivos)
- Verbos auxiliares (be, do, have) con conjugaciones
- Artículos (a, an, the) con reglas y ejemplos
- Adjetivos demostrativos (this, that, these, those)
- Cuantificadores (some, any, much, many, etc.)
- Tooltips en pestañas: al pasar el mouse muestra el nombre completo
- Pestañas ahora muestran solo iconos para ahorrar espacio

### 🐛 Corregido
- Ventana ahora se puede minimizar correctamente
- Ventana se puede redimensionar libremente
- Compatible con función "Acoplar ventana" de Windows
- Eliminada restricción de tamaño mínimo para mejor usabilidad
- Scroll con rueda del mouse ahora funciona en todas las pestañas

### 🎨 Mejorado
- Interfaz más compacta con iconos en pestañas
- Mejor experiencia de usuario con tooltips informativos

## [1.0.1] - 2024-01-15

### 🎨 Mejorado
- Cursor visible en campos de entrada (color morado)
- Efecto focus moderno en inputs
- Mejor espaciado en campos de texto
- Borde sutil en campos activos
- Experiencia de usuario mejorada

### 🐛 Corregido
- Tamaño de ventana ajustado (1200x700)
- Tamaño mínimo aumentado (1150x600)
- Todos los botones de pestañas visibles
- Ventana no se puede achicar más allá del mínimo necesario

## [1.0.0] - 2024-01-15

### ✨ Agregado
- Gestión completa de vocabulario (agregar, editar, eliminar)
- Búsqueda en tiempo real con debouncing
- Pronunciación fonética
- Modo práctica (quiz inglés ↔ español)
- Práctica de caligrafía con oraciones de ejemplo
- 47 preposiciones en inglés con traducciones
- 58 términos de días/meses/tiempo
- Conversor de números a texto en inglés
- Reglas importantes sobre números
- Estadísticas del vocabulario
- Exportar/Importar CSV
- Soporte multiplataforma (Windows/Linux)
- Tema oscuro moderno (morado/violeta)
- Fuente adaptativa según sistema operativo
- Almacenamiento local seguro
- Pestaña de ayuda con soporte técnico
- Manual de usuario integrado
- Términos y condiciones
- Documentación completa en código

### 🎨 Diseño
- Interfaz moderna con tema oscuro
- Responsive (1100x650, mínimo 950x550)
- Scroll en pestañas con mucho contenido
- Emojis para mejor UX

### 🔧 Técnico
- Detección automática de sistema operativo
- Rutas de datos adaptativas
- Validación de campos
- Manejo de errores robusto
- Código documentado

### 📚 Documentación
- README completo
- Guía de instalación (INSTALL.md)
- Guía de contribución (CONTRIBUTING.md)
- Licencia MIT
- .gitignore configurado

## [Unreleased]

### 🚀 Planeado para futuras versiones
- Modo claro/oscuro configurable
- Sincronización en la nube
- Soporte para imágenes
- Pronunciación con audio
- Más idiomas
- Juegos de aprendizaje
- Estadísticas avanzadas
- Exportar a PDF
- Flashcards
- Recordatorios de práctica

---

**Formato de versiones:** [MAJOR.MINOR.PATCH]
- **MAJOR:** Cambios incompatibles con versiones anteriores
- **MINOR:** Nueva funcionalidad compatible con versiones anteriores
- **PATCH:** Correcciones de bugs compatibles con versiones anteriores
