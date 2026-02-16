# Plan de Desarrollo - English Memory v2.0
## Refactorización Completa

---

## 🎯 Objetivos Principales

1. **Arquitectura MVC**: Separar lógica de negocio, presentación y datos
2. **Base de datos SQLite**: Migrar de JSON a base de datos relacional
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

## 🗄️ Fase 1: Migración a SQLite (Semanas 1-2)

### 1.1 Diseño del Esquema

```sql
-- palabras
CREATE TABLE palabras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingles TEXT NOT NULL UNIQUE,
    espanol TEXT NOT NULL,
    pronunciacion TEXT,
    notas TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    veces_practicada INTEGER DEFAULT 0,
    veces_correcta INTEGER DEFAULT 0,
    veces_incorrecta INTEGER DEFAULT 0
);

-- categorias
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT
);

-- palabra_categoria (relación muchos a muchos)
CREATE TABLE palabra_categoria (
    palabra_id INTEGER,
    categoria_id INTEGER,
    FOREIGN KEY (palabra_id) REFERENCES palabras(id) ON DELETE CASCADE,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE,
    PRIMARY KEY (palabra_id, categoria_id)
);

-- practicas
CREATE TABLE practicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    palabra_id INTEGER,
    modo TEXT CHECK(modo IN ('ingles_espanol', 'espanol_ingles')),
    correcta BOOLEAN,
    respuesta_usuario TEXT,
    tiempo_respuesta INTEGER,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (palabra_id) REFERENCES palabras(id) ON DELETE CASCADE
);

-- backups
CREATE TABLE backups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ruta TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo TEXT CHECK(tipo IN ('automatico', 'manual')),
    tamanio INTEGER
);

-- configuracion
CREATE TABLE configuracion (
    clave TEXT PRIMARY KEY,
    valor TEXT,
    tipo TEXT CHECK(tipo IN ('string', 'integer', 'boolean', 'json'))
);

-- indices
CREATE INDEX idx_palabras_ingles ON palabras(ingles);
CREATE INDEX idx_practicas_palabra ON practicas(palabra_id);
CREATE INDEX idx_practicas_fecha ON practicas(fecha);
```

### 1.2 Script de Migración

**migrations/migration_json_to_sqlite.py**
- Leer datos de JSON existente
- Crear base de datos SQLite
- Insertar datos preservando información
- Crear backup del JSON original
- Validar integridad de datos

### 1.3 Modelo de Datos

**src/models/database.py**
```python
import sqlite3
from contextlib import contextmanager
from pathlib import Path

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
```

**src/models/palabra.py**
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Palabra:
    id: Optional[int]
    ingles: str
    espanol: str
    pronunciacion: Optional[str]
    notas: Optional[str]
    fecha_creacion: datetime
    fecha_modificacion: datetime
    veces_practicada: int = 0
    veces_correcta: int = 0
    veces_incorrecta: int = 0
    
    def tasa_exito(self) -> float:
        if self.veces_practicada == 0:
            return 0.0
        return (self.veces_correcta / self.veces_practicada) * 100
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

## 📅 Cronograma Completo

| Fase | Duración | Tareas Principales |
|------|----------|-------------------|
| **Fase 1** | 2 semanas | Diseño BD, migración JSON→SQLite, modelos |
| **Fase 2** | 2 semanas | Refactorización MVC, separación de capas |
| **Fase 3** | 2 semanas | Sistema de plugins, ejemplos |
| **Fase 4** | 2 semanas | API REST, sincronización |
| **Fase 5** | 2 semanas | Tests automatizados, CI/CD |
| **Fase 6** | 1 semana | Empaquetado, documentación |
| **Testing** | 1 semana | QA, corrección de bugs |
| **Release** | - | Lanzamiento v2.0 |

**Total**: ~12 semanas (3 meses)

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

- [ ] Arquitectura MVC completamente implementada
- [ ] Base de datos SQLite funcionando correctamente
- [ ] Al menos 3 plugins funcionales
- [ ] API REST con todos los endpoints
- [ ] Cobertura de tests >80%
- [ ] Documentación completa
- [ ] Migración automática de v1.x funcionando
- [ ] Performance igual o mejor que v1.x
- [ ] Sin bugs críticos

---

## 🎯 Próximos Pasos Inmediatos

1. **Crear repositorio v2.0**: Branch separado o nuevo repo
2. **Configurar entorno de desarrollo**: Virtual env, dependencias
3. **Diseñar esquema de BD**: Revisar y aprobar diseño
4. **Crear script de migración**: Prioridad alta
5. **Implementar modelos básicos**: Palabra, Categoría, Práctica

---

**Fecha de creación**: 2024
**Versión del plan**: 1.0
**Autor**: Equipo English Memory
