from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.shortcuts import get_object_or_404
import json
import re
import uuid
from datetime import datetime

from .serializers import (
    RegisterSerializer, 
    UserSerializer, 
    PasswordResetSerializer, 
    PasswordResetConfirmSerializer,
    PostSerializer,
    CommentSerializer
)
from .models import EnvironmentalData, ChatHistory, Post, Comment
# from .google_search import google_search_service
# from .enhanced_google_search import enhanced_google_search_service
# from .smart_google_search import smart_google_search_service
# from .nlp_processor import nlp_processor
# from .conversation_memory import conversation_memory
# from .intelligent_processor import intelligent_processor
# from .advanced_intelligence import advanced_intelligence

# --- Classe pour récupérer, modifier ou supprimer un post individuel ---
class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_update(self, serializer):
        # Seul l'auteur peut modifier le post
        if self.get_object().author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Vous ne pouvez modifier que vos propres posts.")
        serializer.save()
    
    def perform_destroy(self, instance):
        # Seul l'auteur peut supprimer le post
        if instance.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Vous ne pouvez supprimer que vos propres posts.")
        instance.delete()
User = get_user_model()

# Salutations et messages d'accueil
GREETINGS = {
    "bonjour": "Bonjour ! 🌱 Je suis Bia Safiya, votre assistant environnemental. Comment puis-je vous aider aujourd'hui ?",
    "salut": "Salut ! 🌿 Ravi de vous rencontrer. Je suis spécialisé dans les questions environnementales. Que souhaitez-vous savoir ?",
    "hello": "Hello ! 🌍 Bienvenue ! Je suis là pour répondre à vos questions sur l'environnement.",
    "coucou": "Coucou ! 🌱 Enchanté de faire votre connaissance ! Je suis votre guide environnemental.",
    "hi": "Hi ! 🌿 Welcome ! I'm here to help you with environmental questions.",
    "hey": "Hey ! 🌍 Salut ! Je suis Bia Safiya, votre assistant vert !",
    "bonsoir": "Bonsoir ! 🌱 Comment puis-je vous aider ce soir ?",
    "bonne journée": "Bonne journée à vous aussi ! 🌿 N'hésitez pas si vous avez des questions environnementales !",
    "merci": "De rien ! 🌱 C'est un plaisir de vous aider. N'hésitez pas si vous avez d'autres questions !",
    "au revoir": "Au revoir ! 🌿 Merci d'avoir utilisé Bia Safiya. À bientôt !",
    "bye": "Bye ! 🌍 Take care and keep being eco-friendly !",
    "à bientôt": "À bientôt ! 🌱 N'oubliez pas de prendre soin de notre planète !"
}

# ...existing code...

# (après tous les imports et définitions)

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
import re
import uuid
from datetime import datetime

from .serializers import (
    RegisterSerializer, 
    UserSerializer, 
    PasswordResetSerializer, 
    PasswordResetConfirmSerializer
)
from .models import EnvironmentalData, ChatHistory, Post
# from .google_search import google_search_service
# from .enhanced_google_search import enhanced_google_search_service
# from .smart_google_search import smart_google_search_service
# from .nlp_processor import nlp_processor
# from .conversation_memory import conversation_memory
# from .intelligent_processor import intelligent_processor
# from .advanced_intelligence import advanced_intelligence

# Import des nouveaux modules disponibles (commentés temporairement - manque cv2, tensorflow_hub)
# from .simple_environmental_ai import SimpleEnvironmentalClassifier
# from .environmental_ai import EnvironmentalAI

# Fonctions de remplacement temporaires
def analyze_message(message):
    """Analyse simple d'un message"""
    return {
        'sentiment': 'neutral',
        'keywords': message.lower().split(),
        'intent': 'question'
    }

def generate_contextual_response(session_id, analysis):
    """Génère une réponse contextuelle simple"""
    return None

def search_environmental_info(message):
    """Recherche d'informations environnementales simplifiée"""
    return {
        'query': message,
        'results': [],
        'summary': 'Recherche non disponible temporairement'
    }

def generate_intelligent_response(message):
    """Génère une réponse intelligente simplifiée"""
    return f"Je comprends votre question sur : {message}"

def generate_smart_response(analysis, message):
    """Génère une réponse intelligente à partir de l'analyse"""
    return f"Réponse intelligente pour : {message}"

def analyze_question(message):
    """Analyse une question"""
    return {'complexity': 'medium', 'topic': 'environmental'}

def add_message(session_id, message, response, analysis):
    """Ajoute un message à la mémoire de conversation"""
    pass

User = get_user_model()

