"""Práctica View - Tab de quiz"""
import tkinter as tk
from tkinter import ttk, messagebox
from src.utils import AppConfig

class PracticaView(ttk.Frame):
    def __init__(self, parent, practica_controller, tts):
        super().__init__(parent)
        self.practica_controller = practica_controller
        self.tts = tts
        
        self.practica_palabra = tk.StringVar()
        self.practica_respuesta = tk.StringVar()
        self.practica_modo = tk.StringVar(value='ingles')
        
        self.crear_ui()
        self.nueva_palabra()
    
    def crear_ui(self):
        container = tk.Frame(self, bg=AppConfig.COLOR_BG)
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Label(container, text="🎯 Modo Práctica", font=(AppConfig.FONT_FAMILY, 18, 'bold'), 
                 foreground=AppConfig.COLOR_ACCENT, background=AppConfig.COLOR_BG).pack(pady=(0,20))
        
        # Selector de modo
        frame_modo = tk.Frame(container, bg=AppConfig.COLOR_BG)
        frame_modo.pack(pady=(0,20))
        tk.Radiobutton(frame_modo, text="Inglés → Español", variable=self.practica_modo, 
                      value='ingles', bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG, 
                      selectcolor=AppConfig.COLOR_BUTTON, font=(AppConfig.FONT_FAMILY, 10)).pack(side='left', padx=10)
        tk.Radiobutton(frame_modo, text="Español → Inglés", variable=self.practica_modo, 
                      value='espanol', bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG, 
                      selectcolor=AppConfig.COLOR_BUTTON, font=(AppConfig.FONT_FAMILY, 10)).pack(side='left', padx=10)
        
        # Palabra
        self.label_practica = tk.Label(container, textvariable=self.practica_palabra, 
                                       font=(AppConfig.FONT_FAMILY, 24, 'bold'), bg=AppConfig.COLOR_BG, 
                                       fg=AppConfig.COLOR_ACCENT, wraplength=400)
        self.label_practica.pack(pady=20)
        
        # Respuesta
        ttk.Label(container, text="Tu respuesta:", background=AppConfig.COLOR_BG, 
                 font=(AppConfig.FONT_FAMILY, 12)).pack(pady=(10,5))
        self.entry_respuesta = ttk.Entry(container, width=40, font=(AppConfig.FONT_FAMILY, 14))
        self.entry_respuesta.pack(pady=(0,10), ipady=8)
        self.entry_respuesta.bind('<Return>', lambda e: self.verificar())
        
        # Resultado
        self.label_respuesta = tk.Label(container, textvariable=self.practica_respuesta, 
                                        font=(AppConfig.FONT_FAMILY, 16), bg=AppConfig.COLOR_BG, 
                                        fg=AppConfig.COLOR_SUCCESS, wraplength=500)
        self.label_respuesta.pack(pady=10)
        
        # Botones
        btn_frame = tk.Frame(container, bg=AppConfig.COLOR_BG)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="✓ Verificar", command=self.verificar).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔄 Nueva", command=self.nueva_palabra).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔊 Pronunciar", command=self.pronunciar).pack(side='left', padx=5)
    
    def nueva_palabra(self):
        self.practica_controller.cambiar_modo(self.practica_modo.get())
        palabra = self.practica_controller.obtener_palabra_aleatoria()
        if not palabra:
            self.practica_palabra.set("No hay palabras")
            return
        
        pregunta = self.practica_controller.obtener_pregunta()
        self.practica_palabra.set(f"{'🇬🇧' if self.practica_modo.get() == 'ingles' else '🇪🇸'} {pregunta['pregunta']}")
        self.practica_respuesta.set("")
        self.entry_respuesta.delete(0, tk.END)
        self.entry_respuesta.focus()
    
    def verificar(self):
        respuesta = self.entry_respuesta.get().strip()
        if not respuesta:
            messagebox.showwarning("Advertencia", "Ingresa una respuesta")
            return
        
        es_correcta = self.practica_controller.verificar_respuesta(respuesta)
        pregunta = self.practica_controller.obtener_pregunta()
        
        if es_correcta:
            resultado = f"✅ ¡CORRECTO!\n{pregunta['pregunta']} = {pregunta['respuesta_correcta']}"
            self.label_respuesta.config(fg=AppConfig.COLOR_SUCCESS)
        else:
            resultado = f"❌ INCORRECTO\nTu respuesta: {respuesta}\nRespuesta correcta: {pregunta['respuesta_correcta']}"
            self.label_respuesta.config(fg=AppConfig.COLOR_ERROR)
        
        if pregunta.get('pronunciacion'):
            resultado += f"\n🔊 {pregunta['pronunciacion']}"
        if pregunta.get('notas'):
            resultado += f"\n📝 {pregunta['notas']}"
        
        self.practica_respuesta.set(resultado)
    
    def pronunciar(self):
        if not self.tts.esta_disponible():
            messagebox.showinfo("TTS no disponible", "Instala pyttsx3: pip install pyttsx3")
            return
        try:
            palabra = self.practica_controller.palabra_actual
            if palabra:
                self.tts.pronunciar(palabra)
        except Exception as e:
            messagebox.showerror("Error TTS", str(e))
