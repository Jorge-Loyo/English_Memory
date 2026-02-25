"""Base Plugin - Clase abstracta para plugins"""
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    def __init__(self):
        self.name = ""
        self.version = ""
        self.description = ""
        self.enabled = True
    
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
