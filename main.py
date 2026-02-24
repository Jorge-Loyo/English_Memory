"""
English Memory v1.4.0 - Punto de entrada modular
Aplicación educativa para aprender vocabulario en inglés
"""
import tkinter as tk
from diccionario_gui import DiccionarioApp

def main():
    """Función principal"""
    root = tk.Tk()
    app = DiccionarioApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
