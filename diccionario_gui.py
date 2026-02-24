"""
English Memory v1.3.2
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
- Gramática (pronombres, verbos auxiliares, artículos, demostrativos, cuantificadores)
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
Versión: 1.3.2
Fecha: 2025
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
import shutil
from datetime import datetime
try:
    import pyttsx3
    TTS_DISPONIBLE = True
except:
    TTS_DISPONIBLE = False

# Detectar sistema operativo y configurar ruta apropiada
if platform.system() == 'Windows':
    APP_DIR = Path.home() / 'AppData' / 'Local' / 'DiccionarioPersonal'
else:  # Linux, macOS
    APP_DIR = Path.home() / '.local' / 'share' / 'DiccionarioPersonal'

APP_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVO_DATOS = APP_DIR / 'palabras.json'

# Colores modernos - Tema oscuro
COLOR_BG_DARK = '#1a1625'
COLOR_FG_DARK = '#e9e4f0'
COLOR_ACCENT_DARK = '#a78bfa'
COLOR_BUTTON_DARK = '#2d2438'
COLOR_BUTTON_HOVER_DARK = '#3d3149'

# Colores modernos - Tema claro
COLOR_BG_LIGHT = '#f5f5f5'
COLOR_FG_LIGHT = '#1a1625'
COLOR_ACCENT_LIGHT = '#7c3aed'
COLOR_BUTTON_LIGHT = '#e9e4f0'
COLOR_BUTTON_HOVER_LIGHT = '#d4d4d8'

# Colores actuales (por defecto oscuro)
COLOR_BG = COLOR_BG_DARK
COLOR_FG = COLOR_FG_DARK
COLOR_ACCENT = COLOR_ACCENT_DARK
COLOR_ACCENT_DARK = '#7c3aed'
COLOR_BUTTON = COLOR_BUTTON_DARK
COLOR_BUTTON_HOVER = COLOR_BUTTON_HOVER_DARK
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
        self.root.title("📚 English Memory v1.3.2")
        self.root.geometry("1200x700")
        self.root.configure(bg=COLOR_BG)
        self.datos = cargar_datos()
        self.modo_oscuro = True
        
        # Estilo moderno
        self.configurar_estilos()
        
        # Header
        header = tk.Frame(root, bg=COLOR_BG)
        header.pack(fill='x', padx=20, pady=(20,10))
        header_title = tk.Frame(header, bg=COLOR_BG)
        header_title.pack()
        tk.Label(header_title, text="📚 English Memory v1.3.2", 
                font=(FONT_FAMILY, 24, 'bold'), bg=COLOR_BG, fg=COLOR_ACCENT).pack(side='left')
        ttk.Button(header_title, text="🌓", command=self.toggle_tema, width=3).pack(side='left', padx=10)
        tk.Label(header, text="Aprende y organiza tu vocabulario en inglés", 
                font=(FONT_FAMILY, 10), bg=COLOR_BG, fg=COLOR_FG).pack()
        tk.Label(header, text=f"📁 Datos guardados en: {APP_DIR}", 
                font=(FONT_FAMILY, 8), bg=COLOR_BG, fg=COLOR_BUTTON_HOVER).pack()
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Pestañas
        self.crear_pestaña_consultar()
        self.crear_pestaña_practica()
        self.crear_pestaña_caligrafia()
        self.crear_pestaña_preposiciones()
        self.crear_pestaña_dias_meses()
        self.crear_pestaña_numeros()
        self.crear_pestaña_gramatica()
        self.crear_pestaña_contracciones()
        self.crear_pestaña_verbos()
        self.crear_pestaña_conjugacion()
        self.crear_pestaña_estadisticas()
        self.crear_pestaña_ayuda()
        
        # Tooltips para pestañas
        self.crear_tooltips_pestañas()
        
        # Backup automático cada 5 minutos
        self.programar_backup()
    
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
    
    def crear_tooltips_pestañas(self):
        # Cambiar texto de pestañas a solo iconos
        iconos_tooltips = [
            ("📖", "Vocabulario"),
            ("🎯", "Práctica"),
            ("✍️", "Caligrafía"),
            ("📍", "Preposiciones"),
            ("📅", "Días/Meses"),
            ("🔢", "Números"),
            ("📝", "Gramática"),
            ("🔗", "Contracciones"),
            ("📘", "Verbos"),
            ("⏰", "Conjugación"),
            ("📊", "Estadísticas"),
            ("❓", "Ayuda")
        ]
        
        for i, (icono, tooltip) in enumerate(iconos_tooltips):
            self.notebook.tab(i, text=icono)
        
        # Bind para mostrar tooltips
        self.notebook.bind('<Motion>', self._mostrar_tooltip_pestana)
        self.notebook.bind('<Leave>', self._ocultar_tooltip_pestana)
    
    def _mostrar_tooltip_pestana(self, event):
        try:
            tab_id = self.notebook.index(f"@{event.x},{event.y}")
            tooltips = ["Vocabulario", "Práctica", "Caligrafía", 
                       "Preposiciones", "Días/Meses", "Números", "Gramática",
                       "Contracciones", "Verbos", "Conjugación", "Estadísticas", "Ayuda"]
            
            if hasattr(self, '_tooltip_window'):
                self._tooltip_window.destroy()
            
            self._tooltip_window = tk.Toplevel(self.root)
            self._tooltip_window.wm_overrideredirect(True)
            self._tooltip_window.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(self._tooltip_window, text=tooltips[tab_id], 
                           background="#ffffe0", relief='solid', borderwidth=1, 
                           font=(FONT_FAMILY, 9), padx=5, pady=2)
            label.pack()
        except:
            self._ocultar_tooltip_pestana(None)
    
    def _ocultar_tooltip_pestana(self, event):
        if hasattr(self, '_tooltip_window'):
            self._tooltip_window.destroy()
            delattr(self, '_tooltip_window')
    
    def toggle_tema(self):
        self.modo_oscuro = not self.modo_oscuro
        messagebox.showinfo("Tema", "Función de cambio de tema en desarrollo.\nPor ahora solo está disponible el tema oscuro.")
    
    def pronunciar_palabra(self, palabra):
        if not TTS_DISPONIBLE:
            messagebox.showinfo("TTS no disponible", "La pronunciación TTS no está disponible.\nInstala pyttsx3: pip install pyttsx3")
            return
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.say(palabra)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            messagebox.showerror("Error TTS", f"Error al pronunciar: {str(e)}")
    
    def programar_backup(self):
        self.hacer_backup()
        self.root.after(300000, self.programar_backup)  # 5 minutos
    
    def hacer_backup(self):
        try:
            backup_dir = APP_DIR / 'backups'
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = backup_dir / f'palabras_backup_{timestamp}.json'
            
            if ARCHIVO_DATOS.exists():
                shutil.copy2(ARCHIVO_DATOS, backup_file)
                
                # Mantener solo los últimos 10 backups
                backups = sorted(backup_dir.glob('palabras_backup_*.json'))
                if len(backups) > 10:
                    for old_backup in backups[:-10]:
                        old_backup.unlink()
        except:
            pass
    
    def crear_pestaña_consultar(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📖")
        
        # Búsqueda
        frame_buscar = ttk.Frame(frame)
        frame_buscar.pack(fill='x', padx=20, pady=15)
        
        # Fila 1: Botones de acción
        frame_acciones = tk.Frame(frame_buscar, bg=COLOR_BG)
        frame_acciones.pack(side='left', fill='x', expand=False)
        
        ttk.Button(frame_acciones, text="➕ Agregar", command=self.abrir_modal_agregar).pack(side='left', padx=2)
        ttk.Button(frame_acciones, text="✏️ Editar", command=self.editar_palabra).pack(side='left', padx=2)
        ttk.Button(frame_acciones, text="🗑️ Eliminar", command=self.eliminar_palabra).pack(side='left', padx=2)
        ttk.Button(frame_acciones, text="🔊 Pronunciar", command=self.pronunciar_seleccionada).pack(side='left', padx=2)
        
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
        columns = ('Inglés', 'Español', 'Pronunciación', 'Notas')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        self.tree.heading('Inglés', text='🇬🇧 Inglés')
        self.tree.heading('Español', text='🇪🇸 Español')
        self.tree.heading('Pronunciación', text='🔊 Pronunciación')
        self.tree.heading('Notas', text='📝 Notas')
        
        self.tree.column('Inglés', width=150, minwidth=100)
        self.tree.column('Español', width=250, minwidth=150)
        self.tree.column('Pronunciación', width=200, minwidth=120)
        self.tree.column('Notas', width=300, minwidth=150)
        
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
        self.tree.heading('Notas', text='📝 Notas', command=lambda: self.ordenar_columna('Notas'))
        
        self.mostrar_todas()
        self.orden_actual = {'columna': None, 'reverso': False}
    
    def pronunciar_seleccionada(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una palabra")
            return
        item = self.tree.item(seleccion[0])
        palabra = item['values'][0]
        self.pronunciar_palabra(palabra)
    

    def abrir_modal_agregar(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("➕ Agregar Palabra")
        ventana.geometry("550x520")
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
        
        ttk.Label(container, text="🔊 Pronunciación (opcional)", style='Title.TLabel').pack(pady=(0,5))
        entry_pronunciacion = ttk.Entry(container, width=45, font=(FONT_FAMILY, 11))
        entry_pronunciacion.pack(pady=(0,15), ipady=8)
        
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
            
            pronunciacion = entry_pronunciacion.get().strip()
            if pronunciacion and len(pronunciacion) > 200:
                messagebox.showwarning("Advertencia", "La pronunciación no puede exceder 200 caracteres")
                return
            
            notas = entry_notas.get().strip()
            if len(notas) > 1000:
                messagebox.showwarning("Advertencia", "Las notas no pueden exceder 1000 caracteres")
                return
            
            self.datos[palabra] = {'significado': significado}
            if pronunciacion:
                self.datos[palabra]['pronunciacion'] = pronunciacion
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
            notas = self.datos[palabra].get('notas', '-')
            self.tree.insert('', 'end', values=(palabra, significado, pronunciacion, notas))
    
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
            (palabra, datos.get('significado', ''), datos.get('pronunciacion', '-'), datos.get('notas', '-'))
            for palabra, datos in self.datos.items()
            if busqueda in palabra.lower() or busqueda in datos.get('significado', '').lower()
        ]
        
        for palabra, significado, pronunciacion, notas in sorted(resultados):
            self.tree.insert('', 'end', values=(palabra, significado, pronunciacion, notas))
        
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
        self.notebook.add(frame, text="🎯")
        
        container = tk.Frame(frame, bg=COLOR_BG)
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        self.practica_palabra = tk.StringVar()
        self.practica_respuesta = tk.StringVar()
        self.practica_modo = tk.StringVar(value='ingles')
        self.palabras_erroneas = set()
        
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
        
        # Campo de entrada para respuesta
        ttk.Label(container, text="Tu respuesta:", background=COLOR_BG, 
                 font=(FONT_FAMILY, 12)).pack(pady=(10,5))
        self.entry_respuesta_practica = ttk.Entry(container, width=40, font=(FONT_FAMILY, 14))
        self.entry_respuesta_practica.pack(pady=(0,10), ipady=8)
        self.entry_respuesta_practica.bind('<Return>', lambda e: self.verificar_respuesta())
        
        # Resultado
        self.label_respuesta = tk.Label(container, textvariable=self.practica_respuesta, 
                                        font=(FONT_FAMILY, 16), bg=COLOR_BG, 
                                        fg=COLOR_SUCCESS, wraplength=500)
        self.label_respuesta.pack(pady=10)
        
        # Botones
        btn_frame = tk.Frame(container, bg=COLOR_BG)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="✓ Verificar", command=self.verificar_respuesta).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔄 Nueva Palabra", command=self.nueva_palabra_practica).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔊 Pronunciar", command=lambda: self.pronunciar_palabra(self.palabra_actual_practica) if hasattr(self, 'palabra_actual_practica') else None).pack(side='left', padx=5)
        
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
        self.entry_respuesta_practica.delete(0, tk.END)
        self.entry_respuesta_practica.focus()
    
    def verificar_respuesta(self):
        if not hasattr(self, 'palabra_actual_practica'):
            return
        
        respuesta_usuario = self.entry_respuesta_practica.get().strip().lower()
        if not respuesta_usuario:
            messagebox.showwarning("Advertencia", "Ingresa una respuesta")
            return
        
        palabra = self.palabra_actual_practica
        significado = self.datos[palabra].get('significado', '').lower()
        pronunciacion = self.datos[palabra].get('pronunciacion', '')
        notas = self.datos[palabra].get('notas', '')
        
        # Determinar respuesta correcta
        if self.practica_modo.get() == 'ingles':
            respuesta_correcta = significado
        else:
            respuesta_correcta = palabra.lower()
        
        # Verificar si es correcta (permitir variaciones)
        es_correcta = respuesta_usuario == respuesta_correcta or respuesta_usuario in respuesta_correcta or respuesta_correcta in respuesta_usuario
        
        if es_correcta:
            resultado = f"✅ ¡CORRECTO!\n{palabra} = {self.datos[palabra].get('significado', '')}"
            self.label_respuesta.config(fg=COLOR_SUCCESS)
        else:
            resultado = f"❌ INCORRECTO\nTu respuesta: {respuesta_usuario}\nRespuesta correcta: {respuesta_correcta}"
            self.label_respuesta.config(fg=COLOR_ERROR)
            # Guardar palabra errónea
            self.palabras_erroneas.add(palabra)
        
        if pronunciacion:
            resultado += f"\n🔊 {pronunciacion}"
        if notas:
            resultado += f"\n📝 {notas}"
        
        self.practica_respuesta.set(resultado)
    
    def crear_pestaña_preposiciones(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📍")
        
        # Búsqueda
        frame_buscar = ttk.Frame(frame)
        frame_buscar.pack(fill='x', padx=20, pady=15)
        
        ttk.Label(frame_buscar, text="🔍", font=(FONT_FAMILY, 14)).pack(side='left', padx=(0,5))
        self.entry_buscar_prep = ttk.Entry(frame_buscar, width=30, font=(FONT_FAMILY, 11))
        self.entry_buscar_prep.pack(side='left', padx=5, ipady=5)
        self.entry_buscar_prep.bind('<KeyRelease>', self._on_search_prep_keyrelease)
        self._search_prep_timer = None
        ttk.Button(frame_buscar, text="🔊 Pronunciar", command=self.pronunciar_preposicion_seleccionada).pack(side='left', padx=5)
        
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
    
    def pronunciar_preposicion_seleccionada(self):
        seleccion = self.tree_prep.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una preposición")
            return
        item = self.tree_prep.item(seleccion[0])
        palabra = item['values'][0]
        self.pronunciar_palabra(palabra)
    
    def crear_pestaña_dias_meses(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📅")
        
        # Búsqueda
        frame_buscar = ttk.Frame(frame)
        frame_buscar.pack(fill='x', padx=20, pady=15)
        
        ttk.Label(frame_buscar, text="🔍", font=(FONT_FAMILY, 14)).pack(side='left', padx=(0,5))
        self.entry_buscar_dias = ttk.Entry(frame_buscar, width=30, font=(FONT_FAMILY, 11))
        self.entry_buscar_dias.pack(side='left', padx=5, ipady=5)
        self.entry_buscar_dias.bind('<KeyRelease>', self._on_search_dias_keyrelease)
        self._search_dias_timer = None
        ttk.Button(frame_buscar, text="🔊 Pronunciar", command=self.pronunciar_dia_seleccionado).pack(side='left', padx=5)
        
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
    
    def pronunciar_dia_seleccionado(self):
        seleccion = self.tree_dias.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un día/mes")
            return
        item = self.tree_dias.item(seleccion[0])
        palabra = item['values'][0]
        self.pronunciar_palabra(palabra)
    
    def crear_pestaña_numeros(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔢")
        
        # Canvas con scroll
        canvas = tk.Canvas(frame, bg=COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=COLOR_BG)
        
        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw", width=1000)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel_num(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel_num))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        
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
        ttk.Button(input_frame, text="🔊 Pronunciar", command=self.pronunciar_numero).pack(side='left', padx=5)
        
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
    
    def pronunciar_numero(self):
        try:
            num = int(self.entry_numero.get().strip())
            if num < 0 or num > 999999999:
                messagebox.showwarning("Advertencia", "Ingresa un número entre 0 y 999,999,999")
                return
            resultado = self.numero_a_texto(num)
            self.pronunciar_palabra(resultado)
        except ValueError:
            messagebox.showwarning("Advertencia", "Ingresa un número válido")
    
    def crear_pestaña_gramatica(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📝")
        
        canvas = tk.Canvas(frame, bg=COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=COLOR_BG)
        
        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw", width=1000)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel_gram(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel_gram))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y", pady=20)
        
        # Pronombres
        pron_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        pron_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        ttk.Label(pron_frame, text="👤 Pronombres Personales y Posesivos", font=(FONT_FAMILY, 16, 'bold'), 
                 foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,15))
        
        # Tabla de pronombres
        pron_data = [
            ('I', 'me', 'my', 'mine', 'yo', 'me/mí', 'mi/mis', 'mío/a'),
            ('You', 'you', 'your', 'yours', 'tú/usted', 'te/ti/le', 'tu/su', 'tuyo/suyo'),
            ('He', 'him', 'his', 'his', 'él', 'lo/le', 'su', 'suyo'),
            ('She', 'her', 'her', 'hers', 'ella', 'la/le', 'su', 'suyo'),
            ('It', 'it', 'its', 'its', 'ello', 'lo', 'su', 'suyo'),
            ('We', 'us', 'our', 'ours', 'nosotros', 'nos', 'nuestro/a', 'nuestro/a'),
            ('They', 'them', 'their', 'theirs', 'ellos/as', 'los/las/les', 'su', 'suyo')
        ]
        
        table_frame = tk.Frame(pron_frame, bg=COLOR_BUTTON)
        table_frame.pack(padx=20, pady=(0,15))
        
        headers = ['Sujeto', 'Objeto', 'Adj. Posesivo', 'Pron. Posesivo', 'Español (Suj)', 'Español (Obj)', 'Español (Adj)', 'Español (Pron)']
        for col, header in enumerate(headers):
            tk.Label(table_frame, text=header, font=(FONT_FAMILY, 9, 'bold'), 
                    bg=COLOR_ACCENT, fg=COLOR_BG, width=12, relief='solid', borderwidth=1).grid(row=0, column=col, sticky='ew')
        
        for row, data in enumerate(pron_data, 1):
            for col, value in enumerate(data):
                bg = COLOR_BG if row % 2 == 0 else COLOR_BUTTON_HOVER
                tk.Label(table_frame, text=value, font=(FONT_FAMILY, 9), 
                        bg=bg, fg=COLOR_FG, width=12, relief='solid', borderwidth=1).grid(row=row, column=col, sticky='ew')
        
        # Pronombres reflexivos
        reflex_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        reflex_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        ttk.Label(reflex_frame, text="🪞 Pronombres Reflexivos", font=(FONT_FAMILY, 16, 'bold'), 
                 foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,15))
        
        reflexivos = [
            ('myself', 'yo mismo/a, me', 'I hurt myself'),
            ('yourself', 'tú mismo/a, te', 'You can do it yourself'),
            ('himself', 'él mismo, se', 'He looked at himself'),
            ('herself', 'ella misma, se', 'She taught herself'),
            ('itself', 'sí mismo/a (cosa)', 'The door closed itself'),
            ('ourselves', 'nosotros mismos/as, nos', 'We enjoyed ourselves'),
            ('yourselves', 'ustedes mismos/as, se', 'You all can help yourselves'),
            ('themselves', 'ellos mismos/as, se', 'They prepared themselves')
        ]
        
        reflex_content = tk.Frame(reflex_frame, bg=COLOR_BUTTON)
        reflex_content.pack(padx=30, pady=(0,15), fill='x')
        
        for reflexivo, espanol, ejemplo in reflexivos:
            item_frame = tk.Frame(reflex_content, bg=COLOR_BG, relief='solid', borderwidth=1)
            item_frame.pack(fill='x', pady=3)
            tk.Label(item_frame, text=reflexivo, font=(FONT_FAMILY, 11, 'bold'), 
                    bg=COLOR_BG, fg=COLOR_ACCENT, width=15, anchor='w').pack(side='left', padx=10, pady=5)
            tk.Label(item_frame, text=espanol, font=(FONT_FAMILY, 10), 
                    bg=COLOR_BG, fg=COLOR_FG, width=25, anchor='w').pack(side='left', padx=5)
            tk.Label(item_frame, text=f"Ej: {ejemplo}", font=(FONT_FAMILY, 9, 'italic'), 
                    bg=COLOR_BG, fg=COLOR_BUTTON_HOVER, anchor='w').pack(side='left', padx=5)
        
        # Verbos auxiliares
        aux_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        aux_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        ttk.Label(aux_frame, text="🔧 Verbos Auxiliares", font=(FONT_FAMILY, 16, 'bold'), 
                 foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,15))
        
        aux_data = [
            ('TO BE', 'I am', 'You are', 'He/She/It is', 'We/They are', 'ser/estar'),
            ('TO HAVE', 'I have', 'You have', 'He/She/It has', 'We/They have', 'tener/haber'),
            ('TO DO', 'I do', 'You do', 'He/She/It does', 'We/They do', 'hacer')
        ]
        
        for verbo, yo, tu, el, nosotros, esp in aux_data:
            verb_frame = tk.Frame(aux_frame, bg=COLOR_BG, relief='solid', borderwidth=1)
            verb_frame.pack(fill='x', padx=20, pady=5)
            tk.Label(verb_frame, text=f"{verbo} ({esp})", font=(FONT_FAMILY, 11, 'bold'), 
                    bg=COLOR_BG, fg=COLOR_ACCENT, width=20, anchor='w').pack(side='left', padx=10, pady=5)
            tk.Label(verb_frame, text=f"{yo} | {tu} | {el} | {nosotros}", font=(FONT_FAMILY, 10), 
                    bg=COLOR_BG, fg=COLOR_FG, anchor='w').pack(side='left', padx=10, pady=5)
        
        # Artículos
        art_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        art_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        ttk.Label(art_frame, text="📰 Artículos", font=(FONT_FAMILY, 16, 'bold'), 
                 foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,15))
        
        articulos = [
            ('a', 'un/una (antes de consonante)', 'a book, a car'),
            ('an', 'un/una (antes de vocal)', 'an apple, an hour'),
            ('the', 'el/la/los/las (específico)', 'the book, the sun')
        ]
        
        for art, desc, ej in articulos:
            art_item = tk.Frame(art_frame, bg=COLOR_BG, relief='solid', borderwidth=1)
            art_item.pack(fill='x', padx=20, pady=5)
            tk.Label(art_item, text=art, font=(FONT_FAMILY, 12, 'bold'), 
                    bg=COLOR_BG, fg=COLOR_ACCENT, width=8).pack(side='left', padx=10, pady=8)
            tk.Label(art_item, text=desc, font=(FONT_FAMILY, 10), 
                    bg=COLOR_BG, fg=COLOR_FG, width=35, anchor='w').pack(side='left', padx=5)
            tk.Label(art_item, text=f"Ej: {ej}", font=(FONT_FAMILY, 9, 'italic'), 
                    bg=COLOR_BG, fg=COLOR_BUTTON_HOVER, anchor='w').pack(side='left', padx=5)
        
        # Demostrativos
        dem_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        dem_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        ttk.Label(dem_frame, text="👉 Adjetivos Demostrativos", font=(FONT_FAMILY, 16, 'bold'), 
                 foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,15))
        
        demostrativos = [
            ('this', 'este/esta (singular, cerca)', 'this book'),
            ('that', 'ese/esa/aquel (singular, lejos)', 'that car'),
            ('these', 'estos/estas (plural, cerca)', 'these books'),
            ('those', 'esos/esas/aquellos (plural, lejos)', 'those cars')
        ]
        
        for dem, desc, ej in demostrativos:
            dem_item = tk.Frame(dem_frame, bg=COLOR_BG, relief='solid', borderwidth=1)
            dem_item.pack(fill='x', padx=20, pady=5)
            tk.Label(dem_item, text=dem, font=(FONT_FAMILY, 12, 'bold'), 
                    bg=COLOR_BG, fg=COLOR_ACCENT, width=10).pack(side='left', padx=10, pady=8)
            tk.Label(dem_item, text=desc, font=(FONT_FAMILY, 10), 
                    bg=COLOR_BG, fg=COLOR_FG, width=35, anchor='w').pack(side='left', padx=5)
            tk.Label(dem_item, text=f"Ej: {ej}", font=(FONT_FAMILY, 9, 'italic'), 
                    bg=COLOR_BG, fg=COLOR_BUTTON_HOVER).pack(side='left', padx=5)
        
        # Cuantificadores
        cuant_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        cuant_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        
        ttk.Label(cuant_frame, text="📊 Cuantificadores", font=(FONT_FAMILY, 16, 'bold'), 
                 foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,15))
        
        cuantificadores = [
            ('some', 'algunos/as (afirmativo)', 'I have some books'),
            ('any', 'algún/ningún (negativo/pregunta)', 'Do you have any books?'),
            ('much', 'mucho (incontable)', 'much water'),
            ('many', 'muchos (contable)', 'many books'),
            ('a lot of', 'mucho/muchos (ambos)', 'a lot of water/books'),
            ('few', 'pocos (contable)', 'few books'),
            ('little', 'poco (incontable)', 'little water'),
            ('several', 'varios', 'several options'),
            ('all', 'todo/todos', 'all students'),
            ('no', 'ningún', 'no money')
        ]
        
        for cuant, desc, ej in cuantificadores:
            cuant_item = tk.Frame(cuant_frame, bg=COLOR_BG, relief='solid', borderwidth=1)
            cuant_item.pack(fill='x', padx=20, pady=3)
            tk.Label(cuant_item, text=cuant, font=(FONT_FAMILY, 11, 'bold'), 
                    bg=COLOR_BG, fg=COLOR_ACCENT, width=12, anchor='w').pack(side='left', padx=10, pady=5)
            tk.Label(cuant_item, text=desc, font=(FONT_FAMILY, 10), 
                    bg=COLOR_BG, fg=COLOR_FG, width=30, anchor='w').pack(side='left', padx=5)
            tk.Label(cuant_item, text=f"Ej: {ej}", font=(FONT_FAMILY, 9, 'italic'), 
                    bg=COLOR_BG, fg=COLOR_BUTTON_HOVER, anchor='w').pack(side='left', padx=5)
    
    def crear_pestaña_contracciones(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔗")
        
        # Búsqueda
        frame_buscar = ttk.Frame(frame)
        frame_buscar.pack(fill='x', padx=20, pady=15)
        
        ttk.Label(frame_buscar, text="🔍", font=(FONT_FAMILY, 14)).pack(side='left', padx=(0,5))
        self.entry_buscar_contr = ttk.Entry(frame_buscar, width=30, font=(FONT_FAMILY, 11))
        self.entry_buscar_contr.pack(side='left', padx=5, ipady=5)
        self.entry_buscar_contr.bind('<KeyRelease>', self._on_search_contr_keyrelease)
        self._search_contr_timer = None
        ttk.Button(frame_buscar, text="🔊 Pronunciar", command=self.pronunciar_contraccion_seleccionada).pack(side='left', padx=5)
        
        # Tabla de contracciones
        columns = ('Contracción', 'Palabras Originales', 'Español')
        self.tree_contr = ttk.Treeview(frame, columns=columns, show='headings', height=20)
        
        self.tree_contr.heading('Contracción', text='🔗 Contracción')
        self.tree_contr.heading('Palabras Originales', text='🔤 Palabras Originales')
        self.tree_contr.heading('Español', text='🇪🇸 Español')
        
        self.tree_contr.column('Contracción', width=200, minwidth=150)
        self.tree_contr.column('Palabras Originales', width=300, minwidth=200)
        self.tree_contr.column('Español', width=400, minwidth=250)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree_contr.yview)
        self.tree_contr.configure(yscrollcommand=scrollbar.set)
        
        self.tree_contr.pack(side='left', fill='both', expand=True, padx=(20,0), pady=(0,20))
        scrollbar.pack(side='right', fill='y', pady=(0,20), padx=(0,20))
        
        # Datos de contracciones
        self.contracciones = [
            # Contracciones con BE
            ("I'm", "I am", "yo soy/estoy"),
            ("you're", "you are", "tú eres/estás"),
            ("he's", "he is", "él es/está"),
            ("she's", "she is", "ella es/está"),
            ("it's", "it is", "eso es/está"),
            ("we're", "we are", "nosotros somos/estamos"),
            ("they're", "they are", "ellos son/están"),
            ("that's", "that is", "eso es"),
            ("there's", "there is", "hay"),
            ("here's", "here is", "aquí está"),
            ("who's", "who is", "quién es"),
            ("what's", "what is", "qué es"),
            ("where's", "where is", "dónde está"),
            ("when's", "when is", "cuándo es"),
            ("how's", "how is", "cómo está"),
            ("why's", "why is", "por qué es"),
            
            # Contracciones con HAVE
            ("I've", "I have", "yo he/tengo"),
            ("you've", "you have", "tú has/tienes"),
            ("we've", "we have", "nosotros hemos/tenemos"),
            ("they've", "they have", "ellos han/tienen"),
            ("could've", "could have", "podría haber"),
            ("should've", "should have", "debería haber"),
            ("would've", "would have", "habría"),
            ("might've", "might have", "podría haber"),
            ("must've", "must have", "debe haber"),
            
            # Contracciones con WILL
            ("I'll", "I will", "yo haré/iré"),
            ("you'll", "you will", "tú harás/irás"),
            ("he'll", "he will", "él hará/irá"),
            ("she'll", "she will", "ella hará/irá"),
            ("it'll", "it will", "eso hará"),
            ("we'll", "we will", "nosotros haremos/iremos"),
            ("they'll", "they will", "ellos harán/irán"),
            ("that'll", "that will", "eso hará"),
            ("there'll", "there will", "habrá"),
            
            # Contracciones con WOULD/HAD
            ("I'd", "I would/had", "yo haría/había"),
            ("you'd", "you would/had", "tú harías/habías"),
            ("he'd", "he would/had", "él haría/había"),
            ("she'd", "she would/had", "ella haría/había"),
            ("it'd", "it would/had", "eso haría/había"),
            ("we'd", "we would/had", "nosotros haríamos/habíamos"),
            ("they'd", "they would/had", "ellos harían/habían"),
            ("that'd", "that would/had", "eso haría/había"),
            ("there'd", "there would/had", "habría"),
            
            # Contracciones negativas con BE
            ("isn't", "is not", "no es/está"),
            ("aren't", "are not", "no son/están"),
            ("wasn't", "was not", "no era/estaba"),
            ("weren't", "were not", "no eran/estaban"),
            ("ain't", "am/is/are not", "no soy/es/son (informal)"),
            
            # Contracciones negativas con HAVE
            ("hasn't", "has not", "no ha"),
            ("haven't", "have not", "no he/han"),
            ("hadn't", "had not", "no había"),
            
            # Contracciones negativas con WILL/WOULD
            ("won't", "will not", "no haré/iré"),
            ("wouldn't", "would not", "no haría"),
            ("shan't", "shall not", "no deberé (formal)"),
            
            # Contracciones negativas con DO
            ("don't", "do not", "no hago/haces"),
            ("doesn't", "does not", "no hace"),
            ("didn't", "did not", "no hice/hizo"),
            
            # Contracciones negativas con modales
            ("can't", "cannot", "no puedo/puede"),
            ("couldn't", "could not", "no pude/podía"),
            ("shouldn't", "should not", "no debería"),
            ("mustn't", "must not", "no debe"),
            ("mightn't", "might not", "podría no"),
            ("needn't", "need not", "no necesita"),
            ("daren't", "dare not", "no se atreve"),
            ("oughtn't", "ought not", "no debería"),
            
            # Contracciones informales
            ("let's", "let us", "vamos a/dejemos"),
            ("y'all", "you all", "ustedes (informal)"),
            ("ma'am", "madam", "señora"),
            ("o'clock", "of the clock", "en punto"),
            ("'cause", "because", "porque (informal)"),
            ("gonna", "going to", "voy a (informal)"),
            ("wanna", "want to", "quiero (informal)"),
            ("gotta", "got to", "tengo que (informal)"),
            ("gimme", "give me", "dame (informal)"),
            ("lemme", "let me", "déjame (informal)"),
            ("kinda", "kind of", "tipo de (informal)"),
            ("sorta", "sort of", "algo así (informal)"),
            ("dunno", "don't know", "no sé (informal)"),
            ("woulda", "would have", "habría (informal)"),
            ("coulda", "could have", "podría haber (informal)"),
            ("shoulda", "should have", "debería haber (informal)")
        ]
        
        self.mostrar_todas_contracciones()
    
    def mostrar_todas_contracciones(self):
        for item in self.tree_contr.get_children():
            self.tree_contr.delete(item)
        
        for contraccion, original, espanol in self.contracciones:
            self.tree_contr.insert('', 'end', values=(contraccion, original, espanol))
    
    def _on_search_contr_keyrelease(self, event):
        if self._search_contr_timer:
            self.root.after_cancel(self._search_contr_timer)
        self._search_contr_timer = self.root.after(300, self.buscar_contraccion)
    
    def buscar_contraccion(self):
        busqueda = self.entry_buscar_contr.get().strip().lower()
        
        for item in self.tree_contr.get_children():
            self.tree_contr.delete(item)
        
        if not busqueda:
            self.mostrar_todas_contracciones()
            return
        
        for contraccion, original, espanol in self.contracciones:
            if (busqueda in contraccion.lower() or busqueda in original.lower() or 
                busqueda in espanol.lower()):
                self.tree_contr.insert('', 'end', values=(contraccion, original, espanol))
    
    def pronunciar_contraccion_seleccionada(self):
        seleccion = self.tree_contr.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una contracción")
            return
        item = self.tree_contr.item(seleccion[0])
        palabra = item['values'][0]
        self.pronunciar_palabra(palabra)
    
    def crear_pestaña_verbos(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📘")
        
        frame_buscar = ttk.Frame(frame)
        frame_buscar.pack(fill='x', padx=20, pady=15)
        
        ttk.Label(frame_buscar, text="🔍", font=(FONT_FAMILY, 14)).pack(side='left', padx=(0,5))
        self.entry_buscar_verbos = ttk.Entry(frame_buscar, width=30, font=(FONT_FAMILY, 11))
        self.entry_buscar_verbos.pack(side='left', padx=5, ipady=5)
        self.entry_buscar_verbos.bind('<KeyRelease>', self._on_search_verbos_keyrelease)
        self._search_verbos_timer = None
        ttk.Button(frame_buscar, text="🔊 Pronunciar", command=self.pronunciar_verbo_seleccionado).pack(side='left', padx=5)
        
        columns = ('Infinitivo', 'Pasado', 'Participio', 'Español', 'Tipo')
        self.tree_verbos = ttk.Treeview(frame, columns=columns, show='headings', height=20)
        
        self.tree_verbos.heading('Infinitivo', text='🇬🇧 Infinitivo')
        self.tree_verbos.heading('Pasado', text='⏪ Pasado')
        self.tree_verbos.heading('Participio', text='✅ Participio')
        self.tree_verbos.heading('Español', text='🇪🇸 Español')
        self.tree_verbos.heading('Tipo', text='📋 Tipo')
        
        self.tree_verbos.column('Infinitivo', width=180, minwidth=120)
        self.tree_verbos.column('Pasado', width=180, minwidth=120)
        self.tree_verbos.column('Participio', width=180, minwidth=120)
        self.tree_verbos.column('Español', width=250, minwidth=150)
        self.tree_verbos.column('Tipo', width=120, minwidth=100)
        
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree_verbos.yview)
        self.tree_verbos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_verbos.pack(side='left', fill='both', expand=True, padx=(20,0), pady=(0,20))
        scrollbar.pack(side='right', fill='y', pady=(0,20), padx=(0,20))
        
        self.todos_verbos = [
            ('be', 'was/were', 'been', 'ser/estar', 'Irregular'),('have', 'had', 'had', 'tener/haber', 'Irregular'),
            ('do', 'did', 'done', 'hacer', 'Irregular'),('say', 'said', 'said', 'decir', 'Irregular'),
            ('go', 'went', 'gone', 'ir', 'Irregular'),('get', 'got', 'gotten/got', 'obtener/conseguir', 'Irregular'),
            ('make', 'made', 'made', 'hacer', 'Irregular'),('know', 'knew', 'known', 'saber/conocer', 'Irregular'),
            ('think', 'thought', 'thought', 'pensar', 'Irregular'),('take', 'took', 'taken', 'tomar/llevar', 'Irregular'),
            ('see', 'saw', 'seen', 'ver', 'Irregular'),('come', 'came', 'come', 'venir', 'Irregular'),
            ('give', 'gave', 'given', 'dar', 'Irregular'),('find', 'found', 'found', 'encontrar', 'Irregular'),
            ('tell', 'told', 'told', 'decir/contar', 'Irregular'),('feel', 'felt', 'felt', 'sentir', 'Irregular'),
            ('leave', 'left', 'left', 'dejar/salir', 'Irregular'),('keep', 'kept', 'kept', 'mantener', 'Irregular'),
            ('let', 'let', 'let', 'dejar/permitir', 'Irregular'),('begin', 'began', 'begun', 'comenzar', 'Irregular'),
            ('hear', 'heard', 'heard', 'oír', 'Irregular'),('run', 'ran', 'run', 'correr', 'Irregular'),
            ('bring', 'brought', 'brought', 'traer', 'Irregular'),('write', 'wrote', 'written', 'escribir', 'Irregular'),
            ('sit', 'sat', 'sat', 'sentarse', 'Irregular'),('stand', 'stood', 'stood', 'estar de pie', 'Irregular'),
            ('lose', 'lost', 'lost', 'perder', 'Irregular'),('pay', 'paid', 'paid', 'pagar', 'Irregular'),
            ('meet', 'met', 'met', 'conocer/encontrar', 'Irregular'),('set', 'set', 'set', 'establecer', 'Irregular'),
            ('lead', 'led', 'led', 'liderar/conducir', 'Irregular'),('understand', 'understood', 'understood', 'entender', 'Irregular'),
            ('speak', 'spoke', 'spoken', 'hablar', 'Irregular'),('read', 'read', 'read', 'leer', 'Irregular'),
            ('spend', 'spent', 'spent', 'gastar/pasar tiempo', 'Irregular'),('grow', 'grew', 'grown', 'crecer', 'Irregular'),
            ('win', 'won', 'won', 'ganar', 'Irregular'),('teach', 'taught', 'taught', 'enseñar', 'Irregular'),
            ('buy', 'bought', 'bought', 'comprar', 'Irregular'),('send', 'sent', 'sent', 'enviar', 'Irregular'),
            ('build', 'built', 'built', 'construir', 'Irregular'),('fall', 'fell', 'fallen', 'caer', 'Irregular'),
            ('cut', 'cut', 'cut', 'cortar', 'Irregular'),('sell', 'sold', 'sold', 'vender', 'Irregular'),
            ('carry', 'carried', 'carried', 'llevar/cargar', 'Irregular'),('break', 'broke', 'broken', 'romper', 'Irregular'),
            ('agree', 'agreed', 'agreed', 'estar de acuerdo', 'Irregular'),('hit', 'hit', 'hit', 'golpear', 'Irregular'),
            ('eat', 'ate', 'eaten', 'comer', 'Irregular'),('cover', 'covered', 'covered', 'cubrir', 'Irregular'),
            ('catch', 'caught', 'caught', 'atrapar', 'Irregular'),('draw', 'drew', 'drawn', 'dibujar', 'Irregular'),
            ('choose', 'chose', 'chosen', 'elegir', 'Irregular'),('wear', 'wore', 'worn', 'usar/llevar puesto', 'Irregular'),
            ('drive', 'drove', 'driven', 'conducir', 'Irregular'),('sing', 'sang', 'sung', 'cantar', 'Irregular'),
            ('swim', 'swam', 'swum', 'nadar', 'Irregular'),('fly', 'flew', 'flown', 'volar', 'Irregular'),
            ('drink', 'drank', 'drunk', 'beber', 'Irregular'),('ride', 'rode', 'ridden', 'montar', 'Irregular'),
            ('throw', 'threw', 'thrown', 'lanzar', 'Irregular'),('forget', 'forgot', 'forgotten', 'olvidar', 'Irregular'),
            ('become', 'became', 'become', 'convertirse', 'Irregular'),('hold', 'held', 'held', 'sostener', 'Irregular'),
            ('put', 'put', 'put', 'poner', 'Irregular'),('mean', 'meant', 'meant', 'significar', 'Irregular'),
            ('show', 'showed', 'shown', 'mostrar', 'Irregular'),('lie', 'lay', 'lain', 'yacer/acostarse', 'Irregular'),
            ('lay', 'laid', 'laid', 'poner/colocar', 'Irregular'),('rise', 'rose', 'risen', 'levantarse', 'Irregular'),
            ('shake', 'shook', 'shaken', 'sacudir', 'Irregular'),('wake', 'woke', 'woken', 'despertar', 'Irregular'),
            ('blow', 'blew', 'blown', 'soplar', 'Irregular'),('hide', 'hid', 'hidden', 'esconder', 'Irregular'),
            ('bite', 'bit', 'bitten', 'morder', 'Irregular'),('fight', 'fought', 'fought', 'pelear', 'Irregular'),
            ('freeze', 'froze', 'frozen', 'congelar', 'Irregular'),('steal', 'stole', 'stolen', 'robar', 'Irregular'),
            ('tear', 'tore', 'torn', 'rasgar', 'Irregular'),('swear', 'swore', 'sworn', 'jurar', 'Irregular'),
            ('bear', 'bore', 'born/borne', 'soportar/dar a luz', 'Irregular'),('beat', 'beat', 'beaten', 'golpear/vencer', 'Irregular'),
            ('bend', 'bent', 'bent', 'doblar', 'Irregular'),('bind', 'bound', 'bound', 'atar', 'Irregular'),
            ('bleed', 'bled', 'bled', 'sangrar', 'Irregular'),('breed', 'bred', 'bred', 'criar', 'Irregular'),
            ('burst', 'burst', 'burst', 'estallar', 'Irregular'),('cast', 'cast', 'cast', 'lanzar/echar', 'Irregular'),
            ('cling', 'clung', 'clung', 'aferrarse', 'Irregular'),('creep', 'crept', 'crept', 'arrastrarse', 'Irregular'),
            ('deal', 'dealt', 'dealt', 'tratar/repartir', 'Irregular'),('dig', 'dug', 'dug', 'cavar', 'Irregular'),
            ('feed', 'fed', 'fed', 'alimentar', 'Irregular'),('flee', 'fled', 'fled', 'huir', 'Irregular'),
            ('forbid', 'forbade', 'forbidden', 'prohibir', 'Irregular'),('forgive', 'forgave', 'forgiven', 'perdonar', 'Irregular'),
            ('grind', 'ground', 'ground', 'moler', 'Irregular'),('hang', 'hung', 'hung', 'colgar', 'Irregular'),
            ('hurt', 'hurt', 'hurt', 'herir/doler', 'Irregular'),('kneel', 'knelt', 'knelt', 'arrodillarse', 'Irregular'),
            ('lean', 'leant/leaned', 'leant/leaned', 'apoyarse', 'Irregular'),('leap', 'leapt/leaped', 'leapt/leaped', 'saltar', 'Irregular'),
            ('lend', 'lent', 'lent', 'prestar', 'Irregular'),('light', 'lit', 'lit', 'encender', 'Irregular'),
            ('quit', 'quit', 'quit', 'renunciar', 'Irregular'),('seek', 'sought', 'sought', 'buscar', 'Irregular'),
            ('shine', 'shone', 'shone', 'brillar', 'Irregular'),('shoot', 'shot', 'shot', 'disparar', 'Irregular'),
            ('shrink', 'shrank', 'shrunk', 'encoger', 'Irregular'),('shut', 'shut', 'shut', 'cerrar', 'Irregular'),
            ('sink', 'sank', 'sunk', 'hundir', 'Irregular'),('slide', 'slid', 'slid', 'deslizar', 'Irregular'),
            ('sling', 'slung', 'slung', 'lanzar', 'Irregular'),('slit', 'slit', 'slit', 'cortar/rajar', 'Irregular'),
            ('sow', 'sowed', 'sown', 'sembrar', 'Irregular'),('spin', 'spun', 'spun', 'girar', 'Irregular'),
            ('spit', 'spat', 'spat', 'escupir', 'Irregular'),('split', 'split', 'split', 'dividir', 'Irregular'),
            ('spread', 'spread', 'spread', 'extender', 'Irregular'),('spring', 'sprang', 'sprung', 'saltar', 'Irregular'),
            ('stick', 'stuck', 'stuck', 'pegar', 'Irregular'),('sting', 'stung', 'stung', 'picar', 'Irregular'),
            ('stink', 'stank', 'stunk', 'apestar', 'Irregular'),('strike', 'struck', 'struck', 'golpear', 'Irregular'),
            ('string', 'strung', 'strung', 'ensartar', 'Irregular'),('strive', 'strove', 'striven', 'esforzarse', 'Irregular'),
            ('swear', 'swore', 'sworn', 'jurar', 'Irregular'),('sweep', 'swept', 'swept', 'barrer', 'Irregular'),
            ('swell', 'swelled', 'swollen', 'hinchar', 'Irregular'),('swing', 'swung', 'swung', 'balancear', 'Irregular'),
            ('weep', 'wept', 'wept', 'llorar', 'Irregular'),('wind', 'wound', 'wound', 'enrollar', 'Irregular'),
            ('wring', 'wrung', 'wrung', 'retorcer', 'Irregular'),('can', 'could', '-', 'poder', 'Modal'),
            ('may', 'might', '-', 'poder/permiso', 'Modal'),('must', 'must', '-', 'deber', 'Modal'),
            ('shall', 'should', '-', 'deber', 'Modal'),('will', 'would', '-', 'futuro/condicional', 'Modal'),
            ('accept', 'accepted', 'accepted', 'aceptar', 'Regular'),('add', 'added', 'added', 'agregar', 'Regular'),
            ('allow', 'allowed', 'allowed', 'permitir', 'Regular'),('answer', 'answered', 'answered', 'responder', 'Regular'),
            ('appear', 'appeared', 'appeared', 'aparecer', 'Regular'),('apply', 'applied', 'applied', 'aplicar', 'Regular'),
            ('arrive', 'arrived', 'arrived', 'llegar', 'Regular'),('ask', 'asked', 'asked', 'preguntar', 'Regular'),
            ('attend', 'attended', 'attended', 'asistir', 'Regular'),('avoid', 'avoided', 'avoided', 'evitar', 'Regular'),
            ('bake', 'baked', 'baked', 'hornear', 'Regular'),('believe', 'believed', 'believed', 'creer', 'Regular'),
            ('belong', 'belonged', 'belonged', 'pertenecer', 'Regular'),('boil', 'boiled', 'boiled', 'hervir', 'Regular'),
            ('borrow', 'borrowed', 'borrowed', 'pedir prestado', 'Regular'),('brush', 'brushed', 'brushed', 'cepillar', 'Regular'),
            ('call', 'called', 'called', 'llamar', 'Regular'),('cancel', 'cancelled', 'cancelled', 'cancelar', 'Regular'),
            ('care', 'cared', 'cared', 'cuidar', 'Regular'),('celebrate', 'celebrated', 'celebrated', 'celebrar', 'Regular'),
            ('change', 'changed', 'changed', 'cambiar', 'Regular'),('charge', 'charged', 'charged', 'cobrar', 'Regular'),
            ('check', 'checked', 'checked', 'revisar', 'Regular'),('claim', 'claimed', 'claimed', 'reclamar', 'Regular'),
            ('clean', 'cleaned', 'cleaned', 'limpiar', 'Regular'),('clear', 'cleared', 'cleared', 'despejar', 'Regular'),
            ('climb', 'climbed', 'climbed', 'escalar', 'Regular'),('close', 'closed', 'closed', 'cerrar', 'Regular'),
            ('collect', 'collected', 'collected', 'coleccionar', 'Regular'),('compare', 'compared', 'compared', 'comparar', 'Regular'),
            ('complain', 'complained', 'complained', 'quejarse', 'Regular'),('complete', 'completed', 'completed', 'completar', 'Regular'),
            ('confirm', 'confirmed', 'confirmed', 'confirmar', 'Regular'),('connect', 'connected', 'connected', 'conectar', 'Regular'),
            ('consider', 'considered', 'considered', 'considerar', 'Regular'),('contain', 'contained', 'contained', 'contener', 'Regular'),
            ('continue', 'continued', 'continued', 'continuar', 'Regular'),('control', 'controlled', 'controlled', 'controlar', 'Regular'),
            ('cook', 'cooked', 'cooked', 'cocinar', 'Regular'),('copy', 'copied', 'copied', 'copiar', 'Regular'),
            ('cost', 'costed', 'costed', 'costar', 'Regular'),('count', 'counted', 'counted', 'contar', 'Regular'),
            ('cover', 'covered', 'covered', 'cubrir', 'Regular'),('create', 'created', 'created', 'crear', 'Regular'),
            ('cross', 'crossed', 'crossed', 'cruzar', 'Regular'),('cry', 'cried', 'cried', 'llorar', 'Regular'),
            ('damage', 'damaged', 'damaged', 'dañar', 'Regular'),('dance', 'danced', 'danced', 'bailar', 'Regular'),
            ('decide', 'decided', 'decided', 'decidir', 'Regular'),('deliver', 'delivered', 'delivered', 'entregar', 'Regular'),
            ('depend', 'depended', 'depended', 'depender', 'Regular'),('describe', 'described', 'described', 'describir', 'Regular'),
            ('design', 'designed', 'designed', 'diseñar', 'Regular'),('destroy', 'destroyed', 'destroyed', 'destruir', 'Regular'),
            ('develop', 'developed', 'developed', 'desarrollar', 'Regular'),('die', 'died', 'died', 'morir', 'Regular'),
            ('discover', 'discovered', 'discovered', 'descubrir', 'Regular'),('discuss', 'discussed', 'discussed', 'discutir', 'Regular'),
            ('divide', 'divided', 'divided', 'dividir', 'Regular'),('doubt', 'doubted', 'doubted', 'dudar', 'Regular'),
            ('dress', 'dressed', 'dressed', 'vestir', 'Regular'),('drop', 'dropped', 'dropped', 'dejar caer', 'Regular'),
            ('dry', 'dried', 'dried', 'secar', 'Regular'),('earn', 'earned', 'earned', 'ganar', 'Regular'),
            ('employ', 'employed', 'employed', 'emplear', 'Regular'),('encourage', 'encouraged', 'encouraged', 'animar', 'Regular'),
            ('end', 'ended', 'ended', 'terminar', 'Regular'),('enjoy', 'enjoyed', 'enjoyed', 'disfrutar', 'Regular'),
            ('enter', 'entered', 'entered', 'entrar', 'Regular'),('escape', 'escaped', 'escaped', 'escapar', 'Regular'),
            ('examine', 'examined', 'examined', 'examinar', 'Regular'),('exist', 'existed', 'existed', 'existir', 'Regular'),
            ('expect', 'expected', 'expected', 'esperar', 'Regular'),('experience', 'experienced', 'experienced', 'experimentar', 'Regular'),
            ('explain', 'explained', 'explained', 'explicar', 'Regular'),('express', 'expressed', 'expressed', 'expresar', 'Regular'),
            ('face', 'faced', 'faced', 'enfrentar', 'Regular'),('fail', 'failed', 'failed', 'fallar', 'Regular'),
            ('fear', 'feared', 'feared', 'temer', 'Regular'),('fill', 'filled', 'filled', 'llenar', 'Regular'),
            ('finish', 'finished', 'finished', 'terminar', 'Regular'),('fix', 'fixed', 'fixed', 'arreglar', 'Regular'),
            ('follow', 'followed', 'followed', 'seguir', 'Regular'),('force', 'forced', 'forced', 'forzar', 'Regular'),
            ('form', 'formed', 'formed', 'formar', 'Regular'),('gain', 'gained', 'gained', 'ganar', 'Regular'),
            ('guess', 'guessed', 'guessed', 'adivinar', 'Regular'),('happen', 'happened', 'happened', 'suceder', 'Regular'),
            ('hate', 'hated', 'hated', 'odiar', 'Regular'),('help', 'helped', 'helped', 'ayudar', 'Regular'),
            ('hope', 'hoped', 'hoped', 'esperar', 'Regular'),('identify', 'identified', 'identified', 'identificar', 'Regular'),
            ('imagine', 'imagined', 'imagined', 'imaginar', 'Regular'),('improve', 'improved', 'improved', 'mejorar', 'Regular'),
            ('include', 'included', 'included', 'incluir', 'Regular'),('increase', 'increased', 'increased', 'aumentar', 'Regular'),
            ('inform', 'informed', 'informed', 'informar', 'Regular'),('intend', 'intended', 'intended', 'intentar', 'Regular'),
            ('introduce', 'introduced', 'introduced', 'presentar', 'Regular'),('invite', 'invited', 'invited', 'invitar', 'Regular'),
            ('involve', 'involved', 'involved', 'involucrar', 'Regular'),('join', 'joined', 'joined', 'unirse', 'Regular'),
            ('judge', 'judged', 'judged', 'juzgar', 'Regular'),('jump', 'jumped', 'jumped', 'saltar', 'Regular'),
            ('kick', 'kicked', 'kicked', 'patear', 'Regular'),('kill', 'killed', 'killed', 'matar', 'Regular'),
            ('kiss', 'kissed', 'kissed', 'besar', 'Regular'),('knock', 'knocked', 'knocked', 'golpear', 'Regular'),
            ('land', 'landed', 'landed', 'aterrizar', 'Regular'),('last', 'lasted', 'lasted', 'durar', 'Regular'),
            ('laugh', 'laughed', 'laughed', 'reír', 'Regular'),('learn', 'learned', 'learned', 'aprender', 'Regular'),
            ('like', 'liked', 'liked', 'gustar', 'Regular'),('limit', 'limited', 'limited', 'limitar', 'Regular'),
            ('listen', 'listened', 'listened', 'escuchar', 'Regular'),('live', 'lived', 'lived', 'vivir', 'Regular'),
            ('lock', 'locked', 'locked', 'cerrar con llave', 'Regular'),('look', 'looked', 'looked', 'mirar', 'Regular'),
            ('love', 'loved', 'loved', 'amar', 'Regular'),('manage', 'managed', 'managed', 'manejar', 'Regular'),
            ('mark', 'marked', 'marked', 'marcar', 'Regular'),('marry', 'married', 'married', 'casarse', 'Regular'),
            ('matter', 'mattered', 'mattered', 'importar', 'Regular'),('measure', 'measured', 'measured', 'medir', 'Regular'),
            ('mention', 'mentioned', 'mentioned', 'mencionar', 'Regular'),('miss', 'missed', 'missed', 'extrañar', 'Regular'),
            ('mix', 'mixed', 'mixed', 'mezclar', 'Regular'),('move', 'moved', 'moved', 'mover', 'Regular'),
            ('name', 'named', 'named', 'nombrar', 'Regular'),('need', 'needed', 'needed', 'necesitar', 'Regular'),
            ('note', 'noted', 'noted', 'notar', 'Regular'),('notice', 'noticed', 'noticed', 'notar', 'Regular'),
            ('obtain', 'obtained', 'obtained', 'obtener', 'Regular'),('occur', 'occurred', 'occurred', 'ocurrir', 'Regular'),
            ('offer', 'offered', 'offered', 'ofrecer', 'Regular'),('open', 'opened', 'opened', 'abrir', 'Regular'),
            ('operate', 'operated', 'operated', 'operar', 'Regular'),('order', 'ordered', 'ordered', 'ordenar', 'Regular'),
            ('organize', 'organized', 'organized', 'organizar', 'Regular'),('own', 'owned', 'owned', 'poseer', 'Regular'),
            ('pack', 'packed', 'packed', 'empacar', 'Regular'),('paint', 'painted', 'painted', 'pintar', 'Regular'),
            ('park', 'parked', 'parked', 'estacionar', 'Regular'),('pass', 'passed', 'passed', 'pasar', 'Regular'),
            ('perform', 'performed', 'performed', 'realizar', 'Regular'),('pick', 'picked', 'picked', 'recoger', 'Regular'),
            ('place', 'placed', 'placed', 'colocar', 'Regular'),('plan', 'planned', 'planned', 'planear', 'Regular'),
            ('plant', 'planted', 'planted', 'plantar', 'Regular'),('play', 'played', 'played', 'jugar', 'Regular'),
            ('please', 'pleased', 'pleased', 'complacer', 'Regular'),('point', 'pointed', 'pointed', 'señalar', 'Regular'),
            ('practice', 'practiced', 'practiced', 'practicar', 'Regular'),('pray', 'prayed', 'prayed', 'rezar', 'Regular'),
            ('prefer', 'preferred', 'preferred', 'preferir', 'Regular'),('prepare', 'prepared', 'prepared', 'preparar', 'Regular'),
            ('present', 'presented', 'presented', 'presentar', 'Regular'),('press', 'pressed', 'pressed', 'presionar', 'Regular'),
            ('prevent', 'prevented', 'prevented', 'prevenir', 'Regular'),('print', 'printed', 'printed', 'imprimir', 'Regular'),
            ('produce', 'produced', 'produced', 'producir', 'Regular'),('program', 'programmed', 'programmed', 'programar', 'Regular'),
            ('promise', 'promised', 'promised', 'prometer', 'Regular'),('protect', 'protected', 'protected', 'proteger', 'Regular'),
            ('prove', 'proved', 'proved', 'probar', 'Regular'),('provide', 'provided', 'provided', 'proveer', 'Regular'),
            ('pull', 'pulled', 'pulled', 'jalar', 'Regular'),('push', 'pushed', 'pushed', 'empujar', 'Regular'),
            ('raise', 'raised', 'raised', 'levantar', 'Regular'),('rain', 'rained', 'rained', 'llover', 'Regular'),
            ('reach', 'reached', 'reached', 'alcanzar', 'Regular'),('realize', 'realized', 'realized', 'darse cuenta', 'Regular'),
            ('receive', 'received', 'received', 'recibir', 'Regular'),('recognize', 'recognized', 'recognized', 'reconocer', 'Regular'),
            ('record', 'recorded', 'recorded', 'grabar', 'Regular'),('reduce', 'reduced', 'reduced', 'reducir', 'Regular'),
            ('refer', 'referred', 'referred', 'referir', 'Regular'),('reflect', 'reflected', 'reflected', 'reflejar', 'Regular'),
            ('refuse', 'refused', 'refused', 'rechazar', 'Regular'),('regard', 'regarded', 'regarded', 'considerar', 'Regular'),
            ('relate', 'related', 'related', 'relacionar', 'Regular'),('relax', 'relaxed', 'relaxed', 'relajar', 'Regular'),
            ('remain', 'remained', 'remained', 'permanecer', 'Regular'),('remember', 'remembered', 'remembered', 'recordar', 'Regular'),
            ('remove', 'removed', 'removed', 'remover', 'Regular'),('repair', 'repaired', 'repaired', 'reparar', 'Regular'),
            ('repeat', 'repeated', 'repeated', 'repetir', 'Regular'),('replace', 'replaced', 'replaced', 'reemplazar', 'Regular'),
            ('reply', 'replied', 'replied', 'responder', 'Regular'),('report', 'reported', 'reported', 'reportar', 'Regular'),
            ('represent', 'represented', 'represented', 'representar', 'Regular'),('require', 'required', 'required', 'requerir', 'Regular'),
            ('rest', 'rested', 'rested', 'descansar', 'Regular'),('result', 'resulted', 'resulted', 'resultar', 'Regular'),
            ('return', 'returned', 'returned', 'regresar', 'Regular'),('reveal', 'revealed', 'revealed', 'revelar', 'Regular'),
            ('roll', 'rolled', 'rolled', 'rodar', 'Regular'),('rule', 'ruled', 'ruled', 'gobernar', 'Regular'),
            ('save', 'saved', 'saved', 'guardar', 'Regular'),('search', 'searched', 'searched', 'buscar', 'Regular'),
            ('seem', 'seemed', 'seemed', 'parecer', 'Regular'),('select', 'selected', 'selected', 'seleccionar', 'Regular'),
            ('serve', 'served', 'served', 'servir', 'Regular'),('settle', 'settled', 'settled', 'establecerse', 'Regular'),
            ('share', 'shared', 'shared', 'compartir', 'Regular'),('shout', 'shouted', 'shouted', 'gritar', 'Regular'),
            ('show', 'showed', 'showed', 'mostrar', 'Regular'),('sign', 'signed', 'signed', 'firmar', 'Regular'),
            ('smile', 'smiled', 'smiled', 'sonreír', 'Regular'),('smoke', 'smoked', 'smoked', 'fumar', 'Regular'),
            ('snow', 'snowed', 'snowed', 'nevar', 'Regular'),('sound', 'sounded', 'sounded', 'sonar', 'Regular'),
            ('start', 'started', 'started', 'empezar', 'Regular'),('state', 'stated', 'stated', 'declarar', 'Regular'),
            ('stay', 'stayed', 'stayed', 'quedarse', 'Regular'),('step', 'stepped', 'stepped', 'pisar', 'Regular'),
            ('stop', 'stopped', 'stopped', 'parar', 'Regular'),('store', 'stored', 'stored', 'almacenar', 'Regular'),
            ('study', 'studied', 'studied', 'estudiar', 'Regular'),('succeed', 'succeeded', 'succeeded', 'tener éxito', 'Regular'),
            ('suffer', 'suffered', 'suffered', 'sufrir', 'Regular'),('suggest', 'suggested', 'suggested', 'sugerir', 'Regular'),
            ('suit', 'suited', 'suited', 'convenir', 'Regular'),('supply', 'supplied', 'supplied', 'suministrar', 'Regular'),
            ('support', 'supported', 'supported', 'apoyar', 'Regular'),('suppose', 'supposed', 'supposed', 'suponer', 'Regular'),
            ('surprise', 'surprised', 'surprised', 'sorprender', 'Regular'),('talk', 'talked', 'talked', 'hablar', 'Regular'),
            ('taste', 'tasted', 'tasted', 'probar', 'Regular'),('thank', 'thanked', 'thanked', 'agradecer', 'Regular'),
            ('touch', 'touched', 'touched', 'tocar', 'Regular'),('train', 'trained', 'trained', 'entrenar', 'Regular'),
            ('travel', 'travelled', 'travelled', 'viajar', 'Regular'),('treat', 'treated', 'treated', 'tratar', 'Regular'),
            ('trust', 'trusted', 'trusted', 'confiar', 'Regular'),('try', 'tried', 'tried', 'intentar', 'Regular'),
            ('turn', 'turned', 'turned', 'girar', 'Regular'),('type', 'typed', 'typed', 'escribir a máquina', 'Regular'),
            ('use', 'used', 'used', 'usar', 'Regular'),('visit', 'visited', 'visited', 'visitar', 'Regular'),
            ('vote', 'voted', 'voted', 'votar', 'Regular'),('wait', 'waited', 'waited', 'esperar', 'Regular'),
            ('walk', 'walked', 'walked', 'caminar', 'Regular'),('want', 'wanted', 'wanted', 'querer', 'Regular'),
            ('warn', 'warned', 'warned', 'advertir', 'Regular'),('wash', 'washed', 'washed', 'lavar', 'Regular'),
            ('waste', 'wasted', 'wasted', 'desperdiciar', 'Regular'),('watch', 'watched', 'watched', 'ver', 'Regular'),
            ('welcome', 'welcomed', 'welcomed', 'dar la bienvenida', 'Regular'),('wish', 'wished', 'wished', 'desear', 'Regular'),
            ('wonder', 'wondered', 'wondered', 'preguntarse', 'Regular'),('work', 'worked', 'worked', 'trabajar', 'Regular'),
            ('worry', 'worried', 'worried', 'preocuparse', 'Regular'),('yell', 'yelled', 'yelled', 'gritar', 'Regular')
        ]
        self.mostrar_todos_verbos()
    
    def mostrar_todos_verbos(self):
        for item in self.tree_verbos.get_children():
            self.tree_verbos.delete(item)
        for infinitivo, pasado, participio, espanol, tipo in self.todos_verbos:
            self.tree_verbos.insert('', 'end', values=(infinitivo, pasado, participio, espanol, tipo))
    
    def _on_search_verbos_keyrelease(self, event):
        if self._search_verbos_timer:
            self.root.after_cancel(self._search_verbos_timer)
        self._search_verbos_timer = self.root.after(300, self.buscar_verbos)
    
    def buscar_verbos(self):
        busqueda = self.entry_buscar_verbos.get().strip().lower()
        for item in self.tree_verbos.get_children():
            self.tree_verbos.delete(item)
        if not busqueda:
            self.mostrar_todos_verbos()
            return
        for infinitivo, pasado, participio, espanol, tipo in self.todos_verbos:
            if (busqueda in infinitivo.lower() or busqueda in pasado.lower() or 
                busqueda in participio.lower() or busqueda in espanol.lower() or busqueda in tipo.lower()):
                self.tree_verbos.insert('', 'end', values=(infinitivo, pasado, participio, espanol, tipo))
    
    def pronunciar_verbo_seleccionado(self):
        seleccion = self.tree_verbos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un verbo")
            return
        item = self.tree_verbos.item(seleccion[0])
        palabra = item['values'][0]
        self.pronunciar_palabra(palabra)
    
    def crear_pestaña_conjugacion(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⏰")
        canvas = tk.Canvas(frame, bg=COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=COLOR_BG)
        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw", width=1000)
        canvas.configure(yscrollcommand=scrollbar.set)
        def _on_mousewheel_conj(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel_conj))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y", pady=20)
        
        for tiempo, titulo, uso, ejemplos in [
            ('present', '🕒 Simple Present', 'Acciones habituales', [
                ('Afirmativo', 'I/You/We/They work', 'He/She/It works'),
                ('Negativo', "don't work", "doesn't work"),
                ('Interrogativo', 'Do...work?', 'Does...work?')
            ]),
            ('continuous', '🔄 Present Continuous', 'Acciones en progreso', [
                ('Afirmativo', 'I am | You/We/They are | He/She/It is working', ''),
                ('Negativo', "I'm not | aren't | isn't working", ''),
                ('Interrogativo', 'Am I? | Are you? | Is he? working', '')
            ]),
            ('past', '⏪ Simple Past', 'Acciones completadas', [
                ('Afirmativo', 'I/You/He/She/It/We/They worked', ''),
                ('Negativo', "didn't work", ''),
                ('Interrogativo', 'Did...work?', '')
            ]),
            ('perfect', '✅ Present Perfect', 'Pasado con relevancia', [
                ('Afirmativo', 'I/You/We/They have | He/She/It has worked', ''),
                ('Negativo', "haven't | hasn't worked", ''),
                ('Interrogativo', 'Have...? | Has...? worked', '')
            ]),
            ('future', '⏩ Future Simple', 'Acciones futuras', [
                ('Afirmativo', 'I/You/He/She/It/We/They will work', ''),
                ('Negativo', "won't work", ''),
                ('Interrogativo', 'Will...work?', '')
            ])
        ]:
            f = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
            f.pack(fill='x', padx=20, pady=(0,20), ipady=15)
            ttk.Label(f, text=titulo, font=(FONT_FAMILY, 16, 'bold'), foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,5))
            tk.Label(f, text=f"Uso: {uso}", font=(FONT_FAMILY, 11), bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=5)
            for tipo, forma1, forma2 in ejemplos:
                item = tk.Frame(f, bg=COLOR_BG, relief='solid', borderwidth=1)
                item.pack(fill='x', padx=20, pady=5)
                tk.Label(item, text=tipo, font=(FONT_FAMILY, 11, 'bold'), bg=COLOR_BG, fg=COLOR_ACCENT, width=15).pack(side='left', padx=10, pady=8)
                tk.Label(item, text=forma1, font=(FONT_FAMILY, 10), bg=COLOR_BG, fg=COLOR_FG, anchor='w').pack(side='left', padx=5)
                if forma2:
                    tk.Label(item, text=forma2, font=(FONT_FAMILY, 10), bg=COLOR_BG, fg=COLOR_FG, anchor='w').pack(side='left', padx=5)
        
        modal_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
        modal_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
        ttk.Label(modal_frame, text="🔑 Modal Verbs", font=(FONT_FAMILY, 16, 'bold'), foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,15))
        for modal, sig, ej in [('can','poder','I can swim'),('could','podría','I could help'),('may','permiso','May I?'),
                               ('might','posibilidad','It might rain'),('must','obligación','You must study'),
                               ('should','consejo','You should rest'),('would','condicional','I would like'),('will','futuro','I will go')]:
            item = tk.Frame(modal_frame, bg=COLOR_BG, relief='solid', borderwidth=1)
            item.pack(fill='x', padx=20, pady=3)
            tk.Label(item, text=modal, font=(FONT_FAMILY, 11, 'bold'), bg=COLOR_BG, fg=COLOR_ACCENT, width=10, anchor='w').pack(side='left', padx=10, pady=5)
            tk.Label(item, text=sig, font=(FONT_FAMILY, 10), bg=COLOR_BG, fg=COLOR_FG, width=20, anchor='w').pack(side='left', padx=5)
            tk.Label(item, text=f"Ej: {ej}", font=(FONT_FAMILY, 9, 'italic'), bg=COLOR_BG, fg=COLOR_BUTTON_HOVER, anchor='w').pack(side='left', padx=5)
    
    def crear_pestaña_estadisticas(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊")
        
        self.container_stats = tk.Frame(frame, bg=COLOR_BG)
        self.container_stats.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Label(self.container_stats, text="📊 Estadísticas del Vocabulario", 
                 font=(FONT_FAMILY, 20, 'bold'), foreground=COLOR_ACCENT, 
                 background=COLOR_BG).pack(pady=(0,30))
        
        self.stats_frame = tk.Frame(self.container_stats, bg=COLOR_BG)
        self.stats_frame.pack()
        
        ttk.Button(self.container_stats, text="🔄 Actualizar", command=self.actualizar_estadisticas).pack(pady=20)
        
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
            ("📝 Con notas", con_notas, COLOR_FG),
            ("💾 Backups guardados", self.contar_backups(), COLOR_ACCENT)
        ]
        
        for texto, valor, color in stats:
            frame_stat = tk.Frame(self.stats_frame, bg=COLOR_BG)
            frame_stat.pack(fill='x', pady=10)
            
            tk.Label(frame_stat, text=texto, font=(FONT_FAMILY, 14), 
                    bg=COLOR_BG, fg=COLOR_FG).pack(side='left', padx=20)
            tk.Label(frame_stat, text=str(valor), font=(FONT_FAMILY, 24, 'bold'), 
                    bg=COLOR_BG, fg=color).pack(side='right', padx=20)
        
        # Botones de exportar/importar
        btn_frame = tk.Frame(self.container_stats, bg=COLOR_BG)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="📤 Exportar CSV", command=self.exportar_csv).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📥 Importar CSV", command=self.importar_csv).pack(side='left', padx=5)
    
    def contar_backups(self):
        try:
            backup_dir = APP_DIR / 'backups'
            if backup_dir.exists():
                return len(list(backup_dir.glob('palabras_backup_*.json')))
        except:
            pass
        return 0
    
    def crear_pestaña_caligrafia(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="✍️")
        
        self.indice_caligrafia = 0
        
        # Frame superior
        frame_top = tk.Frame(frame, bg=COLOR_BG)
        frame_top.pack(fill='x', padx=30, pady=20)
        
        ttk.Label(frame_top, text="✍️ Práctica de Caligrafía", 
                 font=(FONT_FAMILY, 18, 'bold'), foreground=COLOR_ACCENT, 
                 background=COLOR_BG).pack(pady=(0,10))
        
        # Selector de modo
        modo_frame = tk.Frame(frame_top, bg=COLOR_BG)
        modo_frame.pack(pady=10)
        
        self.modo_caligrafia = tk.StringVar(value='erroneas')
        tk.Radiobutton(modo_frame, text="Palabras Erróneas", variable=self.modo_caligrafia,
                      value='erroneas', bg=COLOR_BG, fg=COLOR_FG, selectcolor=COLOR_BUTTON,
                      font=(FONT_FAMILY, 10), command=self.cargar_palabras_caligrafia).pack(side='left', padx=10)
        tk.Radiobutton(modo_frame, text="Todo el Vocabulario", variable=self.modo_caligrafia,
                      value='todas', bg=COLOR_BG, fg=COLOR_FG, selectcolor=COLOR_BUTTON,
                      font=(FONT_FAMILY, 10), command=self.cargar_palabras_caligrafia).pack(side='left', padx=10)
        
        self.label_info_caligrafia = tk.Label(frame_top, text="", font=(FONT_FAMILY, 11), 
                                              bg=COLOR_BG, fg=COLOR_FG)
        self.label_info_caligrafia.pack(pady=5)
        
        # Canvas con scroll
        canvas_cal = tk.Canvas(frame, bg=COLOR_BG, highlightthickness=0)
        self.frame_caligrafia_content = tk.Frame(canvas_cal, bg=COLOR_BG)
        
        self.frame_caligrafia_content.bind(
            "<Configure>",
            lambda e: canvas_cal.configure(scrollregion=canvas_cal.bbox("all"))
        )
        
        canvas_cal.create_window((0, 0), window=self.frame_caligrafia_content, anchor="nw", width=1100)
        
        def _on_mousewheel_cal(event):
            canvas_cal.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas_cal.bind("<Enter>", lambda e: canvas_cal.bind_all("<MouseWheel>", _on_mousewheel_cal))
        canvas_cal.bind("<Leave>", lambda e: canvas_cal.unbind_all("<MouseWheel>"))
        
        canvas_cal.pack(fill="both", expand=True, padx=30, pady=(0,10))
        
        # Botones de navegación
        btn_frame = tk.Frame(frame, bg=COLOR_BG)
        btn_frame.pack(pady=(0,20))
        
        ttk.Button(btn_frame, text="◀ Anterior", command=self.palabra_anterior_caligrafia).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_palabras_caligrafia).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Siguiente ▶", command=self.palabra_siguiente_caligrafia).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔊 Pronunciar", command=self.pronunciar_palabra_caligrafia).pack(side='left', padx=5)
        
        self.cargar_palabras_caligrafia()
    
    def cargar_palabras_caligrafia(self):
        modo = self.modo_caligrafia.get() if hasattr(self, 'modo_caligrafia') else 'erroneas'
        
        if modo == 'erroneas':
            # Solo palabras erróneas de práctica
            if hasattr(self, 'palabras_erroneas') and self.palabras_erroneas:
                self.lista_caligrafia = sorted(list(self.palabras_erroneas), key=str.lower)
            else:
                self.lista_caligrafia = []
        else:
            # Todo el vocabulario
            self.lista_caligrafia = sorted(list(self.datos.keys()), key=str.lower)
        
        self.indice_caligrafia = 0
        self.actualizar_caligrafia()
    
    def actualizar_caligrafia(self):
        # Limpiar contenido anterior
        for widget in self.frame_caligrafia_content.winfo_children():
            widget.destroy()
        
        if not self.lista_caligrafia:
            modo = self.modo_caligrafia.get() if hasattr(self, 'modo_caligrafia') else 'erroneas'
            if modo == 'erroneas':
                mensaje = "🎯 No hay palabras erróneas aún\n\n¡Practica en la pestaña Práctica para generar palabras!"
            else:
                mensaje = "📚 No hay palabras en el vocabulario\n\n¡Agrega palabras en la pestaña Vocabulario!"
            
            tk.Label(self.frame_caligrafia_content, text=mensaje,
                    font=(FONT_FAMILY, 14), bg=COLOR_BG, fg=COLOR_FG, 
                    justify='center').pack(expand=True, pady=100)
            self.label_info_caligrafia.config(text="")
            return
        
        palabra = self.lista_caligrafia[self.indice_caligrafia]
        significado = self.datos[palabra].get('significado', '')
        pronunciacion = self.datos[palabra].get('pronunciacion', '')
        
        # Info superior
        modo = self.modo_caligrafia.get() if hasattr(self, 'modo_caligrafia') else 'erroneas'
        if modo == 'erroneas':
            info_texto = f"Palabra {self.indice_caligrafia + 1} de {len(self.lista_caligrafia)} | Total erróneas: {len(self.palabras_erroneas)}"
        else:
            info_texto = f"Palabra {self.indice_caligrafia + 1} de {len(self.lista_caligrafia)} | Total vocabulario: {len(self.datos)}"
        
        self.label_info_caligrafia.config(text=info_texto)
        
        # Tarjeta de palabra
        card_frame = tk.Frame(self.frame_caligrafia_content, bg=COLOR_BUTTON, relief='solid', borderwidth=2)
        card_frame.pack(fill='x', pady=(0,30), padx=50, ipady=20)
        
        tk.Label(card_frame, text=palabra, font=(FONT_FAMILY, 32, 'bold'), 
                bg=COLOR_BUTTON, fg=COLOR_ACCENT).pack(pady=(10,5))
        tk.Label(card_frame, text=significado, font=(FONT_FAMILY, 16), 
                bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=5)
        if pronunciacion:
            tk.Label(card_frame, text=f"🔊 {pronunciacion}", font=(FONT_FAMILY, 13), 
                    bg=COLOR_BUTTON, fg=COLOR_BUTTON_HOVER).pack(pady=(5,10))
        
        # Modelo de repetición espaciada
        practice_frame = tk.Frame(self.frame_caligrafia_content, bg=COLOR_BG)
        practice_frame.pack(fill='both', expand=True, padx=50)
        
        # Inglés
        tk.Label(practice_frame, text="🇬🇧 Inglés:", font=(FONT_FAMILY, 13, 'bold'), 
                bg=COLOR_BG, fg=COLOR_ACCENT, anchor='w').pack(fill='x', pady=(10,5))
        
        self.crear_linea_practica(practice_frame, "1. Copia:", palabra, True)
        self.crear_linea_practica(practice_frame, "2. Con guía:", palabra, False, True)
        self.crear_linea_practica(practice_frame, "3. De memoria:", palabra, False, False)
        
        # Español
        tk.Label(practice_frame, text="\n🇪🇸 Español:", font=(FONT_FAMILY, 13, 'bold'), 
                bg=COLOR_BG, fg=COLOR_ACCENT, anchor='w').pack(fill='x', pady=(15,5))
        
        self.crear_linea_practica(practice_frame, "4. Copia:", significado, True)
        self.crear_linea_practica(practice_frame, "5. Con guía:", significado, False, True)
        self.crear_linea_practica(practice_frame, "6. De memoria:", significado, False, False)
        
        # Oración de contexto
        tk.Label(practice_frame, text="\n📝 Oración:", 
                font=(FONT_FAMILY, 13, 'bold'), bg=COLOR_BG, fg=COLOR_ACCENT, 
                anchor='w').pack(fill='x', pady=(20,5))
        
        tk.Label(practice_frame, text="7. Usa en una oración:", 
                font=(FONT_FAMILY, 11, 'bold'), bg=COLOR_BG, fg=COLOR_FG, 
                anchor='w').pack(fill='x', pady=(5,5))
        
        oracion = self.generar_oracion_simple(palabra, significado)
        tk.Label(practice_frame, text=oracion, font=(FONT_FAMILY, 11, 'italic'), 
                bg=COLOR_BG, fg=COLOR_FG, anchor='w').pack(fill='x', padx=20)
        
        # Campo de texto para la oración
        entry_oracion = ttk.Entry(practice_frame, font=(FONT_FAMILY, 14), width=60)
        entry_oracion.pack(fill='x', pady=10, ipady=10)
    
    def crear_linea_practica(self, parent, titulo, palabra, mostrar_palabra, mostrar_guia=False):
        container = tk.Frame(parent, bg=COLOR_BG)
        container.pack(fill='x', pady=8)
        
        tk.Label(container, text=titulo, font=(FONT_FAMILY, 11, 'bold'), 
                bg=COLOR_BG, fg=COLOR_ACCENT, width=25, anchor='w').pack(side='left')
        
        if mostrar_palabra:
            line_frame = tk.Frame(container, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
            line_frame.pack(side='left', fill='x', expand=True, ipady=10)
            tk.Label(line_frame, text=palabra, font=(FONT_FAMILY, 18, 'bold'), 
                    bg=COLOR_BUTTON, fg=COLOR_BUTTON_HOVER, anchor='w').pack(side='left', padx=20)
        elif mostrar_guia:
            entry = ttk.Entry(container, font=(FONT_FAMILY, 16), width=40)
            entry.pack(side='left', fill='x', expand=True, ipady=8)
            guia = ' '.join(['_' for _ in palabra])
            entry.insert(0, guia)
        else:
            entry = ttk.Entry(container, font=(FONT_FAMILY, 16), width=40)
            entry.pack(side='left', fill='x', expand=True, ipady=8)
    
    def generar_oracion_simple(self, palabra, significado):
        plantillas = [
            f"I need to practice {palabra} more.",
            f"The word {palabra} means {significado}.",
            f"Can you use {palabra} in a sentence?",
            f"I will remember {palabra} now.",
            f"This {palabra} is important to learn."
        ]
        return random.choice(plantillas)
    
    def palabra_anterior_caligrafia(self):
        if self.lista_caligrafia and self.indice_caligrafia > 0:
            self.indice_caligrafia -= 1
            self.actualizar_caligrafia()
    
    def palabra_siguiente_caligrafia(self):
        if self.lista_caligrafia and self.indice_caligrafia < len(self.lista_caligrafia) - 1:
            self.indice_caligrafia += 1
            self.actualizar_caligrafia()
    
    def pronunciar_palabra_caligrafia(self):
        if self.lista_caligrafia and hasattr(self, 'indice_caligrafia'):
            palabra = self.lista_caligrafia[self.indice_caligrafia]
            self.pronunciar_palabra(palabra)
    

    
    def editar_palabra(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una palabra de la tabla")
            return
        
        item = self.tree.item(seleccion[0])
        palabra_actual = str(item['values'][0])
        significado_actual = str(item['values'][1])
        pronunciacion_actual = '' if item['values'][2] == '-' else str(item['values'][2])
        notas_actual = '' if len(item['values']) < 4 or item['values'][3] == '-' else str(item['values'][3])
        
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
        
        ttk.Label(container, text="🔊 Pronunciación (opcional)", style='Title.TLabel').pack(pady=(0,5))
        entry_pronunciacion = ttk.Entry(container, width=45, font=(FONT_FAMILY, 11))
        entry_pronunciacion.insert(0, pronunciacion_actual)
        entry_pronunciacion.pack(pady=(0,15), ipady=8)
        
        ttk.Label(container, text="📝 Notas (opcional)", style='Title.TLabel').pack(pady=(0,5))
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
    


    def crear_pestaña_ayuda(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="❓")
        
        # Canvas con scroll
        canvas = tk.Canvas(frame, bg=COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=COLOR_BG)
        
        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw", width=1000)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel_ayuda(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel_ayuda))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        
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
            ("📚 Vocabulario", "Agrega, edita y elimina palabras. Usa la búsqueda para encontrar rápidamente. Doble clic para editar. Puedes agregar pronunciación y notas."),
            ("🎯 Práctica", "Modo quiz para practicar. Elige entre Inglés→Español o Español→Inglés. Usa TTS para escuchar la pronunciación."),
            ("✍️ Caligrafía", "Practica escribiendo palabras erróneas o todo el vocabulario. Método de repetición espaciada con oraciones de ejemplo."),
            ("📍 Preposiciones", "Consulta 47 preposiciones en inglés con sus traducciones y ejemplos de uso."),
            ("📅 Días/Meses", "Días de la semana, meses del año y 58 términos relacionados con tiempo."),
            ("🔢 Números", "Conversor de números a texto en inglés + reglas importantes sobre ordinales, decimales y fracciones."),
            ("📝 Gramática", "Pronombres personales, posesivos y reflexivos. Verbos auxiliares, artículos, demostrativos y cuantificadores."),
            ("🔗 Contracciones", "93 contracciones en inglés: formales (I'm, you're) e informales (gonna, wanna). Con palabras originales y traducción."),
            ("📘 Verbos", "368 verbos en inglés (124 irregulares + 239 regulares + 5 modales) con infinitivo, pasado, participio y tipo."),
            ("⏰ Conjugación", "6 tiempos verbales (Present, Past, Perfect, Future, Continuous) + Modal Verbs con ejemplos."),
            ("📊 Estadísticas", "Métricas de tu vocabulario: total de palabras, pronunciaciones, notas y backups. Exporta/Importa CSV desde aquí."),
            ("💾 Respaldos", "Backup automático cada 5 minutos. Tus datos están en " + str(APP_DIR) + ". Copia esta carpeta para hacer respaldo manual.")
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
        
        tk.Label(about_frame, text="Versión: 1.3.2", font=(FONT_FAMILY, 11), 
                bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=2)
        tk.Label(about_frame, text="Desarrollado por: Agilize Soluciones", font=(FONT_FAMILY, 11), 
                bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=2)
        tk.Label(about_frame, text="Aplicación educativa para aprendizaje de inglés", font=(FONT_FAMILY, 10), 
                bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=2)
        
        # Nuevas características v1.3.2
        tk.Label(about_frame, text="\n✨ Novedades v1.3.2:", font=(FONT_FAMILY, 11, 'bold'), 
                bg=COLOR_BUTTON, fg=COLOR_ACCENT).pack(pady=(10,5))
        
        novedades = [
            "• 368 verbos totales (124 irregulares + 239 regulares + 5 modales)",
            "• Verbo modal CAN y otros modales agregados",
            "• Más de 200 verbos regulares nuevos",
            "• 68 verbos irregulares adicionales",
            "• Backup automático cada 5 minutos",
            "• Pronunciación TTS integrada"
        ]
        
        for novedad in novedades:
            tk.Label(about_frame, text=novedad, font=(FONT_FAMILY, 9), 
                    bg=COLOR_BUTTON, fg=COLOR_FG, anchor='w').pack(padx=30, anchor='w')
        
        tk.Label(about_frame, text="", bg=COLOR_BUTTON).pack(pady=5)

if __name__ == '__main__':
    root = tk.Tk()
    app = DiccionarioApp(root)
    root.mainloop()
