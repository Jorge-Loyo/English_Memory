"""Números View - Conversor de números y reglas"""
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
        self._crear_conversor(content)
        
        # Números cardinales 1-20
        self._crear_cardinales(content)
        
        # Números ordinales
        self._crear_ordinales(content)
        
        # Decenas y centenas
        self._crear_decenas_centenas(content)
        
        # Reglas de uso
        self._crear_reglas(content)
    
    def _crear_conversor(self, parent):
        conv = tk.Frame(parent, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
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
    
    def _crear_cardinales(self, parent):
        num_frame = tk.Frame(parent, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
        num_frame.pack(fill='x', padx=20, pady=(0,20), ipady=10)
        
        ttk.Label(num_frame, text="📊 Números Cardinales (1-20)", font=(AppConfig.FONT_FAMILY, 14, 'bold'), 
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
    
    def _crear_ordinales(self, parent):
        ord_frame = tk.Frame(parent, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
        ord_frame.pack(fill='x', padx=20, pady=(0,20), ipady=10)
        
        ttk.Label(ord_frame, text="🥇 Números Ordinales (Primero, Segundo...)", font=(AppConfig.FONT_FAMILY, 14, 'bold'), 
                 foreground=AppConfig.COLOR_ACCENT, background=AppConfig.COLOR_BUTTON).pack(pady=(10,10))
        
        grid = tk.Frame(ord_frame, bg=AppConfig.COLOR_BUTTON)
        grid.pack(padx=20, pady=(0,10))
        
        ordinales = [
            ('1st','first'),('2nd','second'),('3rd','third'),('4th','fourth'),('5th','fifth'),
            ('6th','sixth'),('7th','seventh'),('8th','eighth'),('9th','ninth'),('10th','tenth'),
            ('11th','eleventh'),('12th','twelfth'),('13th','thirteenth'),('14th','fourteenth'),('15th','fifteenth'),
            ('16th','sixteenth'),('17th','seventeenth'),('18th','eighteenth'),('19th','nineteenth'),('20th','twentieth'),
            ('21st','twenty-first'),('22nd','twenty-second'),('23rd','twenty-third'),('30th','thirtieth'),('40th','fortieth'),
            ('50th','fiftieth'),('60th','sixtieth'),('70th','seventieth'),('80th','eightieth'),('90th','ninetieth'),('100th','hundredth')
        ]
        
        for i, (num, palabra) in enumerate(ordinales):
            item = tk.Frame(grid, bg=AppConfig.COLOR_BG, relief='solid', borderwidth=1)
            item.grid(row=i//5, column=i%5, padx=5, pady=5, sticky='ew')
            tk.Label(item, text=f"{num} = {palabra}", font=(AppConfig.FONT_FAMILY, 10), 
                    bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG, width=15).pack(padx=10, pady=5)
    
    def _crear_decenas_centenas(self, parent):
        dec_frame = tk.Frame(parent, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
        dec_frame.pack(fill='x', padx=20, pady=(0,20), ipady=10)
        
        ttk.Label(dec_frame, text="📈 Decenas, Centenas y Más", font=(AppConfig.FONT_FAMILY, 14, 'bold'), 
                 foreground=AppConfig.COLOR_ACCENT, background=AppConfig.COLOR_BUTTON).pack(pady=(10,10))
        
        grid = tk.Frame(dec_frame, bg=AppConfig.COLOR_BUTTON)
        grid.pack(padx=20, pady=(0,10))
        
        grandes = [
            ('20','twenty'),('30','thirty'),('40','forty'),('50','fifty'),('60','sixty'),
            ('70','seventy'),('80','eighty'),('90','ninety'),('100','one hundred'),('200','two hundred'),
            ('500','five hundred'),('1,000','one thousand'),('10,000','ten thousand'),('100,000','one hundred thousand'),
            ('1,000,000','one million'),('1,000,000,000','one billion')
        ]
        
        for i, (num, palabra) in enumerate(grandes):
            item = tk.Frame(grid, bg=AppConfig.COLOR_BG, relief='solid', borderwidth=1)
            item.grid(row=i//4, column=i%4, padx=5, pady=5, sticky='ew')
            tk.Label(item, text=f"{num} = {palabra}", font=(AppConfig.FONT_FAMILY, 10), 
                    bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG, width=20).pack(padx=10, pady=5)
    
    def _crear_reglas(self, parent):
        reglas_frame = tk.Frame(parent, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
        reglas_frame.pack(fill='x', padx=20, pady=(0,20), ipady=10)
        
        ttk.Label(reglas_frame, text="📝 Reglas de Uso de Números en Inglés", font=(AppConfig.FONT_FAMILY, 14, 'bold'), 
                 foreground=AppConfig.COLOR_ACCENT, background=AppConfig.COLOR_BUTTON).pack(pady=(10,10))
        
        reglas_text = tk.Text(reglas_frame, font=(AppConfig.FONT_FAMILY, 10), bg=AppConfig.COLOR_BG, 
                             fg=AppConfig.COLOR_FG, wrap='word', height=25, relief='flat', padx=20, pady=10)
        reglas_text.pack(fill='x', padx=20, pady=(0,10))
        
        contenido = """1. NÚMEROS CARDINALES (Cantidad)
   • Se usan para contar: one, two, three, four...
   • Ejemplo: I have three books (Tengo tres libros)

2. NÚMEROS ORDINALES (Orden/Posición)
   • Se usan para indicar orden: first, second, third, fourth...
   • Ejemplo: This is my first car (Este es mi primer auto)
   • Fechas: January 1st, March 3rd, May 21st

3. ESCRITURA DE NÚMEROS
   • 0-9: Escribir en palabras (five apples)
   • 10+: Usar números o palabras según contexto (15 people o fifteen people)
   • Inicio de oración: SIEMPRE en palabras (Twenty students arrived)

4. SEPARADORES
   • Miles: Usar coma (1,000 = one thousand)
   • Decimales: Usar punto (3.14 = three point one four)
   • Ejemplo: 1,234.56 = one thousand two hundred thirty-four point five six

5. HUNDRED, THOUSAND, MILLION
   • NO llevan 's' plural: two hundred (NO two hundreds)
   • Excepción: "hundreds of" = cientos de (cantidad indefinida)
   • Ejemplo: 300 = three hundred | hundreds of people = cientos de personas

6. AND en NÚMEROS
   • Británico: Usar 'and' después de hundred (105 = one hundred and five)
   • Americano: Opcional (105 = one hundred five)

7. FECHAS
   • Formato US: Month Day, Year (January 15, 2025)
   • Formato UK: Day Month Year (15 January 2025)
   • Lectura: January fifteenth, twenty twenty-five

8. HORAS
   • 3:00 = three o'clock
   • 3:15 = three fifteen / quarter past three
   • 3:30 = three thirty / half past three
   • 3:45 = three forty-five / quarter to four

9. PORCENTAJES
   • 50% = fifty percent
   • Ejemplo: Twenty percent of students (20% de estudiantes)

10. FRACCIONES
    • 1/2 = one half / a half
    • 1/3 = one third
    • 1/4 = one quarter / one fourth
    • 2/3 = two thirds
    • 3/4 = three quarters / three fourths

11. TELÉFONOS
    • Leer dígito por dígito: 555-1234 = five five five, one two three four
    • Doble dígito: 555-1122 = five five five, double one double two

12. CERO
    • Zero: Matemáticas y temperatura (0°C = zero degrees)
    • Oh: Teléfonos y números (505 = five oh five)
    • Nil: Deportes británicos (2-0 = two nil)
    • Nought: Británico general"""
        
        reglas_text.insert('1.0', contenido)
        reglas_text.config(state='disabled')
    
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
