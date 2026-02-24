# Plan de Desarrollo - English Memory v2.0
## Refactorización Completa

---

## ✅ Estado Actual: v1.4.0

**Sistema Híbrido Implementado**:
- ✅ JSON para vocabulario (15,000 palabras, compatibilidad)
- ✅ SQLite para estadísticas (practicas, progreso_palabras, estadisticas_diarias)
- ✅ HybridStorage unifica ambos sistemas
- ✅ Tab de Estadísticas Avanzadas con matplotlib
- ✅ 368 verbos (124 irregulares + 239 regulares + 5 modales)
- ✅ TTS integrado con pyttsx3 en 8 tabs

---

## 🎯 Objetivos Principales v2.0

1. **Arquitectura MVC**: Separar lógica de negocio, presentación y datos
2. ~~**Base de datos SQLite**: Migrar de JSON a base de datos relacional~~ ✅ **COMPLETADO** (Sistema Híbrido)
3. **Sistema de Plugins**: Permitir extensiones modulares
4. **API REST**: Sincronización entre dispositivos
5. **Tests Automatizados**: Cobertura de código >80%

---

## 📁 Nueva Estructura del Proyecto

```
English_Memory_v2/
├── src/
│   ├── models/              # Capa de datos
│   │   ├── __init__.py
│   │   ├── database.py      # Conexión y configuración SQLite
│   │   ├── palabra.py       # Modelo Palabra
│   │   ├── estadistica.py   # Modelo Estadística
│   │   ├── practica.py      # Modelo Práctica
│   │   └── backup.py        # Modelo Backup
│   │
│   ├── views/               # Capa de presentación
│   │   ├── __init__.py
│   │   ├── main_window.py   # Ventana principal
│   │   ├── vocabulario_view.py
│   │   ├── practica_view.py
│   │   ├── caligrafia_view.py
│   │   ├── estadisticas_view.py
│   │   └── components/      # Componentes reutilizables
│   │       ├── search_bar.py
│   │       ├── data_table.py
│   │       └── modal_dialog.py
│   │
│   ├── controllers/         # Capa de lógica
│   │   ├── __init__.py
│   │   ├── vocabulario_controller.py
│   │   ├── practica_controller.py
│   │   ├── import_export_controller.py
│   │   └── tts_controller.py
│   │
│   ├── api/                 # API REST
│   │   ├── __init__.py
│   │   ├── server.py        # FastAPI server
│   │   ├── routes/
│   │   │   ├── palabras.py
│   │   │   ├── estadisticas.py
│   │   │   └── sync.py
│   │   └── schemas.py       # Pydantic schemas
│   │
│   ├── plugins/             # Sistema de plugins
│   │   ├── __init__.py
│   │   ├── plugin_manager.py
│   │   ├── base_plugin.py
│   │   └── examples/
│   │       ├── anki_export.py
│   │       └── quizlet_import.py
│   │
│   ├── utils/               # Utilidades
│   │   ├── __init__.py
│   │   ├── config.py        # Configuración
│   │   ├── logger.py        # Logging
│   │   ├── validators.py    # Validaciones
│   │   └── migrations.py    # Migraciones de datos
│   │
│   └── main.py              # Punto de entrada
│
├── tests/                   # Tests automatizados
│   ├── __init__.py
│   ├── test_models/
│   │   ├── test_palabra.py
│   │   └── test_database.py
│   ├── test_controllers/
│   │   └── test_vocabulario.py
│   ├── test_api/
│   │   └── test_endpoints.py
│   └── fixtures/
│       └── sample_data.py
│
├── migrations/              # Migraciones de BD
│   ├── 001_initial_schema.sql
│   ├── 002_add_statistics.sql
│   └── migration_json_to_sqlite.py
│
├── plugins/                 # Plugins de usuario
│   └── README.md
│
├── docs/                    # Documentación
│   ├── API.md
│   ├── PLUGINS.md
│   └── ARCHITECTURE.md
│
├── requirements.txt
├── requirements-dev.txt     # Dependencias de desarrollo
├── pytest.ini
├── .env.example
└── README.md
```

---

