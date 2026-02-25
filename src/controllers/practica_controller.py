"""Controlador de Práctica - Lógica de quiz"""
import random

class PracticaController:
    def __init__(self, storage):
        self.storage = storage
        self.palabra_actual = None
        self.modo = 'ingles'  # 'ingles' o 'espanol'
    
    def obtener_palabra_aleatoria(self):
        """Obtener palabra aleatoria para práctica"""
        palabras = self.storage.obtener_todas_palabras()
        if not palabras:
            return None
        
        self.palabra_actual = random.choice(list(palabras.keys()))
        return self.palabra_actual
    
    def obtener_pregunta(self):
        """Obtener pregunta según el modo"""
        if not self.palabra_actual:
            return None
        
        palabras = self.storage.obtener_todas_palabras()
        datos = palabras.get(self.palabra_actual, {})
        
        if self.modo == 'ingles':
            return {
                'pregunta': self.palabra_actual,
                'respuesta_correcta': datos.get('significado', ''),
                'pronunciacion': datos.get('pronunciacion', ''),
                'notas': datos.get('notas', '')
            }
        else:
            return {
                'pregunta': datos.get('significado', ''),
                'respuesta_correcta': self.palabra_actual,
                'pronunciacion': datos.get('pronunciacion', ''),
                'notas': datos.get('notas', '')
            }
    
    def verificar_respuesta(self, respuesta_usuario):
        """Verificar si la respuesta es correcta"""
        if not self.palabra_actual or not respuesta_usuario:
            return False
        
        pregunta = self.obtener_pregunta()
        if not pregunta:
            return False
        
        respuesta_usuario = respuesta_usuario.strip().lower()
        respuesta_correcta = pregunta['respuesta_correcta'].lower()
        
        # Permitir variaciones
        es_correcta = (
            respuesta_usuario == respuesta_correcta or
            respuesta_usuario in respuesta_correcta or
            respuesta_correcta in respuesta_usuario
        )
        
        # Registrar práctica
        modo_practica = 'ingles_espanol' if self.modo == 'ingles' else 'espanol_ingles'
        self.storage.registrar_practica(
            self.palabra_actual,
            modo_practica,
            es_correcta,
            respuesta_usuario
        )
        
        return es_correcta
    
    def cambiar_modo(self, modo):
        """Cambiar modo de práctica"""
        if modo in ['ingles', 'espanol']:
            self.modo = modo
    
    def obtener_palabras_erroneas(self):
        """Obtener palabras con más errores"""
        return self.storage.obtener_palabras_dificiles(50)
