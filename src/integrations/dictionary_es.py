"""
Diccionario de Español - Obtiene definiciones/significados

API: WordReference y alternativas para obtener definiciones en español

Instalación:
    pip install requests beautifulsoup4

Uso:
    from src.integrations.dictionary_es import SpanishDictionary
    
    dictionary = SpanishDictionary()
    result = dictionary.lookup("feliz")
    print(result['definitions'])
"""

import requests
from bs4 import BeautifulSoup


class SpanishDictionary:
    """Diccionario de español - Obtiene definiciones"""
    
    def __init__(self):
        self.base_url = "https://dle.rae.es"
    
    def lookup(self, word):
        """
        Busca el significado de una palabra en español
        
        Args:
            word (str): Palabra a buscar
        
        Returns:
            dict: Información de la palabra con definiciones
        """
        try:
            # Intentar con API de diccionario español gratuita
            url = f"https://api.dictionaryapi.dev/api/v2/entries/es/{word.lower()}"
            
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_response(data, word)
            else:
                # Si falla, intentar método alternativo
                return self._lookup_alternative(word)
        
        except Exception as e:
            return {'error': 'Palabra no encontrada o error de conexión'}
    
    def _parse_response(self, data, word):
        """Parsea la respuesta de la API"""
        if not data or len(data) == 0:
            return {'error': 'Palabra no encontrada'}
        
        entry = data[0]
        result = {
            'word': entry.get('word', word),
            'phonetic': entry.get('phonetic', ''),
            'meanings': [],
            'synonyms': []
        }
        
        # Procesar significados
        for meaning in entry.get('meanings', []):
            part_of_speech = meaning.get('partOfSpeech', '')
            definitions = []
            
            for definition in meaning.get('definitions', [])[:5]:
                definitions.append({
                    'definition': definition.get('definition', ''),
                    'example': definition.get('example', '')
                })
            
            if definitions:
                result['meanings'].append({
                    'partOfSpeech': part_of_speech,
                    'definitions': definitions
                })
            
            # Sinónimos
            synonyms = meaning.get('synonyms', [])
            result['synonyms'].extend(synonyms[:5])
        
        return result
    
    def _lookup_alternative(self, word):
        """Método alternativo usando scraping simple"""
        try:
            # Usar servicio alternativo
            url = f"https://www.wordreference.com/definicion/{word}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                result = {
                    'word': word,
                    'phonetic': '',
                    'meanings': [],
                    'synonyms': []
                }
                
                # Buscar definiciones
                definitions_found = []
                for ol in soup.find_all('ol'):
                    for li in ol.find_all('li')[:5]:
                        text = li.get_text(strip=True)
                        if text and len(text) > 10:
                            definitions_found.append({'definition': text, 'example': ''})
                
                if definitions_found:
                    result['meanings'].append({
                        'partOfSpeech': 'definición',
                        'definitions': definitions_found
                    })
                    return result
            
            return {'error': 'Palabra no encontrada'}
        
        except Exception:
            return {'error': 'Palabra no encontrada'}
    
    def get_definitions(self, word):
        """Obtiene solo las definiciones"""
        result = self.lookup(word)
        if 'error' in result:
            return []
        
        definitions = []
        for meaning in result['meanings']:
            for definition in meaning['definitions']:
                definitions.append(definition['definition'])
        return definitions


# Funciones de conveniencia
def get_definition(word):
    """Función rápida para obtener definición"""
    dictionary = SpanishDictionary()
    return dictionary.lookup(word)


# Ejemplo de uso
if __name__ == '__main__':
    # Buscar palabra
    result = get_definition("feliz")
    
    if 'error' not in result:
        print(f"Palabra: {result['word']}")
        
        if result['phonetic']:
            print(f"Fonética: {result['phonetic']}")
        
        print("\nSignificados:")
        for meaning in result['meanings']:
            print(f"\n{meaning['partOfSpeech'].upper()}:")
            for i, definition in enumerate(meaning['definitions'], 1):
                print(f"  {i}. {definition['definition']}")
                if definition['example']:
                    print(f"     Ejemplo: {definition['example']}")
        
        if result['synonyms']:
            print(f"\nSinónimos: {', '.join(result['synonyms'])}")
    else:
        print(result['error'])
