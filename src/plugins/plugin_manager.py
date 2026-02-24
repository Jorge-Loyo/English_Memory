"""Plugin Manager - Gestión de plugins"""
import importlib.util
from pathlib import Path

class PluginManager:
    def __init__(self, plugins_dir):
        self.plugins_dir = Path(plugins_dir)
        self.loaded_plugins = {}
        self.app_context = None
    
    def set_app_context(self, context):
        """Establecer contexto de la aplicación"""
        self.app_context = context
    
    def discover_plugins(self):
        """Buscar plugins en directorio"""
        if not self.plugins_dir.exists():
            return []
        
        plugins = []
        for file in self.plugins_dir.glob("*.py"):
            if file.stem.startswith("_"):
                continue
            plugins.append(file.stem)
        return plugins
    
    def load_plugin(self, plugin_name):
        """Cargar plugin dinámicamente"""
        plugin_path = self.plugins_dir / f"{plugin_name}.py"
        if not plugin_path.exists():
            raise FileNotFoundError(f"Plugin {plugin_name} no encontrado")
        
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Buscar clase que herede de BasePlugin
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and hasattr(attr, 'initialize'):
                plugin_instance = attr()
                plugin_instance.initialize(self.app_context)
                self.loaded_plugins[plugin_name] = plugin_instance
                return plugin_instance
        
        raise ValueError(f"No se encontró clase plugin en {plugin_name}")
    
    def unload_plugin(self, plugin_name):
        """Descargar plugin"""
        if plugin_name in self.loaded_plugins:
            self.loaded_plugins[plugin_name].cleanup()
            del self.loaded_plugins[plugin_name]
    
    def execute_plugin(self, plugin_name, *args, **kwargs):
        """Ejecutar plugin"""
        if plugin_name not in self.loaded_plugins:
            self.load_plugin(plugin_name)
        
        return self.loaded_plugins[plugin_name].execute(*args, **kwargs)
    
    def get_loaded_plugins(self):
        """Obtener plugins cargados"""
        return list(self.loaded_plugins.keys())
