"""Caligrafía View - Práctica de escritura"""
import tkinter as tk
from tkinter import ttk
import random
from src.utils import AppConfig

class CaligrafiaView(ttk.Frame):
    def __init__(self, parent, storage, practica_controller, tts):
        super().__init__(parent)
        self.storage = storage
        self.practica_controller = practica_controller
        self.tts = tts
        self.indice = 0
        self.lista_palabras = []
        self.modo = tk.StringVar(value='erroneas')
        
        self.crear_ui()
        self.cargar_palabras()
    
    def crear_ui(self):
        # Header
        frame_top = tk.Frame(self, bg=AppConfig.COLOR_BG)
        frame_top.pack(fill='x', padx=30, pady=20)
        
        ttk.Label(frame_top, text="✍️ Práctica de Caligrafía", 
                 font=(AppConfig.FONT_FAMILY, 18, 'bold'), foreground=AppConfig.COLOR_ACCENT, 
                 background=AppConfig.COLOR_BG).pack(pady=(0,10))
        
        # Selector modo
        modo_frame = tk.Frame(frame_top, bg=AppConfig.COLOR_BG)
        modo_frame.pack(pady=10)
        
        tk.Radiobutton(modo_frame, text="Palabras Erróneas", variable=self.modo,
                      value='erroneas', bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG, 
                      selectcolor=AppConfig.COLOR_BUTTON, font=(AppConfig.FONT_FAMILY, 10), 
                      command=self.cargar_palabras).pack(side='left', padx=10)
        tk.Radiobutton(modo_frame, text="Todo el Vocabulario", variable=self.modo,
                      value='todas', bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG, 
                      selectcolor=AppConfig.COLOR_BUTTON, font=(AppConfig.FONT_FAMILY, 10), 
                      command=self.cargar_palabras).pack(side='left', padx=10)
        
        self.label_info = tk.Label(frame_top, text="", font=(AppConfig.FONT_FAMILY, 11), 
                                   bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG)
        self.label_info.pack(pady=5)
        
        # Canvas con scroll
        canvas_frame = tk.Frame(self, bg=AppConfig.COLOR_BG)
        canvas_frame.pack(fill="both", expand=True, padx=30, pady=(0,10))
        
        canvas = tk.Canvas(canvas_frame, bg=AppConfig.COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        self.content = tk.Frame(canvas, bg=AppConfig.COLOR_BG)
        
        self.content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=self.content, anchor="nw")
        
        # Ajustar ancho del contenido al canvas
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Habilitar scroll con mouse
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones
        btn_frame = tk.Frame(self, bg=AppConfig.COLOR_BG)
        btn_frame.pack(pady=(0,20))
        
        ttk.Button(btn_frame, text="◀ Anterior", command=self.anterior).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_palabras).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Siguiente ▶", command=self.siguiente).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔊 Pronunciar", command=self.pronunciar).pack(side='left', padx=5)
    
    def cargar_palabras(self):
        if self.modo.get() == 'erroneas':
            palabras_erroneas = self.practica_controller.obtener_palabras_erroneas()
            self.lista_palabras = sorted(list(palabras_erroneas)) if palabras_erroneas else []
        else:
            self.lista_palabras = sorted(self.storage.obtener_todas_palabras().keys())
        
        self.indice = 0
        self.actualizar()
    
    def actualizar(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        if not self.lista_palabras:
            msg = "🎯 No hay palabras erróneas" if self.modo.get() == 'erroneas' else "📚 No hay palabras"
            tk.Label(self.content, text=msg, font=(AppConfig.FONT_FAMILY, 14), 
                    bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack(pady=100)
            self.label_info.config(text="")
            return
        
        palabra = self.lista_palabras[self.indice]
        datos = self.storage.obtener_palabra(palabra)
        significado = datos.get('significado', '') if datos else ''
        
        self.label_info.config(text=f"Palabra {self.indice + 1} de {len(self.lista_palabras)}")
        
        # Tarjeta
        card = tk.Frame(self.content, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=2)
        card.pack(fill='x', pady=(0,30), padx=50, ipady=20)
        
        tk.Label(card, text=palabra, font=(AppConfig.FONT_FAMILY, 32, 'bold'), 
                bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_ACCENT).pack(pady=(10,5))
        tk.Label(card, text=significado, font=(AppConfig.FONT_FAMILY, 16), 
                bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_FG).pack(pady=5)
        
        # Práctica
        practice = tk.Frame(self.content, bg=AppConfig.COLOR_BG)
        practice.pack(fill='both', expand=True, padx=50)
        
        tk.Label(practice, text="🇬🇧 Inglés:", font=(AppConfig.FONT_FAMILY, 13, 'bold'), 
                bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT, anchor='w').pack(fill='x', pady=(10,5))
        
        for i, (titulo, mostrar) in enumerate([("1. Copia:", True), ("2. Con guía:", False), ("3. De memoria:", False)], 1):
            self.crear_linea(practice, titulo, palabra if mostrar else "")
        
        tk.Label(practice, text="\n🇪🇸 Español:", font=(AppConfig.FONT_FAMILY, 13, 'bold'), 
                bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT, anchor='w').pack(fill='x', pady=(15,5))
        
        for i, (titulo, mostrar) in enumerate([("4. Copia:", True), ("5. Con guía:", False), ("6. De memoria:", False)], 4):
            self.crear_linea(practice, titulo, significado if mostrar else "")
    
    def crear_linea(self, parent, titulo, texto):
        container = tk.Frame(parent, bg=AppConfig.COLOR_BG)
        container.pack(fill='x', pady=8)
        
        tk.Label(container, text=titulo, font=(AppConfig.FONT_FAMILY, 11, 'bold'), 
                bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT, width=25, anchor='w').pack(side='left')
        
        if texto:
            line = tk.Frame(container, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
            line.pack(side='left', fill='x', expand=True, ipady=10)
            tk.Label(line, text=texto, font=(AppConfig.FONT_FAMILY, 18, 'bold'), 
                    bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_BUTTON_HOVER, anchor='w').pack(side='left', padx=20)
        else:
            entry = ttk.Entry(container, font=(AppConfig.FONT_FAMILY, 16), width=40)
            entry.pack(side='left', fill='x', expand=True, ipady=8)
    
    def anterior(self):
        if self.lista_palabras and self.indice > 0:
            self.indice -= 1
            self.actualizar()
    
    def siguiente(self):
        if self.lista_palabras and self.indice < len(self.lista_palabras) - 1:
            self.indice += 1
            self.actualizar()
    
    def pronunciar(self):
        if self.lista_palabras and self.tts.esta_disponible():
            try:
                self.tts.pronunciar(self.lista_palabras[self.indice])
            except:
                pass