# Salutations et messages d'accueil
GREETINGS = {
    "bonjour": "Bonjour ! 🌱 Je suis Bia Safiya, votre assistant environnemental. Comment puis-je vous aider aujourd'hui ?",
    "salut": "Salut ! 🌿 Ravi de vous rencontrer. Je suis spécialisé dans les questions environnementales. Que souhaitez-vous savoir ?",
    "hello": "Hello ! 🌍 Bienvenue ! Je suis là pour répondre à vos questions sur l'environnement.",
    "coucou": "Coucou ! 🌱 Enchanté de faire votre connaissance ! Je suis votre guide environnemental.",
    "hi": "Hi ! 🌿 Welcome ! I'm here to help you with environmental questions.",
    "hey": "Hey ! 🌍 Salut ! Je suis Bia Safiya, votre assistant vert !",
    "bonsoir": "Bonsoir ! 🌱 Comment puis-je vous aider ce soir ?",
    "bonne journée": "Bonne journée à vous aussi ! 🌿 N'hésitez pas si vous avez des questions environnementales !",
    "merci": "De rien ! 🌱 C'est un plaisir de vous aider. N'hésitez pas si vous avez d'autres questions !",
    "au revoir": "Au revoir ! 🌿 Merci d'avoir utilisé Bia Safiya. À bientôt !",
    "bye": "Bye ! 🌍 Take care and keep being eco-friendly !",
    "à bientôt": "À bientôt ! 🌱 N'oubliez pas de prendre soin de notre planète !"
}

# Mots-clés environnementaux étendus
ENVIRONMENT_KEYWORDS = [
    "écologie", "environnement", "climat", "biodiversité", "pollution", "océan",
    "forêt", "recyclage", "durable", "CO2", "déforestation", "énergies renouvelables",
    "réchauffement", "plastique", "eau", "air", "sol", "déchets", "co2", "changement climatique",
    "nature", "vert", "écologique", "protection", "défendre", "sauvegarder", "préserver",
    "vert", "green", "écologie", "environnemental", "durabilité", "sustainable"
]

