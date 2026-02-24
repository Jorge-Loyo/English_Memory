# Sistema Híbrido JSON + SQLite
## English Memory v1.4.0

## 📋 Descripción

El sistema híbrido combina lo mejor de dos mundos:
- **JSON**: Para vocabulario (simple, portable, editable)
- **SQLite**: Para estadísticas (relacional, queries complejas)

## 🏗️ Arquitectura

```
DiccionarioPersonal/
├── palabras.json          ← Vocabulario (JSON)
├── statistics.db          ← Estadísticas (SQLite)
└── backups/
    ├── palabras_*.json
    └── statistics_*.db
```

### Vocabulario (JSON)
```json
{
  "hello": {
    "significado": "hola",
    "pronunciacion": "/həˈloʊ/",
    "notas": "Saludo común"
  }
}
```

### Estadísticas (SQLite)
```sql
-- Historial completo de prácticas
practicas (id, palabra, modo, correcta, tiempo, fecha)

-- Progreso por palabra
progreso_palabras (palabra, veces_vista, veces_correcta, nivel_dominio)

-- Estadísticas diarias
estadisticas_diarias (fecha, practicas_totales, tasa_exito, tiempo_total)
```

## 🚀 Uso

### Inicializar Storage

```python
from src.models import HybridStorage

# Crear instancia
storage = HybridStorage(APP_DIR)
```

### Operaciones de Vocabulario

```python
# Agregar palabra
storage.agregar_palabra("hello", "hola", "/həˈloʊ/", "Saludo")

# Editar palabra
storage.editar_palabra("hello", "hi", "hola", "/haɪ/")

# Eliminar palabra
storage.eliminar_palabra("hello")

# Buscar palabras
resultados = storage.buscar_palabras("hel")

# Obtener todas
todas = storage.obtener_todas_palabras()
```

### Operaciones de Estadísticas

```python
# Registrar práctica
storage.registrar_practica(
    palabra="hello",
    modo="ingles_espanol",
    correcta=True,
    respuesta_usuario="hola",
    tiempo_respuesta=5000  # milisegundos
)

# Obtener progreso de palabra
progreso = storage.obtener_progreso_palabra("hello")
# {
#   'veces_vista': 10,
#   'veces_correcta': 8,
#   'veces_incorrecta': 2,
#   'ultima_practica': '2025-01-27 10:30:00'
# }

# Palabras más difíciles
dificiles = storage.obtener_palabras_dificiles(10)

# Estadísticas del período
stats = storage.obtener_estadisticas_periodo(30)  # últimos 30 días

# Racha de estudio
racha = storage.obtener_racha_estudio()

# Historial de palabra
historial = storage.obtener_historial_palabra("hello", 20)
```

### Importar/Exportar

```python
# Exportar a CSV
storage.exportar_csv("vocabulario.csv")

# Importar desde CSV
count = storage.importar_csv("vocabulario.csv")
```

## 📊 Queries Disponibles

### 1. Progreso Temporal
```python
stats = storage.obtener_estadisticas_periodo(30)
# Retorna lista de estadísticas diarias
```

### 2. Palabras Difíciles
```python
dificiles = storage.obtener_palabras_dificiles(10)
# Retorna top 10 palabras con menor tasa de éxito
```

### 3. Racha de Estudio
```python
racha = storage.obtener_racha_estudio()
# Retorna días estudiados en últimos 30 días
```

### 4. Historial de Palabra
```python
historial = storage.obtener_historial_palabra("hello", 20)
# Retorna últimas 20 prácticas de la palabra
```

## 🔧 Ventajas

### JSON (Vocabulario)
✅ Simple y portable
✅ Editable manualmente
✅ Backup fácil (copiar archivo)
✅ Compatible con v1.x
✅ Rápido para <15,000 palabras

### SQLite (Estadísticas)
✅ Queries complejas
✅ Relaciones entre datos
✅ Índices para performance
✅ Historial ilimitado
✅ Agregaciones eficientes

## 📈 Performance

### Vocabulario (15,000 palabras)
- Cargar: ~200ms
- Buscar: ~50ms
- Guardar: ~100ms

### Estadísticas (100,000 prácticas)
- Registrar práctica: ~10ms
- Query agregada: ~20ms
- Historial palabra: ~5ms

## 🔄 Migración desde v1.x

El sistema es **100% compatible** con v1.x:
- Lee el mismo `palabras.json`
- Crea `statistics.db` automáticamente
- No requiere migración manual

## 🛡️ Seguridad

### Backups Automáticos
- JSON: Backup cada 5 minutos
- SQLite: Backup diario automático

### Recuperación
```python
# Si statistics.db se corrompe:
# 1. Vocabulario sigue funcionando (JSON intacto)
# 2. Se puede recrear statistics.db vacía
# 3. Solo se pierden estadísticas, no palabras
```

## 📝 Próximos Pasos

### v1.4.0 (Actual)
- [x] Sistema híbrido funcional
- [x] Queries básicas de estadísticas
- [ ] Integrar en GUI
- [ ] Gráficos de progreso

### v1.5.0 (Futuro)
- [ ] Curva de aprendizaje
- [ ] Predicción de retención
- [ ] Exportar estadísticas a CSV
- [ ] Dashboard de progreso

### v2.0.0 (Plan)
- [ ] Migración completa a SQLite
- [ ] API REST
- [ ] Sincronización multi-dispositivo
- [ ] Sistema de plugins

## 🧪 Testing

Ejecutar tests:
```bash
py test_hybrid.py
```

Resultado esperado:
```
OK Storage inicializado
OK 3 palabras agregadas
OK 4 practicas registradas
OK Todas las pruebas pasaron exitosamente!
```

## 📚 Referencias

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [JSON in Python](https://docs.python.org/3/library/json.html)
