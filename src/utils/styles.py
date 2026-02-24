"""Estilos y temas de la aplicación"""
from tkinter import ttk
from .config import AppConfig

class AppStyles:
    @staticmethod
    def configurar_estilos():
        """Configurar todos los estilos de ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook
        style.configure('TNotebook', 
            background=AppConfig.COLOR_BG, 
            borderwidth=0
        )
        style.configure('TNotebook.Tab', 
            background=AppConfig.COLOR_BUTTON, 
            foreground=AppConfig.COLOR_FG,
            padding=[20, 10], 
            font=(AppConfig.FONT_FAMILY, 10, 'bold')
        )
        style.map('TNotebook.Tab', 
            background=[('selected', AppConfig.COLOR_ACCENT)],
            foreground=[('selected', AppConfig.COLOR_BG)]
        )
        
        # Frame
        style.configure('TFrame', background=AppConfig.COLOR_BG)
        
        # Label
        style.configure('TLabel', 
            background=AppConfig.COLOR_BG, 
            foreground=AppConfig.COLOR_FG,
            font=(AppConfig.FONT_FAMILY, 10)
        )
        style.configure('Title.TLabel', 
            font=(AppConfig.FONT_FAMILY, 12, 'bold'),
            foreground=AppConfig.COLOR_ACCENT
        )
        
        # Entry
        style.configure('TEntry', 
            fieldbackground=AppConfig.COLOR_BUTTON,
            foreground=AppConfig.COLOR_FG,
            borderwidth=1, 
            relief='solid',
            insertcolor=AppConfig.COLOR_ACCENT
        )
        style.map('TEntry',
            fieldbackground=[('focus', '#3d3149')],
            bordercolor=[('focus', AppConfig.COLOR_ACCENT)]
        )
        
        # Button
        style.configure('TButton', 
            background=AppConfig.COLOR_ACCENT,
            foreground=AppConfig.COLOR_BG,
            borderwidth=0, 
            font=(AppConfig.FONT_FAMILY, 10, 'bold'),
            padding=[20, 10]
        )
        style.map('TButton', 
            background=[('active', AppConfig.COLOR_BUTTON_HOVER)]
        )
        
        # Treeview (Tablas)
        style.configure('Treeview',
            background=AppConfig.COLOR_BUTTON,
            foreground=AppConfig.COLOR_FG,
            fieldbackground=AppConfig.COLOR_BUTTON,
            borderwidth=0,
            font=(AppConfig.FONT_FAMILY, 10)
        )
        style.configure('Treeview.Heading',
            background=AppConfig.COLOR_ACCENT,
            foreground=AppConfig.COLOR_BG,
            borderwidth=0,
            font=(AppConfig.FONT_FAMILY, 10, 'bold')
        )
        style.map('Treeview',
            background=[('selected', AppConfig.COLOR_ACCENT)],
            foreground=[('selected', AppConfig.COLOR_BG)]
        )
        
        # Scrollbar
        style.configure('Vertical.TScrollbar',
            background=AppConfig.COLOR_BUTTON,
            troughcolor=AppConfig.COLOR_BG,
            borderwidth=0,
            arrowcolor=AppConfig.COLOR_FG
        )
