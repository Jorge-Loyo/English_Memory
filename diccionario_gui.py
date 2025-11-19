"""
English Memory v1.0
===================

Aplicación educativa multiplataforma para aprender y organizar vocabulario en inglés.

Características:
- Gestión de vocabulario (agregar, editar, eliminar, buscar)
- Pronunciación fonética
- Modo práctica (quiz inglés ↔ español)
- Práctica de caligrafía con oraciones
- Preposiciones (47 preposiciones)
- Días/Meses (58 términos)
- Números (conversor + reglas)
- Estadísticas del vocabulario
- Exportar/Importar CSV
- Soporte técnico integrado

Compatibilidad:
- Windows 10/11
- Linux (Ubuntu, Debian, Fedora, etc.)
- macOS (compatible)

Almacenamiento de datos:
- Windows: %LOCALAPPDATA%\\DiccionarioPersonal\\palabras.json
- Linux/macOS: ~/.local/share/DiccionarioPersonal/palabras.json

Soporte:
- Email: administrador@agilizesoluciones.com
- Teléfono: +54 11 6168-2555

Desarrollado por: Agilize Soluciones
Versión: 1.0
Fecha: 2024
Licencia: Uso educativo gratuito
"""

import json
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import random
import csv
from tkinter import filedialog
import threading
import time
import platform

# Detectar sistema operativo y configurar ruta apropiada
if platform.system() == 'Windows':
    APP_DIR = Path.home() / 'AppData' / 'Local' / 'DiccionarioPersonal'
else:  # Linux, macOS
    APP_DIR = Path.home() / '.local' / 'share' / 'DiccionarioPersonal'

APP_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVO_DATOS = APP_DIR / 'palabras.json'

# Colores modernos - Tema morado/violeta
COLOR_BG = '#1a1625'
COLOR_FG = '#e9e4f0'
COLOR_ACCENT = '#a78bfa'
COLOR_ACCENT_DARK = '#7c3aed'
COLOR_BUTTON = '#2d2438'
COLOR_BUTTON_HOVER = '#3d3149'
COLOR_SUCCESS = '#34d399'
COLOR_ERROR = '#f87171'

# Fuente según sistema operativo
if platform.system() == 'Windows':
    FONT_FAMILY = 'Segoe UI'
else:  # Linux, macOS
    FONT_FAMILY = 'Sans'

