"""Plugin de ejemplo: Exportar a CSV"""
from src.plugins import BasePlugin
import csv

class CSVExportPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.name = "CSV Export"
        self.version = "1.0.0"
        self.description = "Exporta vocabulario a CSV"
        self.storage = None
    
    def initialize(self, app_context):
        """Inicializar con contexto"""
        self.storage = app_context.get('storage')
    
    def execute(self, filepath):
        """Exportar a CSV"""
        if not self.storage:
            raise RuntimeError("Plugin no inicializado")
        
        palabras = self.storage.obtener_todas_palabras()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Inglés', 'Español', 'Pronunciación', 'Notas'])
            
            for palabra, datos in palabras.items():
                writer.writerow([
                    palabra,
                    datos.get('significado', ''),
                    datos.get('pronunciacion', ''),
                    datos.get('notas', '')
                ])
        
        return f"Exportadas {len(palabras)} palabras a {filepath}"
