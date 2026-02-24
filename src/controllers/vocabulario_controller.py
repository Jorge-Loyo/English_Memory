"""Controlador de Vocabulario - Lógica de negocio"""

class VocabularioController:
    def __init__(self, storage):
        self.storage = storage
    
    def agregar_palabra(self, ingles, espanol, pronunciacion=None, notas=None):
        """Agregar nueva palabra con validaciones"""
        # Validaciones
        if not ingles or not espanol:
            raise ValueError("Palabra y significado son obligatorios")
        
        if len(ingles) > 100:
            raise ValueError("La palabra no puede exceder 100 caracteres")
        
        if len(espanol) > 500:
            raise ValueError("El significado no puede exceder 500 caracteres")
        
        if pronunciacion and len(pronunciacion) > 200:
            raise ValueError("La pronunciación no puede exceder 200 caracteres")
        
        if notas and len(notas) > 1000:
            raise ValueError("Las notas no pueden exceder 1000 caracteres")
        
        # Verificar duplicados
        if self.storage.existe_palabra(ingles):
            raise ValueError(f"La palabra '{ingles}' ya existe")
        
        # Agregar palabra
        return self.storage.agregar_palabra(ingles, espanol, pronunciacion, notas)
    
    def editar_palabra(self, palabra_actual, nueva_palabra, nuevo_significado, nueva_pronunciacion=None, nuevas_notas=None):
        """Editar palabra existente"""
        # Validaciones
        if not nueva_palabra or not nuevo_significado:
            raise ValueError("Palabra y significado son obligatorios")
        
        if len(nueva_palabra) > 100 or len(nuevo_significado) > 500:
            raise ValueError("Palabra o significado demasiado largo")
        
        if nueva_pronunciacion and len(nueva_pronunciacion) > 200:
            raise ValueError("Pronunciación demasiado larga")
        
        if nuevas_notas and len(nuevas_notas) > 1000:
            raise ValueError("Notas demasiado largas")
        
        # Eliminar palabra anterior
        self.storage.eliminar_palabra(palabra_actual)
        
        # Agregar palabra actualizada
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
