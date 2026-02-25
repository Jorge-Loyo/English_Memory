"""Gramática View - Pronombres y conjugación"""
import tkinter as tk
from tkinter import ttk
from src.utils import AppConfig
from src.data import PRONOMBRES, AUXILIARES, ARTICULOS, DEMOSTRATIVOS, CUANTIFICADORES

class GramaticaView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
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
        
        # Pronombres
        pron_frame = tk.Frame(content, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
        pron_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        ttk.Label(pron_frame, text="👤 Pronombres Personales", font=(AppConfig.FONT_FAMILY, 16, 'bold'), 
                 foreground=AppConfig.COLOR_ACCENT, background=AppConfig.COLOR_BUTTON).pack(pady=(10,15))
        
        # Tabla de pronombres con formato mejorado
        table_frame = tk.Frame(pron_frame, bg=AppConfig.COLOR_BUTTON)
        table_frame.pack(padx=20, pady=(0,10))
        
        for i, row in enumerate(PRONOMBRES):
            row_frame = tk.Frame(table_frame, bg=AppConfig.COLOR_BG if i > 0 else AppConfig.COLOR_BUTTON, 
                                relief='solid', borderwidth=1)
            row_frame.pack(fill='x', pady=1)
            
            for j, cell in enumerate(row):
                width = 15 if j < 5 else 25
                font_style = (AppConfig.FONT_FAMILY, 9, 'bold') if i == 0 else (AppConfig.FONT_FAMILY, 9)
                fg_color = AppConfig.COLOR_ACCENT if i == 0 else AppConfig.COLOR_FG
                
                tk.Label(row_frame, text=str(cell), font=font_style,
                        bg=AppConfig.COLOR_BG if i > 0 else AppConfig.COLOR_BUTTON,
                        fg=fg_color, width=width, anchor='center').pack(side='left', padx=2, pady=5)
        
        # Auxiliares
        aux_frame = tk.Frame(content, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
        aux_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        ttk.Label(aux_frame, text="🔧 Verbos Auxiliares", font=(AppConfig.FONT_FAMILY, 16, 'bold'), 
                 foreground=AppConfig.COLOR_ACCENT, background=AppConfig.COLOR_BUTTON).pack(pady=(10,15))
        
        for verbo, formas in AUXILIARES:
            verb_frame = tk.Frame(aux_frame, bg=AppConfig.COLOR_BG, relief='solid', borderwidth=1)
            verb_frame.pack(fill='x', padx=20, pady=5)
            tk.Label(verb_frame, text=verbo, font=(AppConfig.FONT_FAMILY, 11, 'bold'), 
                    bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT, width=15).pack(side='left', padx=10, pady=5)
            for forma, trad in formas:
                tk.Label(verb_frame, text=f"{forma} ({trad})", font=(AppConfig.FONT_FAMILY, 9), 
                        bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack(side='left', padx=5)
        
        # Artículos
        art_frame = tk.Frame(content, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
        art_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        ttk.Label(art_frame, text="📰 Artículos", font=(AppConfig.FONT_FAMILY, 16, 'bold'), 
                 foreground=AppConfig.COLOR_ACCENT, background=AppConfig.COLOR_BUTTON).pack(pady=(10,15))
        
        for art, desc, ej in ARTICULOS:
            item = tk.Frame(art_frame, bg=AppConfig.COLOR_BG, relief='solid', borderwidth=1)
            item.pack(fill='x', padx=20, pady=5)
            tk.Label(item, text=art, font=(AppConfig.FONT_FAMILY, 12, 'bold'), 
                    bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT, width=8).pack(side='left', padx=10, pady=8)
            tk.Label(item, text=f"{desc} - Ej: {ej}", font=(AppConfig.FONT_FAMILY, 10), 
                    bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack(side='left', padx=5)
        
        # Demostrativos
        dem_frame = tk.Frame(content, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
        dem_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        ttk.Label(dem_frame, text="👉 Demostrativos", font=(AppConfig.FONT_FAMILY, 16, 'bold'), 
                 foreground=AppConfig.COLOR_ACCENT, background=AppConfig.COLOR_BUTTON).pack(pady=(10,15))
        
        for dem, desc, ej in DEMOSTRATIVOS:
            item = tk.Frame(dem_frame, bg=AppConfig.COLOR_BG, relief='solid', borderwidth=1)
            item.pack(fill='x', padx=20, pady=5)
            tk.Label(item, text=dem, font=(AppConfig.FONT_FAMILY, 12, 'bold'), 
                    bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT, width=10).pack(side='left', padx=10, pady=8)
            tk.Label(item, text=f"{desc} - Ej: {ej}", font=(AppConfig.FONT_FAMILY, 10), 
                    bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack(side='left', padx=5)
        
        # Cuantificadores
        cuant_frame = tk.Frame(content, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
        cuant_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        ttk.Label(cuant_frame, text="📊 Cuantificadores", font=(AppConfig.FONT_FAMILY, 16, 'bold'), 
                 foreground=AppConfig.COLOR_ACCENT, background=AppConfig.COLOR_BUTTON).pack(pady=(10,15))
        
        for cuant, desc, ej in CUANTIFICADORES:
            item = tk.Frame(cuant_frame, bg=AppConfig.COLOR_BG, relief='solid', borderwidth=1)
            item.pack(fill='x', padx=20, pady=3)
            tk.Label(item, text=cuant, font=(AppConfig.FONT_FAMILY, 11, 'bold'), 
                    bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT, width=12, anchor='w').pack(side='left', padx=10, pady=5)
            tk.Label(item, text=f"{desc} - Ej: {ej}", font=(AppConfig.FONT_FAMILY, 10), 
                    bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack(side='left', padx=5)


class ConjugacionView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
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
        
        tiempos = [
            ('🕒 Simple Present', 'Acciones habituales', [
                ('Afirmativo', 'I/You/We/They work | He/She/It works'),
                ('Negativo', "don't work | doesn't work"),
                ('Interrogativo', 'Do...work? | Does...work?')
            ]),
            ('🔄 Present Continuous', 'Acciones en progreso', [
                ('Afirmativo', 'I am | You/We/They are | He/She/It is working'),
                ('Negativo', "I'm not | aren't | isn't working"),
                ('Interrogativo', 'Am I? | Are you? | Is he? working')
            ]),
            ('⏪ Simple Past', 'Acciones completadas', [
                ('Afirmativo', 'I/You/He/She/It/We/They worked'),
                ('Negativo', "didn't work"),
                ('Interrogativo', 'Did...work?')
            ]),
            ('✅ Present Perfect', 'Pasado con relevancia', [
                ('Afirmativo', 'I/You/We/They have | He/She/It has worked'),
                ('Negativo', "haven't | hasn't worked"),
                ('Interrogativo', 'Have...? | Has...? worked')
            ]),
            ('⏩ Future Simple', 'Acciones futuras', [
                ('Afirmativo', 'I/You/He/She/It/We/They will work'),
                ('Negativo', "won't work"),
                ('Interrogativo', 'Will...work?')
            ])
        ]
        
        for titulo, uso, ejemplos in tiempos:
            f = tk.Frame(content, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
            f.pack(fill='x', padx=20, pady=(0,20), ipady=15)
            
            ttk.Label(f, text=titulo, font=(AppConfig.FONT_FAMILY, 16, 'bold'), 
                     foreground=AppConfig.COLOR_ACCENT, background=AppConfig.COLOR_BUTTON).pack(pady=(10,5))
            tk.Label(f, text=f"Uso: {uso}", font=(AppConfig.FONT_FAMILY, 11), 
                    bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_FG).pack(pady=5)
            
            for tipo, forma in ejemplos:
                item = tk.Frame(f, bg=AppConfig.COLOR_BG, relief='solid', borderwidth=1)
                item.pack(fill='x', padx=20, pady=5)
                tk.Label(item, text=tipo, font=(AppConfig.FONT_FAMILY, 11, 'bold'), 
                        bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT, width=15).pack(side='left', padx=10, pady=8)
                tk.Label(item, text=forma, font=(AppConfig.FONT_FAMILY, 10), 
                        bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG, anchor='w').pack(side='left', padx=5)
