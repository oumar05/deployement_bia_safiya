"""
Module de traitement NLP pour BiaSavia
"""
import re
from typing import List, Dict, Any

class NLPProcessor:
    """Processeur de langage naturel pour les questions environnementales"""
    
    def __init__(self):
        self.environmental_keywords = {
            'pollution': ['pollution', 'polluant', 'contamination', 'toxique'],
            'climat': ['climat', 'climatique', 'réchauffement', 'température'],
            'energie': ['énergie', 'renouvelable', 'solaire', 'éolien', 'électricité'],
            'biodiversite': ['biodiversité', 'espèces', 'extinction', 'faune', 'flore'],
            'eau': ['eau', 'hydrique', 'rivière', 'océan', 'mer'],
            'air': ['air', 'atmosphère', 'ozone', 'qualité air'],
            'foret': ['forêt', 'déforestation', 'arbres', 'bois'],
            'dechets': ['déchets', 'recyclage', 'plastique', 'ordures']
        }
        
        self.stop_words = {
            'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'et', 'ou', 'mais',
            'donc', 'car', 'ce', 'cette', 'ces', 'son', 'sa', 'ses', 'mon', 'ma',
            'mes', 'ton', 'ta', 'tes', 'notre', 'nos', 'votre', 'vos', 'leur',
            'leurs', 'que', 'qui', 'quoi', 'dont', 'où', 'comment', 'pourquoi',
            'quand', 'est', 'sont', 'était', 'étaient', 'sera', 'seront'
        }
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extrait les mots-clés pertinents d'un texte
        """
        # Nettoyage du texte
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        words = text.split()
        
        # Filtrage des mots vides
        keywords = [word for word in words if word not in self.stop_words and len(word) > 2]
        
        return keywords
    
    def categorize_question(self, question: str) -> str:
        """
        Catégorise une question selon le domaine environnemental
        """
        question_lower = question.lower()
        
        scores = {}
        for category, keywords in self.environmental_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in question_lower:
                    score += 1
            scores[category] = score
        
        # Retourne la catégorie avec le meilleur score
        if scores and max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        return 'general'
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extrait les entités nommées du texte
        """
        entities = {
            'locations': [],
            'organizations': [],
            'pollutants': [],
            'species': []
        }
        
        # Patterns simples pour l'extraction d'entités
        location_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        org_pattern = r'\b[A-Z][A-Z]+\b'
        
        # Extraction basique (à améliorer avec spaCy si disponible)
        locations = re.findall(location_pattern, text)
        organizations = re.findall(org_pattern, text)
        
        entities['locations'] = locations
        entities['organizations'] = organizations
        
        return entities
    
    def generate_response_context(self, question: str, search_results: List[Dict]) -> Dict[str, Any]:
        """
        Génère un contexte pour la réponse basé sur la question et les résultats
        """
        category = self.categorize_question(question)
        keywords = self.extract_keywords(question)
        
        # Analyse des résultats de recherche
        relevant_snippets = []
        for result in search_results:
            snippet = result.get('snippet', '')
            if any(keyword in snippet.lower() for keyword in keywords):
                relevant_snippets.append(snippet)
        
        return {
            'category': category,
            'keywords': keywords,
            'relevant_snippets': relevant_snippets[:3],
            'confidence': min(len(relevant_snippets) * 0.3, 1.0)
        }
    
    def clean_text(self, text: str) -> str:
        """
        Nettoie un texte pour l'affichage
        """
        # Suppression des caractères spéciaux
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Limitation de la longueur
        if len(text) > 1000:
            text = text[:1000] + "..."
        
        return text

# Instance globale du processeur NLP
nlp_processor = NLPProcessor()
