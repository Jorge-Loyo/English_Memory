"""
Diccionario de Inglés usando Free Dictionary API

API: https://dictionaryapi.dev/
No requiere API key - Completamente gratuita

Instalación:
    pip install requests

Uso:
    from src.integrations.dictionary_en import get_definition, get_synonyms
    
    # Obtener definición
    result = get_definition("hello")
    print(result['definitions'])
    
    # Obtener sinónimos
    synonyms = get_synonyms("happy")
    print(synonyms)
"""

import requests

API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"


class EnglishDictionary:
    """Diccionario de inglés usando Free Dictionary API"""
    
    def __init__(self):
        self.base_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    
    def lookup(self, word):
        """
        Busca una palabra en el diccionario
        
        Args:
            word (str): Palabra a buscar
        
        Returns:
            dict: Información completa de la palabra
        """
        try:
            response = requests.get(f"{self.base_url}{word.lower()}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()[0]
                return self._parse_response(data)
            elif response.status_code == 404:
                return {'error': 'Palabra no encontrada'}
            else:
                return {'error': f'Error {response.status_code}'}
        
        except requests.exceptions.RequestException as e:
            return {'error': f'Error de conexión: {str(e)}'}
    
    def _parse_response(self, data):
        """Parsea la respuesta de la API"""
        result = {
            'word': data.get('word', ''),
            'phonetic': data.get('phonetic', ''),
            'phonetics': [],
            'meanings': [],
            'synonyms': [],
            'antonyms': []
        }
        
        # Fonética
        for phonetic in data.get('phonetics', []):
            if phonetic.get('text'):
                result['phonetics'].append({
                    'text': phonetic.get('text', ''),
                    'audio': phonetic.get('audio', '')
                })
        
        # Significados
        for meaning in data.get('meanings', []):
            part_of_speech = meaning.get('partOfSpeech', '')
            definitions = []
            
            for definition in meaning.get('definitions', []):
                definitions.append({
                    'definition': definition.get('definition', ''),
                    'example': definition.get('example', ''),
                    'synonyms': definition.get('synonyms', []),
                    'antonyms': definition.get('antonyms', [])
                })
            
            result['meanings'].append({
                'partOfSpeech': part_of_speech,
                'definitions': definitions
            })
            
            # Recopilar sinónimos y antónimos
            result['synonyms'].extend(meaning.get('synonyms', []))
            result['antonyms'].extend(meaning.get('antonyms', []))
        
        # Eliminar duplicados
        result['synonyms'] = list(set(result['synonyms']))
        result['antonyms'] = list(set(result['antonyms']))
        
        return result
    
    def get_definitions(self, word):
        """Obtiene solo las definiciones"""
        result = self.lookup(word)
        if 'error' in result:
            return []
        
        definitions = []
        for meaning in result['meanings']:
            for definition in meaning['definitions']:
                definitions.append({
                    'type': meaning['partOfSpeech'],
                    'definition': definition['definition'],
                    'example': definition.get('example', '')
                })
        return definitions
    
    def get_synonyms(self, word):
        """Obtiene solo los sinónimos"""
        result = self.lookup(word)
        return result.get('synonyms', [])
    
    def get_antonyms(self, word):
        """Obtiene solo los antónimos"""
        result = self.lookup(word)
        return result.get('antonyms', [])


# Funciones de conveniencia
def get_definition(word):
    """Función rápida para obtener definición"""
    dictionary = EnglishDictionary()
    return dictionary.lookup(word)


def get_synonyms(word):
    """Función rápida para obtener sinónimos"""
    dictionary = EnglishDictionary()
    return dictionary.get_synonyms(word)


def get_antonyms(word):
    """Función rápida para obtener antónimos"""
    dictionary = EnglishDictionary()
    return dictionary.get_antonyms(word)


# Ejemplo de uso
if __name__ == '__main__':
    # Buscar palabra
    result = get_definition("hello")
    
    if 'error' not in result:
        print(f"Palabra: {result['word']}")
        print(f"Fonética: {result['phonetic']}")
        print("\nDefiniciones:")
        for meaning in result['meanings']:
            print(f"\n{meaning['partOfSpeech'].upper()}:")
            for i, definition in enumerate(meaning['definitions'], 1):
                print(f"  {i}. {definition['definition']}")
                if definition['example']:
                    print(f"     Ejemplo: {definition['example']}")
        
        if result['synonyms']:
            print(f"\nSinónimos: {', '.join(result['synonyms'][:5])}")
        
        if result['antonyms']:
            print(f"Antónimos: {', '.join(result['antonyms'][:5])}")
    else:
        print(result['error'])
