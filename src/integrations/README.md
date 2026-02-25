# Integraciones - APIs Externas

Este módulo contiene integraciones con APIs externas para traductor y diccionarios.

## 📦 Instalación de Dependencias

```bash
# Traductor
pip install googletrans==4.0.0-rc1

# Diccionarios (solo requests)
pip install requests
```

## 🌐 Traductor (Google Translate API)

### Características
- Traducción Inglés ↔ Español
- Detección automática de idioma
- Traducción por lotes
- Pronunciación fonética
- **Gratuito** - Sin API key

### Uso Básico

```python
from src.integrations.translator import translate_text, detect_language

# Traducir inglés → español
resultado = translate_text("Hello world", dest='es')
print(resultado)  # "Hola mundo"

# Traducir español → inglés
resultado = translate_text("Buenos días", dest='en')
print(resultado)  # "Good morning"

# Detectar idioma
idioma = detect_language("Hello")
print(idioma)  # "en"
```

### Uso Avanzado

```python
from src.integrations.translator import TranslatorService

translator = TranslatorService()

# Traducción completa
result = translator.translate("How are you?", src='en', dest='es')
print(result['text'])           # "¿Cómo estás?"
print(result['pronunciation'])  # Pronunciación si está disponible

# Traducir múltiples textos
texts = ["Hello", "Goodbye", "Thank you"]
results = translator.translate_batch(texts, dest='es')
for r in results:
    print(r['text'])
```

## 📖 Diccionario de Inglés (Free Dictionary API)

### Características
- Definiciones completas
- Pronunciación fonética
- Ejemplos de uso
- Sinónimos y antónimos
- Tipos de palabra (noun, verb, etc.)
- **Gratuito** - Sin API key

### Uso Básico

```python
from src.integrations.dictionary_en import get_definition, get_synonyms

# Obtener definición completa
result = get_definition("happy")
print(result['word'])           # "happy"
print(result['phonetic'])       # "/ˈhæpi/"

# Ver definiciones
for meaning in result['meanings']:
    print(f"\n{meaning['partOfSpeech']}:")
    for definition in meaning['definitions']:
        print(f"  - {definition['definition']}")
        if definition['example']:
            print(f"    Ejemplo: {definition['example']}")

# Obtener sinónimos
synonyms = get_synonyms("happy")
print(synonyms)  # ['joyful', 'cheerful', 'content', ...]
```

### Estructura de Respuesta

```python
{
    'word': 'hello',
    'phonetic': '/həˈloʊ/',
    'phonetics': [
        {'text': '/həˈloʊ/', 'audio': 'https://...'}
    ],
    'meanings': [
        {
            'partOfSpeech': 'noun',
            'definitions': [
                {
                    'definition': 'A greeting',
                    'example': 'She said hello to everyone',
                    'synonyms': ['greeting', 'salutation'],
                    'antonyms': ['goodbye']
                }
            ]
        }
    ],
    'synonyms': ['hi', 'hey', 'greetings'],
    'antonyms': ['goodbye', 'farewell']
}
```

## 📕 Diccionario de Español (Glosbe API)

### Características
- Definiciones en español
- Ejemplos de uso reales
- Traducciones al inglés
- Contexto de uso
- **Gratuito** - Con límites de uso

### Uso Básico

```python
from src.integrations.dictionary_es import get_definition, get_examples

# Obtener definición
result = get_definition("feliz")
print(result['word'])  # "feliz"

# Ver definiciones
for definition in result['definitions']:
    print(definition['text'])

# Ver ejemplos
examples = get_examples("feliz")
for example in examples:
    print(f"{example['original']} → {example['translation']}")

# Traducir al inglés
from src.integrations.dictionary_es import translate_to_english
translations = translate_to_english("feliz")
print(translations)  # ['happy', 'glad', 'joyful']
```

## 🚀 Integración Futura en la Aplicación

### Pestaña Traductor 🌐

```python
# En app_modular.py o diccionario_gui.py

from src.integrations.translator import TranslatorService

class TraductorView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.translator = TranslatorService()
        self.crear_ui()
    
    def traducir(self):
        texto = self.entry_texto.get()
        modo = self.modo_traduccion.get()  # 'en-es' o 'es-en'
        
        if modo == 'en-es':
            result = self.translator.translate(texto, src='en', dest='es')
        else:
            result = self.translator.translate(texto, src='es', dest='en')
        
        self.label_resultado.config(text=result['text'])
```

### Pestaña Diccionario 📖

```python
from src.integrations.dictionary_en import EnglishDictionary
from src.integrations.dictionary_es import SpanishDictionary

class DiccionarioView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.dict_en = EnglishDictionary()
        self.dict_es = SpanishDictionary()
        self.crear_ui()
    
    def buscar_palabra(self):
        palabra = self.entry_buscar.get()
        idioma = self.idioma_seleccionado.get()  # 'en' o 'es'
        
        if idioma == 'en':
            result = self.dict_en.lookup(palabra)
        else:
            result = self.dict_es.lookup(palabra)
        
        self.mostrar_resultado(result)
```

## ⚠️ Consideraciones

### Límites de Uso
- **Google Translate**: Sin límites oficiales, pero puede bloquearse con uso excesivo
- **Free Dictionary API**: Sin límites conocidos
- **Glosbe API**: ~5000 requests/día (sin API key)

### Manejo de Errores
Todas las funciones devuelven `{'error': 'mensaje'}` en caso de fallo:
- Sin conexión a internet
- Palabra no encontrada
- Límite de API excedido
- Timeout de conexión

### Recomendaciones
1. Implementar caché local para palabras buscadas
2. Guardar traducciones en el vocabulario
3. Mostrar mensaje amigable si no hay internet
4. Agregar timeout a las requests (5 segundos)

## 📝 Notas de Implementación

**No implementar todavía** - Este módulo está preparado para uso futuro.

Cuando se decida implementar:
1. Instalar dependencias: `pip install googletrans==4.0.0-rc1 requests`
2. Crear nueva pestaña en la UI
3. Agregar botones de "Guardar en vocabulario"
4. Implementar historial de traducciones/búsquedas
5. Agregar indicador de conexión a internet

## 🔗 Referencias

- [Google Translate API](https://py-googletrans.readthedocs.io/)
- [Free Dictionary API](https://dictionaryapi.dev/)
- [Glosbe API](https://glosbe.com/a-api)
