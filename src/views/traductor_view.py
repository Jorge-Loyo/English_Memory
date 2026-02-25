"""Vista de Traductor - Inglés ↔ Español"""
import tkinter as tk
from tkinter import ttk, messagebox
from ..utils import AppConfig

class TraductorView(ttk.Frame):
    def __init__(self, parent, tts=None):
        super().__init__(parent)
        self.tts = tts
        self.translator = None
        self.crear_ui()
        self.cargar_traductor()
    
    def cargar_traductor(self):
        """Carga el servicio de traducción"""
        try:
            from ..integrations.translator import TranslatorService
            self.translator = TranslatorService()
        except Exception as e:
            # Traductor no disponible, pero la app sigue funcionando
            self.translator = None
    
    def crear_ui(self):
        container = tk.Frame(self, bg=AppConfig.COLOR_BG)
        container.pack(expand=True, fill='both', padx=40, pady=30)
        
        # Título
        tk.Label(container, text="🌐 Traductor", font=(AppConfig.FONT_FAMILY, 20, 'bold'),
                bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT).pack(pady=(0,20))
        
        # Selector de dirección
        direction_frame = tk.Frame(container, bg=AppConfig.COLOR_BG)
        direction_frame.pack(pady=(0,20))
        
        self.direction = tk.StringVar(value='en-es')
        tk.Radiobutton(direction_frame, text="Inglés → Español", variable=self.direction,
                      value='en-es', bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG,
                      selectcolor=AppConfig.COLOR_BUTTON, font=(AppConfig.FONT_FAMILY, 11)).pack(side='left', padx=10)
        tk.Radiobutton(direction_frame, text="Español → Inglés", variable=self.direction,
                      value='es-en', bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG,
                      selectcolor=AppConfig.COLOR_BUTTON, font=(AppConfig.FONT_FAMILY, 11)).pack(side='left', padx=10)
        
        # Entrada
        tk.Label(container, text="Texto a traducir:", font=(AppConfig.FONT_FAMILY, 12, 'bold'),
                bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack(anchor='w', pady=(10,5))
        
        self.text_input = tk.Text(container, height=6, font=(AppConfig.FONT_FAMILY, 11),
                                 bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_FG,
                                 insertbackground=AppConfig.COLOR_ACCENT, wrap='word')
        self.text_input.pack(fill='x', pady=(0,15))
        
        # Botones
        btn_frame = tk.Frame(container, bg=AppConfig.COLOR_BG)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="🔄 Traducir", command=self.traducir).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ Limpiar", command=self.limpiar).pack(side='left', padx=5)
        
        # Resultado
        tk.Label(container, text="Traducción:", font=(AppConfig.FONT_FAMILY, 12, 'bold'),
                bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack(anchor='w', pady=(20,5))
        
        self.text_output = tk.Text(container, height=6, font=(AppConfig.FONT_FAMILY, 11),
                                  bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_SUCCESS,
                                  wrap='word', state='disabled')
        self.text_output.pack(fill='x', pady=(0,10))
        
        # Botones de resultado
        result_btn_frame = tk.Frame(container, bg=AppConfig.COLOR_BG)
        result_btn_frame.pack(pady=5)
        
        ttk.Button(result_btn_frame, text="🔊 Pronunciar", command=self.pronunciar).pack(side='left', padx=5)
        ttk.Button(result_btn_frame, text="📋 Copiar", command=self.copiar).pack(side='left', padx=5)
    
    def traducir(self):
        if not self.translator:
            messagebox.showwarning("Traductor no disponible",
                                 "El traductor requiere conexión a internet.\nAsegúrate de estar conectado.")
            return
        
        texto = self.text_input.get("1.0", "end-1c").strip()
        if not texto:
            messagebox.showwarning("Advertencia", "Ingresa texto para traducir")
            return
        
        direction = self.direction.get()
        src, dest = direction.split('-')
        
        try:
            result = self.translator.translate(texto, src=src, dest=dest)
            
            self.text_output.config(state='normal')
            self.text_output.delete("1.0", "end")
            self.text_output.insert("1.0", result['text'])
            self.text_output.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"Error al traducir: {str(e)}")
    
    def limpiar(self):
        self.text_input.delete("1.0", "end")
        self.text_output.config(state='normal')
        self.text_output.delete("1.0", "end")
        self.text_output.config(state='disabled')
    
    def pronunciar(self):
        if not self.tts:
            messagebox.showinfo("TTS no disponible", "Pronunciación no disponible")
            return
        
        texto = self.text_output.get("1.0", "end-1c").strip()
        if texto:
            self.tts.speak(texto)
    
    def copiar(self):
        texto = self.text_output.get("1.0", "end-1c").strip()
        if texto:
            self.clipboard_clear()
            self.clipboard_append(texto)
            messagebox.showinfo("Copiado", "Texto copiado al portapapeles")
