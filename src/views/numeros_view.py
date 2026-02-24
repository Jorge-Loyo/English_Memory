"""Números View - Conversor de números"""
import tkinter as tk
from tkinter import ttk, messagebox
from src.utils import AppConfig

class NumerosView(ttk.Frame):
    def __init__(self, parent, tts):
        super().__init__(parent)
        self.tts = tts
        self.crear_ui()
    
    def crear_ui(self):
        canvas = tk.Canvas(self, bg=AppConfig.COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=AppConfig.COLOR_BG)
        
        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw", width=1000)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y", pady=20)
        
        # Conversor
        conv = tk.Frame(content, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
        conv.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        ttk.Label(conv, text="🔢 Conversor de Números", font=(AppConfig.FONT_FAMILY, 16, 'bold'), 
                 foreground=AppConfig.COLOR_ACCENT, background=AppConfig.COLOR_BUTTON).pack(pady=(10,15))
        
        input_frame = tk.Frame(conv, bg=AppConfig.COLOR_BUTTON)
        input_frame.pack(pady=(0,10))
        
        ttk.Label(input_frame, text="Número:", background=AppConfig.COLOR_BUTTON).pack(side='left', padx=5)
        self.entry_numero = ttk.Entry(input_frame, width=20, font=(AppConfig.FONT_FAMILY, 12))
        self.entry_numero.pack(side='left', padx=5, ipady=5)
        ttk.Button(input_frame, text="✓ Convertir", command=self.convertir).pack(side='left', padx=5)
        ttk.Button(input_frame, text="🔊 Pronunciar", command=self.pronunciar).pack(side='left', padx=5)
        
        self.label_resultado = tk.Label(conv, text="", font=(AppConfig.FONT_FAMILY, 14, 'bold'), 
                                        bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_SUCCESS, wraplength=800)
        self.label_resultado.pack(pady=(5,10))
        
        # Números 1-20
        num_frame = tk.Frame(content, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
        num_frame.pack(fill='x', padx=20, pady=(0,20), ipady=10)
        
        ttk.Label(num_frame, text="📊 Números del 1 al 20", font=(AppConfig.FONT_FAMILY, 14, 'bold'), 
                 foreground=AppConfig.COLOR_ACCENT, background=AppConfig.COLOR_BUTTON).pack(pady=(10,10))
        
        grid = tk.Frame(num_frame, bg=AppConfig.COLOR_BUTTON)
        grid.pack(padx=20, pady=(0,10))
        
        nums = [('1','one'),('2','two'),('3','three'),('4','four'),('5','five'),('6','six'),('7','seven'),
                ('8','eight'),('9','nine'),('10','ten'),('11','eleven'),('12','twelve'),('13','thirteen'),
                ('14','fourteen'),('15','fifteen'),('16','sixteen'),('17','seventeen'),('18','eighteen'),
                ('19','nineteen'),('20','twenty')]
        
        for i, (num, palabra) in enumerate(nums):
            item = tk.Frame(grid, bg=AppConfig.COLOR_BG, relief='solid', borderwidth=1)
            item.grid(row=i//5, column=i%5, padx=5, pady=5, sticky='ew')
            tk.Label(item, text=f"{num} = {palabra}", font=(AppConfig.FONT_FAMILY, 10), 
                    bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG, width=15).pack(padx=10, pady=5)
    
    def convertir(self):
        try:
            num = int(self.entry_numero.get().strip())
            if num < 0 or num > 999999999:
                self.label_resultado.config(text="⚠️ Número entre 0 y 999,999,999", fg=AppConfig.COLOR_ERROR)
                return
            resultado = self.numero_a_texto(num)
            self.label_resultado.config(text=f"✅ {resultado}", fg=AppConfig.COLOR_SUCCESS)
        except ValueError:
            self.label_resultado.config(text="⚠️ Ingresa un número válido", fg=AppConfig.COLOR_ERROR)
    
    def numero_a_texto(self, n):
        if n == 0: return "zero"
        
        unidades = ['','one','two','three','four','five','six','seven','eight','nine']
        decenas_esp = ['ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
        decenas = ['','','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
        
        def conv_centenas(num):
            if num == 0: return ''
            elif num < 10: return unidades[num]
            elif num < 20: return decenas_esp[num-10]
            elif num < 100: return decenas[num//10] + ('-' + unidades[num%10] if num%10 else '')
            else: return unidades[num//100] + ' hundred' + (' and ' + conv_centenas(num%100) if num%100 else '')
        
        if n < 1000: return conv_centenas(n)
        elif n < 1000000:
            return conv_centenas(n//1000) + ' thousand' + (' ' + conv_centenas(n%1000) if n%1000 else '')
        else:
            return conv_centenas(n//1000000) + ' million' + (' ' + conv_centenas((n%1000000)//1000) + ' thousand' if (n%1000000)//1000 else '') + (' ' + conv_centenas(n%1000) if n%1000 else '')
    
    def pronunciar(self):
        try:
            num = int(self.entry_numero.get().strip())
            if num < 0 or num > 999999999:
                messagebox.showwarning("Advertencia", "Número entre 0 y 999,999,999")
                return
            if self.tts.esta_disponible():
                self.tts.pronunciar(self.numero_a_texto(num))
        except ValueError:
            messagebox.showwarning("Advertencia", "Ingresa un número válido")