# Questions communes et leurs réponses
COMMON_QUESTIONS = {
    "comment faire pour defendre l'environnement": {
        "answer": """🌿 Voici comment défendre l'environnement au quotidien :

🏠 **À la maison :**
• Éteindre les lumières et appareils inutilisés
• Utiliser des ampoules LED économiques
• Réduire le chauffage et la climatisation
• Installer des panneaux solaires si possible

🚗 **Transport :**
• Privilégier les transports en commun, vélo, marche
• Covoiturage pour les trajets longs
• Choisir des véhicules électriques ou hybrides

🛒 **Consommation :**
• Acheter local et de saison
• Réduire les emballages plastiques
• Choisir des produits durables
• Réparer plutôt que jeter

♻️ **Déchets :**
• Trier et recycler systématiquement
• Composter les déchets organiques
• Réduire les déchets à la source

💧 **Eau :**
• Prendre des douches courtes
• Récupérer l'eau de pluie
• Réparer les fuites

Chaque petit geste compte pour préserver notre planète ! 🌍""",
        "source": "Guide des bonnes pratiques environnementales"
    },
    
    "comment reduire la pollution": {
        "answer": """🌿 Voici comment réduire la pollution au quotidien :

🚗 **Transport :**
• Utiliser les transports en commun
• Privilégier le vélo et la marche
• Covoiturage pour les trajets
• Choisir des véhicules moins polluants

🏠 **Énergie :**
• Utiliser des énergies renouvelables
• Éteindre les appareils en veille
• Isoler sa maison
• Installer des panneaux solaires

🛒 **Consommation :**
• Acheter des produits locaux
• Éviter les emballages plastiques
• Choisir des produits écologiques
• Réduire la consommation de viande

♻️ **Déchets :**
• Trier et recycler
• Composter les déchets organiques
• Acheter en vrac
• Réutiliser et réparer

💧 **Eau :**
• Éviter les produits polluants
• Ne pas jeter de déchets dans l'eau
• Utiliser des produits d'entretien écologiques

Chaque action compte pour un air et une eau plus propres ! 🌱""",
        "source": "Programme des Nations Unies pour l'Environnement"
    },
    
    "pourquoi recycler": {
        "answer": """🌿 Le recyclage est essentiel pour plusieurs raisons :

♻️ **Économie des ressources :**
• Évite l'extraction de nouvelles matières premières
• Réduit la consommation d'énergie
• Préserve les ressources naturelles

🌍 **Protection de l'environnement :**
• Réduit la pollution de l'air et de l'eau
• Diminue les émissions de CO2
• Évite l'enfouissement des déchets

💰 **Avantages économiques :**
• Crée des emplois dans l'économie circulaire
• Réduit les coûts de gestion des déchets
• Génère de nouvelles matières premières

📊 **Impact concret :**
• Recycler 1 tonne de papier = 17 arbres sauvés
• Recycler 1 tonne d'aluminium = 95% d'énergie économisée
• Recycler 1 tonne de verre = 1 tonne de CO2 évitée

🔄 **Comment bien recycler :**
• Trier correctement (papier, verre, plastique, métal)
• Nettoyer les emballages
• Respecter les consignes locales
• Éviter les erreurs de tri

Le recyclage, c'est un geste simple mais puissant ! 💪""",
        "source": "ADEME (Agence de l'Environnement et de la Maîtrise de l'Énergie)"
    },
    "que je dois savoir sur co2": {
        "answer": """🌿 Voici ce que vous devez savoir sur le CO2 :

📊 **Qu'est-ce que le CO2 ?**
• Dioxyde de carbone - gaz à effet de serre naturel
• Essentiel pour la photosynthèse des plantes
• Présent dans l'atmosphère depuis des millions d'années

📈 **Problème actuel :**
• Concentration atmosphérique : 420 ppm (vs 280 ppm avant 1850)
• Augmentation de 50% depuis l'ère industrielle
• Principal responsable du réchauffement climatique

🌍 **Sources principales :**
• Combustion des énergies fossiles (pétrole, charbon, gaz)
• Déforestation et changement d'usage des sols
• Industries (ciment, acier, chimie)
• Transport routier et aérien

🌡️ **Effets sur le climat :**
• Réchauffement global de la planète
• Fonte des glaces et montée des océans
• Modification des précipitations
• Multiplication des événements extrêmes

📊 **Chiffres clés :**
• 40 milliards de tonnes de CO2 émises par an
• 1 tonne de CO2 = 5000 km en voiture
• 1 arbre absorbe 22 kg de CO2 par an

💡 **Solutions individuelles :**
• Réduire sa consommation d'énergie
• Privilégier les transports doux
• Acheter local et de saison
• Planter des arbres

Le CO2, c'est le défi climatique du siècle ! 🌱""",
        "source": "GIEC (Groupe d'experts intergouvernemental sur l'évolution du climat)"
    },
    
    "comment lutter contre le co2": {
        "answer": """🌿 Voici comment lutter contre le CO2 au quotidien :

🚗 **Transport (40% des émissions) :**
• Marcher ou faire du vélo pour les courts trajets
• Utiliser les transports en commun
• Covoiturage pour les trajets longs
• Choisir des véhicules électriques ou hybrides
• Éviter l'avion pour les trajets courts

🏠 **Énergie domestique (25% des émissions) :**
• Isoler sa maison (toit, murs, fenêtres)
• Utiliser des ampoules LED
• Éteindre les appareils en veille
• Installer des panneaux solaires
• Réduire le chauffage de 1°C

🛒 **Consommation (20% des émissions) :**
• Acheter local et de saison
• Réduire la consommation de viande
• Éviter les produits sur-emballés
• Choisir des produits durables
• Réparer plutôt que jeter

♻️ **Déchets (5% des émissions) :**
• Trier et recycler systématiquement
• Composter les déchets organiques
• Acheter en vrac
• Réutiliser les objets

🌱 **Actions positives :**
• Planter des arbres (1 arbre = 22 kg CO2/an)
• Soutenir les projets de reforestation
• Participer à des actions de nettoyage
• Sensibiliser son entourage

📊 **Impact concret :**
• Réduire sa consommation de viande = -500 kg CO2/an
• Prendre le vélo au lieu de la voiture = -2 tonnes CO2/an
• Isoler sa maison = -1 tonne CO2/an

Chaque geste compte pour réduire notre empreinte carbone ! 💪""",
        "source": "ADEME - Guide de l'éco-citoyen"
    }
}

def extract_keywords(message):
    """Extrait les mots-clés pertinents du message"""
    message_lower = message.lower()
    keywords = []
    
    # Chercher les mots-clés environnementaux
    for keyword in ENVIRONMENT_KEYWORDS:
        if keyword in message_lower:
            keywords.append(keyword)
    
    # Chercher des patterns spécifiques
    patterns = {
        r'\b(comment|comment faire|que faire)\b': 'action',
        r'\b(pourquoi|pour quoi)\b': 'explication',
        r'\b(quelles? sont|quels? sont)\b': 'causes',
        r'\b(comment réduire|réduire|diminuer)\b': 'reduction',
        r'\b(défendre|protéger|sauvegarder|préserver)\b': 'protection',
        r'\b(pollution|polluer)\b': 'pollution',
        r'\b(climat|réchauffement|co2)\b': 'climat',
        r'\b(recyclage|recycler)\b': 'recyclage',
        r'\b(environnement|écologie)\b': 'environnement'
    }
    
    for pattern, category in patterns.items():
        if re.search(pattern, message_lower):
            keywords.append(category)
    
    return keywords

