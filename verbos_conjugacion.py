# Código para agregar al archivo diccionario_gui.py
# Insertar después de la función crear_pestaña_gramatica

def crear_pestaña_verbos(self):
    frame = ttk.Frame(self.notebook)
    self.notebook.add(frame, text="📘")
    
    # Búsqueda
    frame_buscar = ttk.Frame(frame)
    frame_buscar.pack(fill='x', padx=20, pady=15)
    
    ttk.Label(frame_buscar, text="🔍", font=(FONT_FAMILY, 14)).pack(side='left', padx=(0,5))
    self.entry_buscar_verbos = ttk.Entry(frame_buscar, width=30, font=(FONT_FAMILY, 11))
    self.entry_buscar_verbos.pack(side='left', padx=5, ipady=5)
    self.entry_buscar_verbos.bind('<KeyRelease>', self._on_search_verbos_keyrelease)
    self._search_verbos_timer = None
    
    # Tabla de verbos
    columns = ('Infinitivo', 'Pasado', 'Participio', 'Español')
    self.tree_verbos = ttk.Treeview(frame, columns=columns, show='headings', height=20)
    
    self.tree_verbos.heading('Infinitivo', text='🇬🇧 Infinitivo')
    self.tree_verbos.heading('Pasado', text='⏪ Pasado')
    self.tree_verbos.heading('Participio', text='✅ Participio')
    self.tree_verbos.heading('Español', text='🇪🇸 Español')
    
    self.tree_verbos.column('Infinitivo', width=200, minwidth=150)
    self.tree_verbos.column('Pasado', width=200, minwidth=150)
    self.tree_verbos.column('Participio', width=200, minwidth=150)
    self.tree_verbos.column('Español', width=300, minwidth=200)
    
    scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree_verbos.yview)
    self.tree_verbos.configure(yscrollcommand=scrollbar.set)
    
    self.tree_verbos.pack(side='left', fill='both', expand=True, padx=(20,0), pady=(0,20))
    scrollbar.pack(side='right', fill='y', pady=(0,20), padx=(0,20))
    
    # Datos de verbos irregulares comunes (100 verbos)
    self.verbos_irregulares = [
        ('be', 'was/were', 'been', 'ser/estar'),
        ('have', 'had', 'had', 'tener/haber'),
        ('do', 'did', 'done', 'hacer'),
        ('say', 'said', 'said', 'decir'),
        ('go', 'went', 'gone', 'ir'),
        ('get', 'got', 'gotten/got', 'obtener/conseguir'),
        ('make', 'made', 'made', 'hacer'),
        ('know', 'knew', 'known', 'saber/conocer'),
        ('think', 'thought', 'thought', 'pensar'),
        ('take', 'took', 'taken', 'tomar/llevar'),
        ('see', 'saw', 'seen', 'ver'),
        ('come', 'came', 'come', 'venir'),
        ('want', 'wanted', 'wanted', 'querer'),
        ('give', 'gave', 'given', 'dar'),
        ('use', 'used', 'used', 'usar'),
        ('find', 'found', 'found', 'encontrar'),
        ('tell', 'told', 'told', 'decir/contar'),
        ('ask', 'asked', 'asked', 'preguntar'),
        ('work', 'worked', 'worked', 'trabajar'),
        ('seem', 'seemed', 'seemed', 'parecer'),
        ('feel', 'felt', 'felt', 'sentir'),
        ('try', 'tried', 'tried', 'intentar'),
        ('leave', 'left', 'left', 'dejar/salir'),
        ('call', 'called', 'called', 'llamar'),
        ('keep', 'kept', 'kept', 'mantener'),
        ('let', 'let', 'let', 'dejar/permitir'),
        ('begin', 'began', 'begun', 'comenzar'),
        ('show', 'showed', 'shown', 'mostrar'),
        ('hear', 'heard', 'heard', 'oír'),
        ('play', 'played', 'played', 'jugar'),
        ('run', 'ran', 'run', 'correr'),
        ('move', 'moved', 'moved', 'mover'),
        ('live', 'lived', 'lived', 'vivir'),
        ('believe', 'believed', 'believed', 'creer'),
        ('bring', 'brought', 'brought', 'traer'),
        ('happen', 'happened', 'happened', 'suceder'),
        ('write', 'wrote', 'written', 'escribir'),
        ('sit', 'sat', 'sat', 'sentarse'),
        ('stand', 'stood', 'stood', 'estar de pie'),
        ('lose', 'lost', 'lost', 'perder'),
        ('pay', 'paid', 'paid', 'pagar'),
        ('meet', 'met', 'met', 'conocer/encontrar'),
        ('include', 'included', 'included', 'incluir'),
        ('continue', 'continued', 'continued', 'continuar'),
        ('set', 'set', 'set', 'establecer'),
        ('learn', 'learned/learnt', 'learned/learnt', 'aprender'),
        ('change', 'changed', 'changed', 'cambiar'),
        ('lead', 'led', 'led', 'liderar/conducir'),
        ('understand', 'understood', 'understood', 'entender'),
        ('watch', 'watched', 'watched', 'mirar/ver'),
        ('follow', 'followed', 'followed', 'seguir'),
        ('stop', 'stopped', 'stopped', 'parar'),
        ('create', 'created', 'created', 'crear'),
        ('speak', 'spoke', 'spoken', 'hablar'),
        ('read', 'read', 'read', 'leer'),
        ('spend', 'spent', 'spent', 'gastar/pasar tiempo'),
        ('grow', 'grew', 'grown', 'crecer'),
        ('open', 'opened', 'opened', 'abrir'),
        ('walk', 'walked', 'walked', 'caminar'),
        ('win', 'won', 'won', 'ganar'),
        ('teach', 'taught', 'taught', 'enseñar'),
        ('offer', 'offered', 'offered', 'ofrecer'),
        ('remember', 'remembered', 'remembered', 'recordar'),
        ('consider', 'considered', 'considered', 'considerar'),
        ('appear', 'appeared', 'appeared', 'aparecer'),
        ('buy', 'bought', 'bought', 'comprar'),
        ('serve', 'served', 'served', 'servir'),
        ('die', 'died', 'died', 'morir'),
        ('send', 'sent', 'sent', 'enviar'),
        ('build', 'built', 'built', 'construir'),
        ('stay', 'stayed', 'stayed', 'quedarse'),
        ('fall', 'fell', 'fallen', 'caer'),
        ('cut', 'cut', 'cut', 'cortar'),
        ('reach', 'reached', 'reached', 'alcanzar'),
        ('kill', 'killed', 'killed', 'matar'),
        ('raise', 'raised', 'raised', 'levantar/criar'),
        ('pass', 'passed', 'passed', 'pasar'),
        ('sell', 'sold', 'sold', 'vender'),
        ('decide', 'decided', 'decided', 'decidir'),
        ('return', 'returned', 'returned', 'regresar'),
        ('explain', 'explained', 'explained', 'explicar'),
        ('hope', 'hoped', 'hoped', 'esperar'),
        ('develop', 'developed', 'developed', 'desarrollar'),
        ('carry', 'carried', 'carried', 'llevar/cargar'),
        ('break', 'broke', 'broken', 'romper'),
        ('receive', 'received', 'received', 'recibir'),
        ('agree', 'agreed', 'agreed', 'estar de acuerdo'),
        ('support', 'supported', 'supported', 'apoyar'),
        ('hit', 'hit', 'hit', 'golpear'),
        ('produce', 'produced', 'produced', 'producir'),
        ('eat', 'ate', 'eaten', 'comer'),
        ('cover', 'covered', 'covered', 'cubrir'),
        ('catch', 'caught', 'caught', 'atrapar'),
        ('draw', 'drew', 'drawn', 'dibujar'),
        ('choose', 'chose', 'chosen', 'elegir'),
        ('wear', 'wore', 'worn', 'usar/llevar puesto'),
        ('drive', 'drove', 'driven', 'conducir'),
        ('sing', 'sang', 'sung', 'cantar'),
        ('swim', 'swam', 'swum', 'nadar'),
        ('fly', 'flew', 'flown', 'volar'),
        ('drink', 'drank', 'drunk', 'beber'),
        ('ride', 'rode', 'ridden', 'montar'),
        ('throw', 'threw', 'thrown', 'lanzar'),
        ('forget', 'forgot', 'forgotten', 'olvidar')
    ]
    
    self.mostrar_todos_verbos()

