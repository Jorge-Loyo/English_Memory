"""
Hybrid Storage System
Combina JSON (vocabulario) + SQLite (estadísticas)
"""
import json
from pathlib import Path
from .database import Database

class HybridStorage:
    def __init__(self, app_dir):
        self.app_dir = Path(app_dir)
        self.json_path = self.app_dir / 'palabras.json'
        self.db_path = self.app_dir / 'statistics.db'
        
        # Inicializar almacenamiento JSON (vocabulario)
        self.vocabulario = self._load_json()
        
        # Inicializar base de datos SQLite (estadísticas)
        self.stats_db = Database(self.db_path)
    
    def _load_json(self):
        """Cargar vocabulario desde JSON"""
        if self.json_path.exists():
            try:
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    contenido = f.read().strip()
                    if contenido:
                        return json.loads(contenido)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al cargar JSON: {e}")
        return {}
    
    def _save_json(self):
        """Guardar vocabulario en JSON"""
        try:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(self.vocabulario, f, ensure_ascii=False, indent=2)
            return True
        except (IOError, PermissionError) as e:
            print(f"Error al guardar JSON: {e}")
            return False
    
    # ========== OPERACIONES DE VOCABULARIO (JSON) ==========
    
    def agregar_palabra(self, palabra, significado, pronunciacion=None, notas=None):
        """Agregar palabra al vocabulario"""
        self.vocabulario[palabra] = {'significado': significado}
        if pronunciacion:
            self.vocabulario[palabra]['pronunciacion'] = pronunciacion
        if notas:
            self.vocabulario[palabra]['notas'] = notas
        return self._save_json()
    
    def editar_palabra(self, palabra_antigua, palabra_nueva, significado, pronunciacion=None, notas=None):
        """Editar palabra existente"""
        if palabra_antigua in self.vocabulario:
            del self.vocabulario[palabra_antigua]
        
        self.vocabulario[palabra_nueva] = {'significado': significado}
        if pronunciacion:
            self.vocabulario[palabra_nueva]['pronunciacion'] = pronunciacion
        if notas:
            self.vocabulario[palabra_nueva]['notas'] = notas
        return self._save_json()
    
    def eliminar_palabra(self, palabra):
        """Eliminar palabra del vocabulario"""
        if palabra in self.vocabulario:
            del self.vocabulario[palabra]
            return self._save_json()
        return False
    
    def obtener_palabra(self, palabra):
        """Obtener datos de una palabra"""
        return self.vocabulario.get(palabra)
    
    def obtener_todas_palabras(self):
        """Obtener todo el vocabulario"""
        return self.vocabulario
    
    def buscar_palabras(self, query):
        """Buscar palabras por texto"""
        query = query.lower()
        resultados = {}
        for palabra, datos in self.vocabulario.items():
            if query in palabra.lower() or query in datos.get('significado', '').lower():
                resultados[palabra] = datos
        return resultados
    
    # ========== OPERACIONES DE ESTADÍSTICAS (SQLite) ==========
    
    def registrar_practica(self, palabra, modo, correcta, respuesta_usuario=None, tiempo_respuesta=None):
        """Registrar práctica en base de datos"""
        return self.stats_db.registrar_practica(palabra, modo, correcta, respuesta_usuario, tiempo_respuesta)
    
    def obtener_progreso_palabra(self, palabra):
        """Obtener progreso de una palabra"""
        return self.stats_db.obtener_progreso_palabra(palabra)
    
    def obtener_estadisticas_periodo(self, dias=30):
        """Obtener estadísticas de período"""
        return self.stats_db.obtener_estadisticas_periodo(dias)
    
    def obtener_palabras_dificiles(self, limite=10):
        """Obtener palabras más difíciles"""
        return self.stats_db.obtener_palabras_dificiles(limite)
    
    def obtener_racha_estudio(self):
        """Obtener racha de estudio"""
        return self.stats_db.obtener_racha_estudio()
    
    def obtener_historial_palabra(self, palabra, limite=20):
        """Obtener historial de prácticas de una palabra"""
        return self.stats_db.obtener_historial_palabra(palabra, limite)
    
    # ========== UTILIDADES ==========
    
    def exportar_csv(self, archivo):
        """Exportar vocabulario a CSV (compatible con v1.x)"""
        import csv
        try:
            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Inglés', 'Español', 'Pronunciación', 'Notas'])
                for palabra, datos in self.vocabulario.items():
                    writer.writerow([
                        palabra,
                        datos.get('significado', ''),
                        datos.get('pronunciacion', ''),
                        datos.get('notas', '')
                    ])
            return True
        except Exception as e:
            print(f"Error al exportar CSV: {e}")
            return False
    
    def importar_csv(self, archivo):
        """Importar vocabulario desde CSV"""
        import csv
        try:
            count = 0
            with open(archivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    palabra = row.get('Inglés', '').strip().lower()
                    significado = row.get('Español', '').strip()
                    
                    if palabra and significado:
                        self.vocabulario[palabra] = {'significado': significado}
                        
                        pronunciacion = row.get('Pronunciación', '').strip()
                        if pronunciacion:
                            self.vocabulario[palabra]['pronunciacion'] = pronunciacion
                        
                        notas = row.get('Notas', '').strip()
                        if notas:
                            self.vocabulario[palabra]['notas'] = notas
                        
                        count += 1
            
            self._save_json()
            return count
        except Exception as e:
            print(f"Error al importar CSV: {e}")
            return 0