## 🗄️ Fase 1: Sistema Híbrido SQLite ✅ COMPLETADO

### 1.1 Esquema Implementado (v1.4.0)

**Ubicación**: `src/models/schema.sql`

```sql
-- ✅ IMPLEMENTADO
CREATE TABLE practicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    palabra TEXT NOT NULL,
    modo TEXT NOT NULL,
    correcta INTEGER NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE progreso_palabras (
    palabra TEXT PRIMARY KEY,
    total_practicas INTEGER DEFAULT 0,
    practicas_correctas INTEGER DEFAULT 0,
    practicas_incorrectas INTEGER DEFAULT 0,
    ultima_practica TIMESTAMP,
    racha_actual INTEGER DEFAULT 0
);

CREATE TABLE estadisticas_diarias (
    fecha DATE PRIMARY KEY,
    total_practicas INTEGER DEFAULT 0,
    practicas_correctas INTEGER DEFAULT 0,
    tiempo_estudio_minutos INTEGER DEFAULT 0
);
```

### 1.2 Arquitectura Híbrida Actual

**✅ Implementado en v1.4.0**:
- `src/models/database.py`: Clase Database con context manager
- `src/models/hybrid_storage.py`: HybridStorage unifica JSON + SQLite
- `diccionario_gui.py`: Integración completa con HybridStorage
- Vocabulario permanece en JSON (compatibilidad, simplicidad)
- Estadísticas en SQLite (queries complejas, análisis temporal)

### 1.3 Próximas Mejoras para v2.0

**Tablas adicionales a implementar**:

```sql
-- categorias (NUEVO)
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    color TEXT
);

-- palabra_categoria (NUEVO)
CREATE TABLE palabra_categoria (
    palabra TEXT NOT NULL,
    categoria_id INTEGER,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE,
    PRIMARY KEY (palabra, categoria_id)
);

-- backups (NUEVO)
CREATE TABLE backups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ruta TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo TEXT CHECK(tipo IN ('automatico', 'manual')),
    tamanio INTEGER
);

-- configuracion (NUEVO)
CREATE TABLE configuracion (
    clave TEXT PRIMARY KEY,
    valor TEXT,
    tipo TEXT CHECK(tipo IN ('string', 'integer', 'boolean', 'json'))
);

-- indices adicionales
CREATE INDEX idx_palabra_categoria ON palabra_categoria(palabra);
CREATE INDEX idx_practicas_fecha ON practicas(fecha);
```

---

## 🏗️ Fase 2: Arquitectura MVC (Semanas 3-4)

### 2.1 Separación de Responsabilidades

**Controllers**: Lógica de negocio
- Validaciones
- Operaciones CRUD
- Coordinación entre modelos y vistas

**Views**: Solo presentación
- Renderizado de UI
- Eventos de usuario
- Actualización de widgets

**Models**: Acceso a datos
- Queries SQL
- Validaciones de datos
- Relaciones entre entidades

### 2.2 Implementación de Controllers

**src/controllers/vocabulario_controller.py**
```python
class VocabularioController:
    def __init__(self, db):
        self.db = db
        self.palabra_model = PalabraModel(db)
    
    def agregar_palabra(self, ingles, espanol, pronunciacion=None, notas=None):
        # Validaciones
        if not self.validar_palabra(ingles, espanol):
            raise ValueError("Datos inválidos")
        
        # Verificar duplicados
        if self.palabra_model.existe(ingles):
            raise ValueError("Palabra ya existe")
        
        # Crear palabra
        return self.palabra_model.crear(ingles, espanol, pronunciacion, notas)
    
    def buscar_palabras(self, query):
        return self.palabra_model.buscar(query)
```

### 2.3 Refactorización de Views

**src/views/vocabulario_view.py**
```python
class VocabularioView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()
        self.bind_events()
    
    def setup_ui(self):
        # Crear componentes
        self.search_bar = SearchBar(self)
        self.data_table = DataTable(self, columns=['Inglés', 'Español'])
        self.action_buttons = ActionButtons(self)
    
    def bind_events(self):
        self.action_buttons.on_add(self.handle_add)
        self.action_buttons.on_edit(self.handle_edit)
        self.search_bar.on_search(self.handle_search)
```

