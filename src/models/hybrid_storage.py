"""
Hybrid Storage System
Combina JSON (vocabulario) + SQLite (estadísticas)
"""
import json
from pathlib import Path
from .database import Database
from src.utils import BackupManager

class HybridStorage:
    def __init__(self, app_dir):
        self.app_dir = Path(app_dir)
        self.json_path = self.app_dir / 'palabras.json'
        self.db_path = self.app_dir / 'statistics.db'
        
        # Inicializar gestor de backups
        self.backup_manager = BackupManager(max_backups=10)
        
        # Crear backup inicial si existen archivos
        self._crear_backup_inicial()
        
        # Inicializar almacenamiento JSON (vocabulario)
        self.vocabulario = self._load_json()
        
        # Inicializar base de datos SQLite (estadísticas)
        self.stats_db = Database(self.db_path)
    
    def _crear_backup_inicial(self):
        """Crear backup inicial al iniciar la aplicación"""
        try:
            if self.json_path.exists():
                self.backup_manager.crear_backup(str(self.json_path))
        except Exception:
            pass  # Ignorar errores en backup inicial
    
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
        """Guardar vocabulario en JSON con backup automático"""
        try:
            # Crear backup antes de guardar
            if self.json_path.exists():
                self.backup_manager.crear_backup(str(self.json_path))
            
            # Guardar archivo
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
            self._save_json()
            return True
        return False
    
    def obtener_palabra(self, palabra):
        """Obtener datos de una palabra"""
        return self.vocabulario.get(palabra)
    
    def obtener_todas_palabras(self):
        """Obtener todo el vocabulario"""
        return self.vocabulario
    
    def existe_palabra(self, palabra):
        """Verificar si una palabra existe"""
        return palabra in self.vocabulario
    
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
    
    # ========== CATEGORÍAS ==========
    
    def agregar_categoria(self, nombre, descripcion=None, color=None):
        """Agregar nueva categoría"""
        return self.stats_db.agregar_categoria(nombre, descripcion, color)
    
    def asignar_categoria(self, palabra, categoria_id):
        """Asignar categoría a palabra"""
        return self.stats_db.asignar_categoria(palabra, categoria_id)
    
    # ========== BACKUPS ==========
    
    def registrar_backup(self, ruta, tipo='automatico', tamanio=0):
        """Registrar backup en BD"""
        return self.stats_db.registrar_backup(ruta, tipo, tamanio)
    
    # ========== CONFIGURACIÓN ==========
    
    def obtener_config(self, clave, default=None):
        """Obtener configuración"""
        return self.stats_db.obtener_config(clave, default)
    
    def guardar_config(self, clave, valor, tipo='string'):
        """Guardar configuración"""
        return self.stats_db.guardar_config(clave, valor, tipo)
    
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
