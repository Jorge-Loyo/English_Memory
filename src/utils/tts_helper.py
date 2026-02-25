"""Helper para Text-to-Speech"""
import threading
try:
    import pyttsx3
    TTS_DISPONIBLE = True
except ImportError:
    TTS_DISPONIBLE = False

class TTSHelper:
    def __init__(self):
        self.disponible = TTS_DISPONIBLE
        self._lock = threading.Lock()
    
    def pronunciar(self, texto):
        """Pronunciar texto usando TTS"""
        if not self.disponible:
            raise RuntimeError("TTS no disponible. Instala pyttsx3: pip install pyttsx3")
        
        def _speak():
            with self._lock:
                engine = None
                try:
                    engine = pyttsx3.init()
                    engine.setProperty('rate', 150)
                    engine.say(texto)
                    engine.runAndWait()
                except Exception as e:
                    raise RuntimeError(f"Error al pronunciar: {str(e)}")
                finally:
                    if engine:
                        try:
                            engine.stop()
                        except:
                            pass
                        del engine
        
        thread = threading.Thread(target=_speak, daemon=True)
        thread.start()
    
    def esta_disponible(self):
        """Verificar si TTS está disponible"""
        return self.disponible