def find_best_response(message, keywords, session_id=None):
    """Trouve la meilleure réponse basée sur le message et les mots-clés"""
    
    message_lower = message.lower()
    message_clean = re.sub(r'[^\w\s]', '', message_lower)
    
    # 0. ANALYSE NLP AVANCÉE
    nlp_analysis = analyze_message(message)
    print(f"🧠 Analyse NLP: {nlp_analysis}")
    
    # 0.5. GÉNÉRER RÉPONSE CONTEXTUELLE SI SESSION_ID FOURNI
    contextual_response = ""
    if session_id:
        contextual_response = generate_contextual_response(session_id, nlp_analysis)
        if contextual_response:
            print(f"🧠 Réponse contextuelle générée pour session {session_id}")
    
    # 1. ESSAYER GOOGLE SEARCH INTELLIGENT EN PREMIER (priorité haute)
    if getattr(settings, 'GOOGLE_SEARCH_ENABLED', False):
        try:
            # Utiliser le service intelligent qui comprend vraiment les questions
            google_response = search_environmental_info(message)
            if google_response:
                print(f"🧠 Google Search intelligent utilisé pour: {message}")
                # Ajouter la réponse contextuelle si elle existe
                if contextual_response:
                    google_response = contextual_response + "\n\n" + str(google_response)
                return google_response, "Recherche Google intelligente avec compréhension des questions"
        except Exception as e:
            print(f"Erreur Google Search intelligent: {e}")
            # Fallback vers le service amélioré
            try:
                google_response = enhanced_google_search_service.search_environmental_info(message)
                if google_response:
                    print(f"🔍 Google Search amélioré utilisé pour: {message}")
                    if contextual_response:
                        google_response = contextual_response + "\n\n" + google_response
                    return google_response, "Recherche Google améliorée avec 3 réponses structurées"
            except Exception as e2:
                print(f"Erreur Google Search amélioré: {e2}")
                # Fallback vers l'ancien service
                try:
                    google_response = google_search_service.search_environmental_info(message)
                    if google_response:
                        print(f"🔍 Google Search fallback utilisé pour: {message}")
                        if contextual_response:
                            google_response = contextual_response + "\n\n" + google_response
                        return google_response, "Recherche Google spécialisée environnement"
                except Exception as e3:
                    print(f"Erreur Google Search fallback: {e3}")
    
    # 2. ANALYSE INTELLIGENTE DE LA QUESTION (fallback)
    intelligent_response = intelligent_processor.generate_intelligent_response(message)
    if intelligent_response:
        print(f"🧠 Réponse intelligente générée pour: {message}")
        return intelligent_response, "Analyse intelligente spécialisée"
    
    # 3. RÉPONSE INTELLIGENTE BASÉE SUR L'ANALYSE NLP
    if nlp_analysis['entities'] or nlp_analysis['keywords']:
        smart_response = nlp_processor.generate_smart_response(nlp_analysis, message)
        print(f"🧠 Réponse intelligente générée pour: {message}")
        # Ajouter la réponse contextuelle si elle existe
        if contextual_response:
            smart_response = contextual_response + "\n\n" + smart_response
        return smart_response, "Analyse NLP intelligente"
    
    # 3. Vérifier les questions communes avec correspondance exacte
    for question, response in COMMON_QUESTIONS.items():
        if question in message_clean or message_clean in question:
            print(f"📚 Question commune utilisée pour: {message}")
            final_response = response["answer"]
            # Ajouter la réponse contextuelle si elle existe
            if contextual_response:
                final_response = contextual_response + "\n\n" + final_response
            return final_response, response["source"]
    
    # 4. Recherche intelligente basée sur le type de question
    if "que je dois savoir" in message_lower or "qu'est-ce que" in message_lower or "c'est quoi" in message_lower:
        # Questions de définition
        if "co2" in message_lower or "dioxyde" in message_lower:
            final_response = COMMON_QUESTIONS["que je dois savoir sur co2"]["answer"]
            if contextual_response:
                final_response = contextual_response + "\n\n" + final_response
            return final_response, COMMON_QUESTIONS["que je dois savoir sur co2"]["source"]
        elif "pollution" in message_lower:
            final_response = """🌿 La pollution est la dégradation de l'environnement par des substances nocives :

🌍 **Types de pollution :**
• Pollution de l'air (gaz d'échappement, industries)
• Pollution de l'eau (déchets, produits chimiques)
• Pollution des sols (pesticides, déchets)
• Pollution sonore (trafic, industries)

📊 **Chiffres alarmants :**
• 9 millions de décès par an liés à la pollution
• 8 millions de tonnes de plastique dans l'océan
• 91% de la population respire un air pollué

💡 **Solutions :**
• Réduire les émissions de CO2
• Trier et recycler les déchets
• Utiliser des transports propres
• Choisir des produits écologiques

La pollution, c'est l'affaire de tous ! 🌱"""
            if contextual_response:
                final_response = contextual_response + "\n\n" + final_response
            return final_response, "Organisation Mondiale de la Santé"
    
    elif "comment lutter" in message_lower or "comment combattre" in message_lower or "comment réduire" in message_lower:
        # Questions d'action
        if "co2" in message_lower or "carbone" in message_lower:
            final_response = COMMON_QUESTIONS["comment lutter contre le co2"]["answer"]
            if contextual_response:
                final_response = contextual_response + "\n\n" + final_response
            return final_response, COMMON_QUESTIONS["comment lutter contre le co2"]["source"]
        elif "pollution" in message_lower:
            final_response = COMMON_QUESTIONS["comment reduire la pollution"]["answer"]
            if contextual_response:
                final_response = contextual_response + "\n\n" + final_response
            return final_response, COMMON_QUESTIONS["comment reduire la pollution"]["source"]
        else:
            final_response = COMMON_QUESTIONS["comment faire pour defendre l'environnement"]["answer"]
            if contextual_response:
                final_response = contextual_response + "\n\n" + final_response
            return final_response, COMMON_QUESTIONS["comment faire pour defendre l'environnement"]["source"]
    
    elif "pourquoi" in message_lower:
        # Questions d'explication
        if "recycler" in message_lower or "recyclage" in message_lower:
            final_response = COMMON_QUESTIONS["pourquoi recycler"]["answer"]
            if contextual_response:
                final_response = contextual_response + "\n\n" + final_response
            return final_response, COMMON_QUESTIONS["pourquoi recycler"]["source"]
        else:
            final_response = """🌿 Voici pourquoi c'est important :

🌍 **Pour la planète :**
• Préserver les écosystèmes
• Maintenir la biodiversité
• Lutter contre le changement climatique

👥 **Pour les humains :**
• Améliorer la qualité de l'air
• Assurer la sécurité alimentaire
• Préserver la santé publique

🔮 **Pour l'avenir :**
• Transmettre un monde viable
• Créer une société durable
• Garantir les ressources futures

💡 **Chaque action compte, même la plus petite !**"""
            if contextual_response:
                final_response = contextual_response + "\n\n" + final_response
            return final_response, "Guide environnemental"
    
    # 5. Chercher dans la base de données avec un algorithme amélioré
    best_match = None
    best_score = 0
    
    for data_entry in EnvironmentalData.objects.all():
        score = 0
        
        # Score basé sur les mots-clés
        entry_keywords = data_entry.keyword.lower().split()
        message_words = message.lower().split()
        
        for word in message_words:
            if word in entry_keywords:
                score += 2  # Score plus élevé pour les mots-clés exacts
            elif any(keyword in word for keyword in keywords):
                score += 1  # Score pour les mots-clés environnementaux
        
        # Bonus pour les questions similaires
        if any(word in data_entry.question.lower() for word in message_words):
            score += 3
        
        # Bonus pour les catégories correspondantes
        if any(keyword in data_entry.category for keyword in keywords):
            score += 2
        
        if score > best_score:
            best_score = score
            best_match = data_entry
    
    if best_match and best_score >= 2:
        print(f"🗄️ Base de données utilisée pour: {message}")
        final_response = f"🌿 {best_match.answer}\n\n📚 Source: {best_match.source}"
        if contextual_response:
            final_response = contextual_response + "\n\n" + final_response
        return final_response, best_match.source
    
    return None, None

