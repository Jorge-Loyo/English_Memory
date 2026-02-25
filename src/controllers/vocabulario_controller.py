"""Controlador de Vocabulario - Lógica de negocio"""
from src.utils import Validator

class VocabularioController:
    def __init__(self, storage):
        self.storage = storage
    
    def agregar_palabra(self, ingles, espanol, pronunciacion=None, notas=None):
        """Agregar nueva palabra con validaciones"""
        # Validar con Validator centralizado
        ingles = Validator.validar_palabra(ingles, max_length=100)
        espanol = Validator.validar_traduccion(espanol, max_length=500)
        
        if pronunciacion:
            pronunciacion = Validator.validar_traduccion(pronunciacion, max_length=200)
        
        if notas:
            notas = Validator.validar_traduccion(notas, max_length=1000)
        
        # Verificar duplicados
        if self.storage.existe_palabra(ingles):
            raise ValueError(f"La palabra '{ingles}' ya existe")
        
        return self.storage.agregar_palabra(ingles, espanol, pronunciacion, notas)
    
    def editar_palabra(self, palabra_actual, nueva_palabra, nuevo_significado, nueva_pronunciacion=None, nuevas_notas=None):
        """Editar palabra existente"""
        # Validar con Validator centralizado
        nueva_palabra = Validator.validar_palabra(nueva_palabra, max_length=100)
        nuevo_significado = Validator.validar_traduccion(nuevo_significado, max_length=500)
        
        if nueva_pronunciacion:
            nueva_pronunciacion = Validator.validar_traduccion(nueva_pronunciacion, max_length=200)
        
        if nuevas_notas:
            nuevas_notas = Validator.validar_traduccion(nuevas_notas, max_length=1000)
        
        # Eliminar palabra anterior y agregar actualizada
        self.storage.eliminar_palabra(palabra_actual)
        return self.storage.agregar_palabra(nueva_palabra, nuevo_significado, nueva_pronunciacion, nuevas_notas)
    
    def eliminar_palabra(self, palabra):
        """Eliminar palabra"""
        return self.storage.eliminar_palabra(palabra)
    
    def buscar_palabras(self, query):
        """Buscar palabras por término"""
        if not query:
            return self.storage.obtener_todas_palabras()
        
        query = query.lower()
        todas = self.storage.obtener_todas_palabras()
        
        return {
            palabra: datos
            for palabra, datos in todas.items()
            if query in palabra.lower() or query in datos.get('significado', '').lower()
        }
    
    def obtener_todas(self):
        """Obtener todas las palabras"""
        return self.storage.obtener_todas_palabras()
    
    def obtener_estadisticas(self):
        """Obtener estadísticas del vocabulario"""
        todas = self.storage.obtener_todas_palabras()
        total = len(todas)
        con_pronunciacion = sum(1 for d in todas.values() if 'pronunciacion' in d)
        con_notas = sum(1 for d in todas.values() if 'notas' in d)
        
        return {
            'total': total,
            'con_pronunciacion': con_pronunciacion,
            'sin_pronunciacion': total - con_pronunciacion,
            'con_notas': con_notas
        }
