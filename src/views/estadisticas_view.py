"""Estadísticas View - Métricas del vocabulario"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from src.utils import AppConfig

class EstadisticasView(ttk.Frame):
    def __init__(self, parent, vocab_controller, storage):
        super().__init__(parent)
        self.vocab_controller = vocab_controller
        self.storage = storage
        self.crear_ui()
    
    def crear_ui(self):
        container = tk.Frame(self, bg=AppConfig.COLOR_BG)
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        ttk.Label(container, text="📊 Estadísticas del Vocabulario", 
                 font=(AppConfig.FONT_FAMILY, 20, 'bold'), foreground=AppConfig.COLOR_ACCENT, 
                 background=AppConfig.COLOR_BG).pack(pady=(0,30))
        
        self.stats_frame = tk.Frame(container, bg=AppConfig.COLOR_BG)
        self.stats_frame.pack()
        
        ttk.Button(container, text="🔄 Actualizar", command=self.actualizar).pack(pady=20)
        
        # Botones exportar/importar
        btn_frame = tk.Frame(container, bg=AppConfig.COLOR_BG)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="📤 Exportar CSV", command=self.exportar).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📥 Importar CSV", command=self.importar).pack(side='left', padx=5)
        
        self.actualizar()
    
    def actualizar(self):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        stats = self.vocab_controller.obtener_estadisticas()
        
        datos = [
            ("📚 Total de palabras", stats['total'], AppConfig.COLOR_ACCENT),
            ("🔊 Con pronunciación", stats['con_pronunciacion'], AppConfig.COLOR_SUCCESS),
            ("❌ Sin pronunciación", stats['sin_pronunciacion'], AppConfig.COLOR_ERROR),
            ("📝 Con notas", stats['con_notas'], AppConfig.COLOR_FG)
        ]
        
        for texto, valor, color in datos:
            frame = tk.Frame(self.stats_frame, bg=AppConfig.COLOR_BG)
            frame.pack(fill='x', pady=10)
            
            tk.Label(frame, text=texto, font=(AppConfig.FONT_FAMILY, 14), 
                    bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack(side='left', padx=20)
            tk.Label(frame, text=str(valor), font=(AppConfig.FONT_FAMILY, 24, 'bold'), 
                    bg=AppConfig.COLOR_BG, fg=color).pack(side='right', padx=20)
    
    def exportar(self):
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if archivo:
            try:
                palabras = self.storage.obtener_todas_palabras()
                with open(archivo, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Inglés', 'Español', 'Pronunciación', 'Notas'])
                    for palabra, datos in palabras.items():
                        writer.writerow([
                            palabra,
                            datos.get('significado', ''),
                            datos.get('pronunciacion', ''),
                            datos.get('notas', '')
                        ])
                messagebox.showinfo("Éxito", "Vocabulario exportado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def importar(self):
        archivo = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if archivo:
            try:
                count = 0
                with open(archivo, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        palabra = row.get('Inglés', '').strip()
                        significado = row.get('Español', '').strip()
                        
                        if palabra and significado:
                            try:
                                self.vocab_controller.agregar_palabra(
                                    palabra, significado,
                                    row.get('Pronunciación', '').strip() or None,
                                    row.get('Notas', '').strip() or None
                                )
                                count += 1
                            except:
                                pass
                
                self.actualizar()
                messagebox.showinfo("Éxito", f"{count} palabras importadas correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al importar: {str(e)}")
