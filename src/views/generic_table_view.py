"""Generic Table View - Para tabs con tablas simples"""
import tkinter as tk
from tkinter import ttk, messagebox
from src.utils import AppConfig

class GenericTableView(ttk.Frame):
    def __init__(self, parent, title, columns, data, tts=None):
        super().__init__(parent)
        self.title = title
        self.columns = columns
        self.data = data
        self.tts = tts
        
        self.crear_ui()
        self.cargar_datos()
    
    def crear_ui(self):
        # Búsqueda
        frame_buscar = ttk.Frame(self)
        frame_buscar.pack(fill='x', padx=20, pady=15)
        
        ttk.Label(frame_buscar, text="🔍", font=(AppConfig.FONT_FAMILY, 14)).pack(side='left', padx=(0,5))
        self.entry_buscar = ttk.Entry(frame_buscar, width=30, font=(AppConfig.FONT_FAMILY, 11))
        self.entry_buscar.pack(side='left', padx=5, ipady=5)
        self.entry_buscar.bind('<KeyRelease>', lambda e: self.buscar())
        
        if self.tts:
            ttk.Button(frame_buscar, text="🔊 Pronunciar", command=self.pronunciar).pack(side='left', padx=5)
        
        # Tabla
        self.tree = ttk.Treeview(self, columns=self.columns, show='headings', height=20)
        
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=300)
        
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=(20,0), pady=(0,20))
        scrollbar.pack(side='right', fill='y', pady=(0,20), padx=(0,20))
    
    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for row in self.data:
            self.tree.insert('', 'end', values=row)
    
    def buscar(self):
        query = self.entry_buscar.get().strip().lower()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not query:
            self.cargar_datos()
            return
        
        for row in self.data:
            if any(query in str(val).lower() for val in row):
                self.tree.insert('', 'end', values=row)
    
    def pronunciar(self):
        if not self.tts or not self.tts.esta_disponible():
            messagebox.showinfo("TTS no disponible", "Instala pyttsx3")
            return
        
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un elemento")
            return
        
        item = self.tree.item(seleccion[0])
        palabra = item['values'][0]
        
        try:
            self.tts.pronunciar(palabra)
        except Exception as e:
            messagebox.showerror("Error TTS", str(e))
