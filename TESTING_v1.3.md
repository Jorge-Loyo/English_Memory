# 🧪 Guía de Testing - English Memory v1.3.0

## ✅ Checklist de Testing

### 🔧 Preparación

- [ ] Python 3.7+ instalado
- [ ] Dependencias instaladas: `pip install -r requirements.txt`
- [ ] pyttsx3 instalado (opcional): `pip install pyttsx3`

### 📖 Pestaña Vocabulario

- [ ] Agregar palabra nueva
- [ ] Editar palabra existente (doble clic)
- [ ] Eliminar palabra
- [ ] Buscar palabra en tiempo real
- [ ] Ordenar por columnas (clic en headers)
- [ ] Exportar a CSV
- [ ] Importar desde CSV
- [ ] **NUEVO**: Botón TTS pronuncia palabra seleccionada

### 🎯 Pestaña Práctica

- [ ] Cambiar modo (Inglés→Español / Español→Inglés)
- [ ] Nueva palabra aleatoria
- [ ] Escribir respuesta y verificar
- [ ] Respuesta correcta muestra verde
- [ ] Respuesta incorrecta muestra rojo y guarda palabra
- [ ] **NUEVO**: Botón TTS pronuncia palabra actual

### ✍️ Pestaña Caligrafía

- [ ] Muestra palabras erróneas de práctica
- [ ] Navegación anterior/siguiente
- [ ] 7 líneas de práctica (copia, guía, memoria)
- [ ] Contador de progreso
- [ ] Actualizar lista

### 📍 Pestaña Preposiciones

- [ ] Muestra 47 preposiciones
- [ ] Búsqueda funciona
- [ ] Tabla ordenada alfabéticamente

### 📅 Pestaña Días/Meses

- [ ] Muestra 58 términos
- [ ] Búsqueda por categoría funciona
- [ ] Todas las categorías visibles

### 🔢 Pestaña Números

- [ ] Conversor funciona (0-999,999,999)
- [ ] Números 1-20 visibles
- [ ] Decenas y grandes números visibles
- [ ] 10 reglas mostradas

### 📝 Pestaña Gramática

- [ ] Tabla de pronombres completa
- [ ] Verbos auxiliares (TO BE, TO HAVE, TO DO)
- [ ] Artículos (a, an, the)
- [ ] Demostrativos (this, that, these, those)
- [ ] Cuantificadores (10 elementos)

### 📘 Pestaña Verbos (NUEVA)

- [ ] Muestra 100 verbos irregulares
- [ ] 4 columnas: Infinitivo, Pasado, Participio, Español
- [ ] Búsqueda funciona en todas las columnas
- [ ] Scroll funciona correctamente

### ⏰ Pestaña Conjugación (NUEVA)

- [ ] Simple Present visible con ejemplos
- [ ] Present Continuous visible
- [ ] Simple Past visible
- [ ] Present Perfect visible
- [ ] Future Simple visible
- [ ] Modal Verbs (8 modales) visibles
- [ ] Scroll funciona correctamente

### 📊 Pestaña Estadísticas

- [ ] Total de palabras correcto
- [ ] Con/Sin pronunciación correcto
- [ ] Con notas correcto
- [ ] **NUEVO**: Contador de backups funciona
- [ ] Botón actualizar funciona

### ❓ Pestaña Ayuda

- [ ] Información de soporte visible
- [ ] Manual de usuario completo
- [ ] Términos y condiciones
- [ ] Acerca de con versión 1.3
- [ ] **NUEVO**: Sección de novedades v1.3

### 🌓 Toggle Tema (NUEVO)

- [ ] Botón 🌓 visible en header
- [ ] Clic muestra mensaje de reinicio
- [ ] Variable modo_oscuro cambia

### 💾 Backup Automático (NUEVO)

- [ ] Carpeta backups se crea automáticamente
- [ ] Backup se genera al iniciar
- [ ] Archivos tienen formato: palabras_backup_YYYYMMDD_HHMMSS.json
- [ ] Solo mantiene últimos 10 backups
- [ ] Estadísticas muestra contador correcto

### 🔊 TTS (NUEVO - Opcional)

Si pyttsx3 está instalado:
- [ ] Botón TTS visible en Vocabulario
- [ ] Botón Pronunciar visible en Práctica
- [ ] Pronunciación funciona al hacer clic
- [ ] No hay errores si no está instalado

## 🖥️ Testing de Ejecutable

### Windows

```bash
# Crear ejecutable
python build_exe.py

# Verificar
cd dist
"English Memory.exe"
```

- [ ] Ejecutable se crea sin errores
- [ ] Aplicación inicia correctamente
- [ ] Todas las pestañas funcionan
- [ ] Datos se guardan en %LOCALAPPDATA%\DiccionarioPersonal
- [ ] Backups se crean en %LOCALAPPDATA%\DiccionarioPersonal\backups

### Linux

```bash
# Crear ejecutable
chmod +x build_linux.sh
./build_linux.sh

# Verificar
cd dist
./English\ Memory
```

- [ ] Ejecutable se crea sin errores
- [ ] Aplicación inicia correctamente
- [ ] Todas las pestañas funcionan
- [ ] Datos se guardan en ~/.local/share/DiccionarioPersonal
- [ ] Backups se crean en ~/.local/share/DiccionarioPersonal/backups

## 📦 Testing de Instalador Portable

```bash
# Crear instalador
python crear_instalador_portable.py
```

- [ ] Carpeta instalador_portable se crea
- [ ] Contiene: English Memory.exe, INSTALAR.bat, DESINSTALAR.bat, LEEME.txt
- [ ] LEEME.txt muestra versión 1.3
- [ ] INSTALAR.bat funciona
- [ ] Accesos directos se crean
- [ ] DESINSTALAR.bat funciona

## 🐛 Testing de Errores

### Casos Edge

- [ ] Agregar palabra vacía (debe rechazar)
- [ ] Agregar palabra duplicada (debe advertir)
- [ ] Buscar sin palabras en vocabulario
- [ ] Práctica sin palabras (debe mostrar mensaje)
- [ ] Caligrafía sin palabras erróneas (debe mostrar mensaje)
- [ ] Conversor con número inválido (debe mostrar error)
- [ ] Conversor con número fuera de rango (debe advertir)

### Compatibilidad

- [ ] Windows 10
- [ ] Windows 11
- [ ] Ubuntu 20.04+
- [ ] Debian 11+
- [ ] Fedora 35+

## 📊 Resultados Esperados

### Funcionalidad
- ✅ 11 pestañas funcionando
- ✅ TTS opcional (si pyttsx3 instalado)
- ✅ Backup automático cada 5 minutos
- ✅ Toggle tema (requiere reinicio)
- ✅ 100 verbos irregulares
- ✅ 6 tiempos verbales

### Performance
- ✅ Inicio rápido (< 3 segundos)
- ✅ Búsqueda instantánea
- ✅ Sin lag en scroll
- ✅ Backup no bloquea UI

### Datos
- ✅ Datos persisten entre sesiones
- ✅ Backups se crean automáticamente
- ✅ Importar/Exportar CSV funciona
- ✅ No hay pérdida de datos

## 📝 Reporte de Bugs

Si encuentras bugs, reporta con:
- Versión: 1.3.0
- Sistema operativo
- Pasos para reproducir
- Comportamiento esperado vs actual
- Screenshots si es posible

Enviar a: administrador@agilizesoluciones.com

---

**Testing completado**: ___/___/2024  
**Testeado por**: _______________  
**Resultado**: ☐ Aprobado ☐ Con observaciones ☐ Rechazado
