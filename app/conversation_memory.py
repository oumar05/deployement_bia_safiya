"""
Module de mémoire conversationnelle pour BiaSavia
"""
from typing import Dict, List, Any
import json
from datetime import datetime

class ConversationMemory:
    """Gestionnaire de mémoire pour les conversations du chatbot"""
    
    def __init__(self):
        self.conversations = {}  # session_id -> conversation_data
        self.max_history_length = 10  # Nombre max de messages à retenir
    
    def add_message(self, session_id: str, user_message: str, bot_response: str, category: str = None):
        """
        Ajoute un message à l'historique de conversation
        """
        if session_id not in self.conversations:
            self.conversations[session_id] = {
                'messages': [],
                'context': {},
                'created_at': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat()
            }
        
        conversation = self.conversations[session_id]
        
        # Ajouter le nouveau message
        message_data = {
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'bot_response': bot_response,
            'category': category
        }
        
        conversation['messages'].append(message_data)
        conversation['last_activity'] = datetime.now().isoformat()
        
        # Limiter la taille de l'historique
        if len(conversation['messages']) > self.max_history_length:
            conversation['messages'] = conversation['messages'][-self.max_history_length:]
    
    def get_conversation_history(self, session_id: str, limit: int = None) -> List[Dict]:
        """
        Récupère l'historique de conversation pour une session
        """
        if session_id not in self.conversations:
            return []
        
        messages = self.conversations[session_id]['messages']
        
        if limit:
            return messages[-limit:]
        
        return messages
    
    def get_conversation_context(self, session_id: str) -> Dict[str, Any]:
        """
        Récupère le contexte de conversation (sujets abordés, préférences, etc.)
        """
        if session_id not in self.conversations:
            return {}
        
        conversation = self.conversations[session_id]
        messages = conversation['messages']
        
        # Analyser les sujets abordés
        topics = {}
        for message in messages:
            category = message.get('category')
            if category:
                topics[category] = topics.get(category, 0) + 1
        
        # Identifier le sujet principal
        main_topic = max(topics.keys(), key=topics.get) if topics else None
        
        context = {
            'main_topic': main_topic,
            'topics_discussed': topics,
            'conversation_length': len(messages),
            'last_activity': conversation.get('last_activity'),
            'session_duration': self._calculate_session_duration(session_id)
        }
        
        return context
    
    def _calculate_session_duration(self, session_id: str) -> str:
        """
        Calcule la durée de la session
        """
        if session_id not in self.conversations:
            return "0 minutes"
        
        conversation = self.conversations[session_id]
        created_at = datetime.fromisoformat(conversation['created_at'])
        last_activity = datetime.fromisoformat(conversation['last_activity'])
        
        duration = last_activity - created_at
        minutes = int(duration.total_seconds() / 60)
        
        return f"{minutes} minutes"
    
    def clear_session(self, session_id: str):
        """
        Efface l'historique d'une session
        """
        if session_id in self.conversations:
            del self.conversations[session_id]
    
    def get_recent_topics(self, session_id: str, limit: int = 3) -> List[str]:
        """
        Récupère les sujets récents abordés dans la conversation
        """
        messages = self.get_conversation_history(session_id, limit=limit)
        
        topics = []
        for message in reversed(messages):  # Plus récents en premier
            category = message.get('category')
            if category and category not in topics:
                topics.append(category)
        
        return topics
    
    def suggest_follow_up_questions(self, session_id: str) -> List[str]:
        """
        Suggère des questions de suivi basées sur l'historique
        """
        context = self.get_conversation_context(session_id)
        main_topic = context.get('main_topic')
        
        suggestions = {
            'pollution': [
                "Comment réduire la pollution de l'air ?",
                "Quels sont les effets de la pollution sur la santé ?",
                "Comment mesurer la qualité de l'air ?"
            ],
            'climat': [
                "Quelles sont les causes du réchauffement climatique ?",
                "Comment agir contre le changement climatique ?",
                "Quels sont les gaz à effet de serre ?"
            ],
            'energie': [
                "Quelles sont les énergies renouvelables ?",
                "Comment économiser l'énergie à la maison ?",
                "Qu'est-ce que la transition énergétique ?"
            ],
            'biodiversite': [
                "Comment protéger la biodiversité ?",
                "Quelles espèces sont menacées ?",
                "Qu'est-ce qu'un écosystème ?"
            ]
        }
        
        if main_topic and main_topic in suggestions:
            return suggestions[main_topic]
        
        # Questions générales si pas de sujet principal
        return [
            "Comment protéger l'environnement ?",
            "Quels sont les enjeux écologiques actuels ?",
            "Comment adopter un mode de vie durable ?"
        ]

# Instance globale de la mémoire conversationnelle
conversation_memory = ConversationMemory()
