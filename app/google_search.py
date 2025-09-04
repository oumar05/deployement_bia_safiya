"""
Module de recherche Google de base pour BiaSavia
"""
import requests
from bs4 import BeautifulSoup
import time

class GoogleSearchService:
    """Service de recherche Google pour les questions environnementales"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search(self, query, num_results=5):
        """
        Effectue une recherche Google et retourne les résultats
        """
        try:
            # Construction de l'URL de recherche Google
            search_url = f"https://www.google.com/search?q={query}&num={num_results}"
            
            # Envoi de la requête
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parsing du HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraction des résultats
            results = []
            search_results = soup.find_all('div', class_='g')
            
            for result in search_results[:num_results]:
                title_element = result.find('h3')
                link_element = result.find('a')
                snippet_element = result.find('span', {'data-ved': True})
                
                if title_element and link_element:
                    title = title_element.get_text()
                    link = link_element.get('href', '')
                    snippet = snippet_element.get_text() if snippet_element else ""
                    
                    if link.startswith('/url?q='):
                        link = link.split('/url?q=')[1].split('&')[0]
                    
                    results.append({
                        'title': title,
                        'link': link,
                        'snippet': snippet
                    })
            
            return results
            
        except Exception as e:
            print(f"Erreur lors de la recherche Google: {e}")
            return []
    
    def search_environmental_data(self, query):
        """
        Recherche spécialisée pour les données environnementales
        """
        environmental_query = f"{query} environnement écologie pollution climat"
        return self.search(environmental_query)

# Instance globale du service
google_search_service = GoogleSearchService()
