"""English Memory v1.4.0 - Versión Modular"""
import tkinter as tk
from src.models import HybridStorage
from src.controllers import VocabularioController, PracticaController
from src.utils import AppConfig, TTSHelper
from src.views import MainWindow, VocabularioView, PracticaView, GenericTableView
from src.data import PREPOSICIONES, DIAS_MESES, CONTRACCIONES, TODOS_VERBOS

def main():
    # Inicializar
    storage = HybridStorage(AppConfig.APP_DIR)
    vocab_controller = VocabularioController(storage)
    practica_controller = PracticaController(storage)
    tts = TTSHelper()
    
    # Ventana principal
    root = tk.Tk()
    main_window = MainWindow(root, storage, vocab_controller, practica_controller, tts)
    
    # Tab 1: Vocabulario
    vocab_view = VocabularioView(main_window.notebook, vocab_controller, tts)
    main_window.agregar_tab(vocab_view, "📖")
    
    # Tab 2: Práctica
    practica_view = PracticaView(main_window.notebook, practica_controller, tts)
    main_window.agregar_tab(practica_view, "🎯")
    
    # Tab 3: Preposiciones
    prep_data = [(k, v) for k, v in sorted(PREPOSICIONES.items())]
    prep_view = GenericTableView(main_window.notebook, "Preposiciones", 
                                  ('🇬🇧 Preposición', '🇪🇸 Traducción'), prep_data, tts)
    main_window.agregar_tab(prep_view, "📍")
    
    # Tab 4: Días/Meses
    dias_view = GenericTableView(main_window.notebook, "Días/Meses", 
                                  ('🇬🇧 Inglés', '🇪🇸 Español', '📂 Categoría'), DIAS_MESES, tts)
    main_window.agregar_tab(dias_view, "📅")
    
    # Tab 5: Contracciones
    contr_view = GenericTableView(main_window.notebook, "Contracciones", 
                                   ('Contracción', 'Original', 'Español'), CONTRACCIONES)
    main_window.agregar_tab(contr_view, "🔗")
    
    # Tab 6: Verbos
    verbos_data = [(v[0], v[1], v[2], v[3]) for v in TODOS_VERBOS]
    verbos_view = GenericTableView(main_window.notebook, "Verbos", 
                                    ('Infinitivo', 'Pasado', 'Participio', 'Español'), verbos_data)
    main_window.agregar_tab(verbos_view, "📘")
    
    # TODO: Tabs restantes (Caligrafía, Números, Gramática, Conjugación, Estadísticas, Ayuda)
    
    root.mainloop()

if __name__ == '__main__':
    main()
