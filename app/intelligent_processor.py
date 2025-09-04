"""
Module de traitement intelligent pour BiaSavia
"""
from .nlp_processor import nlp_processor
from .smart_google_search import smart_google_search_service
from .conversation_memory import conversation_memory
from typing import Dict, Any, List

class IntelligentProcessor:
    """Processeur intelligent pour analyser et répondre aux questions"""
    
    def __init__(self):
        self.confidence_threshold = 0.6
        
    def process_question(self, question: str, session_id: str = None) -> Dict[str, Any]:
        """
        Traite une question de manière intelligente
        """
        # Analyse de la question
        category = nlp_processor.categorize_question(question)
        keywords = nlp_processor.extract_keywords(question)
        
        # Récupération du contexte de conversation
        conversation_context = {}
        if session_id:
            conversation_context = conversation_memory.get_conversation_context(session_id)
        
        # Recherche intelligente
        search_results = smart_google_search_service.smart_search(question)
        
        # Génération du contexte de réponse
        response_context = nlp_processor.generate_response_context(question, search_results)
        
        # Extraction de la réponse
        answer = smart_google_search_service.extract_answer_from_results(search_results, question)
        
        # Amélioration de la réponse avec le contexte
        enhanced_answer = self._enhance_answer_with_context(
            answer, category, conversation_context, response_context
        )
        
        # Suggestions de questions de suivi
        follow_up_suggestions = []
        if session_id:
            follow_up_suggestions = conversation_memory.suggest_follow_up_questions(session_id)
        
        result = {
            'answer': enhanced_answer,
            'category': category,
            'keywords': keywords,
            'confidence': response_context.get('confidence', 0.5),
            'sources': [result['link'] for result in search_results[:3]],
            'follow_up_suggestions': follow_up_suggestions[:3],
            'search_results': search_results[:3]
        }
        
        # Sauvegarder dans la mémoire de conversation
        if session_id:
            conversation_memory.add_message(session_id, question, enhanced_answer, category)
        
        return result
    
    def _enhance_answer_with_context(self, base_answer: str, category: str, 
                                   conversation_context: Dict, response_context: Dict) -> str:
        """
        Améliore la réponse avec le contexte de conversation et de recherche
        """
        enhanced_answer = base_answer
        
        # Ajouter une introduction contextuelle
        intro_phrases = {
            'pollution': "Concernant la pollution environnementale, ",
            'climat': "En ce qui concerne le climat et le réchauffement climatique, ",
            'energie': "Pour les questions d'énergie et de durabilité, ",
            'biodiversite': "Au sujet de la biodiversité et de la conservation, ",
            'eau': "Concernant les ressources en eau, ",
            'air': "En matière de qualité de l'air, ",
            'foret': "Pour les questions forestières, ",
            'dechets': "Concernant la gestion des déchets, "
        }
        
        if category in intro_phrases and not enhanced_answer.startswith(intro_phrases[category]):
            enhanced_answer = intro_phrases[category] + enhanced_answer.lower()
        
        # Ajouter des informations contextuelles si pertinentes
        if conversation_context.get('main_topic') == category:
            enhanced_answer += "\n\nComme nous en avons déjà parlé dans notre conversation, ce sujet est particulièrement important pour l'environnement."
        
        # Ajouter une conclusion selon la confiance
        confidence = response_context.get('confidence', 0.5)
        if confidence < 0.3:
            enhanced_answer += "\n\nCette information nécessite une vérification supplémentaire. Je vous recommande de consulter des sources officielles pour plus de détails."
        elif confidence > 0.8:
            enhanced_answer += "\n\nCette information est basée sur des sources fiables et récentes."
        
        return enhanced_answer
    
    def analyze_conversation_trends(self, session_id: str) -> Dict[str, Any]:
        """
        Analyse les tendances de conversation pour personnaliser les réponses
        """
        if not session_id:
            return {}
        
        context = conversation_memory.get_conversation_context(session_id)
        recent_topics = conversation_memory.get_recent_topics(session_id)
        
        trends = {
            'user_interests': list(context.get('topics_discussed', {}).keys()),
            'engagement_level': self._calculate_engagement_level(context),
            'preferred_topics': recent_topics,
            'session_quality': self._assess_session_quality(context)
        }
        
        return trends
    
    def _calculate_engagement_level(self, context: Dict) -> str:
        """
        Calcule le niveau d'engagement de l'utilisateur
        """
        conversation_length = context.get('conversation_length', 0)
        topics_count = len(context.get('topics_discussed', {}))
        
        if conversation_length >= 10 and topics_count >= 3:
            return 'high'
        elif conversation_length >= 5 and topics_count >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _assess_session_quality(self, context: Dict) -> str:
        """
        Évalue la qualité de la session de conversation
        """
        conversation_length = context.get('conversation_length', 0)
        topics_diversity = len(context.get('topics_discussed', {}))
        
        if conversation_length >= 8 and topics_diversity >= 3:
            return 'excellent'
        elif conversation_length >= 5 and topics_diversity >= 2:
            return 'good'
        elif conversation_length >= 3:
            return 'fair'
        else:
            return 'poor'

# Instance globale du processeur intelligent
intelligent_processor = IntelligentProcessor()
