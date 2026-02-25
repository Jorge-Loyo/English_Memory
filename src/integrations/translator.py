"""
Traductor Inglés ↔ Español usando MyMemory Translation API (gratuita)

No requiere instalación adicional, solo requests

Uso:
    from src.integrations.translator import translate_text
    
    # Traducir
    result = translate_text("Hello world", dest='es')
    print(result)  # "Hola mundo"
"""

import requests


class TranslatorService:
    """Servicio de traducción usando MyMemory Translation API gratuita"""
    
    def __init__(self):
        self.base_url = "https://api.mymemory.translated.net/get"
    
    def translate(self, text, src='en', dest='es'):
        """
        Traduce texto entre idiomas
        
        Args:
            text (str): Texto a traducir
            src (str): Idioma origen ('en', 'es')
            dest (str): Idioma destino ('en', 'es')
        
        Returns:
            dict: {'text': texto_traducido, 'src': idioma_origen, 'dest': idioma_destino}
        """
        try:
            params = {
                'q': text,
                'langpair': f'{src}|{dest}'
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('responseStatus') == 200:
                    return {
                        'text': data['responseData']['translatedText'],
                        'src': src,
                        'dest': dest
                    }
            
            return {'error': 'Error al traducir'}
        except Exception as e:
            return {'error': str(e)}


# Funciones de conveniencia
def translate_text(text, src='en', dest='es'):
    """Función rápida para traducir texto"""
    service = TranslatorService()
    result = service.translate(text, src=src, dest=dest)
    return result.get('text', result.get('error', 'Error desconocido'))


# Ejemplo de uso
if __name__ == '__main__':
    # Traducir inglés → español
    print(translate_text("Hello, how are you?", src='en', dest='es'))
    
    # Traducir español → inglés
    print(translate_text("Hola, ¿cómo estás?", src='es', dest='en'))
