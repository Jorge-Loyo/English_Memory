"""Main Window - Ventana principal con tabs"""
import tkinter as tk
from tkinter import ttk
from src.utils import AppConfig, AppStyles

class MainWindow:
    def __init__(self, root, storage, vocab_controller, practica_controller, tts):
        self.root = root
        self.storage = storage
        self.vocab_controller = vocab_controller
        self.practica_controller = practica_controller
        self.tts = tts
        
        self.root.title(f"📚 {AppConfig.APP_NAME} v{AppConfig.VERSION}")
        self.root.geometry("1200x700")
        self.root.configure(bg=AppConfig.COLOR_BG)
        
        AppStyles.configurar_estilos()
        self.crear_header()
        self.crear_notebook()
    
    def crear_header(self):
        """Crear header con título"""
        header = tk.Frame(self.root, bg=AppConfig.COLOR_BG)
        header.pack(fill='x', padx=20, pady=(20,10))
        
        tk.Label(header, text=f"📚 {AppConfig.APP_NAME} v{AppConfig.VERSION}", 
                font=(AppConfig.FONT_FAMILY, 24, 'bold'), 
                bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT).pack()
        
        tk.Label(header, text="Aprende y organiza tu vocabulario en inglés", 
                font=(AppConfig.FONT_FAMILY, 10), 
                bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack()
    
    def crear_notebook(self):
        """Crear notebook con tabs"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.tooltips = {}
        self.notebook.bind('<Motion>', self._on_tab_motion)
        self.notebook.bind('<Leave>', lambda e: self._ocultar_tooltip())
    
    def agregar_tab(self, frame, icono, tooltip=""):
        """Agregar tab al notebook"""
        tab_id = len(self.notebook.tabs())
        self.notebook.add(frame, text=icono)
        if tooltip:
            self.tooltips[tab_id] = tooltip
    
    def _on_tab_motion(self, event):
        """Manejar movimiento del mouse sobre tabs"""
        try:
            tab_id = self.notebook.index(f"@{event.x},{event.y}")
            if tab_id in self.tooltips:
                # Verificar si cambió de tab
                if not hasattr(self, '_current_tab') or self._current_tab != tab_id:
                    self._ocultar_tooltip()
                    self._current_tab = tab_id
                    self._tooltip = tk.Toplevel(self.root)
                    self._tooltip.wm_overrideredirect(True)
                    self._tooltip.wm_geometry(f"+{event.x_root+15}+{event.y_root+15}")
                    
                    # Frame con sombra
                    frame = tk.Frame(self._tooltip, bg='#4a4a4a', relief='solid', borderwidth=2)
                    frame.pack()
                    
                    tk.Label(frame, text=self.tooltips[tab_id], 
                            background='#4a4a4a',
                            foreground='white',
                            font=(AppConfig.FONT_FAMILY, 10, 'bold'),
                            padx=12, pady=6).pack()
            else:
                self._ocultar_tooltip()
                if hasattr(self, '_current_tab'):
                    delattr(self, '_current_tab')
        except:
            self._ocultar_tooltip()
            if hasattr(self, '_current_tab'):
                delattr(self, '_current_tab')
    
    def _ocultar_tooltip(self):
        """Ocultar tooltip"""
        if hasattr(self, '_tooltip'):
            try:
                self._tooltip.destroy()
                delattr(self, '_tooltip')
            except:
                pass
