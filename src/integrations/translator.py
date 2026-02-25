"""
Traductor Inglés ↔ Español usando Google Translate API (gratuita)

Instalación:
    pip install googletrans==4.0.0-rc1

Uso:
    from src.integrations.translator import translate_text, detect_language
    
    # Traducir
    result = translate_text("Hello world", dest='es')
    print(result)  # "Hola mundo"
    
    # Detectar idioma
    lang = detect_language("Hello world")
    print(lang)  # "en"
"""

try:
    from googletrans import Translator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False
    print("⚠️ googletrans no instalado. Ejecuta: pip install googletrans==4.0.0-rc1")


class TranslatorService:
    """Servicio de traducción usando Google Translate API gratuita"""
    
    def __init__(self):
        if not TRANSLATOR_AVAILABLE:
            raise ImportError("googletrans no está instalado")
        self.translator = Translator()
    
    def translate(self, text, src='auto', dest='es'):
        """
        Traduce texto entre idiomas
        
        Args:
            text (str): Texto a traducir
            src (str): Idioma origen ('en', 'es', 'auto')
            dest (str): Idioma destino ('en', 'es')
        
        Returns:
            dict: {'text': texto_traducido, 'src': idioma_origen, 'dest': idioma_destino}
        """
        try:
            result = self.translator.translate(text, src=src, dest=dest)
            return {
                'text': result.text,
                'src': result.src,
                'dest': result.dest,
                'pronunciation': result.pronunciation if hasattr(result, 'pronunciation') else None
            }
        except Exception as e:
            return {'error': str(e)}
    
    def detect_language(self, text):
        """
        Detecta el idioma del texto
        
        Args:
            text (str): Texto a analizar
        
        Returns:
            str: Código de idioma ('en', 'es', etc.)
        """
        try:
            result = self.translator.detect(text)
            return result.lang
        except Exception as e:
            return None
    
    def translate_batch(self, texts, src='auto', dest='es'):
        """
        Traduce múltiples textos
        
        Args:
            texts (list): Lista de textos a traducir
            src (str): Idioma origen
            dest (str): Idioma destino
        
        Returns:
            list: Lista de traducciones
        """
        try:
            results = self.translator.translate(texts, src=src, dest=dest)
            return [{'text': r.text, 'src': r.src, 'dest': r.dest} for r in results]
        except Exception as e:
            return [{'error': str(e)}]


# Funciones de conveniencia
def translate_text(text, src='auto', dest='es'):
    """Función rápida para traducir texto"""
    if not TRANSLATOR_AVAILABLE:
        return "Error: googletrans no instalado"
    
    service = TranslatorService()
    result = service.translate(text, src=src, dest=dest)
    return result.get('text', result.get('error', 'Error desconocido'))


def detect_language(text):
    """Función rápida para detectar idioma"""
    if not TRANSLATOR_AVAILABLE:
        return None
    
    service = TranslatorService()
    return service.detect_language(text)


# Ejemplo de uso
if __name__ == '__main__':
    if TRANSLATOR_AVAILABLE:
        # Traducir inglés → español
        print(translate_text("Hello, how are you?", dest='es'))
        
        # Traducir español → inglés
        print(translate_text("Hola, ¿cómo estás?", dest='en'))
        
        # Detectar idioma
        print(detect_language("Good morning"))
        print(detect_language("Buenos días"))
    else:
        print("Instala googletrans para usar el traductor")
