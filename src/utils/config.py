"""Configuración de la aplicación"""
import platform
from pathlib import Path

class AppConfig:
    VERSION = "1.4.0"
    APP_NAME = "English Memory"
    
    # Detectar sistema operativo y configurar ruta
    if platform.system() == 'Windows':
        APP_DIR = Path.home() / 'AppData' / 'Local' / 'DiccionarioPersonal'
    else:  # Linux, macOS
        APP_DIR = Path.home() / '.local' / 'share' / 'DiccionarioPersonal'
    
    APP_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVO_DATOS = APP_DIR / 'palabras.json'
    DB_PATH = APP_DIR / 'statistics.db'
    
    # Colores - Tema oscuro
    COLOR_BG_DARK = '#1a1625'
    COLOR_FG_DARK = '#e9e4f0'
    COLOR_ACCENT_DARK = '#a78bfa'
    COLOR_BUTTON_DARK = '#2d2438'
    COLOR_BUTTON_HOVER_DARK = '#3d3149'
    
    # Colores - Tema claro
    COLOR_BG_LIGHT = '#f5f5f5'
    COLOR_FG_LIGHT = '#1a1625'
    COLOR_ACCENT_LIGHT = '#7c3aed'
    COLOR_BUTTON_LIGHT = '#e9e4f0'
    COLOR_BUTTON_HOVER_LIGHT = '#d4d4d8'
    
    # Colores actuales (por defecto oscuro)
    COLOR_BG = COLOR_BG_DARK
    COLOR_FG = COLOR_FG_DARK
    COLOR_ACCENT = COLOR_ACCENT_DARK
    COLOR_BUTTON = COLOR_BUTTON_DARK
    COLOR_BUTTON_HOVER = COLOR_BUTTON_HOVER_DARK
    COLOR_SUCCESS = '#34d399'
    COLOR_ERROR = '#f87171'
    
    # Fuente según sistema operativo
    if platform.system() == 'Windows':
        FONT_FAMILY = 'Segoe UI'
    else:  # Linux, macOS
        FONT_FAMILY = 'Sans'
    
    @classmethod
    def get_colors(cls):
        """Obtener diccionario de colores"""
        return {
            'bg': cls.COLOR_BG,
            'fg': cls.COLOR_FG,
            'accent': cls.COLOR_ACCENT,
            'button': cls.COLOR_BUTTON,
            'button_hover': cls.COLOR_BUTTON_HOVER,
            'success': cls.COLOR_SUCCESS,
            'error': cls.COLOR_ERROR
        }
