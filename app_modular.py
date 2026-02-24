"""English Memory v1.4.0 - Versión Modular"""
import tkinter as tk
from src.models import HybridStorage
from src.controllers import VocabularioController, PracticaController
from src.utils import AppConfig, TTSHelper
from src.views import MainWindow, VocabularioView, PracticaView, GenericTableView
from src.data import PREPOSICIONES, DIAS_MESES, CONTRACCIONES, TODOS_VERBOS, PRONOMBRES, AUXILIARES, ARTICULOS, DEMOSTRATIVOS, CUANTIFICADORES

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
    
    # Tab 3: Caligrafía (placeholder simple)
    caligrafia_frame = tk.Frame(main_window.notebook, bg=AppConfig.COLOR_BG)
    tk.Label(caligrafia_frame, text="✍️ Caligrafía\n\nFuncionalidad en desarrollo", 
             font=(AppConfig.FONT_FAMILY, 16), bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack(expand=True)
    main_window.agregar_tab(caligrafia_frame, "✍️")
    
    # Tab 4: Preposiciones
    prep_data = [(k, v) for k, v in sorted(PREPOSICIONES.items())]
    prep_view = GenericTableView(main_window.notebook, "Preposiciones", 
                                  ('🇬🇧 Preposición', '🇪🇸 Traducción'), prep_data, tts)
    main_window.agregar_tab(prep_view, "📍")
    
    # Tab 5: Días/Meses
    dias_view = GenericTableView(main_window.notebook, "Días/Meses", 
                                  ('🇬🇧 Inglés', '🇪🇸 Español', '📂 Categoría'), DIAS_MESES, tts)
    main_window.agregar_tab(dias_view, "📅")
    
    # Tab 6: Números (placeholder)
    numeros_frame = tk.Frame(main_window.notebook, bg=AppConfig.COLOR_BG)
    tk.Label(numeros_frame, text="🔢 Números\n\nConversor en desarrollo", 
             font=(AppConfig.FONT_FAMILY, 16), bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack(expand=True)
    main_window.agregar_tab(numeros_frame, "🔢")
    
    # Tab 7: Gramática
    gramatica_frame = tk.Frame(main_window.notebook, bg=AppConfig.COLOR_BG)
    canvas = tk.Canvas(gramatica_frame, bg=AppConfig.COLOR_BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(gramatica_frame, orient="vertical", command=canvas.yview)
    content = tk.Frame(canvas, bg=AppConfig.COLOR_BG)
    content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=content, anchor="nw", width=1000)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
    scrollbar.pack(side="right", fill="y", pady=20)
    
    # Pronombres
    tk.Label(content, text="👤 Pronombres Personales", font=(AppConfig.FONT_FAMILY, 14, 'bold'),
             bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT).pack(pady=10)
    for row in PRONOMBRES:
        tk.Label(content, text=" | ".join(str(x) for x in row), font=(AppConfig.FONT_FAMILY, 9),
                bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_FG).pack(fill='x', padx=20, pady=2)
    
    main_window.agregar_tab(gramatica_frame, "📝")
    
    # Tab 8: Contracciones
    contr_view = GenericTableView(main_window.notebook, "Contracciones", 
                                   ('Contracción', 'Original', 'Español'), CONTRACCIONES)
    main_window.agregar_tab(contr_view, "🔗")
    
    # Tab 9: Verbos
    verbos_data = [(v[0], v[1], v[2], v[3]) for v in TODOS_VERBOS]
    verbos_view = GenericTableView(main_window.notebook, "Verbos", 
                                    ('Infinitivo', 'Pasado', 'Participio', 'Español'), verbos_data)
    main_window.agregar_tab(verbos_view, "📘")
    
    # Tab 10: Conjugación (placeholder)
    conjugacion_frame = tk.Frame(main_window.notebook, bg=AppConfig.COLOR_BG)
    tk.Label(conjugacion_frame, text="⏰ Conjugación\n\nTiempos verbales en desarrollo", 
             font=(AppConfig.FONT_FAMILY, 16), bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack(expand=True)
    main_window.agregar_tab(conjugacion_frame, "⏰")
    
    # Tab 11: Estadísticas
    stats_frame = tk.Frame(main_window.notebook, bg=AppConfig.COLOR_BG)
    stats_container = tk.Frame(stats_frame, bg=AppConfig.COLOR_BG)
    stats_container.pack(expand=True)
    tk.Label(stats_container, text="📊 Estadísticas del Vocabulario", 
             font=(AppConfig.FONT_FAMILY, 18, 'bold'), bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT).pack(pady=20)
    
    stats = vocab_controller.obtener_estadisticas()
    info = f"""Total de palabras: {stats['total']}
Con pronunciación: {stats['con_pronunciacion']}
Sin pronunciación: {stats['sin_pronunciacion']}
Con notas: {stats['con_notas']}"""
    tk.Label(stats_container, text=info, font=(AppConfig.FONT_FAMILY, 14), 
             bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG, justify='left').pack(pady=20)
    main_window.agregar_tab(stats_frame, "📊")
    
    # Tab 12: Estadísticas Avanzadas (placeholder)
    stats_adv_frame = tk.Frame(main_window.notebook, bg=AppConfig.COLOR_BG)
    tk.Label(stats_adv_frame, text="📈 Estadísticas Avanzadas\n\nGráficos en desarrollo", 
             font=(AppConfig.FONT_FAMILY, 16), bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack(expand=True)
    main_window.agregar_tab(stats_adv_frame, "📈")
    
    # Tab 13: Ayuda
    ayuda_frame = tk.Frame(main_window.notebook, bg=AppConfig.COLOR_BG)
    ayuda_container = tk.Frame(ayuda_frame, bg=AppConfig.COLOR_BG)
    ayuda_container.pack(expand=True)
    tk.Label(ayuda_container, text="❓ Ayuda y Soporte", 
             font=(AppConfig.FONT_FAMILY, 18, 'bold'), bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT).pack(pady=20)
    ayuda_text = f"""English Memory v{AppConfig.VERSION}\n\nSoporte:\n📧 administrador@agilizesoluciones.com\n📱 +54 11 6168-2555"""
    tk.Label(ayuda_container, text=ayuda_text, font=(AppConfig.FONT_FAMILY, 12), 
             bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG, justify='center').pack(pady=20)
    main_window.agregar_tab(ayuda_frame, "❓")
    
    root.mainloop()

if __name__ == '__main__':
    main()