def save_chat_history(session_id, user_message, bot_response, category=None):
    """Sauvegarde une conversation dans l'historique"""
    try:
        ChatHistory.objects.create(
            session_id=session_id,
            user_message=user_message,
            bot_response=bot_response,
            category=category
        )
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de l'historique: {e}")
        return False

def get_chat_history(session_id=None, limit=50):
    """Récupère l'historique des conversations"""
    try:
        if session_id:
            # Historique pour une session spécifique
            history = ChatHistory.objects.filter(session_id=session_id).order_by('-timestamp')[:limit]
        else:
            # Historique global (dernières conversations)
            history = ChatHistory.objects.all().order_by('-timestamp')[:limit]
        
        return [
            {
                'id': chat.id,
                'session_id': chat.session_id,
                'user_message': chat.user_message,
                'bot_response': chat.bot_response,
                'timestamp': chat.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'category': chat.category
            }
            for chat in history
        ]
    except Exception as e:
        print(f"Erreur lors de la récupération de l'historique: {e}")
        return []

def clear_chat_history(session_id=None):
    """Efface l'historique des conversations"""
    try:
        if session_id:
            ChatHistory.objects.filter(session_id=session_id).delete()
        else:
            ChatHistory.objects.all().delete()
        return True
    except Exception as e:
        print(f"Erreur lors de l'effacement de l'historique: {e}")
        return False

