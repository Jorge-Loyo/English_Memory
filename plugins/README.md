# Plugins de Usuario

Este directorio contiene plugins personalizados para English Memory.

## Crear un Plugin

1. Crea un archivo `.py` en este directorio
2. Importa `BasePlugin` de `src.plugins`
3. Crea una clase que herede de `BasePlugin`
4. Implementa los métodos `initialize()` y `execute()`

## Ejemplo

```python
from src.plugins import BasePlugin

class MiPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.name = "Mi Plugin"
        self.version = "1.0.0"
        self.description = "Descripción"
    
    def initialize(self, app_context):
        self.storage = app_context.get('storage')
    
    def execute(self, *args, **kwargs):
        # Tu código aquí
        return "Resultado"
```

## Plugins Disponibles

- `csv_export.py` - Exportar vocabulario a CSV
