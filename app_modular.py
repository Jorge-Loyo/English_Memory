"""English Memory v1.4.0 - Versión Modular"""
import tkinter as tk
from src.models import HybridStorage
from src.controllers import VocabularioController, PracticaController
from src.utils import AppConfig, TTSHelper, AppStyles
from src.views import (MainWindow, VocabularioView, PracticaView, GenericTableView,
                       CaligrafiaView, NumerosView, GramaticaView, ConjugacionView, EstadisticasView)
from src.data import PREPOSICIONES, DIAS_MESES, CONTRACCIONES, TODOS_VERBOS, VERBOS_FRASALES

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
    main_window.agregar_tab(vocab_view, "📖", "Vocabulario")
    
    # Tab 2: Práctica
    practica_view = PracticaView(main_window.notebook, practica_controller, tts)
    main_window.agregar_tab(practica_view, "🎯", "Práctica")
    
    # Tab 3: Caligrafía
    caligrafia_view = CaligrafiaView(main_window.notebook, storage, practica_controller, tts)
    main_window.agregar_tab(caligrafia_view, "✍️", "Caligrafía")
    
    # Tab 4: Preposiciones
    prep_data = [(k, v) for k, v in sorted(PREPOSICIONES.items())]
    prep_view = GenericTableView(main_window.notebook, "Preposiciones", 
                                  ('🇬🇧 Preposición', '🇪🇸 Traducción'), prep_data, tts)
    main_window.agregar_tab(prep_view, "📍", "Preposiciones")
    
    # Tab 5: Días/Meses
    dias_view = GenericTableView(main_window.notebook, "Días/Meses", 
                                  ('🇬🇧 Inglés', '🇪🇸 Español', '📂 Categoría'), DIAS_MESES, tts)
    main_window.agregar_tab(dias_view, "📅", "Días/Meses")
    
    # Tab 6: Números
    numeros_view = NumerosView(main_window.notebook, tts)
    main_window.agregar_tab(numeros_view, "🔢", "Números")
    
    # Tab 7: Gramática
    gramatica_view = GramaticaView(main_window.notebook)
    main_window.agregar_tab(gramatica_view, "📝", "Gramática")
    
    # Tab 8: Contracciones
    contr_view = GenericTableView(main_window.notebook, "Contracciones", 
                                   ('Contracción', 'Original', 'Español'), CONTRACCIONES)
    main_window.agregar_tab(contr_view, "🔗", "Contracciones")
    
    # Tab 9: Verbos
    verbos_data = [(v[0], v[1], v[2], v[3]) for v in TODOS_VERBOS]
    verbos_view = GenericTableView(main_window.notebook, "Verbos", 
                                    ('Infinitivo', 'Pasado', 'Participio', 'Español'), verbos_data)
    main_window.agregar_tab(verbos_view, "📘", "Verbos")
    
    # Tab 10: Verbos Frasales
    frasales_view = GenericTableView(main_window.notebook, "Verbos Frasales",
                                      ('Phrasal Verb', 'Significado'), VERBOS_FRASALES, tts)
    main_window.agregar_tab(frasales_view, "🔤", "Verbos Frasales")
    
    # Tab 11: Conjugación
    conjugacion_view = ConjugacionView(main_window.notebook)
    main_window.agregar_tab(conjugacion_view, "⏰", "Conjugación")
    
    # Tab 11: Conjugación
    conjugacion_view = ConjugacionView(main_window.notebook)
    main_window.agregar_tab(conjugacion_view, "⏰", "Conjugación")
    
    # Tab 12: Estadísticas
    stats_view = EstadisticasView(main_window.notebook, vocab_controller, storage)
    main_window.agregar_tab(stats_view, "📊", "Estadísticas")
    
    # Tab 13: Estadísticas Avanzadas (placeholder)
    stats_adv_frame = tk.Frame(main_window.notebook, bg=AppConfig.COLOR_BG)
    tk.Label(stats_adv_frame, text="📈 Estadísticas Avanzadas\n\nGráficos en desarrollo", 
             font=(AppConfig.FONT_FAMILY, 16), bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack(expand=True)
    main_window.agregar_tab(stats_adv_frame, "📈", "Estadísticas Avanzadas")
    
    # Tab 14: Ayuda
    ayuda_frame = tk.Frame(main_window.notebook, bg=AppConfig.COLOR_BG)
    ayuda_container = tk.Frame(ayuda_frame, bg=AppConfig.COLOR_BG)
    ayuda_container.pack(expand=True)
    tk.Label(ayuda_container, text="❓ Ayuda y Soporte", 
             font=(AppConfig.FONT_FAMILY, 18, 'bold'), bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT).pack(pady=20)
    ayuda_text = f"""English Memory v{AppConfig.VERSION}\n\nSoporte:\n📧 administrador@agilizesoluciones.com\n📱 +54 11 6168-2555"""
    tk.Label(ayuda_container, text=ayuda_text, font=(AppConfig.FONT_FAMILY, 12), 
             bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG, justify='center').pack(pady=20)
    main_window.agregar_tab(ayuda_frame, "❓", "Ayuda")
    
    root.mainloop()

if __name__ == '__main__':
    main()
