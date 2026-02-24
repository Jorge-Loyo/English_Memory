"""Vocabulario View - Tab de gestión de vocabulario"""
import tkinter as tk
from tkinter import ttk, messagebox
from src.utils import AppConfig

class VocabularioView(ttk.Frame):
    def __init__(self, parent, vocab_controller, tts):
        super().__init__(parent)
        self.vocab_controller = vocab_controller
        self.tts = tts
        self.configure(style='TFrame')
        
        self.crear_ui()
        self.cargar_datos()
    
    def crear_ui(self):
        """Crear interfaz"""
        # Búsqueda y acciones
        frame_top = ttk.Frame(self)
        frame_top.pack(fill='x', padx=20, pady=15)
        
        # Botones de acción
        frame_acciones = tk.Frame(frame_top, bg=AppConfig.COLOR_BG)
        frame_acciones.pack(side='left')
        
        ttk.Button(frame_acciones, text="➕ Agregar", 
                  command=self.agregar_palabra).pack(side='left', padx=2)
        ttk.Button(frame_acciones, text="✏️ Editar", 
                  command=self.editar_palabra).pack(side='left', padx=2)
        ttk.Button(frame_acciones, text="🗑️ Eliminar", 
                  command=self.eliminar_palabra).pack(side='left', padx=2)
        ttk.Button(frame_acciones, text="🔊 Pronunciar", 
                  command=self.pronunciar_seleccionada).pack(side='left', padx=2)
        
        # Búsqueda
        frame_search = tk.Frame(frame_top, bg=AppConfig.COLOR_BG)
        frame_search.pack(side='right')
        
        ttk.Button(frame_search, text="📋 Ver Todas", 
                  command=self.mostrar_todas).pack(side='right', padx=2)
        self.entry_buscar = ttk.Entry(frame_search, width=25, 
                                      font=(AppConfig.FONT_FAMILY, 11))
        self.entry_buscar.pack(side='right', padx=5, ipady=5)
        self.entry_buscar.bind('<KeyRelease>', lambda e: self.buscar())
        
        # Tabla
        columns = ('Inglés', 'Español', 'Pronunciación', 'Notas')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=15)
        
        self.tree.heading('Inglés', text='🇬🇧 Inglés')
        self.tree.heading('Español', text='🇪🇸 Español')
        self.tree.heading('Pronunciación', text='🔊 Pronunciación')
        self.tree.heading('Notas', text='📝 Notas')
        
        self.tree.column('Inglés', width=150)
        self.tree.column('Español', width=250)
        self.tree.column('Pronunciación', width=200)
        self.tree.column('Notas', width=300)
        
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=(20,0), pady=(0,20))
        scrollbar.pack(side='right', fill='y', pady=(0,20), padx=(0,20))
        
        self.tree.bind('<Double-Button-1>', lambda e: self.editar_palabra())
    
    def cargar_datos(self):
        """Cargar datos en la tabla"""
        self.mostrar_todas()
    
    def mostrar_todas(self):
        """Mostrar todas las palabras"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        palabras = self.vocab_controller.obtener_todas()
        for palabra in sorted(palabras.keys(), key=str.lower):
            datos = palabras[palabra]
            self.tree.insert('', 'end', values=(
                palabra,
                datos.get('significado', ''),
                datos.get('pronunciacion', '-'),
                datos.get('notas', '-')
            ))
    
    def buscar(self):
        """Buscar palabras"""
        query = self.entry_buscar.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not query:
            self.mostrar_todas()
            return
        
        resultados = self.vocab_controller.buscar_palabras(query)
        for palabra in sorted(resultados.keys()):
            datos = resultados[palabra]
            self.tree.insert('', 'end', values=(
                palabra,
                datos.get('significado', ''),
                datos.get('pronunciacion', '-'),
                datos.get('notas', '-')
            ))
    
    def agregar_palabra(self):
        """Abrir modal para agregar palabra"""
        ventana = tk.Toplevel(self)
        ventana.title("➕ Agregar Palabra")
        ventana.geometry("550x520")
        ventana.configure(bg=AppConfig.COLOR_BG)
        ventana.grab_set()
        
        container = tk.Frame(ventana, bg=AppConfig.COLOR_BG)
        container.pack(expand=True, fill='both', padx=40, pady=30)
        
        ttk.Label(container, text="🇬🇧 Palabra en inglés").pack(pady=(0,5))
        entry_palabra = ttk.Entry(container, width=45, font=(AppConfig.FONT_FAMILY, 11))
        entry_palabra.pack(pady=(0,15), ipady=8)
        entry_palabra.focus()
        
        ttk.Label(container, text="🇪🇸 Significado en español").pack(pady=(0,5))
        entry_significado = ttk.Entry(container, width=45, font=(AppConfig.FONT_FAMILY, 11))
        entry_significado.pack(pady=(0,15), ipady=8)
        
        ttk.Label(container, text="🔊 Pronunciación (opcional)").pack(pady=(0,5))
        entry_pronunciacion = ttk.Entry(container, width=45, font=(AppConfig.FONT_FAMILY, 11))
        entry_pronunciacion.pack(pady=(0,15), ipady=8)
        
        ttk.Label(container, text="📝 Notas (opcional)").pack(pady=(0,5))
        entry_notas = ttk.Entry(container, width=45, font=(AppConfig.FONT_FAMILY, 11))
        entry_notas.pack(pady=(0,25), ipady=8)
        
        def guardar():
            try:
                self.vocab_controller.agregar_palabra(
                    entry_palabra.get().strip(),
                    entry_significado.get().strip(),
                    entry_pronunciacion.get().strip() or None,
                    entry_notas.get().strip() or None
                )
                messagebox.showinfo("Éxito", "Palabra guardada")
                ventana.destroy()
                self.mostrar_todas()
            except ValueError as e:
                messagebox.showwarning("Advertencia", str(e))
        
        btn_frame = tk.Frame(container, bg=AppConfig.COLOR_BG)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="💾 Guardar", command=guardar).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="❌ Cancelar", command=ventana.destroy).pack(side='left', padx=5)
    
    def editar_palabra(self):
        """Editar palabra seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una palabra")
            return
        
        item = self.tree.item(seleccion[0])
        palabra_actual = item['values'][0]
        
        # Similar a agregar_palabra pero con valores pre-llenados
        messagebox.showinfo("Info", "Función editar en desarrollo")
    
    def eliminar_palabra(self):
        """Eliminar palabra seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una palabra")
            return
        
        item = self.tree.item(seleccion[0])
        palabra = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{palabra}'?"):
            self.vocab_controller.eliminar_palabra(palabra)
            self.mostrar_todas()
    
    def pronunciar_seleccionada(self):
        """Pronunciar palabra seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una palabra")
            return
        
        item = self.tree.item(seleccion[0])
        palabra = item['values'][0]
        
        if not self.tts.esta_disponible():
            messagebox.showinfo("TTS no disponible", 
                              "Instala pyttsx3: pip install pyttsx3")
            return
        
        try:
            self.tts.pronunciar(palabra)
        except Exception as e:
            messagebox.showerror("Error TTS", str(e))
