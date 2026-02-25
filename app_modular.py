"""English Memory v1.4.0 - Versión Modular"""
import tkinter as tk
from tkinter import ttk
from src.models import HybridStorage
from src.controllers import VocabularioController, PracticaController
from src.utils import AppConfig, TTSHelper, AppStyles
from src.views import (MainWindow, VocabularioView, PracticaView, GenericTableView,
                       CaligrafiaView, NumerosView, GramaticaView, ConjugacionView, EstadisticasView,
                       TraductorView, DiccionarioAPIView)
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
                                   ('Contracción', 'Original', 'Español'), CONTRACCIONES, tts)
    main_window.agregar_tab(contr_view, "🔗", "Contracciones")
    
    # Tab 9: Verbos
    verbos_data = [(v[0], v[1], v[2], v[3], v[4], v[5], v[6]) for v in TODOS_VERBOS]
    verbos_view = GenericTableView(main_window.notebook, "Verbos", 
                                    ('Infinitivo', 'Español', 'Pasado', 'Español Pasado', 'Participio', 'Español Participio', 'Tipo'), verbos_data)
    main_window.agregar_tab(verbos_view, "📘", "Verbos")
    
    # Tab 10: Verbos Frasales
    frasales_view = GenericTableView(main_window.notebook, "Verbos Frasales",
                                      ('Phrasal Verb', 'Significado'), VERBOS_FRASALES, tts)
    main_window.agregar_tab(frasales_view, "🔤", "Verbos Frasales")
    
    # Tab 11: Conjugación
    conjugacion_view = ConjugacionView(main_window.notebook)
    main_window.agregar_tab(conjugacion_view, "⏰", "Conjugación")
    
    # Tab 12: Traductor
    traductor_view = TraductorView(main_window.notebook, tts)
    main_window.agregar_tab(traductor_view, "🌐", "Traductor")
    
    # Tab 13: Diccionario
    diccionario_view = DiccionarioAPIView(main_window.notebook, tts)
    main_window.agregar_tab(diccionario_view, "📖", "Diccionario API")
    
    # Tab 14: Estadísticas
    stats_view = EstadisticasView(main_window.notebook, vocab_controller, storage)
    main_window.agregar_tab(stats_view, "📊", "Estadísticas")
    
    # Tab 15: Estadísticas Avanzadas (placeholder)
    stats_adv_frame = tk.Frame(main_window.notebook, bg=AppConfig.COLOR_BG)
    tk.Label(stats_adv_frame, text="📈 Estadísticas Avanzadas\n\nGráficos en desarrollo", 
             font=(AppConfig.FONT_FAMILY, 16), bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG).pack(expand=True)
    main_window.agregar_tab(stats_adv_frame, "📈", "Estadísticas Avanzadas")
    
    # Tab 16: Ayuda
    ayuda_frame = tk.Frame(main_window.notebook, bg=AppConfig.COLOR_BG)
    
    # Canvas con scroll
    canvas_ayuda = tk.Canvas(ayuda_frame, bg=AppConfig.COLOR_BG, highlightthickness=0)
    scrollbar_ayuda = ttk.Scrollbar(ayuda_frame, orient="vertical", command=canvas_ayuda.yview)
    content_ayuda = tk.Frame(canvas_ayuda, bg=AppConfig.COLOR_BG)
    
    content_ayuda.bind("<Configure>", lambda e: canvas_ayuda.configure(scrollregion=canvas_ayuda.bbox("all")))
    canvas_ayuda.create_window((0, 0), window=content_ayuda, anchor="nw", width=1000)
    canvas_ayuda.configure(yscrollcommand=scrollbar_ayuda.set)
    
    def _on_mousewheel_ayuda(event):
        canvas_ayuda.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas_ayuda.bind("<Enter>", lambda e: canvas_ayuda.bind_all("<MouseWheel>", _on_mousewheel_ayuda))
    canvas_ayuda.bind("<Leave>", lambda e: canvas_ayuda.unbind_all("<MouseWheel>"))
    
    canvas_ayuda.pack(side="left", fill="both", expand=True, padx=20, pady=20)
    scrollbar_ayuda.pack(side="right", fill="y", pady=20)
    
    # Soporte
    soporte_frame = tk.Frame(content_ayuda, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
    soporte_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
    
    tk.Label(soporte_frame, text="📞 Soporte Técnico", font=(AppConfig.FONT_FAMILY, 16, 'bold'), 
            bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_ACCENT).pack(pady=(10,15))
    tk.Label(soporte_frame, text="¿Necesitas ayuda? Contáctanos:", font=(AppConfig.FONT_FAMILY, 11), 
            bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_FG).pack(pady=5)
    tk.Label(soporte_frame, text="📧 Email: Jorgenayati@gmail.com", 
            font=(AppConfig.FONT_FAMILY, 11, 'bold'), bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_SUCCESS).pack(pady=5)
    tk.Label(soporte_frame, text="📱 Teléfono: +54 11 6168-2555", 
            font=(AppConfig.FONT_FAMILY, 11, 'bold'), bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_SUCCESS).pack(pady=(5,15))
    
    # Manual de Usuario
    manual_frame = tk.Frame(content_ayuda, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
    manual_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
    
    tk.Label(manual_frame, text="📚 Manual de Usuario", font=(AppConfig.FONT_FAMILY, 16, 'bold'), 
            bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_ACCENT).pack(pady=(10,15))
    
    manual_text = [
        ("📚 Vocabulario", "Agrega, edita y elimina palabras. Usa la búsqueda para encontrar rápidamente. Doble clic para editar."),
        ("🎯 Práctica", "Modo quiz para practicar. Elige entre Inglés→Español o Español→Inglés. Usa TTS para escuchar."),
        ("✍️ Caligrafía", "Practica escribiendo palabras erróneas o todo el vocabulario con repetición espaciada."),
        ("📍 Preposiciones", "Consulta 47 preposiciones en inglés con traducciones y ejemplos."),
        ("📅 Días/Meses", "Días de la semana, meses del año y 58 términos relacionados con tiempo."),
        ("🔢 Números", "Conversor de números + reglas de ordinales, decimales, fracciones y más."),
        ("📝 Gramática", "Pronombres, verbos auxiliares, artículos, demostrativos y cuantificadores."),
        ("🔗 Contracciones", "93 contracciones en inglés: formales (I'm, you're) e informales (gonna, wanna)."),
        ("📘 Verbos", "368 verbos (124 irregulares + 239 regulares + 5 modales) con infinitivo, pasado y participio."),
        ("🔤 Verbos Frasales", "Verbos frasales comunes con sus significados y ejemplos de uso."),
        ("⏰ Conjugación", "6 tiempos verbales (Present, Past, Perfect, Future, Continuous) + Modal Verbs."),
        ("🌐 Traductor", "Traductor bidireccional Inglés↔Español con pronunciación integrada."),
        ("📚 Diccionario API", "Diccionario completo con definiciones, sinónimos y ejemplos en ambos idiomas."),
        ("📊 Estadísticas", "Métricas de tu vocabulario: total de palabras, pronunciaciones, notas y backups."),
        ("💾 Respaldos", "Backup automático antes de cada guardado. Mantiene últimos 10 backups.")
    ]
    
    manual_content = tk.Frame(manual_frame, bg=AppConfig.COLOR_BUTTON)
    manual_content.pack(padx=30, pady=(0,15), fill='x')
    
    for titulo, desc in manual_text:
        item_frame = tk.Frame(manual_content, bg=AppConfig.COLOR_BG, relief='solid', borderwidth=1)
        item_frame.pack(fill='x', pady=5)
        tk.Label(item_frame, text=titulo, font=(AppConfig.FONT_FAMILY, 11, 'bold'), 
                bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_ACCENT, anchor='w').pack(padx=10, pady=(5,2), fill='x')
        tk.Label(item_frame, text=desc, font=(AppConfig.FONT_FAMILY, 10), 
                bg=AppConfig.COLOR_BG, fg=AppConfig.COLOR_FG, anchor='w', wraplength=850, justify='left').pack(padx=10, pady=(2,5), fill='x')
    
    # Términos y Condiciones
    terminos_frame = tk.Frame(content_ayuda, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
    terminos_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
    
    tk.Label(terminos_frame, text="📜 Términos y Condiciones", font=(AppConfig.FONT_FAMILY, 16, 'bold'), 
            bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_ACCENT).pack(pady=(10,15))
    
    terminos = [
        "1. Uso Educativo: Esta aplicación es de uso gratuito con fines educativos.",
        "2. Privacidad: Todos tus datos se almacenan localmente en tu computadora.",
        "3. Respaldos: Es responsabilidad del usuario hacer respaldos de sus datos.",
        "4. Garantía: La aplicación se proporciona 'tal cual' sin garantías de ningún tipo.",
        "5. Soporte: El soporte técnico se proporciona por email o teléfono.",
        "6. Actualizaciones: Las actualizaciones son opcionales y se notificarán por email.",
        "7. Licencia: Software de uso libre para fines educativos personales.",
        "8. Modificaciones: Nos reservamos el derecho de modificar estos términos."
    ]
    
    terminos_content = tk.Frame(terminos_frame, bg=AppConfig.COLOR_BUTTON)
    terminos_content.pack(padx=30, pady=(0,15), fill='x')
    
    for termino in terminos:
        tk.Label(terminos_content, text=termino, font=(AppConfig.FONT_FAMILY, 10), 
                bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_FG, anchor='w', wraplength=850, justify='left').pack(anchor='w', pady=3)
    
    # Acerca de
    about_frame = tk.Frame(content_ayuda, bg=AppConfig.COLOR_BUTTON, relief='solid', borderwidth=1)
    about_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
    
    tk.Label(about_frame, text="ℹ️ Acerca de English Memory", font=(AppConfig.FONT_FAMILY, 16, 'bold'), 
            bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_ACCENT).pack(pady=(10,10))
    tk.Label(about_frame, text=f"Versión: {AppConfig.VERSION}", font=(AppConfig.FONT_FAMILY, 11), 
            bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_FG).pack(pady=2)
    tk.Label(about_frame, text="Desarrollado por: Agilize Soluciones", font=(AppConfig.FONT_FAMILY, 11), 
            bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_FG).pack(pady=2)
    tk.Label(about_frame, text="Aplicación educativa para aprendizaje de inglés", font=(AppConfig.FONT_FAMILY, 10), 
            bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_FG).pack(pady=2)
    
    tk.Label(about_frame, text="\n✨ Novedades v1.4.0:", font=(AppConfig.FONT_FAMILY, 11, 'bold'), 
            bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_ACCENT).pack(pady=(10,5))
    
    novedades = [
        "• Validación centralizada de datos",
        "• Sistema de backups automáticos",
        "• Pronunciación TTS mejorada",
        "• Diccionario con definiciones completas",
        "• Traductor con MyMemory API",
        "• Números ordinales y reglas completas"
    ]
    
    for novedad in novedades:
        tk.Label(about_frame, text=novedad, font=(AppConfig.FONT_FAMILY, 9), 
                bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_FG, anchor='w').pack(padx=30, anchor='w')
    
    # Sugerencias
    tk.Label(about_frame, text="\n💡 Sugerencias para la próxima versión:", font=(AppConfig.FONT_FAMILY, 11, 'bold'), 
            bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_ACCENT).pack(pady=(10,5))
    tk.Label(about_frame, text="¿Tienes ideas para mejorar la aplicación?", font=(AppConfig.FONT_FAMILY, 9), 
            bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_FG).pack(padx=30)
    tk.Label(about_frame, text="Envía tus sugerencias, mejoras o reportes de errores a:", font=(AppConfig.FONT_FAMILY, 9), 
            bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_FG).pack(padx=30)
    tk.Label(about_frame, text="📧 Jorgenayati@gmail.com", font=(AppConfig.FONT_FAMILY, 9, 'bold'), 
            bg=AppConfig.COLOR_BUTTON, fg=AppConfig.COLOR_SUCCESS).pack(padx=30, pady=(5,0))
    
    tk.Label(about_frame, text="", bg=AppConfig.COLOR_BUTTON).pack(pady=5)
    
    main_window.agregar_tab(ayuda_frame, "❓", "Ayuda")
    
    root.mainloop()

if __name__ == '__main__':
    main()