---

## 🔌 Fase 3: Sistema de Plugins (Semanas 5-6)

### 3.1 Arquitectura de Plugins

**src/plugins/base_plugin.py**
```python
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    def __init__(self):
        self.name = ""
        self.version = ""
        self.description = ""
    
    @abstractmethod
    def initialize(self, app_context):
        """Inicializar plugin con contexto de la app"""
        pass
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        """Ejecutar funcionalidad del plugin"""
        pass
    
    def cleanup(self):
        """Limpieza al desactivar plugin"""
        pass
```

**src/plugins/plugin_manager.py**
```python
class PluginManager:
    def __init__(self, plugins_dir):
        self.plugins_dir = plugins_dir
        self.loaded_plugins = {}
    
    def discover_plugins(self):
        """Buscar plugins en directorio"""
        pass
    
    def load_plugin(self, plugin_name):
        """Cargar plugin dinámicamente"""
        pass
    
    def unload_plugin(self, plugin_name):
        """Descargar plugin"""
        pass
    
    def execute_plugin(self, plugin_name, *args, **kwargs):
        """Ejecutar plugin"""
        pass
```

### 3.2 Plugins de Ejemplo

**Anki Export Plugin**
- Exportar vocabulario a formato Anki (.apkg)
- Incluir audio TTS
- Configurar campos personalizados

**Quizlet Import Plugin**
- Importar sets de Quizlet
- Mapear campos automáticamente
- Sincronizar actualizaciones

**Estadísticas Avanzadas Plugin**
- Gráficos de progreso
- Curva de olvido
- Predicción de retención

---

## 🌐 Fase 4: API REST (Semanas 7-8)

### 4.1 Configuración FastAPI

**src/api/server.py**
```python
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="English Memory API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "English Memory API v2.0"}
```

### 4.2 Endpoints Principales

**GET /api/palabras** - Listar palabras
**POST /api/palabras** - Crear palabra
**GET /api/palabras/{id}** - Obtener palabra
**PUT /api/palabras/{id}** - Actualizar palabra
**DELETE /api/palabras/{id}** - Eliminar palabra

**GET /api/estadisticas** - Estadísticas generales
**GET /api/estadisticas/progreso** - Progreso temporal

**POST /api/sync/push** - Enviar cambios
**POST /api/sync/pull** - Recibir cambios
**GET /api/sync/status** - Estado de sincronización

### 4.3 Schemas Pydantic

**src/api/schemas.py**
```python
from pydantic import BaseModel, Field
from datetime import datetime

class PalabraCreate(BaseModel):
    ingles: str = Field(..., min_length=1, max_length=100)
    espanol: str = Field(..., min_length=1, max_length=500)
    pronunciacion: str | None = None
    notas: str | None = None

class PalabraResponse(PalabraCreate):
    id: int
    fecha_creacion: datetime
    veces_practicada: int
    tasa_exito: float
```

### 4.4 Sistema de Sincronización

**Estrategia**: Last-Write-Wins con timestamps
- Cada cambio tiene timestamp
- Conflictos se resuelven por fecha más reciente
- Backup automático antes de sync
- Log de cambios sincronizados

---

## 🧪 Fase 5: Tests Automatizados (Semanas 9-10)

### 5.1 Configuración de Testing

**pytest.ini**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=src
    --cov-report=html
    --cov-report=term-missing
```

**requirements-dev.txt**
```
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
faker==20.1.0
```

### 5.2 Tests de Modelos

**tests/test_models/test_palabra.py**
```python
import pytest
from src.models.palabra import Palabra, PalabraModel

def test_crear_palabra(db_fixture):
    model = PalabraModel(db_fixture)
    palabra = model.crear("hello", "hola")
    assert palabra.id is not None
    assert palabra.ingles == "hello"

def test_palabra_duplicada(db_fixture):
    model = PalabraModel(db_fixture)
    model.crear("hello", "hola")
    with pytest.raises(ValueError):
        model.crear("hello", "hola")

