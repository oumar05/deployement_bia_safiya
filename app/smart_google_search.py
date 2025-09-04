"""
Module de recherche Google intelligente pour BiaSavia
"""
from .enhanced_google_search import EnhancedGoogleSearchService
import json
import re

class SmartGoogleSearchService(EnhancedGoogleSearchService):
    """Service de recherche Google intelligent avec IA"""
    
    def __init__(self):
        super().__init__()
        self.question_patterns = {
            'what': ['qu\'est-ce que', 'que', 'quoi', 'what'],
            'how': ['comment', 'how'],
            'why': ['pourquoi', 'why'],
            'when': ['quand', 'when'],
            'where': ['où', 'where']
        }
    
    def smart_search(self, user_question):
        """
        Recherche intelligente basée sur la compréhension de la question
        """
        # Analyse du type de question
        question_type = self._analyze_question_type(user_question)
        
        # Génération de requêtes optimisées
        optimized_queries = self._generate_optimized_queries(user_question, question_type)
        
        # Collecte des résultats
        all_results = []
        for query in optimized_queries:
            results = self.enhanced_search(query)
            all_results.extend(results)
        
        # Déduplication et tri
        unique_results = self._deduplicate_results(all_results)
        
        return unique_results[:5]
    
    def _analyze_question_type(self, question):
        """
        Analyse le type de question posée
        """
        question_lower = question.lower()
        
        for q_type, patterns in self.question_patterns.items():
            for pattern in patterns:
                if pattern in question_lower:
                    return q_type
        
        return 'general'
    
    def _generate_optimized_queries(self, question, question_type):
        """
        Génère des requêtes optimisées selon le type de question
        """
        base_query = question
        queries = []
        
        if question_type == 'what':
            queries.append(f"définition {base_query}")
            queries.append(f"{base_query} explication")
        elif question_type == 'how':
            queries.append(f"{base_query} méthode")
            queries.append(f"{base_query} guide")
        elif question_type == 'why':
            queries.append(f"{base_query} causes")
            queries.append(f"{base_query} raisons")
        else:
            queries.append(base_query)
        
        # Ajouter le contexte environnemental
        env_queries = []
        for query in queries:
            env_queries.append(f"{query} environnement")
        
        return queries + env_queries
    
    def _deduplicate_results(self, results):
        """
        Supprime les doublons et trie par pertinence
        """
        seen_links = set()
        unique_results = []
        
        for result in results:
            if result['link'] not in seen_links:
                seen_links.add(result['link'])
                unique_results.append(result)
        
        # Tri par score de pertinence
        unique_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return unique_results
    
    def extract_answer_from_results(self, results, question):
        """
        Extrait une réponse pertinente des résultats de recherche
        """
        answer_parts = []
        
        for result in results[:3]:  # Utiliser les 3 meilleurs résultats
            snippet = result['snippet']
            if len(snippet) > 50:  # Seulement les snippets substantiels
                answer_parts.append(snippet)
        
        if answer_parts:
            # Combiner les informations
            combined_answer = " ".join(answer_parts[:2])  # Limiter la longueur
            return combined_answer[:500] + "..." if len(combined_answer) > 500 else combined_answer
        
        return "Je n'ai pas trouvé d'informations pertinentes pour répondre à votre question."

# Instance globale du service intelligent
smart_google_search_service = SmartGoogleSearchService()
