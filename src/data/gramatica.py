"""Gramática en inglés - Pronombres, artículos, etc."""

# Pronombres personales
PRONOMBRES = [
    ('Sujeto', 'Objeto', 'Adj. Posesivo', 'Pron. Posesivo', 'Reflexivo', 'Español'),
    ('I', 'me', 'my', 'mine', 'myself', 'yo/me/mi/mío'),
    ('you', 'you', 'your', 'yours', 'yourself', 'tú/te/tu/tuyo'),
    ('he', 'him', 'his', 'his', 'himself', 'él/lo/su/suyo'),
    ('she', 'her', 'her', 'hers', 'herself', 'ella/la/su/suya'),
    ('it', 'it', 'its', 'its', 'itself', 'eso/lo/su'),
    ('we', 'us', 'our', 'ours', 'ourselves', 'nosotros/nos/nuestro'),
    ('you', 'you', 'your', 'yours', 'yourselves', 'ustedes/los/su'),
    ('they', 'them', 'their', 'theirs', 'themselves', 'ellos/los/su')
]

# Verbos auxiliares
AUXILIARES = [
    ('TO BE', [
        ('I am', 'yo soy/estoy'),
        ('You are', 'tú eres/estás'),
        ('He/She/It is', 'él/ella es/está'),
        ('We are', 'nosotros somos/estamos'),
        ('They are', 'ellos son/están')
    ]),
    ('TO HAVE', [
        ('I have', 'yo tengo/he'),
        ('You have', 'tú tienes/has'),
        ('He/She/It has', 'él/ella tiene/ha'),
        ('We have', 'nosotros tenemos/hemos'),
        ('They have', 'ellos tienen/han')
    ]),
    ('TO DO', [
        ('I do', 'yo hago'),
        ('You do', 'tú haces'),
        ('He/She/It does', 'él/ella hace'),
        ('We do', 'nosotros hacemos'),
        ('They do', 'ellos hacen')
    ])
]

# Artículos
ARTICULOS = [
    ('a', 'un/una (antes de consonante)', 'a book, a car'),
    ('an', 'un/una (antes de vocal)', 'an apple, an hour'),
    ('the', 'el/la/los/las (específico)', 'the book, the sun')
]

# Demostrativos
DEMOSTRATIVOS = [
    ('this', 'este/esta (singular cerca)', 'this book'),
    ('that', 'ese/esa (singular lejos)', 'that car'),
    ('these', 'estos/estas (plural cerca)', 'these books'),
    ('those', 'esos/esas (plural lejos)', 'those cars')
]

# Cuantificadores
CUANTIFICADORES = [
    ('some', 'algunos/algo (afirmativo)', 'I have some money'),
    ('any', 'algún/ningún (negativo/interrogativo)', 'I don\'t have any money'),
    ('much', 'mucho (incontable)', 'much water'),
    ('many', 'muchos (contable)', 'many books'),
    ('a lot of', 'mucho/muchos', 'a lot of people'),
    ('few', 'pocos (contable)', 'few students'),
    ('little', 'poco (incontable)', 'little time'),
    ('several', 'varios', 'several options'),
    ('all', 'todo/todos', 'all people'),
    ('no', 'ningún', 'no money')
]