@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "").lower()
            session_id = data.get("session_id", str(uuid.uuid4()))
            
            print(f"Message reçu: {message}")  # Debug log

            # 1. Vérifier les salutations en premier
            message_clean = re.sub(r'[^\w\s]', '', message.lower())
            for greeting, response in GREETINGS.items():
                if greeting in message_clean or message_clean in greeting:
                    # Sauvegarder l'historique
                    save_chat_history(session_id, message, response, "greeting")
                    return JsonResponse({"response": response, "session_id": session_id})

            # 2. UTILISER LE SYSTÈME D'INTELLIGENCE AVANCÉE
            print(f"🧠 Utilisation du système d'intelligence avancée...")
            
            # Analyser la question avec le nouveau système
            analysis = advanced_intelligence.analyze_question(message)
            print(f"📊 Analyse : {analysis}")
            
            # Générer une réponse intelligente
            final_response = advanced_intelligence.generate_smart_response(message)
            category = "advanced_intelligence"
            
            # Si la réponse est générique, essayer les autres systèmes
            if "Pour vous aider au mieux" in final_response or "Pour vous donner une réponse" in final_response:
                # Essayer le processeur intelligent existant
                intelligent_response = intelligent_processor.generate_intelligent_response(message)
                if intelligent_response:
                    final_response = intelligent_response
                    category = "intelligent_environmental"
                else:
                    # Essayer la recherche Google intelligente
                    try:
                        google_response = smart_google_search_service.search_environmental_info(message)
                        if google_response and len(google_response) > 100:
                            final_response = google_response
                            category = "google_search"
                        else:
                            # Réponse générique mais intelligente et claire
                            if "comment" in message or "que faire" in message:
                                final_response = """🌿 **Voici des actions concrètes pour agir :**

1️⃣ **À LA MAISON**
   ✅ Éteindre les lumières inutiles
   ✅ Prendre des douches courtes (5 minutes max)
   ✅ Trier ses déchets (4 poubelles)
   ✅ Baisser le chauffage de 1°C
   ✅ Utiliser des produits écologiques

2️⃣ **DANS LES TRANSPORTS**
   ✅ Marcher pour les trajets < 1 km
   ✅ Prendre le vélo pour les trajets < 5 km
   ✅ Utiliser les transports en commun
   ✅ Faire du covoiturage
   ✅ Choisir une voiture électrique si possible

3️⃣ **DANS LA CONSOMMATION**
   ✅ Acheter local et de saison
   ✅ Éviter les emballages plastiques
   ✅ Choisir des produits durables
   ✅ Réparer au lieu de jeter
   ✅ Acheter d'occasion

4️⃣ **DANS LA VIE QUOTIDIENNE**
   ✅ Participer à des actions de nettoyage
   ✅ Planter des arbres
   ✅ Sensibiliser son entourage
   ✅ Soutenir des associations
   ✅ Voter pour des politiques vertes

💡 **Conseil :** Commencez par 1 action simple, puis ajoutez-en d'autres progressivement !

🌱 **Impact :** Chaque petit geste compte pour préserver notre planète !"""
                                category = "action"
                            elif "pourquoi" in message:
                                final_response = """🌿 **Voici pourquoi c'est important :**

🌍 **Pour la planète :**
   • Préserver les écosystèmes
   • Maintenir la biodiversité
   • Lutter contre le changement climatique
   • Protéger les ressources naturelles

👥 **Pour les humains :**
   • Améliorer la qualité de l'air
   • Assurer la sécurité alimentaire
   • Préserver la santé publique
   • Créer un monde plus juste

🔮 **Pour l'avenir :**
   • Transmettre un monde viable
   • Créer une société durable
   • Garantir les ressources futures
   • Donner l'exemple aux générations suivantes

💡 **En résumé :** Protéger l'environnement, c'est protéger notre santé, notre alimentation et notre avenir !"""
                                category = "explanation"
                            else:
                                final_response = f"""🌿 **Informations sur « {message} » :**

Cette question touche à un sujet environnemental important. Voici ce que je peux vous dire :

📋 **Contexte général :**
   • Tous les sujets environnementaux sont liés
   • Chaque action a des conséquences
   • Nous faisons partie de l'écosystème

💡 **Pour aller plus loin :**
   • Posez des questions plus spécifiques
   • Demandez des exemples concrets
   • Interrogez-moi sur les solutions pratiques
   • Demandez des chiffres et des données

🌱 **Mon rôle :** Je suis là pour vous informer, vous guider et vous encourager !

💬 **Exemples de questions :**
   • "Comment réduire la pollution ?"
   • "Pourquoi recycler est important ?"
   • "Qu'est-ce que le développement durable ?"
   • "Comment protéger la biodiversité ?" """
                                category = "general"
                    except Exception as e:
                        print(f"❌ Erreur lors de la recherche Google : {e}")
                        final_response = """🌿 **Je suis là pour vous aider !**

💡 **Pour vous donner une réponse précise, pourriez-vous reformuler votre question ?**

Par exemple :
• "Qu'est-ce que la pollution plastique ?"
• "Comment réduire mes déchets ?"
• "Pourquoi recycler est important ?"
• "Statistiques déchets France 2024"

🌱 **Je peux vous aider sur :**
• Définitions et concepts
• Solutions pratiques
• Statistiques et données
• Conseils d'action

N'hésitez pas à poser votre question ! 🌍"""
                        category = "help"

            # Sauvegarder l'historique
            save_chat_history(session_id, message, final_response, category)
            
            # Ajouter à la mémoire conversationnelle
            nlp_analysis = nlp_processor.analyze_message(message)
            conversation_memory.add_message(session_id, message, final_response, nlp_analysis)

            print(f"Réponse envoyée: {final_response[:100]}...")  # Debug log
            return JsonResponse({"response": final_response, "session_id": session_id})
        except json.JSONDecodeError as e:
            print(f"Erreur JSON: {e}")  # Debug log
            return JsonResponse({"response": "Erreur : requête invalide."}, status=400)
        except Exception as e:
            print(f"Erreur générale: {e}")  # Debug log
            return JsonResponse({"response": "Erreur serveur interne."}, status=500)

    return JsonResponse({"response": "Méthode non autorisée."}, status=405)

