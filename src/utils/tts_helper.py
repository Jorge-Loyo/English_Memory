"""Helper para Text-to-Speech"""
try:
    import pyttsx3
    TTS_DISPONIBLE = True
except ImportError:
    TTS_DISPONIBLE = False

class TTSHelper:
    def __init__(self):
        self.disponible = TTS_DISPONIBLE
        self.engine = None
    
    def pronunciar(self, texto):
        """Pronunciar texto usando TTS"""
        if not self.disponible:
            raise RuntimeError("TTS no disponible. Instala pyttsx3: pip install pyttsx3")
        
        try:
            if not self.engine:
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 150)
            
            self.engine.say(texto)
            self.engine.runAndWait()
        except Exception as e:
            raise RuntimeError(f"Error al pronunciar: {str(e)}")
    
    def esta_disponible(self):
        """Verificar si TTS está disponible"""
        return self.disponible