def test_tasa_exito():
    palabra = Palabra(
        id=1, ingles="test", espanol="prueba",
        veces_practicada=10, veces_correcta=8
    )
    assert palabra.tasa_exito() == 80.0
```

### 5.3 Tests de Controllers

**tests/test_controllers/test_vocabulario.py**
```python
def test_agregar_palabra_valida(controller):
    palabra = controller.agregar_palabra("test", "prueba")
    assert palabra.id is not None

def test_buscar_palabras(controller):
    controller.agregar_palabra("hello", "hola")
    resultados = controller.buscar_palabras("hel")
    assert len(resultados) == 1
```

### 5.4 Tests de API

**tests/test_api/test_endpoints.py**
```python
from fastapi.testclient import TestClient

def test_listar_palabras(client):
    response = client.get("/api/palabras")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_crear_palabra(client):
    data = {"ingles": "test", "espanol": "prueba"}
    response = client.post("/api/palabras", json=data)
    assert response.status_code == 201
```

### 5.5 Cobertura de Tests

**Objetivo**: >80% de cobertura
- Models: 90%
- Controllers: 85%
- API: 80%
- Utils: 75%

---

## 📦 Fase 6: Empaquetado y Distribución (Semana 11)

### 6.1 Configuración de Build

**setup.py**
```python
from setuptools import setup, find_packages

setup(
    name="english-memory",
    version="2.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "customtkinter>=5.2.0",
        "pyttsx3>=2.90",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
    ],
    entry_points={
        "console_scripts": [
            "english-memory=main:main",
            "english-memory-api=api.server:start",
        ],
    },
)
```

### 6.2 Docker Support

**Dockerfile**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
CMD ["uvicorn", "src.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///data/english_memory.db
```

---

## 🎨 Mejoras Adicionales v2.0

### Interfaz de Usuario
- [ ] Tema claro/oscuro funcional sin reiniciar
- [ ] Animaciones suaves en transiciones
- [ ] Drag & drop para importar archivos
- [ ] Atajos de teclado personalizables
- [ ] Modo pantalla completa

### Funcionalidades
- [ ] Spaced Repetition System (SRS)
- [ ] Flashcards con imágenes
- [ ] Reconocimiento de voz
- [ ] Gamificación (puntos, logros, rachas)
- [ ] Modo offline completo

### Sincronización
- [ ] Sincronización automática en segundo plano
- [ ] Resolución de conflictos manual
- [ ] Historial de versiones
- [ ] Compartir vocabulario con otros usuarios

### Estadísticas Avanzadas
- [ ] Gráficos de progreso temporal
- [ ] Heatmap de actividad
- [ ] Predicción de retención
- [ ] Palabras más difíciles
- [ ] Tiempo de estudio por día

---

## 📅 Cronograma Actualizado v2.0

| Fase | Duración | Tareas Principales | Estado |
|------|----------|-------------------|--------|
| **v1.4.0** | ✅ | Sistema híbrido JSON+SQLite, estadísticas avanzadas | ✅ COMPLETADO |
| **Fase 1A** | 1-2 semanas | Expandir BD: categorías, backups, configuración | 🔜 SIGUIENTE |
| **Fase 1B** | 2-3 semanas | Refactorización MVC, separación de capas | ⏳ Pendiente |
| **Fase 2** | 2 semanas | Sistema de plugins, ejemplos | ⏳ Pendiente |
| **Fase 3** | 2 semanas | API REST, sincronización | ⏳ Pendiente |
| **Fase 4** | 1-2 semanas | Tests automatizados, CI/CD | ⏳ Pendiente |
| **Fase 5** | 1 semana | Empaquetado, documentación | ⏳ Pendiente |
| **Testing** | 1 semana | QA, corrección de bugs | ⏳ Pendiente |
| **Release** | - | Lanzamiento v2.0 | ⏳ Pendiente |

**Total restante**: ~10 semanas (2.5 meses)

---

## 🚀 Estrategia de Migración para Usuarios

### Migración Automática
1. Detectar versión 1.x al iniciar v2.0
2. Ofrecer migración automática
3. Crear backup completo de datos v1.x
4. Ejecutar script de migración
5. Validar integridad de datos
6. Mantener backup por 30 días

