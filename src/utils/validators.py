"""Validación centralizada de datos"""

class Validator:
    @staticmethod
    def validar_palabra(texto, max_length=100):
        """Validar palabra o texto"""
        if not texto or not isinstance(texto, str):
            raise ValueError("El texto debe ser una cadena válida")
        
        texto = texto.strip()
        if not texto:
            raise ValueError("El texto no puede estar vacío")
        
        if len(texto) > max_length:
            raise ValueError(f"El texto excede {max_length} caracteres")
        
        return texto
    
    @staticmethod
    def validar_traduccion(texto, max_length=200):
        """Validar traducción (permite más caracteres)"""
        return Validator.validar_palabra(texto, max_length)
    
    @staticmethod
    def validar_numero(valor, min_val=None, max_val=None):
        """Validar número entero"""
        try:
            num = int(valor)
            if min_val is not None and num < min_val:
                raise ValueError(f"El valor debe ser mayor o igual a {min_val}")
            if max_val is not None and num > max_val:
                raise ValueError(f"El valor debe ser menor o igual a {max_val}")
            return num
        except (ValueError, TypeError):
            raise ValueError("Debe ser un número válido")