def cargar_datos():
    if ARCHIVO_DATOS.exists():
        try:
            with open(ARCHIVO_DATOS, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()
                if contenido:
                    return json.loads(contenido)
        except (json.JSONDecodeError, IOError, PermissionError) as e:
            # Mostrar error en GUI si está disponible
            try:
                messagebox.showerror("Error", f"Error al cargar datos: {e}")
            except:
                print(f"Error al cargar datos: {e}")
    return {}

def guardar_datos(datos):
    try:
        with open(ARCHIVO_DATOS, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        return True
    except (IOError, PermissionError) as e:
        try:
            messagebox.showerror("Error", f"Error al guardar datos: {e}")
        except:
            print(f"Error al guardar datos: {e}")
        return False

class DiccionarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 English Memory v1.0")
        self.root.geometry("1200x700")
        self.root.minsize(1150, 600)
        self.root.configure(bg=COLOR_BG)
        self.datos = cargar_datos()
        
        # Estilo moderno
        self.configurar_estilos()
        
        # Header
        header = tk.Frame(root, bg=COLOR_BG)
        header.pack(fill='x', padx=20, pady=(20,10))
        tk.Label(header, text="📚 English Memory v1.0", 
                font=(FONT_FAMILY, 24, 'bold'), bg=COLOR_BG, fg=COLOR_ACCENT).pack()
        tk.Label(header, text="Aprende y organiza tu vocabulario en inglés", 
                font=(FONT_FAMILY, 10), bg=COLOR_BG, fg=COLOR_FG).pack()
        tk.Label(header, text=f"📁 Datos guardados en: {APP_DIR}", 
                font=(FONT_FAMILY, 8), bg=COLOR_BG, fg=COLOR_BUTTON_HOVER).pack()
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Pestañas
        self.crear_pestaña_consultar()
        self.crear_pestaña_pronunciacion()
        self.crear_pestaña_practica()
        self.crear_pestaña_caligrafia()
        self.crear_pestaña_preposiciones()
        self.crear_pestaña_dias_meses()
        self.crear_pestaña_numeros()
        self.crear_pestaña_estadisticas()
        self.crear_pestaña_ayuda()
    
    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook
        style.configure('TNotebook', background=COLOR_BG, borderwidth=0)
        style.configure('TNotebook.Tab', background=COLOR_BUTTON, foreground=COLOR_FG, 
                       padding=[20, 10], font=(FONT_FAMILY, 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', COLOR_ACCENT)], 
                 foreground=[('selected', COLOR_BG)])
        
        # Frame
        style.configure('TFrame', background=COLOR_BG)
        
        # Label
        style.configure('TLabel', background=COLOR_BG, foreground=COLOR_FG, 
                       font=(FONT_FAMILY, 10))
        style.configure('Title.TLabel', font=(FONT_FAMILY, 12, 'bold'), 
                       foreground=COLOR_ACCENT)
        
        # Entry
        style.configure('TEntry', fieldbackground=COLOR_BUTTON, foreground=COLOR_FG, 
                       borderwidth=1, relief='solid', insertcolor=COLOR_ACCENT)
        style.map('TEntry', 
                 fieldbackground=[('focus', '#3d3149')],
                 bordercolor=[('focus', COLOR_ACCENT)])
        
        # Button
        style.configure('TButton', background=COLOR_ACCENT, foreground=COLOR_BG, 
                       borderwidth=0, font=(FONT_FAMILY, 10, 'bold'), padding=[20, 10])
        style.map('TButton', background=[('active', COLOR_BUTTON_HOVER)])
        
        # Treeview
        style.configure('Treeview', background=COLOR_BUTTON, foreground=COLOR_FG, 
                       fieldbackground=COLOR_BUTTON, borderwidth=0, 
                       font=(FONT_FAMILY, 10))
        style.configure('Treeview.Heading', background=COLOR_ACCENT, 
                       foreground=COLOR_BG, borderwidth=0, 
                       font=(FONT_FAMILY, 10, 'bold'))
        style.map('Treeview', background=[('selected', COLOR_ACCENT)], 
                 foreground=[('selected', COLOR_BG)])
    
    def crear_pestaña_consultar(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📖 Vocabulario")
        
        # Búsqueda
        frame_buscar = ttk.Frame(frame)
        frame_buscar.pack(fill='x', padx=20, pady=15)
        
        # Fila 1: Botones de acción
        frame_acciones = tk.Frame(frame_buscar, bg=COLOR_BG)
        frame_acciones.pack(side='left', fill='x', expand=False)
        
        ttk.Button(frame_acciones, text="➕ Agregar", command=self.abrir_modal_agregar).pack(side='left', padx=2)
        ttk.Button(frame_acciones, text="✏️ Editar", command=self.editar_palabra).pack(side='left', padx=2)
        ttk.Button(frame_acciones, text="🗑️ Eliminar", command=self.eliminar_palabra).pack(side='left', padx=2)
        ttk.Button(frame_acciones, text="📤 Exportar", command=self.exportar_csv).pack(side='left', padx=2)
        ttk.Button(frame_acciones, text="📥 Importar", command=self.importar_csv).pack(side='left', padx=2)
        
        # Fila 1: Búsqueda
        frame_search = tk.Frame(frame_buscar, bg=COLOR_BG)
        frame_search.pack(side='right', fill='x', expand=False)
        
        ttk.Button(frame_search, text="📋 Ver Todas", command=self.mostrar_todas).pack(side='right', padx=2)
        self.entry_buscar = ttk.Entry(frame_search, width=25, font=(FONT_FAMILY, 11))
        self.entry_buscar.pack(side='right', padx=5, ipady=5)
        self.entry_buscar.bind('<KeyRelease>', self._on_search_keyrelease)
        self._search_timer = None
        ttk.Label(frame_search, text="🔍", font=(FONT_FAMILY, 14)).pack(side='right', padx=(0,5))
        
        # Tabla
        columns = ('Inglés', 'Español', 'Pronunciación')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        self.tree.heading('Inglés', text='🇬🇧 Inglés')
        self.tree.heading('Español', text='🇪🇸 Español')
        self.tree.heading('Pronunciación', text='🔊 Pronunciación')
        
        self.tree.column('Inglés', width=200, minwidth=150)
        self.tree.column('Español', width=400, minwidth=200)
        self.tree.column('Pronunciación', width=300, minwidth=150)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=(20,0), pady=(0,20))
        scrollbar.pack(side='right', fill='y', pady=(0,20), padx=(0,20))
        
        # Doble click para editar
        self.tree.bind('<Double-Button-1>', self._on_double_click)
        
        # Click en encabezados para ordenar
        self.tree.heading('Inglés', text='🇬🇧 Inglés', command=lambda: self.ordenar_columna('Inglés'))
        self.tree.heading('Español', text='🇪🇸 Español', command=lambda: self.ordenar_columna('Español'))
        self.tree.heading('Pronunciación', text='🔊 Pronunciación', command=lambda: self.ordenar_columna('Pronunciación'))
        
        self.mostrar_todas()
        self.orden_actual = {'columna': None, 'reverso': False}
    
    def crear_pestaña_pronunciacion(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔊 Pronunciación")
        
        container = tk.Frame(frame, bg=COLOR_BG)
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Label(container, text="🇬🇧 Palabra en inglés", style='Title.TLabel').pack(pady=(0,10))
        self.entry_palabra_pron = ttk.Entry(container, width=50, font=(FONT_FAMILY, 12))
        self.entry_palabra_pron.pack(pady=(0,20), ipady=10)
        
        ttk.Label(container, text="🔊 Pronunciación (fonética)", style='Title.TLabel').pack(pady=(0,10))
        self.entry_pronunciacion = ttk.Entry(container, width=50, font=(FONT_FAMILY, 12))
        self.entry_pronunciacion.pack(pady=(0,30), ipady=10)
        
        ttk.Button(container, text="💾 Guardar Pronunciación", command=self.guardar_pronunciacion).pack(pady=10)
    
    def abrir_modal_agregar(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("➕ Agregar Palabra")
        ventana.geometry("550x420")
        ventana.configure(bg=COLOR_BG)
        ventana.grab_set()
        ventana.resizable(False, False)
        
        container = tk.Frame(ventana, bg=COLOR_BG)
        container.pack(expand=True, fill='both', padx=40, pady=30)
        
        ttk.Label(container, text="🇬🇧 Palabra en inglés", style='Title.TLabel').pack(pady=(0,5))
        entry_palabra = ttk.Entry(container, width=45, font=(FONT_FAMILY, 11))
        entry_palabra.pack(pady=(0,15), ipady=8)
        entry_palabra.focus()
        
        ttk.Label(container, text="🇪🇸 Significado en español", style='Title.TLabel').pack(pady=(0,5))
        entry_significado = ttk.Entry(container, width=45, font=(FONT_FAMILY, 11))
        entry_significado.pack(pady=(0,15), ipady=8)
        
        ttk.Label(container, text="📝 Notas (opcional)", style='Title.TLabel').pack(pady=(0,5))
        entry_notas = ttk.Entry(container, width=45, font=(FONT_FAMILY, 11))
        entry_notas.pack(pady=(0,25), ipady=8)
        
        def guardar():
            palabra = entry_palabra.get().strip()
            significado = entry_significado.get().strip()
            
            if not palabra or not significado:
                messagebox.showwarning("Advertencia", "Completa todos los campos")
                return
            
            if len(palabra) > 100:
                messagebox.showwarning("Advertencia", "La palabra no puede exceder 100 caracteres")
                return
            
            if len(significado) > 500:
                messagebox.showwarning("Advertencia", "El significado no puede exceder 500 caracteres")
                return
            
            if palabra in self.datos:
                messagebox.showwarning("Palabra duplicada", f"'{palabra}' ya está en el vocabulario")
                return
            
            notas = entry_notas.get().strip()
            if len(notas) > 1000:
                messagebox.showwarning("Advertencia", "Las notas no pueden exceder 1000 caracteres")
                return
            
            self.datos[palabra] = {'significado': significado}
            if notas:
                self.datos[palabra]['notas'] = notas
            
            if guardar_datos(self.datos):
                messagebox.showinfo("Éxito", f"Palabra '{palabra}' guardada")
                ventana.destroy()
                self.mostrar_todas()
            else:
                messagebox.showerror("Error", "No se pudo guardar la palabra")
        
        btn_frame = tk.Frame(container, bg=COLOR_BG)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="💾 Guardar", command=guardar).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana.destroy).pack(side='left', padx=5)
    
    def mostrar_todas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for palabra in sorted(self.datos.keys(), key=str.lower):
            significado = self.datos[palabra].get('significado', '')
            pronunciacion = self.datos[palabra].get('pronunciacion', '-')
            self.tree.insert('', 'end', values=(palabra, significado, pronunciacion))
    
    def _on_double_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == 'cell':
            self.editar_palabra()
    
    def _on_search_keyrelease(self, event):
        # Debouncing: esperar 300ms antes de buscar
        if self._search_timer:
            self.root.after_cancel(self._search_timer)
        self._search_timer = self.root.after(300, self.buscar_palabra)
    
    def buscar_palabra(self):
        busqueda = self.entry_buscar.get().strip().lower()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not busqueda:
            self.mostrar_todas()
            return
        
        resultados = [
            (palabra, datos.get('significado', ''), datos.get('pronunciacion', '-'))
            for palabra, datos in self.datos.items()
            if busqueda in palabra.lower() or busqueda in datos.get('significado', '').lower()
        ]
        
        for palabra, significado, pronunciacion in sorted(resultados):
            self.tree.insert('', 'end', values=(palabra, significado, pronunciacion))
        
        if not resultados:
            messagebox.showinfo("Búsqueda", f"No se encontraron palabras con '{busqueda}'")
    
    def ordenar_columna(self, columna):
        if self.orden_actual['columna'] == columna:
            self.orden_actual['reverso'] = not self.orden_actual['reverso']
        else:
            self.orden_actual['columna'] = columna
            self.orden_actual['reverso'] = False
        
        items = [(self.tree.set(item, columna), item) for item in self.tree.get_children('')]
        items.sort(key=lambda x: str(x[0]).lower(), reverse=self.orden_actual['reverso'])
        
        for index, (val, item) in enumerate(items):
            self.tree.move(item, '', index)
    
    def exportar_csv(self):
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if archivo:
            try:
                with open(archivo, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Inglés', 'Español', 'Pronunciación', 'Notas'])
                    for palabra, datos in self.datos.items():
                        writer.writerow([
                            palabra,
                            datos.get('significado', ''),
                            datos.get('pronunciacion', ''),
                            datos.get('notas', '')
                        ])
                messagebox.showinfo("Éxito", "Vocabulario exportado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def importar_csv(self):
        archivo = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    count = 0
                    for row in reader:
                        palabra = row.get('Inglés', '').strip().lower()
                        significado = row.get('Español', '').strip()
                        
                        if palabra and significado and len(palabra) <= 100 and len(significado) <= 500:
                            self.datos[palabra] = {'significado': significado}
                            
                            pronunciacion = row.get('Pronunciación', '').strip()
                            if pronunciacion and len(pronunciacion) <= 200:
                                self.datos[palabra]['pronunciacion'] = pronunciacion
                            
                            notas = row.get('Notas', '').strip()
                            if notas and len(notas) <= 1000:
                                self.datos[palabra]['notas'] = notas
                            
                            count += 1
                
                guardar_datos(self.datos)
                self.mostrar_todas()
                messagebox.showinfo("Éxito", f"{count} palabras importadas correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al importar: {str(e)}")
    
    def crear_pestaña_practica(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎯 Práctica")
        
        container = tk.Frame(frame, bg=COLOR_BG)
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        self.practica_palabra = tk.StringVar()
        self.practica_respuesta = tk.StringVar()
        self.practica_modo = tk.StringVar(value='ingles')
        
        ttk.Label(container, text="🎯 Modo Práctica", font=(FONT_FAMILY, 18, 'bold'), 
                 foreground=COLOR_ACCENT, background=COLOR_BG).pack(pady=(0,20))
        
        # Selector de modo
        frame_modo = tk.Frame(container, bg=COLOR_BG)
        frame_modo.pack(pady=(0,20))
        tk.Radiobutton(frame_modo, text="Inglés → Español", variable=self.practica_modo, 
                      value='ingles', bg=COLOR_BG, fg=COLOR_FG, selectcolor=COLOR_BUTTON,
                      font=(FONT_FAMILY, 10)).pack(side='left', padx=10)
        tk.Radiobutton(frame_modo, text="Español → Inglés", variable=self.practica_modo, 
                      value='español', bg=COLOR_BG, fg=COLOR_FG, selectcolor=COLOR_BUTTON,
                      font=(FONT_FAMILY, 10)).pack(side='left', padx=10)
        
        # Palabra a practicar
        self.label_practica = tk.Label(container, textvariable=self.practica_palabra, 
                                       font=(FONT_FAMILY, 24, 'bold'), bg=COLOR_BG, 
                                       fg=COLOR_ACCENT, wraplength=400)
        self.label_practica.pack(pady=20)
        
        # Respuesta
        self.label_respuesta = tk.Label(container, textvariable=self.practica_respuesta, 
                                        font=(FONT_FAMILY, 16), bg=COLOR_BG, 
                                        fg=COLOR_SUCCESS, wraplength=400)
        self.label_respuesta.pack(pady=10)
        
        # Botones
        btn_frame = tk.Frame(container, bg=COLOR_BG)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="🔄 Nueva Palabra", command=self.nueva_palabra_practica).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="👁️ Ver Respuesta", command=self.mostrar_respuesta_practica).pack(side='left', padx=5)
        
        self.nueva_palabra_practica()
    
    def nueva_palabra_practica(self):
        if not self.datos:
            self.practica_palabra.set("No hay palabras en el vocabulario")
            self.practica_respuesta.set("")
            return
        
        palabra = random.choice(list(self.datos.keys()))
        self.palabra_actual_practica = palabra
        
        if self.practica_modo.get() == 'ingles':
            self.practica_palabra.set(f"🇬🇧 {palabra}")
        else:
            significado = self.datos[palabra].get('significado', '')
            self.practica_palabra.set(f"🇪🇸 {significado}")
        
        self.practica_respuesta.set("")
    
    def mostrar_respuesta_practica(self):
        if not hasattr(self, 'palabra_actual_practica'):
            return
        
        palabra = self.palabra_actual_practica
        significado = self.datos[palabra].get('significado', '')
        pronunciacion = self.datos[palabra].get('pronunciacion', '')
        notas = self.datos[palabra].get('notas', '')
        
        if self.practica_modo.get() == 'ingles':
            respuesta = f"✅ {significado}"
        else:
            respuesta = f"✅ {palabra}"
        
        if pronunciacion:
            respuesta += f"\n🔊 {pronunciacion}"
        if notas:
            respuesta += f"\n📝 {notas}"
        
        self.practica_respuesta.set(respuesta)
    
    def crear_pestaña_preposiciones(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📍 Preposiciones")
        
        # Búsqueda
        frame_buscar = ttk.Frame(frame)
        frame_buscar.pack(fill='x', padx=20, pady=15)
        
        ttk.Label(frame_buscar, text="🔍", font=(FONT_FAMILY, 14)).pack(side='left', padx=(0,5))
        self.entry_buscar_prep = ttk.Entry(frame_buscar, width=30, font=(FONT_FAMILY, 11))
        self.entry_buscar_prep.pack(side='left', padx=5, ipady=5)
        self.entry_buscar_prep.bind('<KeyRelease>', self._on_search_prep_keyrelease)
        self._search_prep_timer = None
        
        # Tabla de preposiciones
        columns = ('Inglés', 'Español')
        self.tree_prep = ttk.Treeview(frame, columns=columns, show='headings', height=20)
        
        self.tree_prep.heading('Inglés', text='🇬🇧 Preposición')
        self.tree_prep.heading('Español', text='🇪🇸 Traducción')
        
        self.tree_prep.column('Inglés', width=300, minwidth=200)
        self.tree_prep.column('Español', width=600, minwidth=300)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree_prep.yview)
        self.tree_prep.configure(yscrollcommand=scrollbar.set)
        
        self.tree_prep.pack(side='left', fill='both', expand=True, padx=(20,0), pady=(0,20))
        scrollbar.pack(side='right', fill='y', pady=(0,20), padx=(0,20))
        
        # Datos de preposiciones
        self.preposiciones = {
            'about': 'acerca de, sobre',
            'above': 'encima de, sobre',
            'across': 'a través de, al otro lado',
            'after': 'después de, tras',
            'against': 'contra',
            'along': 'a lo largo de',
            'among': 'entre (varios)',
            'around': 'alrededor de',
            'at': 'en, a',
            'before': 'antes de',
            'behind': 'detrás de',
            'below': 'debajo de',
            'beneath': 'bajo, debajo de',
            'beside': 'al lado de, junto a',
            'between': 'entre (dos)',
            'beyond': 'más allá de',
            'by': 'por, junto a, cerca de',
            'down': 'abajo, hacia abajo',
            'during': 'durante',
            'except': 'excepto',
            'for': 'para, por',
            'from': 'de, desde',
            'in': 'en, dentro de',
            'inside': 'dentro de',
            'into': 'hacia dentro, en',
            'like': 'como',
            'near': 'cerca de',
            'of': 'de',
            'off': 'fuera de, lejos de',
            'on': 'en, sobre',
            'onto': 'sobre, encima de',
            'out': 'fuera',
            'outside': 'fuera de',
            'over': 'sobre, encima de',
            'past': 'más allá de, pasado',
            'since': 'desde',
            'through': 'a través de',
            'throughout': 'a lo largo de, durante todo',
            'to': 'a, hacia',
            'toward': 'hacia',
            'under': 'bajo, debajo de',
            'underneath': 'debajo de',
            'until': 'hasta',
            'up': 'arriba, hacia arriba',
            'upon': 'sobre, encima de',
            'with': 'con',
            'within': 'dentro de',
            'without': 'sin'
        }
        
        self.mostrar_todas_preposiciones()
    
    def mostrar_todas_preposiciones(self):
        for item in self.tree_prep.get_children():
            self.tree_prep.delete(item)
        
        for prep, trad in sorted(self.preposiciones.items()):
            self.tree_prep.insert('', 'end', values=(prep, trad))
    
    def _on_search_prep_keyrelease(self, event):
        if self._search_prep_timer:
            self.root.after_cancel(self._search_prep_timer)
        self._search_prep_timer = self.root.after(300, self.buscar_preposicion)
    
    def buscar_preposicion(self):
        busqueda = self.entry_buscar_prep.get().strip().lower()
        
        for item in self.tree_prep.get_children():
            self.tree_prep.delete(item)
        
        if not busqueda:
            self.mostrar_todas_preposiciones()
            return
        
        for prep, trad in sorted(self.preposiciones.items()):
            if busqueda in prep.lower() or busqueda in trad.lower():
                self.tree_prep.insert('', 'end', values=(prep, trad))
    
    def crear_pestaña_dias_meses(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📅 Días/Meses")
        
        # Búsqueda
        frame_buscar = ttk.Frame(frame)
        frame_buscar.pack(fill='x', padx=20, pady=15)
        
        ttk.Label(frame_buscar, text="🔍", font=(FONT_FAMILY, 14)).pack(side='left', padx=(0,5))
        self.entry_buscar_dias = ttk.Entry(frame_buscar, width=30, font=(FONT_FAMILY, 11))
        self.entry_buscar_dias.pack(side='left', padx=5, ipady=5)
        self.entry_buscar_dias.bind('<KeyRelease>', self._on_search_dias_keyrelease)
        self._search_dias_timer = None
        
        # Tabla
        columns = ('Inglés', 'Español', 'Categoría')
        self.tree_dias = ttk.Treeview(frame, columns=columns, show='headings', height=20)
        
        self.tree_dias.heading('Inglés', text='🇬🇧 Inglés')
        self.tree_dias.heading('Español', text='🇪🇸 Español')
        self.tree_dias.heading('Categoría', text='📂 Categoría')
        
        self.tree_dias.column('Inglés', width=250, minwidth=150)
        self.tree_dias.column('Español', width=350, minwidth=200)
        self.tree_dias.column('Categoría', width=200, minwidth=150)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree_dias.yview)
        self.tree_dias.configure(yscrollcommand=scrollbar.set)
        
        self.tree_dias.pack(side='left', fill='both', expand=True, padx=(20,0), pady=(0,20))
        scrollbar.pack(side='right', fill='y', pady=(0,20), padx=(0,20))
        
        # Datos
        self.dias_meses = [
            ('Monday', 'lunes', 'Días de la semana'),
            ('Tuesday', 'martes', 'Días de la semana'),
            ('Wednesday', 'miércoles', 'Días de la semana'),
            ('Thursday', 'jueves', 'Días de la semana'),
            ('Friday', 'viernes', 'Días de la semana'),
            ('Saturday', 'sábado', 'Días de la semana'),
            ('Sunday', 'domingo', 'Días de la semana'),
            ('January', 'enero', 'Meses del año'),
            ('February', 'febrero', 'Meses del año'),
            ('March', 'marzo', 'Meses del año'),
            ('April', 'abril', 'Meses del año'),
            ('May', 'mayo', 'Meses del año'),
            ('June', 'junio', 'Meses del año'),
            ('July', 'julio', 'Meses del año'),
            ('August', 'agosto', 'Meses del año'),
            ('September', 'septiembre', 'Meses del año'),
            ('October', 'octubre', 'Meses del año'),
            ('November', 'noviembre', 'Meses del año'),
            ('December', 'diciembre', 'Meses del año'),
            ('day', 'día', 'Términos generales'),
            ('week', 'semana', 'Términos generales'),
            ('month', 'mes', 'Términos generales'),
            ('year', 'año', 'Términos generales'),
            ('weekend', 'fin de semana', 'Términos generales'),
            ('weekday', 'día de semana', 'Términos generales'),
            ('today', 'hoy', 'Términos generales'),
            ('tomorrow', 'mañana', 'Términos generales'),
            ('yesterday', 'ayer', 'Términos generales'),
            ('daily', 'diario, diariamente', 'Frecuencia'),
            ('weekly', 'semanal, semanalmente', 'Frecuencia'),
            ('monthly', 'mensual, mensualmente', 'Frecuencia'),
            ('yearly', 'anual, anualmente', 'Frecuencia'),
            ('annually', 'anualmente', 'Frecuencia'),
            ('biweekly', 'quincenal', 'Frecuencia'),
            ('fortnight', 'quincena', 'Frecuencia'),
            ('morning', 'mañana', 'Partes del día'),
            ('afternoon', 'tarde', 'Partes del día'),
            ('evening', 'tarde-noche', 'Partes del día'),
            ('night', 'noche', 'Partes del día'),
            ('midnight', 'medianoche', 'Partes del día'),
            ('noon', 'mediodía', 'Partes del día'),
            ('dawn', 'amanecer', 'Partes del día'),
            ('dusk', 'atardecer', 'Partes del día'),
            ('date', 'fecha', 'Términos generales'),
            ('calendar', 'calendario', 'Términos generales'),
            ('schedule', 'horario, agenda', 'Términos generales'),
            ('appointment', 'cita', 'Términos generales'),
            ('deadline', 'fecha límite', 'Términos generales'),
            ('season', 'estación, temporada', 'Términos generales'),
            ('spring', 'primavera', 'Estaciones'),
            ('summer', 'verano', 'Estaciones'),
            ('autumn/fall', 'otoño', 'Estaciones'),
            ('winter', 'invierno', 'Estaciones'),
            ('workday', 'día laboral', 'Términos generales'),
            ('holiday', 'día festivo, vacaciones', 'Términos generales'),
            ('vacation', 'vacaciones', 'Términos generales'),
            ('birthday', 'cumpleaños', 'Términos generales'),
            ('anniversary', 'aniversario', 'Términos generales')
        ]
        
        self.mostrar_todos_dias_meses()
    
    def mostrar_todos_dias_meses(self):
        for item in self.tree_dias.get_children():
            self.tree_dias.delete(item)
        
        for ingles, espanol, categoria in self.dias_meses:
            self.tree_dias.insert('', 'end', values=(ingles, espanol, categoria))
    
    def _on_search_dias_keyrelease(self, event):
        if self._search_dias_timer:
            self.root.after_cancel(self._search_dias_timer)
        self._search_dias_timer = self.root.after(300, self.buscar_dias_meses)
    
    def buscar_dias_meses(self):
        busqueda = self.entry_buscar_dias.get().strip().lower()
        
        for item in self.tree_dias.get_children():
            self.tree_dias.delete(item)
        
        if not busqueda:
            self.mostrar_todos_dias_meses()
            return
        
        for ingles, espanol, categoria in self.dias_meses:
            if busqueda in ingles.lower() or busqueda in espanol.lower() or busqueda in categoria.lower():
                self.tree_dias.insert('', 'end', values=(ingles, espanol, categoria))
    
    def crear_pestaña_numeros(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔢 Números")
        
        # Canvas con scroll
        canvas = tk.Canvas(frame, bg=COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=COLOR_BG)
        
        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw", width=1000)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel_num(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel_num)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y", pady=20)
        
        # Conversor
        conversor_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        conversor_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        ttk.Label(conversor_frame, text="🔢 Conversor de Números", font=(FONT_FAMILY, 16, 'bold'), 
                 foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,15))
        
        input_frame = tk.Frame(conversor_frame, bg=COLOR_BUTTON)
        input_frame.pack(pady=(0,10))
        
        ttk.Label(input_frame, text="Número:", background=COLOR_BUTTON).pack(side='left', padx=5)
        self.entry_numero = ttk.Entry(input_frame, width=20, font=(FONT_FAMILY, 12))
        self.entry_numero.pack(side='left', padx=5, ipady=5)
        ttk.Button(input_frame, text="✓ Convertir", command=self.convertir_numero).pack(side='left', padx=5)
        
        self.label_resultado = tk.Label(conversor_frame, text="", font=(FONT_FAMILY, 14, 'bold'), 
                                        bg=COLOR_BUTTON, fg=COLOR_SUCCESS, wraplength=800)
        self.label_resultado.pack(pady=(5,10))
        
        # Números 1-20
        numeros_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        numeros_frame.pack(fill='x', padx=20, pady=(0,20), ipady=10)
        
        ttk.Label(numeros_frame, text="📊 Números del 1 al 20", font=(FONT_FAMILY, 14, 'bold'), 
                 foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,10))
        
        numeros_1_20 = [
            ('1', 'one'), ('2', 'two'), ('3', 'three'), ('4', 'four'), ('5', 'five'),
            ('6', 'six'), ('7', 'seven'), ('8', 'eight'), ('9', 'nine'), ('10', 'ten'),
            ('11', 'eleven'), ('12', 'twelve'), ('13', 'thirteen'), ('14', 'fourteen'), ('15', 'fifteen'),
            ('16', 'sixteen'), ('17', 'seventeen'), ('18', 'eighteen'), ('19', 'nineteen'), ('20', 'twenty')
        ]
        
        grid_frame = tk.Frame(numeros_frame, bg=COLOR_BUTTON)
        grid_frame.pack(padx=20, pady=(0,10))
        
        for i, (num, palabra) in enumerate(numeros_1_20):
            row = i // 5
            col = i % 5
            item_frame = tk.Frame(grid_frame, bg=COLOR_BG, relief='solid', borderwidth=1)
            item_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            tk.Label(item_frame, text=f"{num} = {palabra}", font=(FONT_FAMILY, 10), 
                    bg=COLOR_BG, fg=COLOR_FG, width=15).pack(padx=10, pady=5)
        
        # Decenas
        decenas_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        decenas_frame.pack(fill='x', padx=20, pady=(0,20), ipady=10)
        
        ttk.Label(decenas_frame, text="📈 Decenas y Números Grandes", font=(FONT_FAMILY, 14, 'bold'), 
                 foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,10))
        
        decenas = [
            ('10', 'ten'), ('20', 'twenty'), ('30', 'thirty'), ('40', 'forty'), ('50', 'fifty'),
            ('60', 'sixty'), ('70', 'seventy'), ('80', 'eighty'), ('90', 'ninety'), ('100', 'one hundred'),
            ('1,000', 'one thousand'), ('10,000', 'ten thousand'), ('100,000', 'one hundred thousand'),
            ('1,000,000', 'one million'), ('1,000,000,000', 'one billion')
        ]
        
        grid_decenas = tk.Frame(decenas_frame, bg=COLOR_BUTTON)
        grid_decenas.pack(padx=20, pady=(0,10))
        
        for i, (num, palabra) in enumerate(decenas):
            row = i // 3
            col = i % 3
            item_frame = tk.Frame(grid_decenas, bg=COLOR_BG, relief='solid', borderwidth=1)
            item_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            tk.Label(item_frame, text=f"{num} = {palabra}", font=(FONT_FAMILY, 10), 
                    bg=COLOR_BG, fg=COLOR_FG, width=25).pack(padx=10, pady=5)
        
        # Reglas importantes
        reglas_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        reglas_frame.pack(fill='x', padx=20, pady=(0,20), ipady=10)
        
        ttk.Label(reglas_frame, text="📚 Reglas Importantes", font=(FONT_FAMILY, 14, 'bold'), 
                 foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,10))
        
        reglas = [
            "• Números 21-99: Se unen con guión (twenty-one, thirty-five, ninety-nine)",
            "• Hundred/Thousand/Million: Siempre en singular (two hundred, five thousand)",
            "• 'And' se usa después de hundred: 105 = one hundred and five",
            "• Números ordinales: 1st (first), 2nd (second), 3rd (third), 4th (fourth)...",
            "• Decimales: Se usa 'point' (3.5 = three point five)",
            "• Cero: 'zero' (matemáticas), 'oh' (teléfonos), 'nil' (deportes)",
            "• Fracciones: 1/2 (one half), 1/4 (one quarter), 3/4 (three quarters)",
            "• Porcentajes: 50% = fifty percent",
            "• Años: 2024 = twenty twenty-four, 1900 = nineteen hundred",
            "• Teléfonos: Se dicen dígito por dígito (555-1234 = five five five, one two three four)"
        ]
        
        reglas_text = tk.Frame(reglas_frame, bg=COLOR_BUTTON)
        reglas_text.pack(padx=30, pady=(0,15), fill='x')
        
        for regla in reglas:
            tk.Label(reglas_text, text=regla, font=(FONT_FAMILY, 10), bg=COLOR_BUTTON, 
                    fg=COLOR_FG, anchor='w', justify='left').pack(anchor='w', pady=3)
    
    def convertir_numero(self):
        try:
            num = int(self.entry_numero.get().strip())
            if num < 0 or num > 999999999:
                self.label_resultado.config(text="⚠️ Ingresa un número entre 0 y 999,999,999", fg=COLOR_ERROR)
                return
            
            resultado = self.numero_a_texto(num)
            self.label_resultado.config(text=f"✅ {resultado}", fg=COLOR_SUCCESS)
        except ValueError:
            self.label_resultado.config(text="⚠️ Ingresa un número válido", fg=COLOR_ERROR)
    
    def numero_a_texto(self, n):
        if n == 0:
            return "zero"
        
        unidades = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        decenas_especiales = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 
                             'sixteen', 'seventeen', 'eighteen', 'nineteen']
        decenas = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
        
        def convertir_centenas(num):
            if num == 0:
                return ''
            elif num < 10:
                return unidades[num]
            elif num < 20:
                return decenas_especiales[num - 10]
            elif num < 100:
                return decenas[num // 10] + ('-' + unidades[num % 10] if num % 10 != 0 else '')
            else:
                return unidades[num // 100] + ' hundred' + (' and ' + convertir_centenas(num % 100) if num % 100 != 0 else '')
        
        if n < 1000:
            return convertir_centenas(n)
        elif n < 1000000:
            miles = n // 1000
            resto = n % 1000
            return convertir_centenas(miles) + ' thousand' + (' ' + convertir_centenas(resto) if resto != 0 else '')
        else:
            millones = n // 1000000
            resto = n % 1000000
            resultado = convertir_centenas(millones) + ' million'
            if resto >= 1000:
                resultado += ' ' + convertir_centenas(resto // 1000) + ' thousand'
                resto = resto % 1000
            if resto > 0:
                resultado += ' ' + convertir_centenas(resto)
            return resultado
    
    def crear_pestaña_estadisticas(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Estadísticas")
        
        container = tk.Frame(frame, bg=COLOR_BG)
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Label(container, text="📊 Estadísticas del Vocabulario", 
                 font=(FONT_FAMILY, 20, 'bold'), foreground=COLOR_ACCENT, 
                 background=COLOR_BG).pack(pady=(0,30))
        
        self.stats_frame = tk.Frame(container, bg=COLOR_BG)
        self.stats_frame.pack()
        
        ttk.Button(container, text="🔄 Actualizar", command=self.actualizar_estadisticas).pack(pady=20)
        
        self.actualizar_estadisticas()
        self.cargar_palabras_caligrafia()
    
    def actualizar_estadisticas(self):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        total = len(self.datos)
        con_pronunciacion = sum(1 for d in self.datos.values() if 'pronunciacion' in d)
        sin_pronunciacion = total - con_pronunciacion
        con_notas = sum(1 for d in self.datos.values() if 'notas' in d)
        
        stats = [
            ("📚 Total de palabras", total, COLOR_ACCENT),
            ("🔊 Con pronunciación", con_pronunciacion, COLOR_SUCCESS),
            ("❌ Sin pronunciación", sin_pronunciacion, COLOR_ERROR),
            ("📝 Con notas", con_notas, COLOR_FG)
        ]
        
        for texto, valor, color in stats:
            frame_stat = tk.Frame(self.stats_frame, bg=COLOR_BG)
            frame_stat.pack(fill='x', pady=10)
            
            tk.Label(frame_stat, text=texto, font=(FONT_FAMILY, 14), 
                    bg=COLOR_BG, fg=COLOR_FG).pack(side='left', padx=20)
            tk.Label(frame_stat, text=str(valor), font=(FONT_FAMILY, 24, 'bold'), 
                    bg=COLOR_BG, fg=color).pack(side='right', padx=20)
    
    def crear_pestaña_caligrafia(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="✍️ Caligrafía")
        
        # Frame superior para selección
        frame_top = tk.Frame(frame, bg=COLOR_BG)
        frame_top.pack(fill='x', padx=30, pady=20)
        
        ttk.Label(frame_top, text="✍️ Práctica de Caligrafía", 
                 font=(FONT_FAMILY, 18, 'bold'), foreground=COLOR_ACCENT, 
                 background=COLOR_BG).pack(pady=(0,15))
        
        # Selector de palabra
        frame_selector = tk.Frame(frame_top, bg=COLOR_BG)
        frame_selector.pack(pady=10)
        
        ttk.Label(frame_selector, text="Selecciona palabra:").pack(side='left', padx=5)
        
        self.combo_caligrafia = ttk.Combobox(frame_selector, width=30, font=(FONT_FAMILY, 11), state='readonly')
        self.combo_caligrafia.pack(side='left', padx=5)
        self.combo_caligrafia.bind('<<ComboboxSelected>>', self.actualizar_caligrafia)
        
        ttk.Button(frame_selector, text="🔄 Actualizar Lista", 
                  command=self.cargar_palabras_caligrafia).pack(side='left', padx=5)
        
        # Frame de contenido con scroll
        self.canvas_caligrafia = tk.Canvas(frame, bg=COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.canvas_caligrafia.yview)
        self.frame_caligrafia_content = tk.Frame(self.canvas_caligrafia, bg=COLOR_BG)
        
        self.frame_caligrafia_content.bind(
            "<Configure>",
            lambda e: self.canvas_caligrafia.configure(scrollregion=self.canvas_caligrafia.bbox("all"))
        )
        
        self.canvas_caligrafia.create_window((0, 0), window=self.frame_caligrafia_content, anchor="nw", width=950)
        self.canvas_caligrafia.configure(yscrollcommand=scrollbar.set)
        
        # Habilitar scroll con mouse wheel
        def _on_mousewheel(event):
            self.canvas_caligrafia.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas_caligrafia.bind_all("<MouseWheel>", _on_mousewheel)
        
        self.canvas_caligrafia.pack(side="left", fill="both", expand=True, padx=30, pady=(0,20))
        scrollbar.pack(side="right", fill="y", pady=(0,20))
        
        self.cargar_palabras_caligrafia()
    
    def cargar_palabras_caligrafia(self):
        palabras = sorted(self.datos.keys(), key=str.lower)
        self.combo_caligrafia['values'] = palabras
        if palabras:
            self.combo_caligrafia.current(0)
            self.actualizar_caligrafia()
    
    def actualizar_caligrafia(self, event=None):
        # Limpiar contenido anterior
        for widget in self.frame_caligrafia_content.winfo_children():
            widget.destroy()
        
        palabra = self.combo_caligrafia.get()
        if not palabra or palabra not in self.datos:
            return
        
        significado = self.datos[palabra].get('significado', '')
        pronunciacion = self.datos[palabra].get('pronunciacion', '')
        
        # Información de la palabra
        info_frame = tk.Frame(self.frame_caligrafia_content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        info_frame.pack(fill='x', pady=(0,20), padx=10, ipady=10)
        
        tk.Label(info_frame, text=f"🇬🇧 {palabra}", font=(FONT_FAMILY, 16, 'bold'), 
                bg=COLOR_BUTTON, fg=COLOR_ACCENT).pack(pady=5)
        tk.Label(info_frame, text=f"🇪🇸 {significado}", font=(FONT_FAMILY, 12), 
                bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=2)
        if pronunciacion:
            tk.Label(info_frame, text=f"🔊 {pronunciacion}", font=(FONT_FAMILY, 11), 
                    bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=2)
        
        # Sección de caligrafía
        tk.Label(self.frame_caligrafia_content, text="✍️ Practica escribiendo:", 
                font=(FONT_FAMILY, 14, 'bold'), bg=COLOR_BG, fg=COLOR_ACCENT).pack(anchor='w', pady=(10,10), padx=10)
        
        # Líneas para practicar escritura
        for i in range(5):
            line_frame = tk.Frame(self.frame_caligrafia_content, bg=COLOR_BG)
            line_frame.pack(fill='x', pady=5, padx=10)
            
            tk.Label(line_frame, text=palabra, font=(FONT_FAMILY, 14), 
                    bg=COLOR_BG, fg=COLOR_FG, width=20, anchor='w').pack(side='left', padx=5)
            tk.Label(line_frame, text="_" * 50, font=(FONT_FAMILY, 14), 
                    bg=COLOR_BG, fg=COLOR_BUTTON_HOVER).pack(side='left')
        
        # Sección de oraciones
        tk.Label(self.frame_caligrafia_content, text="📝 Oraciones de ejemplo:", 
                font=(FONT_FAMILY, 14, 'bold'), bg=COLOR_BG, fg=COLOR_ACCENT).pack(anchor='w', pady=(20,10), padx=10)
        
        oraciones = self.generar_oraciones(palabra)
        
        for i, oracion in enumerate(oraciones, 1):
            oracion_frame = tk.Frame(self.frame_caligrafia_content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
            oracion_frame.pack(fill='x', pady=5, padx=10, ipady=8)
            
            tk.Label(oracion_frame, text=f"{i}. {oracion}", font=(FONT_FAMILY, 11), 
                    bg=COLOR_BUTTON, fg=COLOR_FG, wraplength=700, justify='left').pack(anchor='w', padx=10, pady=5)
            
            # Líneas para copiar la oración
            for _ in range(2):
                tk.Label(oracion_frame, text="_" * 80, font=(FONT_FAMILY, 10), 
                        bg=COLOR_BUTTON, fg=COLOR_BUTTON_HOVER).pack(anchor='w', padx=10, pady=2)
    
    def generar_oraciones(self, palabra):
        # Plantillas mejoradas con diferentes estructuras
        plantillas_basicas = [
            f"I use {palabra} every day.",
            f"The {palabra} is very important.",
            f"Can you give me the {palabra}?",
            f"This {palabra} is amazing.",
            f"I need a {palabra} right now."
        ]
        
        plantillas_avanzadas = [
            f"Where can I find a good {palabra}?",
            f"My favorite {palabra} is here.",
            f"That {palabra} looks fantastic.",
            f"Have you seen my {palabra}?",
            f"The best {palabra} costs a lot."
        ]
        
        # Combinar y seleccionar aleatoriamente
        todas_plantillas = plantillas_basicas + plantillas_avanzadas
        return random.sample(todas_plantillas, min(5, len(todas_plantillas)))
    
    def editar_palabra(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una palabra de la tabla")
            return
        
        item = self.tree.item(seleccion[0])
        palabra_actual = str(item['values'][0])
        significado_actual = str(item['values'][1])
        pronunciacion_actual = '' if item['values'][2] == '-' else str(item['values'][2])
        
        # Ventana de edición
        ventana = tk.Toplevel(self.root)
        ventana.title("✏️ Editar Palabra")
        ventana.geometry("550x500")
        ventana.configure(bg=COLOR_BG)
        ventana.grab_set()
        
        container = tk.Frame(ventana, bg=COLOR_BG)
        container.pack(expand=True, fill='both', padx=40, pady=30)
        
        ttk.Label(container, text="🇬🇧 Palabra en inglés", style='Title.TLabel').pack(pady=(0,5))
        entry_palabra = ttk.Entry(container, width=45, font=(FONT_FAMILY, 11))
        entry_palabra.insert(0, palabra_actual)
        entry_palabra.pack(pady=(0,15), ipady=8)
        
        ttk.Label(container, text="🇪🇸 Significado en español", style='Title.TLabel').pack(pady=(0,5))
        entry_significado = ttk.Entry(container, width=45, font=(FONT_FAMILY, 11))
        entry_significado.insert(0, significado_actual)
        entry_significado.pack(pady=(0,15), ipady=8)
        
        ttk.Label(container, text="🔊 Pronunciación", style='Title.TLabel').pack(pady=(0,5))
        entry_pronunciacion = ttk.Entry(container, width=45, font=(FONT_FAMILY, 11))
        entry_pronunciacion.insert(0, pronunciacion_actual)
        entry_pronunciacion.pack(pady=(0,15), ipady=8)
        
        notas_actual = '' if 'notas' not in self.datos[palabra_actual] else self.datos[palabra_actual].get('notas', '')
        ttk.Label(container, text="📝 Notas", style='Title.TLabel').pack(pady=(0,5))
        entry_notas = ttk.Entry(container, width=45, font=(FONT_FAMILY, 11))
        entry_notas.insert(0, notas_actual)
        entry_notas.pack(pady=(0,25), ipady=8)
        
        def guardar_cambios():
            nueva_palabra = entry_palabra.get().strip()
            nuevo_significado = entry_significado.get().strip()
            nueva_pronunciacion = entry_pronunciacion.get().strip()
            
            if not nueva_palabra or not nuevo_significado:
                messagebox.showwarning("Advertencia", "Completa palabra y significado")
                return
            
            if len(nueva_palabra) > 100 or len(nuevo_significado) > 500:
                messagebox.showwarning("Advertencia", "Palabra o significado demasiado largo")
                return
            
            if nueva_pronunciacion and len(nueva_pronunciacion) > 200:
                messagebox.showwarning("Advertencia", "Pronunciación demasiado larga")
                return
            
            try:
                # Eliminar palabra anterior si existe
                if palabra_actual in self.datos:
                    del self.datos[palabra_actual]
                
                # Agregar palabra nueva/actualizada
                self.datos[nueva_palabra] = {
                    'significado': nuevo_significado
                }
                
                if nueva_pronunciacion:
                    self.datos[nueva_palabra]['pronunciacion'] = nueva_pronunciacion
                
                nuevas_notas = entry_notas.get().strip()
                if nuevas_notas:
                    self.datos[nueva_palabra]['notas'] = nuevas_notas
                
                # Guardar en archivo
                if guardar_datos(self.datos):
                    messagebox.showinfo("Éxito", f"Palabra '{nueva_palabra}' actualizada correctamente")
                    ventana.destroy()
                    self.mostrar_todas()
                else:
                    messagebox.showerror("Error", "No se pudo guardar los cambios")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        btn_frame = tk.Frame(container, bg=COLOR_BG)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="💾 Guardar Cambios", command=guardar_cambios).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana.destroy).pack(side='left', padx=5)
    
    def eliminar_palabra(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una palabra de la tabla")
            return
        
        item = self.tree.item(seleccion[0])
        palabra = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{palabra}'?"):
            del self.datos[palabra]
            if guardar_datos(self.datos):
                messagebox.showinfo("Éxito", f"'{palabra}' eliminada")
                self.mostrar_todas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la palabra")
    
    def guardar_pronunciacion(self):
        palabra = self.entry_palabra_pron.get().strip()
        pronunciacion = self.entry_pronunciacion.get().strip()
        
        if not palabra or not pronunciacion:
            messagebox.showwarning("Advertencia", "Completa todos los campos")
            return
        
        if len(pronunciacion) > 200:
            messagebox.showwarning("Advertencia", "Pronunciación demasiado larga (máximo 200 caracteres)")
            return
        
        if palabra not in self.datos:
            messagebox.showerror("Error", f"'{palabra}' no existe en el vocabulario")
            return
        
        self.datos[palabra]['pronunciacion'] = pronunciacion
        
        if guardar_datos(self.datos):
            messagebox.showinfo("Éxito", f"Pronunciación de '{palabra}' guardada")
            self.entry_palabra_pron.delete(0, tk.END)
            self.entry_pronunciacion.delete(0, tk.END)
            self.mostrar_todas()
        else:
            messagebox.showerror("Error", "No se pudo guardar la pronunciación")

    def crear_pestaña_ayuda(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="❓ Ayuda")
        
        # Canvas con scroll
        canvas = tk.Canvas(frame, bg=COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=COLOR_BG)
        
        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw", width=1000)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel_ayuda(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel_ayuda)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y", pady=20)
        
        # Soporte
        soporte_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        soporte_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        tk.Label(soporte_frame, text="📞 Soporte Técnico", font=(FONT_FAMILY, 16, 'bold'), 
                bg=COLOR_BUTTON, fg=COLOR_ACCENT).pack(pady=(10,15))
        
        tk.Label(soporte_frame, text="¿Necesitas ayuda? Contáctanos:", font=(FONT_FAMILY, 11), 
                bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=5)
        
        tk.Label(soporte_frame, text="📧 Email: administrador@agilizesoluciones.com", 
                font=(FONT_FAMILY, 11, 'bold'), bg=COLOR_BUTTON, fg=COLOR_SUCCESS).pack(pady=5)
        
        tk.Label(soporte_frame, text="📱 Teléfono: +54 11 6168-2555", 
                font=(FONT_FAMILY, 11, 'bold'), bg=COLOR_BUTTON, fg=COLOR_SUCCESS).pack(pady=(5,15))
        
        # Manual de Usuario
        manual_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        manual_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        tk.Label(manual_frame, text="📚 Manual de Usuario", font=(FONT_FAMILY, 16, 'bold'), 
                bg=COLOR_BUTTON, fg=COLOR_ACCENT).pack(pady=(10,15))
        
        manual_text = [
            ("📚 Vocabulario", "Agrega, edita y elimina palabras. Usa la búsqueda para encontrar rápidamente. Doble clic para editar."),
            ("🔊 Pronunciación", "Agrega la pronunciación fonética de cualquier palabra de tu vocabulario."),
            ("🎯 Práctica", "Modo quiz para practicar. Elige entre Inglés→Español o Español→Inglés."),
            ("✍️ Caligrafía", "Practica escribiendo palabras y oraciones de ejemplo."),
            ("📍 Preposiciones", "Consulta 47 preposiciones en inglés con sus traducciones."),
            ("📅 Días/Meses", "Días de la semana, meses del año y términos relacionados."),
            ("🔢 Números", "Conversor de números a texto en inglés + reglas importantes."),
            ("📄 Exportar/Importar", "Guarda tu vocabulario en CSV o importa palabras desde un archivo."),
            ("💾 Respaldos", "Tus datos están en " + str(APP_DIR) + ". Copia esta carpeta para hacer respaldo.")
        ]
        
        manual_content = tk.Frame(manual_frame, bg=COLOR_BUTTON)
        manual_content.pack(padx=30, pady=(0,15), fill='x')
        
        for titulo, desc in manual_text:
            item_frame = tk.Frame(manual_content, bg=COLOR_BG, relief='solid', borderwidth=1)
            item_frame.pack(fill='x', pady=5)
            tk.Label(item_frame, text=titulo, font=(FONT_FAMILY, 11, 'bold'), 
                    bg=COLOR_BG, fg=COLOR_ACCENT, anchor='w').pack(padx=10, pady=(5,2), fill='x')
            tk.Label(item_frame, text=desc, font=(FONT_FAMILY, 10), 
                    bg=COLOR_BG, fg=COLOR_FG, anchor='w', wraplength=850, justify='left').pack(padx=10, pady=(2,5), fill='x')
        
        # Términos y Condiciones
        terminos_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        terminos_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        tk.Label(terminos_frame, text="📜 Términos y Condiciones", font=(FONT_FAMILY, 16, 'bold'), 
                bg=COLOR_BUTTON, fg=COLOR_ACCENT).pack(pady=(10,15))
        
        terminos = [
            "1. Uso Educativo: Esta aplicación es de uso gratuito con fines educativos.",
            "2. Privacidad: Todos tus datos se almacenan localmente en tu computadora. No se envía información a servidores externos.",
            "3. Respaldos: Es responsabilidad del usuario hacer respaldos de sus datos.",
            "4. Garantía: La aplicación se proporciona 'tal cual' sin garantías de ningún tipo.",
            "5. Soporte: El soporte técnico se proporciona por email o teléfono durante horario laboral.",
            "6. Actualizaciones: Las actualizaciones son opcionales y se notificarán por email.",
            "7. Licencia: Software de uso libre para fines educativos personales.",
            "8. Modificaciones: Nos reservamos el derecho de modificar estos términos en cualquier momento."
        ]
        
        terminos_content = tk.Frame(terminos_frame, bg=COLOR_BUTTON)
        terminos_content.pack(padx=30, pady=(0,15), fill='x')
        
        for termino in terminos:
            tk.Label(terminos_content, text=termino, font=(FONT_FAMILY, 10), 
                    bg=COLOR_BUTTON, fg=COLOR_FG, anchor='w', wraplength=850, justify='left').pack(anchor='w', pady=3)
        
        # Acerca de
        about_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        about_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        tk.Label(about_frame, text="ℹ️ Acerca de English Memory", font=(FONT_FAMILY, 16, 'bold'), 
                bg=COLOR_BUTTON, fg=COLOR_ACCENT).pack(pady=(10,10))
        
        tk.Label(about_frame, text="Versión: 1.0", font=(FONT_FAMILY, 11), 
                bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=2)
        tk.Label(about_frame, text="Desarrollado por: Agilize Soluciones", font=(FONT_FAMILY, 11), 
                bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=2)
        tk.Label(about_frame, text="Aplicación educativa para aprendizaje de inglés", font=(FONT_FAMILY, 10), 
                bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=(2,15))

if __name__ == '__main__':
    root = tk.Tk()
    app = DiccionarioApp(root)
    root.mainloop()
