"""
Module de recherche Google améliorée pour BiaSavia
"""
from .google_search import GoogleSearchService
import re

class EnhancedGoogleSearchService(GoogleSearchService):
    """Service de recherche Google amélioré avec filtrage et traitement"""
    
    def __init__(self):
        super().__init__()
        self.environmental_keywords = [
            'pollution', 'climat', 'écologie', 'environnement', 'biodiversité',
            'énergie renouvelable', 'développement durable', 'réchauffement climatique',
            'déforestation', 'conservation', 'émissions', 'carbone'
        ]
    
    def enhanced_search(self, query, context="environnement"):
        """
        Recherche améliorée avec contexte environnemental
        """
        # Amélioration de la requête avec contexte
        enhanced_query = f"{query} {context}"
        
        results = self.search(enhanced_query, num_results=8)
        
        # Filtrage et scoring des résultats
        scored_results = []
        for result in results:
            score = self._calculate_relevance_score(result)
            result['relevance_score'] = score
            scored_results.append(result)
        
        # Tri par score de pertinence
        scored_results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return scored_results[:5]
    
    def _calculate_relevance_score(self, result):
        """
        Calcule un score de pertinence basé sur les mots-clés environnementaux
        """
        score = 0
        text_content = f"{result['title']} {result['snippet']}".lower()
        
        # Points pour les mots-clés environnementaux
        for keyword in self.environmental_keywords:
            if keyword in text_content:
                score += 2
        
        # Points pour la longueur du snippet (plus d'info = mieux)
        if len(result['snippet']) > 100:
            score += 1
        
        # Points pour les sources fiables (domaines .org, .edu, .gov)
        if any(domain in result['link'] for domain in ['.org', '.edu', '.gov']):
            score += 3
        
        return score
    
    def search_with_filters(self, query, site_filter=None, time_filter=None):
        """
        Recherche avec filtres spécifiques
        """
        filtered_query = query
        
        if site_filter:
            filtered_query += f" site:{site_filter}"
        
        if time_filter:
            filtered_query += f" {time_filter}"
        
        return self.enhanced_search(filtered_query)

# Instance globale du service amélioré
enhanced_google_search_service = EnhancedGoogleSearchService()