### Compatibilidad
- Importar/exportar CSV compatible con v1.x
- Documentación de migración manual
- Soporte para ambas versiones durante 6 meses

---

## 📚 Documentación Requerida

### Para Desarrolladores
- **ARCHITECTURE.md**: Explicación de arquitectura MVC
- **PLUGINS.md**: Guía para crear plugins
- **API.md**: Documentación completa de API
- **CONTRIBUTING.md**: Guía de contribución

### Para Usuarios
- **USER_GUIDE.md**: Manual de usuario completo
- **MIGRATION_GUIDE.md**: Guía de migración v1→v2
- **FAQ.md**: Preguntas frecuentes
- **CHANGELOG.md**: Registro de cambios

---

## 🔧 Herramientas y Tecnologías

### Backend
- **SQLite**: Base de datos
- **FastAPI**: Framework API REST
- **Pydantic**: Validación de datos
- **Alembic**: Migraciones de BD (opcional)

### Frontend
- **CustomTkinter**: UI moderna
- **Pillow**: Procesamiento de imágenes
- **Matplotlib**: Gráficos estadísticos

### Testing
- **pytest**: Framework de testing
- **pytest-cov**: Cobertura de código
- **faker**: Datos de prueba

### DevOps
- **GitHub Actions**: CI/CD
- **Docker**: Containerización
- **pre-commit**: Hooks de git

---

## ✅ Criterios de Éxito

### v1.4.0 (Completado)
- ✅ Sistema híbrido JSON+SQLite funcionando
- ✅ Estadísticas avanzadas con matplotlib
- ✅ TTS integrado en 8 tabs
- ✅ 368 verbos totales
- ✅ Executable 54.1 MB funcional

### v2.0 (Pendiente)
- [ ] Arquitectura MVC completamente implementada
- [x] Base de datos SQLite funcionando correctamente (híbrido)
- [ ] Sistema de categorías funcional
- [ ] Al menos 3 plugins funcionales
- [ ] API REST con todos los endpoints
- [ ] Cobertura de tests >80%
- [ ] Documentación completa (API, Plugins, Arquitectura)
- [ ] Sincronización multi-dispositivo
- [ ] Performance igual o mejor que v1.4.0
- [ ] Sin bugs críticos

---

## 🎯 Próximos Pasos Inmediatos

### Fase 1A: Expandir Sistema Híbrido (1-2 semanas)
1. ✅ ~~Sistema híbrido básico~~ (COMPLETADO v1.4.0)
2. **Agregar tablas**: categorias, palabra_categoria, backups, configuracion
3. **Migrar configuración**: Mover settings de JSON a tabla configuracion
4. **Sistema de categorías**: UI para crear/asignar categorías a palabras
5. **Backups automáticos**: Registrar en tabla backups con metadata

### Fase 1B: Refactorización MVC (2-3 semanas)
1. **Separar controllers**: Extraer lógica de diccionario_gui.py
2. **Crear views modulares**: Un archivo por tab principal
3. **Modelos de dominio**: Clases Palabra, Categoria, Practica con métodos
4. **Reorganizar estructura**: Mover a src/models, src/views, src/controllers

### Fase 2: Sistema de Plugins (2 semanas)
1. **Plugin manager**: Descubrimiento y carga dinámica
2. **Base plugin**: Clase abstracta con hooks
3. **Plugins ejemplo**: Anki export, Quizlet import, estadísticas avanzadas

### Fase 3: API REST (2 semanas)
1. **FastAPI server**: Endpoints CRUD para palabras
2. **Sincronización**: Push/pull con resolución de conflictos
3. **Autenticación**: JWT tokens para multi-usuario

### Fase 4: Tests y CI/CD (1-2 semanas)
1. **pytest setup**: Configuración y fixtures
2. **Tests unitarios**: Models, controllers, API
3. **GitHub Actions**: CI/CD pipeline automático

---

**Fecha de creación**: 2024
**Versión del plan**: 1.0
**Autor**: Equipo English Memory