@csrf_exempt
def chat_history_view(request):
    """Vue pour récupérer l'historique des conversations"""
    if request.method == "GET":
        try:
            session_id = request.GET.get('session_id')
            limit = int(request.GET.get('limit', 50))
            
            history = get_chat_history(session_id, limit)
            
            return JsonResponse({
                "success": True,
                "history": history,
                "count": len(history)
            })
        except Exception as e:
            print(f"Erreur lors de la récupération de l'historique: {e}")
            return JsonResponse({
                "success": False,
                "error": "Erreur lors de la récupération de l'historique"
            }, status=500)
    
    elif request.method == "DELETE":
        try:
            session_id = request.GET.get('session_id')
            
            if clear_chat_history(session_id):
                return JsonResponse({
                    "success": True,
                    "message": "Historique supprimé avec succès"
                })
            else:
                return JsonResponse({
                    "success": False,
                    "error": "Erreur lors de la suppression"
                }, status=500)
        except Exception as e:
            print(f"Erreur lors de la suppression de l'historique: {e}")
            return JsonResponse({
                "success": False,
                "error": "Erreur lors de la suppression de l'historique"
            }, status=500)
    
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

class RegisterView(generics.CreateAPIView):
    """Vue pour l'inscription des utilisateurs"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """Gestion améliorée de la création d'utilisateur"""
        try:
            serializer = self.get_serializer(data=request.data)
            
            if not serializer.is_valid():
                # Retourner les erreurs directement pour chaque champ
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Créer l'utilisateur
            user = serializer.save()
            
            return Response(
                {
                    "success": True,
                    "message": "Compte créé avec succès ! Bienvenue sur Bia Savia.",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    }
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "Une erreur inattendue est survenue. Veuillez réessayer.",
                    "errors": {"general": "Erreur serveur"}
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserProfileView(generics.RetrieveAPIView):
    """Vue pour récupérer le profil utilisateur"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class PasswordResetView(generics.GenericAPIView):
    """Vue pour demander la réinitialisation du mot de passe"""
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Si cet email existe, un lien de réinitialisation sera envoyé"}, 
                status=status.HTTP_200_OK
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Lien frontend où l'utilisateur va changer son mot de passe
        reset_link = f"http://127.0.0.1:8000/api/password-reset-confirm/{uid}/{token}/"

        # Utiliser l'EmailService pour un design professionnel
        from .email_service import EmailService
        
        try:
            success = EmailService.send_password_reset_email(
                user_email=user.email,
                reset_token=token,
                reset_url=reset_link
            )
            
            if not success:
                return Response(
                    {"detail": "Erreur lors de l'envoi de l'email"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except Exception as e:
            return Response(
                {"detail": "Erreur lors de l'envoi de l'email"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"detail": "Email envoyé avec succès"}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(generics.GenericAPIView):
    """Vue pour confirmer la réinitialisation du mot de passe"""
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64=None, token=None, *args, **kwargs):
        """
        Vérifier le token et rediriger vers l'application mobile
        Cette méthode est appelée quand l'utilisateur clique sur le lien dans l'email
        """
        if not uidb64 or not token:
            return Response(
                {"detail": "Paramètres manquants"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Décoder l'UID
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            
            # Vérifier le token
            token_generator = PasswordResetTokenGenerator()
            if not token_generator.check_token(user, token):
                # Token invalide - afficher une page d'erreur
                html_content = """
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Lien Expiré - Bia Savia</title>
                    <style>
                        body { font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 20px; }
                        .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; text-align: center; }
                        .error { color: #e74c3c; }
                        .btn { background-color: #27AE60; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1 class="error">⚠️ Lien Expiré</h1>
                        <p>Ce lien de réinitialisation est invalide ou a expiré.</p>
                        <p>Veuillez demander un nouveau lien de réinitialisation.</p>
                        <a href="biasavia://forgot-password" class="btn">Demander un nouveau lien</a>
                    </div>
                </body>
                </html>
                """
                return HttpResponse(html_content, content_type='text/html')
            
            # Token valide - rediriger vers l'application mobile avec les paramètres
            mobile_url = f"biasavia://reset-password?uid={uidb64}&token={token}"
            
            # Page de redirection avec fallback pour navigateurs
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Redirection - Bia Savia</title>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 20px; }}
                    .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; text-align: center; }}
                    .success {{ color: #27AE60; }}
                    .btn {{ background-color: #27AE60; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }}
                    .spinner {{ border: 4px solid #f3f3f3; border-top: 4px solid #27AE60; border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 20px auto; }}
                    @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
                </style>
                <script>
                    // Tentative de redirection automatique vers l'app mobile
                    setTimeout(function() {{
                        window.location.href = "{mobile_url}";
                    }}, 1000);
                </script>
            </head>
            <body>
                <div class="container">
                    <h1 class="success">✅ Lien Valide</h1>
                    <div class="spinner"></div>
                    <p>Redirection vers l'application Bia Savia...</p>
                    <p>Si la redirection ne fonctionne pas automatiquement :</p>
                    <a href="{mobile_url}" class="btn">Ouvrir l'application</a>
                </div>
            </body>
            </html>
            """
            return HttpResponse(html_content, content_type='text/html')
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            # Utilisateur invalide - afficher une page d'erreur
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Erreur - Bia Savia</title>
                <style>
                    body { font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 20px; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; text-align: center; }
                    .error { color: #e74c3c; }
                    .btn { background-color: #27AE60; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1 class="error">❌ Lien Invalide</h1>
                    <p>Ce lien de réinitialisation n'est pas valide.</p>
                    <p>Veuillez vérifier le lien ou demander un nouveau lien de réinitialisation.</p>
                    <a href="biasavia://forgot-password" class="btn">Demander un nouveau lien</a>
                </div>
            </body>
            </html>
            """
            return HttpResponse(html_content, content_type='text/html')

    def post(self, request, uidb64=None, token=None, *args, **kwargs):
        # Support pour les paramètres URL et JSON
        data = request.data.copy()
        
        # Si les paramètres sont dans l'URL, les utiliser
        if uidb64 and token:
            data['uidb64'] = uidb64
            data['token'] = token
        # Sinon, ils doivent être dans le JSON de la requête
        elif 'uidb64' not in data or 'token' not in data:
            return Response(
                {"detail": "UID et token requis"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            serializer.save()
            return Response(
                {"detail": "Mot de passe réinitialisé avec succès"}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"detail": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from django.core.files.storage import default_storage

class PostPagination(PageNumberPagination):
    page_size = 5

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination

    def perform_create(self, serializer):
        print(f"Données reçues pour le post : {self.request.data}")
        images = self.request.data.get('images', [])
        import json
        if isinstance(images, str):
            try:
                images = json.loads(images)
            except Exception:
                images = []
        print(f"Images reçues pour le post : {images}")
        if not images:
            print("Avertissement : aucune image reçue pour ce post.")
        serializer.save(author=self.request.user, images=images)

class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        image = request.FILES.get('image')
        if image:
            path = default_storage.save(f"posts/{image.name}", image)
            image_url = request.build_absolute_uri(default_storage.url(path))
            return Response({'url': image_url}, status=200)
        return Response({'error': 'No image uploaded'}, status=400)

class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            user = request.user
            if user in post.likes.all():
                post.likes.remove(user)
            else:
                post.likes.add(user)
            return Response({'message': 'Like updated'}, status=200)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


class LikeCommentView(APIView):
    """Vue pour liker/unliker un commentaire"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
            user = request.user
            if user in comment.likes.all():
                comment.likes.remove(user)
                message = 'Like removed from comment'
            else:
                comment.likes.add(user)
                message = 'Comment liked'
            return Response({'message': message, 'likes_count': comment.likes_count}, status=200)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=404)


class ReplyToCommentView(generics.CreateAPIView):
    """Vue pour répondre à un commentaire"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        parent_comment_id = self.kwargs['pk']
        try:
            parent_comment = Comment.objects.get(pk=parent_comment_id)
            # La réponse sera liée au même post que le commentaire parent
            serializer.save(
                author=self.request.user, 
                post=parent_comment.post,
                parent=parent_comment
            )
        except Comment.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound("Parent comment not found")


class CommentRepliesView(generics.ListAPIView):
    """Vue pour récupérer les réponses d'un commentaire"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        parent_comment_id = self.kwargs['pk']
        return Comment.objects.filter(parent_id=parent_comment_id).order_by('created_at')
