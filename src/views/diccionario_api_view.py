"""Vista de Diccionario - Inglés y Español"""
import tkinter as tk
from tkinter import ttk, messagebox
from ..utils import AppConfig

class DiccionarioAPIView(ttk.Frame):
    def __init__(self, parent, tts=None):
        super().__init__(parent)
        self.tts = tts
        self.dict_en = None
        self.dict_es = None
        self.crear_ui()
        self.cargar_diccionarios()
    
    def cargar_diccionarios(self):
        """Carga los servicios de diccionario"""
        try:
            from ..integrations.dictionary_en import EnglishDictionary
            from ..integrations.dictionary_es import SpanishDictionary
            self.dict_en = EnglishDictionary()
            self.dict_es = SpanishDictionary()
        except Exception as e:
            # Diccionarios no disponibles, pero la app sigue funcionando
            self.dict_en = None
            self.dict_es = None
    
    def crear_ui(self):
        container = tk.Frame(self, bg=AppConfig.COLOR_BG)
        container.pack(expand=True, fill='both', padx=40, pady=30)
        
        # Título
        tk.Label(container, text="📖 Diccionario", font=(AppConfig.FONT_FAMILY, 20, 'bold'),
                bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT).pack(pady=(0,20))
        
        # Selector de idioma
        lang_frame = tk.Frame(container, bg=AppConfig.COLOR_BG)
        lang_frame.pack(pady=(0,20))
        
        self.language = tk.StringVar(value='en')
        tk.Radiobutton(lang_frame, text="🇬🇧 Inglés", variable=self.language,
                      value='en', bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG,
                      selectcolor=AppConfig.COLOR_BUTTON, font=(AppConfig.FONT_FAMILY, 11)).pack(side='left', padx=10)
        tk.Radiobutton(lang_frame, text="🇪🇸 Español", variable=self.language,
                      value='es', bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG,
                      selectcolor=AppConfig.COLOR_BUTTON, font=(AppConfig.FONT_FAMILY, 11)).pack(side='left', padx=10)
        
        # Búsqueda
        search_frame = tk.Frame(container, bg=AppConfig.COLOR_BG)
        search_frame.pack(fill='x', pady=(0,20))
        
        tk.Label(search_frame, text="Palabra:", font=(AppConfig.FONT_FAMILY, 12),
                bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack(side='left', padx=(0,10))
        
        self.entry_word = ttk.Entry(search_frame, font=(AppConfig.FONT_FAMILY, 12), width=30)
        self.entry_word.pack(side='left', padx=5, ipady=5)
        self.entry_word.bind('<Return>', lambda e: self.buscar())
        
        ttk.Button(search_frame, text="🔍 Buscar", command=self.buscar).pack(side='left', padx=5)
        ttk.Button(search_frame, text="🧹 Limpiar", command=self.limpiar).pack(side='left', padx=5)
        
        # Canvas con scroll para resultados
        canvas = tk.Canvas(container, bg=AppConfig.COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.result_frame = tk.Frame(canvas, bg=AppConfig.COLOR_BG)
        
        self.result_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.result_frame, anchor="nw", width=700)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind scroll a todo el canvas y sus hijos
        def bind_mousewheel(widget):
            widget.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
            widget.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
            for child in widget.winfo_children():
                bind_mousewheel(child)
        
        bind_mousewheel(canvas)
        self.canvas = canvas
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def buscar(self):
        palabra = self.entry_word.get().strip()
        if not palabra:
            messagebox.showwarning("Advertencia", "Ingresa una palabra")
            return
        
        # Verificar si los diccionarios están disponibles
        if not self.dict_en and not self.dict_es:
            messagebox.showwarning("Diccionarios no disponibles",
                                 "Los diccionarios requieren conexión a internet.\nAsegúrate de estar conectado.")
            return
        
        # Limpiar resultados anteriores
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        lang = self.language.get()
        
        if lang == 'en':
            self.buscar_ingles(palabra)
        else:
            self.buscar_espanol(palabra)
    
    def buscar_ingles(self, palabra):
        if not self.dict_en:
            messagebox.showerror("Error", "Diccionario no disponible")
            return
        
        result = self.dict_en.lookup(palabra)
        
        if 'error' in result:
            lbl = tk.Label(self.result_frame, text=f"❌ {result['error']}", 
                    font=(AppConfig.FONT_FAMILY, 12), bg=AppConfig.COLOR_BG,
                    fg=AppConfig.COLOR_ERROR, cursor="xterm")
            lbl.pack(pady=20)
            self._enable_text_selection(lbl)
            return
        
        # Palabra y fonética
        lbl = tk.Label(self.result_frame, text=result['word'], 
                font=(AppConfig.FONT_FAMILY, 18, 'bold'), bg=AppConfig.COLOR_BG,
                fg=AppConfig.COLOR_ACCENT, cursor="xterm")
        lbl.pack(anchor='w', pady=(10,5))
        self._enable_text_selection(lbl)
        
        if result['phonetic']:
            lbl = tk.Label(self.result_frame, text=result['phonetic'],
                    font=(AppConfig.FONT_FAMILY, 12), bg=AppConfig.COLOR_BG,
                    fg=AppConfig.COLOR_FG, cursor="xterm")
            lbl.pack(anchor='w', pady=(0,10))
            self._enable_text_selection(lbl)
        
        # Sinónimos al principio
        if result['synonyms']:
            syn_frame = tk.Frame(self.result_frame, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
            syn_frame.pack(fill='x', pady=10)
            lbl = tk.Label(syn_frame, text="SINÓNIMOS",
                    font=(AppConfig.FONT_FAMILY, 11, 'bold'), bg=AppConfig.COLOR_BUTTON,
                    fg=AppConfig.COLOR_ACCENT, cursor="xterm")
            lbl.pack(anchor='w', padx=10, pady=(10,5))
            self._enable_text_selection(lbl)
            lbl = tk.Label(syn_frame, text=', '.join(result['synonyms'][:10]),
                    font=(AppConfig.FONT_FAMILY, 10), bg=AppConfig.COLOR_BUTTON,
                    fg=AppConfig.COLOR_SUCCESS, wraplength=650, justify='left', cursor="xterm")
            lbl.pack(anchor='w', padx=20, pady=(0,10))
            self._enable_text_selection(lbl)
        
        # Definiciones
        for meaning in result['meanings']:
            frame = tk.Frame(self.result_frame, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
            frame.pack(fill='x', pady=10)
            
            lbl = tk.Label(frame, text=meaning['partOfSpeech'].upper(),
                    font=(AppConfig.FONT_FAMILY, 11, 'bold'), bg=AppConfig.COLOR_BUTTON,
                    fg=AppConfig.COLOR_ACCENT, cursor="xterm")
            lbl.pack(anchor='w', padx=10, pady=(10,5))
            self._enable_text_selection(lbl)
            
            for i, definition in enumerate(meaning['definitions'][:5], 1):
                lbl = tk.Label(frame, text=f"{i}. {definition['definition']}",
                        font=(AppConfig.FONT_FAMILY, 10), bg=AppConfig.COLOR_BUTTON,
                        fg=AppConfig.COLOR_FG, wraplength=650, justify='left', cursor="xterm")
                lbl.pack(anchor='w', padx=20, pady=2)
                self._enable_text_selection(lbl)
                
                if definition['example']:
                    lbl = tk.Label(frame, text=f"   Ejemplo: {definition['example']}",
                            font=(AppConfig.FONT_FAMILY, 9, 'italic'), bg=AppConfig.COLOR_BUTTON,
                            fg=AppConfig.COLOR_BUTTON_HOVER, wraplength=650, justify='left', cursor="xterm")
                    lbl.pack(anchor='w', padx=20, pady=2)
                    self._enable_text_selection(lbl)
            
            tk.Label(frame, text="", bg=AppConfig.COLOR_BUTTON).pack(pady=5)
        
        self._bind_scroll_to_children()
    
    def buscar_espanol(self, palabra):
        if not self.dict_es:
            messagebox.showerror("Error", "Diccionario no disponible")
            return
        
        result = self.dict_es.lookup(palabra)
        
        if 'error' in result:
            txt = self._create_selectable_text(self.result_frame, f"❌ {result['error']}",
                    (AppConfig.FONT_FAMILY, 12), AppConfig.COLOR_BG, AppConfig.COLOR_ERROR)
            txt.pack(pady=20, fill='x')
            return
        
        # Palabra principal con diseño mejorado
        header_frame = tk.Frame(self.result_frame, bg='#2c3e50', relief='solid', borderwidth=2)
        header_frame.pack(fill='x', pady=(10,15))
        
        txt = self._create_selectable_text(header_frame, result['word'],
                (AppConfig.FONT_FAMILY, 22, 'bold'), '#2c3e50', '#ecf0f1')
        txt.pack(anchor='w', padx=15, pady=(15,5), fill='x')
        
        if result.get('phonetic'):
            txt = self._create_selectable_text(header_frame, f"🔊 {result['phonetic']}",
                    (AppConfig.FONT_FAMILY, 12), '#2c3e50', '#95a5a6')
            txt.pack(anchor='w', padx=15, pady=(0,15), fill='x')
        
        # Sinónimos al principio con diseño mejorado
        if result.get('synonyms'):
            syn_frame = tk.Frame(self.result_frame, bg='#27ae60', relief='solid', borderwidth=2)
            syn_frame.pack(fill='x', pady=10)
            txt = self._create_selectable_text(syn_frame, "💡 SINÓNIMOS",
                    (AppConfig.FONT_FAMILY, 12, 'bold'), '#27ae60', 'white')
            txt.pack(anchor='w', padx=15, pady=(12,8), fill='x')
            txt = self._create_selectable_text(syn_frame, ', '.join(result['synonyms'][:10]),
                    (AppConfig.FONT_FAMILY, 11), '#27ae60', '#ecf0f1', height=2)
            txt.pack(anchor='w', padx=15, pady=(0,12), fill='x')
        
        # Definiciones/Significados con diseño mejorado
        for idx, meaning in enumerate(result.get('meanings', []), 1):
            frame = tk.Frame(self.result_frame, bg='#34495e', relief='solid', borderwidth=2)
            frame.pack(fill='x', pady=10)
            
            # Header del tipo de palabra
            type_frame = tk.Frame(frame, bg='#3498db')
            type_frame.pack(fill='x')
            txt = self._create_selectable_text(type_frame, f"📚 {meaning['partOfSpeech'].upper()}",
                    (AppConfig.FONT_FAMILY, 11, 'bold'), '#3498db', 'white')
            txt.pack(anchor='w', padx=15, pady=8, fill='x')
            
            # Definiciones
            for i, definition in enumerate(meaning['definitions'][:5], 1):
                def_frame = tk.Frame(frame, bg='#34495e')
                def_frame.pack(fill='x', padx=15, pady=8)
                
                txt = self._create_selectable_text(def_frame, f"{i}. {definition['definition']}",
                        (AppConfig.FONT_FAMILY, 11), '#34495e', '#ecf0f1', height=3)
                txt.pack(anchor='w', fill='x', expand=True)
                
                if definition.get('example'):
                    ex_frame = tk.Frame(frame, bg='#2c3e50')
                    ex_frame.pack(fill='x', padx=30, pady=(0,8))
                    txt = self._create_selectable_text(ex_frame, f"💬 {definition['example']}",
                            (AppConfig.FONT_FAMILY, 10, 'italic'), '#2c3e50', '#95a5a6', height=2)
                    txt.pack(anchor='w', padx=10, pady=5, fill='x')
            
            tk.Label(frame, text="", bg='#34495e').pack(pady=5)
        
        self._bind_scroll_to_children()
    
    def limpiar(self):
        """Limpia el campo de búsqueda y los resultados"""
        self.entry_word.delete(0, 'end')
        for widget in self.result_frame.winfo_children():
            widget.destroy()
    
    def _enable_text_selection(self, label):
        """Habilita selección y copia de texto en un Label"""
        # Menú contextual
        menu = tk.Menu(label, tearoff=0)
        menu.add_command(label="Copiar", command=lambda: self._copy_label_text(label))
        
        def show_menu(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()
        
        label.bind("<Button-3>", show_menu)
    
    def _copy_label_text(self, label):
        """Copia el texto de un label al portapapeles"""
        text = label.cget('text')
        self.clipboard_clear()
        self.clipboard_append(text)
    
    def _create_selectable_text(self, parent, text, font, bg, fg, **kwargs):
        """Crea un widget Text seleccionable que parece un Label"""
        text_widget = tk.Text(parent, font=font, bg=bg, fg=fg, 
                             height=1, wrap='word', relief='flat', 
                             borderwidth=0, cursor="xterm", **kwargs)
        text_widget.insert('1.0', text)
        text_widget.config(state='disabled')
        
        # Habilitar selección y copia
        def copy_selection(event=None):
            try:
                selected = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
                self.clipboard_clear()
                self.clipboard_append(selected)
            except:
                pass
        
        # Menú contextual
        menu = tk.Menu(text_widget, tearoff=0)
        menu.add_command(label="Copiar", command=copy_selection)
        
        def show_menu(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()
        
        text_widget.bind("<Button-3>", show_menu)
        text_widget.bind("<Control-c>", copy_selection)
        
        return text_widget
    
    def _bind_scroll_to_children(self):
        """Bind scroll a todos los widgets hijos"""
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def bind_recursive(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            for child in widget.winfo_children():
                bind_recursive(child)
        
        bind_recursive(self.result_frame)
    
    def pronunciar(self):
        """Pronuncia la palabra buscada"""
        if not self.tts:
            return
        
        palabra = self.entry_word.get().strip()
        if palabra:
            self.tts.speak(palabra)
