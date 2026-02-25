"""Sistema de backups automáticos"""
import shutil
from pathlib import Path
from datetime import datetime

class BackupManager:
    def __init__(self, backup_dir=None, max_backups=10):
        """
        Inicializar gestor de backups
        
        Args:
            backup_dir: Directorio para backups (None = mismo directorio que archivo)
            max_backups: Número máximo de backups a mantener
        """
        self.backup_dir = backup_dir
        self.max_backups = max_backups
    
    def crear_backup(self, source_file):
        """
        Crear backup de un archivo
        
        Args:
            source_file: Ruta del archivo a respaldar
            
        Returns:
            Ruta del archivo de backup creado
        """
        source_path = Path(source_file)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {source_file}")
        
        # Determinar directorio de backup
        if self.backup_dir:
            backup_path = Path(self.backup_dir)
            backup_path.mkdir(parents=True, exist_ok=True)
        else:
            backup_path = source_path.parent
        
        # Crear nombre de backup con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = backup_path / f"{source_path.name}.backup_{timestamp}"
        
        # Copiar archivo
        shutil.copy2(source_path, backup_file)
        
        # Limpiar backups antiguos
        self._limpiar_backups_antiguos(source_path.name, backup_path)
        
        return str(backup_file)
    
    def _limpiar_backups_antiguos(self, base_name, backup_dir):
        """Eliminar backups antiguos manteniendo solo los más recientes"""
        pattern = f"{base_name}.backup_*"
        backups = sorted(backup_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
        
        # Eliminar backups excedentes
        for backup in backups[self.max_backups:]:
            try:
                backup.unlink()
            except Exception:
                pass  # Ignorar errores al eliminar
    
    def restaurar_backup(self, backup_file, target_file):
        """
        Restaurar un backup
        
        Args:
            backup_file: Ruta del backup a restaurar
            target_file: Ruta destino
        """
        backup_path = Path(backup_file)
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup no encontrado: {backup_file}")
        
        shutil.copy2(backup_path, target_file)
    
    def listar_backups(self, base_name, backup_dir=None):
        """
        Listar backups disponibles para un archivo
        
        Args:
            base_name: Nombre base del archivo
            backup_dir: Directorio donde buscar (None = directorio actual)
            
        Returns:
            Lista de rutas de backups ordenados por fecha (más reciente primero)
        """
        search_dir = Path(backup_dir) if backup_dir else Path.cwd()
        pattern = f"{base_name}.backup_*"
        backups = sorted(search_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
        return [str(b) for b in backups]
