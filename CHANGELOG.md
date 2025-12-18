# 📝 Changelog

Todos los cambios notables en este proyecto serán documentados aquí.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

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
