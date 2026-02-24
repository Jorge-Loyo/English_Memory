"""Main Window - Ventana principal con tabs"""
import tkinter as tk
from tkinter import ttk
from src.utils import AppConfig

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
        
        self.configurar_estilos()
        self.crear_header()
        self.crear_notebook()
    
    def configurar_estilos(self):
        """Configurar estilos de ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TNotebook', background=AppConfig.COLOR_BG, borderwidth=0)
        style.configure('TNotebook.Tab', background=AppConfig.COLOR_BUTTON, 
                       foreground=AppConfig.COLOR_FG, padding=[20, 10], 
                       font=(AppConfig.FONT_FAMILY, 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', AppConfig.COLOR_ACCENT)], 
                 foreground=[('selected', AppConfig.COLOR_BG)])
        
        style.configure('TFrame', background=AppConfig.COLOR_BG)
        style.configure('TLabel', background=AppConfig.COLOR_BG, 
                       foreground=AppConfig.COLOR_FG, font=(AppConfig.FONT_FAMILY, 10))
    
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
    
    def agregar_tab(self, frame, icono):
        """Agregar tab al notebook"""
        self.notebook.add(frame, text=icono)