def mostrar_todos_verbos(self):
    for item in self.tree_verbos.get_children():
        self.tree_verbos.delete(item)
    
    for infinitivo, pasado, participio, espanol in self.verbos_irregulares:
        self.tree_verbos.insert('', 'end', values=(infinitivo, pasado, participio, espanol))

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
    
    for infinitivo, pasado, participio, espanol in self.verbos_irregulares:
        if (busqueda in infinitivo.lower() or busqueda in pasado.lower() or 
            busqueda in participio.lower() or busqueda in espanol.lower()):
            self.tree_verbos.insert('', 'end', values=(infinitivo, pasado, participio, espanol))

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
    
    # Simple Present
    present_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
    present_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
    
    ttk.Label(present_frame, text="🕒 Simple Present (Presente Simple)", font=(FONT_FAMILY, 16, 'bold'), 
             foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,15))
    
    tk.Label(present_frame, text="Uso: Acciones habituales, verdades generales", 
            font=(FONT_FAMILY, 11), bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=5)
    
    present_ejemplos = [
        ('Afirmativo', 'I/You/We/They work', 'He/She/It works'),
        ('Negativo', "I/You/We/They don't work", "He/She/It doesn't work"),
        ('Interrogativo', 'Do I/you/we/they work?', 'Does he/she/it work?')
    ]
    
    for tipo, forma1, forma2 in present_ejemplos:
        item = tk.Frame(present_frame, bg=COLOR_BG, relief='solid', borderwidth=1)
        item.pack(fill='x', padx=20, pady=5)
        tk.Label(item, text=tipo, font=(FONT_FAMILY, 11, 'bold'), 
                bg=COLOR_BG, fg=COLOR_ACCENT, width=15).pack(side='left', padx=10, pady=8)
        tk.Label(item, text=forma1, font=(FONT_FAMILY, 10), 
                bg=COLOR_BG, fg=COLOR_FG, width=25, anchor='w').pack(side='left', padx=5)
        tk.Label(item, text=forma2, font=(FONT_FAMILY, 10), 
                bg=COLOR_BG, fg=COLOR_FG, anchor='w').pack(side='left', padx=5)
    
    # Present Continuous
    continuous_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
    continuous_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
    
    ttk.Label(continuous_frame, text="🔄 Present Continuous (Presente Continuo)", font=(FONT_FAMILY, 16, 'bold'), 
             foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,15))
    
    tk.Label(continuous_frame, text="Uso: Acciones en progreso ahora", 
            font=(FONT_FAMILY, 11), bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=5)
    
    continuous_ejemplos = [
        ('Afirmativo', 'I am working', 'You/We/They are working', 'He/She/It is working'),
        ('Negativo', "I'm not working", "You/We/They aren't working", "He/She/It isn't working"),
        ('Interrogativo', 'Am I working?', 'Are you/we/they working?', 'Is he/she/it working?')
    ]
    
    for tipo, forma1, forma2, forma3 in continuous_ejemplos:
        item = tk.Frame(continuous_frame, bg=COLOR_BG, relief='solid', borderwidth=1)
        item.pack(fill='x', padx=20, pady=5)
        tk.Label(item, text=tipo, font=(FONT_FAMILY, 11, 'bold'), 
                bg=COLOR_BG, fg=COLOR_ACCENT, width=15).pack(side='left', padx=10, pady=8)
        tk.Label(item, text=f"{forma1} | {forma2} | {forma3}", font=(FONT_FAMILY, 9), 
                bg=COLOR_BG, fg=COLOR_FG, anchor='w').pack(side='left', padx=5)
    
    # Simple Past
    past_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
    past_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
    
    ttk.Label(past_frame, text="⏪ Simple Past (Pasado Simple)", font=(FONT_FAMILY, 16, 'bold'), 
             foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,15))
    
    tk.Label(past_frame, text="Uso: Acciones completadas en el pasado", 
            font=(FONT_FAMILY, 11), bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=5)
    
    past_ejemplos = [
        ('Afirmativo', 'I/You/He/She/It/We/They worked'),
        ('Negativo', "I/You/He/She/It/We/They didn't work"),
        ('Interrogativo', 'Did I/you/he/she/it/we/they work?')
    ]
    
    for tipo, forma in past_ejemplos:
        item = tk.Frame(past_frame, bg=COLOR_BG, relief='solid', borderwidth=1)
        item.pack(fill='x', padx=20, pady=5)
        tk.Label(item, text=tipo, font=(FONT_FAMILY, 11, 'bold'), 
                bg=COLOR_BG, fg=COLOR_ACCENT, width=15).pack(side='left', padx=10, pady=8)
        tk.Label(item, text=forma, font=(FONT_FAMILY, 10), 
                bg=COLOR_BG, fg=COLOR_FG, anchor='w').pack(side='left', padx=5)
    
    # Present Perfect
    perfect_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
    perfect_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
    
    ttk.Label(perfect_frame, text="✅ Present Perfect (Presente Perfecto)", font=(FONT_FAMILY, 16, 'bold'), 
             foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,15))
    
    tk.Label(perfect_frame, text="Uso: Acciones pasadas con relevancia presente", 
            font=(FONT_FAMILY, 11), bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=5)
    
    perfect_ejemplos = [
        ('Afirmativo', 'I/You/We/They have worked', 'He/She/It has worked'),
        ('Negativo', "I/You/We/They haven't worked", "He/She/It hasn't worked"),
        ('Interrogativo', 'Have I/you/we/they worked?', 'Has he/she/it worked?')
    ]
    
    for tipo, forma1, forma2 in perfect_ejemplos:
        item = tk.Frame(perfect_frame, bg=COLOR_BG, relief='solid', borderwidth=1)
        item.pack(fill='x', padx=20, pady=5)
        tk.Label(item, text=tipo, font=(FONT_FAMILY, 11, 'bold'), 
                bg=COLOR_BG, fg=COLOR_ACCENT, width=15).pack(side='left', padx=10, pady=8)
        tk.Label(item, text=forma1, font=(FONT_FAMILY, 10), 
                bg=COLOR_BG, fg=COLOR_FG, width=30, anchor='w').pack(side='left', padx=5)
        tk.Label(item, text=forma2, font=(FONT_FAMILY, 10), 
                bg=COLOR_BG, fg=COLOR_FG, anchor='w').pack(side='left', padx=5)
    
    # Future Simple
    future_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
    future_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
    
    ttk.Label(future_frame, text="⏩ Future Simple (Futuro Simple)", font=(FONT_FAMILY, 16, 'bold'), 
             foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,15))
    
    tk.Label(future_frame, text="Uso: Acciones futuras", 
            font=(FONT_FAMILY, 11), bg=COLOR_BUTTON, fg=COLOR_FG).pack(pady=5)
    
    future_ejemplos = [
        ('Afirmativo', 'I/You/He/She/It/We/They will work'),
        ('Negativo', "I/You/He/She/It/We/They won't work"),
        ('Interrogativo', 'Will I/you/he/she/it/we/they work?')
    ]
    
    for tipo, forma in future_ejemplos:
        item = tk.Frame(future_frame, bg=COLOR_BG, relief='solid', borderwidth=1)
        item.pack(fill='x', padx=20, pady=5)
        tk.Label(item, text=tipo, font=(FONT_FAMILY, 11, 'bold'), 
                bg=COLOR_BG, fg=COLOR_ACCENT, width=15).pack(side='left', padx=10, pady=8)
        tk.Label(item, text=forma, font=(FONT_FAMILY, 10), 
                bg=COLOR_BG, fg=COLOR_FG, anchor='w').pack(side='left', padx=5)
    
    # Modal Verbs
    modal_frame = tk.Frame(content, bg=COLOR_BUTTON, relief='solid', borderwidth=1)
    modal_frame.pack(fill='x', padx=20, pady=(0,20), ipady=15)
    
    ttk.Label(modal_frame, text="🔑 Modal Verbs (Verbos Modales)", font=(FONT_FAMILY, 16, 'bold'), 
             foreground=COLOR_ACCENT, background=COLOR_BUTTON).pack(pady=(10,15))
    
    modales = [
        ('can', 'poder (habilidad)', 'I can swim'),
        ('could', 'podría (posibilidad)', 'I could help you'),
        ('may', 'poder (permiso)', 'May I come in?'),
        ('might', 'podría (posibilidad menor)', 'It might rain'),
        ('must', 'deber (obligación)', 'You must study'),
        ('should', 'debería (consejo)', 'You should rest'),
        ('would', 'condicional', 'I would like coffee'),
        ('will', 'futuro', 'I will go tomorrow')
    ]
    
    for modal, significado, ejemplo in modales:
        item = tk.Frame(modal_frame, bg=COLOR_BG, relief='solid', borderwidth=1)
        item.pack(fill='x', padx=20, pady=3)
        tk.Label(item, text=modal, font=(FONT_FAMILY, 11, 'bold'), 
                bg=COLOR_BG, fg=COLOR_ACCENT, width=10, anchor='w').pack(side='left', padx=10, pady=5)
        tk.Label(item, text=significado, font=(FONT_FAMILY, 10), 
                bg=COLOR_BG, fg=COLOR_FG, width=25, anchor='w').pack(side='left', padx=5)
        tk.Label(item, text=f"Ej: {ejemplo}", font=(FONT_FAMILY, 9, 'italic'), 
                bg=COLOR_BG, fg=COLOR_BUTTON_HOVER, anchor='w').pack(side='left', padx=5)
