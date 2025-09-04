"""
Module d'intelligence avancée pour BiaSavia
"""
from .intelligent_processor import intelligent_processor
from .nlp_processor import nlp_processor
from typing import Dict, Any, List
import json
import random

class AdvancedIntelligence:
    """Système d'intelligence avancée pour des réponses personnalisées"""
    
    def __init__(self):
        self.learning_database = {}  # Stockage des patterns d'apprentissage
        self.response_templates = self._initialize_response_templates()
        
    def _initialize_response_templates(self) -> Dict[str, List[str]]:
        """
        Initialise les templates de réponses pour différents contextes
        """
        return {
            'greeting': [
                "Bonjour ! Je suis votre assistant environnemental BiaSavia. Comment puis-je vous aider aujourd'hui ?",
                "Salut ! Prêt à explorer des questions environnementales ? Que souhaitez-vous savoir ?",
                "Bienvenue ! Je suis là pour répondre à vos questions sur l'environnement et l'écologie."
            ],
            'thanks': [
                "Je suis ravi d'avoir pu vous aider ! N'hésitez pas si vous avez d'autres questions environnementales.",
                "De rien ! C'est un plaisir de partager des connaissances sur l'environnement.",
                "Avec plaisir ! Ensemble, nous pouvons mieux comprendre et protéger notre planète."
            ],
            'complex_question': [
                "C'est une question très intéressante et complexe. Laissez-moi vous donner une réponse détaillée.",
                "Cette question touche à plusieurs aspects environnementaux. Voici ce que je peux vous expliquer :",
                "Excellente question ! Il y a plusieurs éléments à considérer :"
            ],
            'uncertainty': [
                "Je ne suis pas entièrement certain de cette information. Voici ce que je peux vous dire, mais je recommande de vérifier avec des sources officielles.",
                "Cette question nécessite des recherches approfondies. Voici les informations disponibles, mais je suggère de consulter des experts.",
                "C'est un sujet en évolution. Basé sur les informations actuelles :"
            ]
        }
    
    def generate_intelligent_response(self, question: str, session_id: str = None, 
                                    user_profile: Dict = None) -> Dict[str, Any]:
        """
        Génère une réponse intelligente et personnalisée
        """
        # Traitement initial de la question
        base_result = intelligent_processor.process_question(question, session_id)
        
        # Analyse du contexte utilisateur
        user_context = self._analyze_user_context(session_id, user_profile)
        
        # Personnalisation de la réponse
        personalized_response = self._personalize_response(
            base_result, user_context, question
        )
        
        # Ajout d'éléments interactifs
        interactive_elements = self._generate_interactive_elements(
            base_result['category'], user_context
        )
        
        # Recommandations d'actions
        action_recommendations = self._generate_action_recommendations(
            base_result['category'], user_context
        )
        
        # Résultat final enrichi
        enhanced_result = {
            **base_result,
            'personalized_response': personalized_response,
            'interactive_elements': interactive_elements,
            'action_recommendations': action_recommendations,
            'user_context': user_context,
            'response_quality': self._assess_response_quality(base_result)
        }
        
        # Apprentissage et amélioration
        self._learn_from_interaction(question, enhanced_result, session_id)
        
        return enhanced_result
    
    def _analyze_user_context(self, session_id: str = None, user_profile: Dict = None) -> Dict[str, Any]:
        """
        Analyse le contexte utilisateur pour personnaliser la réponse
        """
        context = {
            'expertise_level': 'beginner',  # beginner, intermediate, expert
            'interests': [],
            'interaction_style': 'formal',  # formal, casual, technical
            'session_history': {}
        }
        
        if session_id:
            # Analyse des tendances de conversation
            trends = intelligent_processor.analyze_conversation_trends(session_id)
            context['session_history'] = trends
            
            # Déduction du niveau d'expertise
            if trends.get('engagement_level') == 'high':
                context['expertise_level'] = 'intermediate'
            if len(trends.get('user_interests', [])) > 3:
                context['expertise_level'] = 'expert'
            
            context['interests'] = trends.get('user_interests', [])
        
        if user_profile:
            context.update(user_profile)
        
        return context
    
    def _personalize_response(self, base_result: Dict, user_context: Dict, question: str) -> str:
        """
        Personnalise la réponse selon le contexte utilisateur
        """
        base_answer = base_result['answer']
        expertise_level = user_context.get('expertise_level', 'beginner')
        
        # Adaptation selon le niveau d'expertise
        if expertise_level == 'beginner':
            # Ajouter des explications simples
            personalized = self._simplify_response(base_answer)
        elif expertise_level == 'expert':
            # Ajouter des détails techniques
            personalized = self._add_technical_details(base_answer, base_result['category'])
        else:
            personalized = base_answer
        
        # Ajouter un préambule approprié
        if base_result.get('confidence', 0) > 0.8:
            template = random.choice(self.response_templates['complex_question'])
        else:
            template = random.choice(self.response_templates['uncertainty'])
        
        return f"{template}\n\n{personalized}"
    
    def _simplify_response(self, response: str) -> str:
        """
        Simplifie une réponse pour les débutants
        """
        # Ajouter des explications de base
        simplified = response
        
        # Remplacer les termes techniques par des explications simples
        technical_terms = {
            'biodiversité': 'la variété des espèces vivantes',
            'écosystème': 'un ensemble d\'organismes vivants et leur environnement',
            'carbone': 'un élément chimique présent dans le CO2',
            'photosynthèse': 'le processus par lequel les plantes produisent de l\'oxygène'
        }
        
        for term, explanation in technical_terms.items():
            if term in simplified.lower():
                simplified = simplified.replace(term, f"{term} ({explanation})")
        
        return simplified
    
    def _add_technical_details(self, response: str, category: str) -> str:
        """
        Ajoute des détails techniques pour les experts
        """
        technical_additions = {
            'pollution': "\n\nNote technique : Les polluants peuvent être mesurés en ppm (parties par million) ou µg/m³.",
            'climat': "\n\nNote technique : Les modèles climatiques utilisent des équations de transfert radiatif complexes.",
            'energie': "\n\nNote technique : L'efficacité énergétique se mesure souvent en kWh/m² ou en coefficient de performance (COP).",
            'biodiversite': "\n\nNote technique : La biodiversité peut être quantifiée via l'indice de Shannon ou l'indice de Simpson."
        }
        
        if category in technical_additions:
            return response + technical_additions[category]
        
        return response
    
    def _generate_interactive_elements(self, category: str, user_context: Dict) -> List[Dict]:
        """
        Génère des éléments interactifs pour engager l'utilisateur
        """
        elements = []
        
        # Quiz environnemental
        if category in ['pollution', 'climat', 'energie']:
            elements.append({
                'type': 'quiz',
                'title': f'Quiz sur {category}',
                'description': 'Testez vos connaissances !',
                'questions': self._generate_quiz_questions(category)
            })
        
        # Calculateur d'impact
        if category in ['energie', 'climat']:
            elements.append({
                'type': 'calculator',
                'title': 'Calculateur d\'empreinte carbone',
                'description': 'Calculez votre impact environnemental'
            })
        
        # Actions suggérées
        elements.append({
            'type': 'action_list',
            'title': 'Actions que vous pouvez entreprendre',
            'actions': self._generate_action_list(category)
        })
        
        return elements
    
    def _generate_quiz_questions(self, category: str) -> List[Dict]:
        """
        Génère des questions de quiz selon la catégorie
        """
        quiz_database = {
            'pollution': [
                {
                    'question': 'Quel est le principal gaz responsable de l\'effet de serre ?',
                    'options': ['CO2', 'O2', 'N2', 'H2O'],
                    'correct': 0
                }
            ],
            'climat': [
                {
                    'question': 'Quelle est la température moyenne d\'augmentation prévue d\'ici 2100 ?',
                    'options': ['1-2°C', '2-4°C', '4-6°C', '6-8°C'],
                    'correct': 1
                }
            ],
            'energie': [
                {
                    'question': 'Quelle énergie renouvelable a le plus de potentiel mondial ?',
                    'options': ['Solaire', 'Éolien', 'Hydraulique', 'Géothermique'],
                    'correct': 0
                }
            ]
        }
        
        return quiz_database.get(category, [])
    
    def _generate_action_list(self, category: str) -> List[str]:
        """
        Génère une liste d'actions selon la catégorie
        """
        actions = {
            'pollution': [
                'Utiliser les transports en commun',
                'Réduire la consommation de plastique',
                'Choisir des produits éco-labellisés'
            ],
            'climat': [
                'Réduire sa consommation énergétique',
                'Adopter une alimentation moins carnée',
                'Compenser ses émissions de carbone'
            ],
            'energie': [
                'Installer des ampoules LED',
                'Isoler son logement',
                'Utiliser des appareils économes en énergie'
            ]
        }
        
        return actions.get(category, ['Sensibiliser son entourage', 'S\'informer régulièrement'])
    
    def _generate_action_recommendations(self, category: str, user_context: Dict) -> List[Dict]:
        """
        Génère des recommandations d'actions personnalisées
        """
        expertise_level = user_context.get('expertise_level', 'beginner')
        
        recommendations = []
        
        if expertise_level == 'beginner':
            recommendations = [
                {'action': 'Commencer par de petits gestes', 'difficulty': 'facile'},
                {'action': 'Se documenter sur le sujet', 'difficulty': 'facile'},
                {'action': 'Partager ses apprentissages', 'difficulty': 'moyen'}
            ]
        elif expertise_level == 'expert':
            recommendations = [
                {'action': 'Devenir ambassadeur environnemental', 'difficulty': 'difficile'},
                {'action': 'Participer à des projets de recherche', 'difficulty': 'difficile'},
                {'action': 'Créer des initiatives locales', 'difficulty': 'moyen'}
            ]
        
        return recommendations
    
    def _assess_response_quality(self, result: Dict) -> Dict[str, Any]:
        """
        Évalue la qualité de la réponse générée
        """
        confidence = result.get('confidence', 0)
        sources_count = len(result.get('sources', []))
        answer_length = len(result.get('answer', ''))
        
        quality_score = (confidence * 0.4 + 
                        min(sources_count / 3, 1) * 0.3 + 
                        min(answer_length / 500, 1) * 0.3)
        
        quality_level = 'excellent' if quality_score > 0.8 else \
                       'good' if quality_score > 0.6 else \
                       'fair' if quality_score > 0.4 else 'poor'
        
        return {
            'score': quality_score,
            'level': quality_level,
            'factors': {
                'confidence': confidence,
                'sources_count': sources_count,
                'answer_completeness': min(answer_length / 500, 1)
            }
        }
    
    def _learn_from_interaction(self, question: str, result: Dict, session_id: str = None):
        """
        Apprend des interactions pour améliorer les futures réponses
        """
        # Stockage des patterns d'apprentissage
        pattern_key = result.get('category', 'general')
        
        if pattern_key not in self.learning_database:
            self.learning_database[pattern_key] = {
                'frequent_questions': {},
                'successful_responses': [],
                'user_feedback': []
            }
        
        # Enregistrer la question fréquente
        question_lower = question.lower()
        freq_questions = self.learning_database[pattern_key]['frequent_questions']
        freq_questions[question_lower] = freq_questions.get(question_lower, 0) + 1
        
        # Enregistrer la réponse si elle est de bonne qualité
        if result.get('response_quality', {}).get('score', 0) > 0.7:
            self.learning_database[pattern_key]['successful_responses'].append({
                'question': question,
                'answer': result.get('answer', ''),
                'confidence': result.get('confidence', 0)
            })

# Instance globale de l'intelligence avancée
advanced_intelligence = AdvancedIntelligence()
