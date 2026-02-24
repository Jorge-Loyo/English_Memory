"""
Database Manager para English Memory
Maneja conexiones y operaciones con SQLite
"""
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime

class Database:
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.init_database()
    
    def init_database(self):
        """Inicializar base de datos con schema"""
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Crear schema si no existe
        schema_path = Path(__file__).parent / 'schema.sql'
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        with self.get_connection() as conn:
            conn.executescript(schema_sql)
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexiones SQLite"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def registrar_practica(self, palabra, modo, correcta, respuesta_usuario=None, tiempo_respuesta=None):
        """Registrar una práctica en el historial"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO practicas (palabra, modo, correcta, respuesta_usuario, tiempo_respuesta)
                VALUES (?, ?, ?, ?, ?)
            """, (palabra, modo, correcta, respuesta_usuario, tiempo_respuesta))
            
            # Actualizar progreso de la palabra
            cursor.execute("""
                INSERT INTO progreso_palabras (palabra, veces_vista, veces_correcta, veces_incorrecta, ultima_practica)
                VALUES (?, 1, ?, ?, ?)
                ON CONFLICT(palabra) DO UPDATE SET
                    veces_vista = veces_vista + 1,
                    veces_correcta = veces_correcta + ?,
                    veces_incorrecta = veces_incorrecta + ?,
                    ultima_practica = ?
            """, (
                palabra,
                1 if correcta else 0,
                0 if correcta else 1,
                datetime.now(),
                1 if correcta else 0,
                0 if correcta else 1,
                datetime.now()
            ))
            
            # Actualizar estadísticas diarias
            fecha_hoy = datetime.now().date()
            cursor.execute("""
                INSERT INTO estadisticas_diarias (fecha, palabras_practicadas, practicas_totales, practicas_correctas, tiempo_total)
                VALUES (?, 1, 1, ?, ?)
                ON CONFLICT(fecha) DO UPDATE SET
                    practicas_totales = practicas_totales + 1,
                    practicas_correctas = practicas_correctas + ?,
                    tiempo_total = tiempo_total + ?
            """, (
                fecha_hoy,
                1 if correcta else 0,
                tiempo_respuesta or 0,
                1 if correcta else 0,
                tiempo_respuesta or 0
            ))
    
    def obtener_progreso_palabra(self, palabra):
        """Obtener progreso de una palabra específica"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM progreso_palabras WHERE palabra = ?
            """, (palabra,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def obtener_estadisticas_periodo(self, dias=30):
        """Obtener estadísticas de los últimos N días"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT fecha, practicas_totales, practicas_correctas, tiempo_total
                FROM estadisticas_diarias
                WHERE fecha >= DATE('now', '-' || ? || ' days')
                ORDER BY fecha DESC
            """, (dias,))
            return [dict(row) for row in cursor.fetchall()]
    
    def obtener_palabras_dificiles(self, limite=10):
        """Obtener las palabras más difíciles"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT palabra, veces_vista, veces_correcta, veces_incorrecta,
                       CAST(veces_correcta AS REAL) / veces_vista * 100 as tasa_exito
                FROM progreso_palabras
                WHERE veces_vista >= 3
                ORDER BY tasa_exito ASC, veces_vista DESC
                LIMIT ?
            """, (limite,))
            return [dict(row) for row in cursor.fetchall()]
    
    def obtener_racha_estudio(self):
        """Calcular racha de días consecutivos estudiando"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(DISTINCT fecha) as dias_estudiados
                FROM estadisticas_diarias
                WHERE fecha >= DATE('now', '-30 days')
            """)
            row = cursor.fetchone()
            return row['dias_estudiados'] if row else 0
    
    def obtener_historial_palabra(self, palabra, limite=20):
        """Obtener historial de prácticas de una palabra"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT modo, correcta, respuesta_usuario, tiempo_respuesta, fecha
                FROM practicas
                WHERE palabra = ?
                ORDER BY fecha DESC
                LIMIT ?
            """, (palabra, limite))
            return [dict(row) for row in cursor.fetchall()]
    
    def agregar_categoria(self, nombre, descripcion=None, color=None):
        """Agregar nueva categoría"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO categorias (nombre, descripcion, color)
                VALUES (?, ?, ?)
            """, (nombre, descripcion, color))
            return cursor.lastrowid
    
    def asignar_categoria(self, palabra, categoria_id):
        """Asignar categoría a palabra"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO palabra_categoria (palabra, categoria_id)
                VALUES (?, ?)
            """, (palabra, categoria_id))
    
    def registrar_backup(self, ruta, tipo='automatico', tamanio=0):
        """Registrar backup en BD"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO backups (ruta, tipo, tamanio)
                VALUES (?, ?, ?)
            """, (ruta, tipo, tamanio))
    
    def obtener_config(self, clave, default=None):
        """Obtener valor de configuración"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT valor FROM configuracion WHERE clave = ?", (clave,))
            row = cursor.fetchone()
            return row['valor'] if row else default
    
    def guardar_config(self, clave, valor, tipo='string'):
        """Guardar configuración"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO configuracion (clave, valor, tipo)
                VALUES (?, ?, ?)
            """, (clave, str(valor), tipo))
