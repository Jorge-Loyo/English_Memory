# Arquitectura Modular - English Memory v1.4.0

## Estructura Actual

```
English_Memory/
├── src/
│   ├── models/              # ✅ Capa de datos
│   │   ├── __init__.py
│   │   ├── database.py      # Conexión SQLite
│   │   ├── hybrid_storage.py # Storage híbrido JSON+SQLite
│   │   └── schema.sql       # Esquema de BD
│   │
│   ├── controllers/         # ✅ NUEVO - Lógica de negocio
│   │   ├── __init__.py
│   │   ├── vocabulario_controller.py  # CRUD vocabulario
│   │   └── practica_controller.py     # Lógica de quiz
│   │
│   ├── views/               # ✅ NUEVO - Capa de presentación
│   │   ├── __init__.py
│   │   └── components/      # Componentes reutilizables
│   │       └── __init__.py
│   │
│   └── utils/               # ✅ NUEVO - Utilidades
│       ├── __init__.py
│       ├── config.py        # Configuración centralizada
│       └── tts_helper.py    # Helper TTS
│
├── diccionario_gui.py       # ⚠️ Monolito actual (a refactorizar)
├── main.py                  # ✅ NUEVO - Punto de entrada
└── README.md
```

## Componentes Creados

### 1. Controllers (Lógica de Negocio)

#### VocabularioController
- `agregar_palabra()`: Validaciones + agregar
- `editar_palabra()`: Actualizar palabra existente
- `eliminar_palabra()`: Eliminar palabra
- `buscar_palabras()`: Búsqueda con filtros
- `obtener_estadisticas()`: Métricas del vocabulario

#### PracticaController
- `obtener_palabra_aleatoria()`: Selección aleatoria
- `obtener_pregunta()`: Generar pregunta según modo
- `verificar_respuesta()`: Validar respuesta + registrar
- `cambiar_modo()`: Alternar inglés/español
- `obtener_palabras_erroneas()`: Top palabras difíciles

### 2. Utils (Utilidades)

#### AppConfig
- Configuración centralizada (rutas, colores, fuentes)
- Detección automática de SO
- Constantes de la aplicación

#### TTSHelper
- Encapsulación de pyttsx3
- Manejo de errores TTS
- Verificación de disponibilidad

### 3. Main
- Punto de entrada limpio
- Separación de responsabilidades

## Próximos Pasos

### Fase 1: Refactorizar diccionario_gui.py
1. **Extraer Views**:
   - `VocabularioView`: Tab de vocabulario
   - `PracticaView`: Tab de práctica
   - `CaligrafiaView`: Tab de caligrafía
   - `EstadisticasView`: Tab de estadísticas

2. **Crear Componentes Reutilizables**:
   - `SearchBar`: Barra de búsqueda
   - `DataTable`: Tabla con Treeview
   - `ModalDialog`: Diálogos modales
   - `TabBase`: Clase base para tabs

3. **Integrar Controllers**:
   - Reemplazar lógica inline con controllers
   - Usar VocabularioController en VocabularioView
   - Usar PracticaController en PracticaView

### Fase 2: Separar Datos Estáticos
1. Crear `src/data/`:
   - `preposiciones.py`: 47 preposiciones
   - `dias_meses.py`: 58 términos temporales
   - `contracciones.py`: 93 contracciones
   - `verbos.py`: 368 verbos
   - `gramatica.py`: Pronombres, artículos, etc.

### Fase 3: Crear MainWindow
1. `src/views/main_window.py`:
   - Gestión de tabs
   - Header y footer
   - Tema y estilos
   - Backups automáticos

## Beneficios de la Modularización

✅ **Mantenibilidad**: Código organizado por responsabilidad  
✅ **Testabilidad**: Controllers y utils fáciles de testear  
✅ **Reutilización**: Componentes compartidos entre views  
✅ **Escalabilidad**: Fácil agregar nuevas features  
✅ **Colaboración**: Múltiples desarrolladores pueden trabajar en paralelo  

## Compatibilidad

- ✅ 100% compatible con v1.4.0
- ✅ Sin cambios en datos (JSON + SQLite)
- ✅ Misma funcionalidad, mejor estructura
- ✅ Preparado para v2.0 (plugins, API REST)
