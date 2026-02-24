"""
English Memory v1.4.0 - Versión Modular
Punto de entrada con arquitectura MVC
"""
import tkinter as tk
from src.models import HybridStorage
from src.controllers import VocabularioController, PracticaController
from src.utils import AppConfig, TTSHelper
from src.views import MainWindow, VocabularioView

def main():
    """Función principal"""
    # Inicializar storage
    storage = HybridStorage(AppConfig.APP_DIR)
    
    # Inicializar controllers
    vocab_controller = VocabularioController(storage)
    practica_controller = PracticaController(storage)
    
    # Inicializar TTS
    tts = TTSHelper()
    
    # Crear ventana principal
    root = tk.Tk()
    main_window = MainWindow(root, storage, vocab_controller, practica_controller, tts)
    
    # Crear y agregar tabs
    vocab_view = VocabularioView(main_window.notebook, vocab_controller, tts)
    main_window.agregar_tab(vocab_view, "📖")
    
    # TODO: Agregar resto de tabs
    
    root.mainloop()

if __name__ == '__main__':
    main()
