import os
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import cv2
import logging
from typing import Tuple, Dict, Any
from django.conf import settings

logger = logging.getLogger(__name__)

class EnvironmentalImageClassifier:
    """
    Service d'IA pour classifier les images selon leur contenu environnemental
    Utilise MobileNetV2 pré-entraîné sur ImageNet
    """
    
    def __init__(self):
        self.model = None
        self.is_loaded = False
        self.model_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"
        
        # Catégories environnementales acceptées (indices ImageNet)
        self.environmental_categories = {
            # Nature et paysages
            'forest': [968, 969, 970], # forêt
            'tree': [986, 987, 988, 989], # arbres
            'mountain': [974, 975, 976], # montagnes
            'water': [625, 626, 627, 628], # eau, rivières, lacs
            'beach': [978, 979], # plage
            'flower': [985], # fleurs
            
            # Animaux
            'bird': list(range(80, 101)), # oiseaux
            'fish': list(range(389, 397)), # poissons
            'mammal': list(range(285, 310)), # mammifères
            'insect': list(range(318, 328)), # insectes
            
            # Agriculture
            'farm': [408, 409], # ferme
            'vegetable': [936, 937, 938], # légumes
            'fruit': [948, 949, 950, 951], # fruits
        }
        
        # Catégories à rejeter
        self.forbidden_categories = {
            # Sports
            'sports': list(range(768, 795)), # équipements sportifs
            'ball': [722, 723, 724, 725], # ballons
            
            # Divertissement
            'music': [420, 421, 422], # instruments
            'entertainment': [438, 439, 440], # divertissement
            
            # Mode et luxe
            'clothing': list(range(450, 520)), # vêtements
            'jewelry': [695, 696], # bijoux
            
            # Véhicules non-écologiques
            'vehicle': list(range(565, 580)), # voitures normales
        }

    async def load_model(self):
        """Charge le modèle MobileNetV2"""
        try:
            if self.is_loaded:
                return True
                
            logger.info("🚀 Chargement du modèle MobileNetV2...")
            
            # Charger le modèle depuis TensorFlow Hub
            self.model = hub.load(self.model_url)
            self.is_loaded = True
            
            logger.info("✅ Modèle MobileNetV2 chargé avec succès !")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement du modèle: {e}")
            return False

    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Préprocesse l'image pour le modèle"""
        try:
            # Charger l'image
            image = Image.open(image_path).convert('RGB')
            
            # Redimensionner à 224x224 (taille attendue par MobileNetV2)
            image = image.resize((224, 224))
            
            # Convertir en array numpy
            image_array = np.array(image)
            
            # Normaliser (0-255 vers 0-1)
            image_array = image_array.astype(np.float32) / 255.0
            
            # Ajouter la dimension batch
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            logger.error(f"❌ Erreur préprocessing image: {e}")
            raise

    async def classify_image(self, image_path: str) -> Dict[str, Any]:
        """Classifie une image et détermine si elle est environnementale"""
        try:
            if not self.is_loaded:
                await self.load_model()
            
            logger.info(f"🔍 Analyse de l'image: {image_path}")
            
            # Préprocesser l'image
            processed_image = self.preprocess_image(image_path)
            
            # Prédiction
            predictions = self.model(processed_image)
            probabilities = tf.nn.softmax(predictions[0])
            
            # Obtenir les top 5 prédictions
            top_k = tf.nn.top_k(probabilities, k=5)
            top_classes = top_k.indices.numpy()
            top_scores = top_k.values.numpy()
            
            # Analyser si c'est environnemental
            is_environmental = self._analyze_environmental_content(top_classes, top_scores)
            
            # Score de confiance
            confidence_score = float(np.max(top_scores))
            
            result = {
                'is_environmental': is_environmental,
                'confidence': confidence_score,
                'top_predictions': [
                    {
                        'class_id': int(class_id),
                        'score': float(score)
                    }
                    for class_id, score in zip(top_classes, top_scores)
                ],
                'explanation': self._get_explanation(top_classes, is_environmental)
            }
            
            logger.info(f"✅ Résultat: {'Acceptée' if is_environmental else 'Rejetée'} (confiance: {confidence_score:.2f})")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la classification: {e}")
            return {
                'is_environmental': False,
                'confidence': 0.0,
                'error': str(e)
            }

    def _analyze_environmental_content(self, top_classes: np.ndarray, top_scores: np.ndarray) -> bool:
        """Analyse si le contenu est environnemental basé sur les prédictions"""
        
        # Vérifier d'abord si c'est du contenu interdit
        for class_id, score in zip(top_classes, top_scores):
            if score > 0.3:  # Seuil de confiance
                for category, forbidden_ids in self.forbidden_categories.items():
                    if class_id in forbidden_ids:
                        logger.info(f"🚫 Contenu interdit détecté: {category} (score: {score:.2f})")
                        return False
        
        # Vérifier si c'est du contenu environnemental
        environmental_score = 0.0
        for class_id, score in zip(top_classes, top_scores):
            for category, env_ids in self.environmental_categories.items():
                if class_id in env_ids:
                    environmental_score += score
                    logger.info(f"🌱 Contenu environnemental détecté: {category} (score: {score:.2f})")
        
        # Décision basée sur le score environnemental
        return environmental_score > 0.4  # Seuil d'acceptation

    def _get_explanation(self, top_classes: np.ndarray, is_environmental: bool) -> str:
        """Génère une explication de la décision"""
        if is_environmental:
            return "Image acceptée: Contenu environnemental détecté (nature, animaux, écologie)"
        else:
            # Vérifier la raison du rejet
            for class_id in top_classes:
                for category, forbidden_ids in self.forbidden_categories.items():
                    if class_id in forbidden_ids:
                        return f"Image rejetée: Contenu de type '{category}' détecté"
            
            return "Image rejetée: Contenu non-environnemental"

    async def batch_classify(self, image_paths: list) -> Dict[str, Any]:
        """Classifie plusieurs images en lot"""
        results = {
            'total': len(image_paths),
            'accepted': 0,
            'rejected': 0,
            'details': []
        }
        
        for image_path in image_paths:
            result = await self.classify_image(image_path)
            
            if result.get('is_environmental', False):
                results['accepted'] += 1
            else:
                results['rejected'] += 1
            
            results['details'].append({
                'image': image_path,
                'result': result
            })
        
        return results

# Instance globale du classificateur
environmental_classifier = EnvironmentalImageClassifier()
