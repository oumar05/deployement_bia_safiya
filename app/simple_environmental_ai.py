import os
import numpy as np
from PIL import Image
import logging
from typing import Tuple, Dict, Any
from django.conf import settings

logger = logging.getLogger(__name__)

class SimpleEnvironmentalClassifier:
  
    
    def __init__(self):
        self.is_loaded = True
        
        # Palettes de couleurs environnementales
        self.environmental_colors = {
            'green': [(0, 100, 0), (50, 205, 50), (34, 139, 34), (0, 128, 0), (173, 255, 47)],
            'brown': [(139, 69, 19), (160, 82, 45), (210, 180, 140), (222, 184, 135)],
            'blue': [(0, 0, 255), (30, 144, 255), (135, 206, 235), (173, 216, 230)],
            'earth': [(139, 90, 43), (205, 133, 63), (244, 164, 96)]
        }
        
        # Mots-clés pour noms de fichiers
        self.environmental_keywords = [
            'nature', 'arbre', 'tree', 'forest', 'foret', 'plant', 'plante',
            'flower', 'fleur', 'leaf', 'feuille', 'green', 'vert', 'water', 'eau',
            'river', 'riviere', 'lake', 'lac', 'mountain', 'montagne', 'sky', 'ciel',
            'bird', 'oiseau', 'animal', 'garden', 'jardin', 'farm', 'ferme',
            'eco', 'bio', 'organic', 'environment', 'environnement', 'natural',
            'recycl', 'solar', 'solaire', 'wind', 'vent', 'energy', 'energie'
        ]
        
        # Mots-clés interdits
        self.forbidden_keywords = [
            'sport', 'football', 'basketball', 'tennis', 'game', 'jeu',
            'fashion', 'mode', 'luxury', 'luxe', 'party', 'fete', 'club',
            'car', 'voiture', 'motor', 'moteur', 'electronic', 'electronique',
            'phone', 'telephone', 'computer', 'ordinateur', 'brand', 'marque'
        ]

    async def load_model(self):
        """Simule le chargement du modèle"""
        logger.info("🌱 Chargement du classificateur environnemental simple...")
        self.is_loaded = True
        return True

    def _analyze_colors(self, image_path: str) -> float:
        """Analyse la dominance des couleurs environnementales"""
        try:
            # Charger et redimensionner l'image
            image = Image.open(image_path).convert('RGB')
            image = image.resize((64, 64))  # Réduire pour l'analyse rapide
            
            # Convertir en array numpy
            img_array = np.array(image)
            pixels = img_array.reshape(-1, 3)
            
            environmental_score = 0.0
            total_pixels = len(pixels)
            
            # Analyser chaque pixel
            for pixel in pixels:
                r, g, b = pixel
                
                # Score pour les verts (nature)
                if g > r and g > b and g > 80:
                    environmental_score += 2.0
                
                # Score pour les bleus (eau, ciel)
                elif b > r and b > g and b > 100:
                    environmental_score += 1.5
                
                # Score pour les bruns (terre, troncs)
                elif r > 100 and g > 60 and b < 100 and abs(r-g) < 50:
                    environmental_score += 1.0
            
            # Normaliser le score
            return min(environmental_score / total_pixels, 1.0)
            
        except Exception as e:
            logger.error(f"Erreur analyse couleurs: {e}")
            return 0.0

    def _analyze_filename(self, image_path: str) -> float:
        """Analyse le nom du fichier pour des indices environnementaux"""
        filename = os.path.basename(image_path).lower()
        
        # Vérifier les mots-clés interdits
        for keyword in self.forbidden_keywords:
            if keyword in filename:
                return -1.0  # Score très négatif
        
        # Vérifier les mots-clés environnementaux
        score = 0.0
        for keyword in self.environmental_keywords:
            if keyword in filename:
                score += 0.3
        
        return min(score, 1.0)

    def _analyze_image_stats(self, image_path: str) -> float:
        """Analyse statistique de l'image"""
        try:
            image = Image.open(image_path).convert('RGB')
            img_array = np.array(image)
            
            # Calculer des statistiques
            mean_vals = np.mean(img_array, axis=(0, 1))
            std_vals = np.std(img_array, axis=(0, 1))
        
            
            green_dominance = mean_vals[1] / (mean_vals[0] + mean_vals[2] + 1)
            color_variation = np.mean(std_vals) / 255.0
            
            # Score basé sur ces caractéristiques
            nature_score = (green_dominance * 0.6 + color_variation * 0.4)
            
            return min(nature_score, 1.0)
            
        except Exception as e:
            logger.error(f"Erreur analyse stats: {e}")
            return 0.0

    async def classify_image(self, image_path: str) -> Dict[str, Any]:
        """Classifie une image comme environnementale ou non"""
        try:
            logger.info(f"🔍 Analyse de l'image: {image_path}")
            
            # Analyse multi-critères
            color_score = self._analyze_colors(image_path)
            filename_score = self._analyze_filename(image_path)
            stats_score = self._analyze_image_stats(image_path)
            
            # Si le nom de fichier contient des mots interdits
            if filename_score < 0:
                return {
                    'is_environmental': False,
                    'confidence': 0.9,
                    'explanation': 'Contenu non-environnemental détecté dans le nom du fichier',
                    'scores': {
                        'color': color_score,
                        'filename': filename_score,
                        'stats': stats_score
                    }
                }
            
            # Score combiné
            combined_score = (color_score * 0.5 + filename_score * 0.2 + stats_score * 0.3)
            
            # Seuil de décision
            is_environmental = combined_score > 0.4
            confidence = min(combined_score + 0.1, 0.95) if is_environmental else min(1.0 - combined_score + 0.1, 0.95)
            
            explanation = self._get_explanation(is_environmental, color_score, filename_score, stats_score)
            
            result = {
                'is_environmental': is_environmental,
                'confidence': float(confidence),
                'explanation': explanation,
                'scores': {
                    'color': float(color_score),
                    'filename': float(filename_score),
                    'stats': float(stats_score),
                    'combined': float(combined_score)
                }
            }
            
            logger.info(f"✅ Résultat: {'Acceptée' if is_environmental else 'Rejetée'} (score: {combined_score:.2f})")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la classification: {e}")
            return {
                'is_environmental': False,
                'confidence': 0.0,
                'error': str(e)
            }

    def _get_explanation(self, is_environmental: bool, color_score: float, filename_score: float, stats_score: float) -> str:
        """Génère une explication de la décision"""
        if is_environmental:
            reasons = []
            if color_score > 0.3:
                reasons.append("couleurs naturelles détectées")
            if filename_score > 0.2:
                reasons.append("nom de fichier environnemental")
            if stats_score > 0.3:
                reasons.append("caractéristiques visuelles naturelles")
            
            if reasons:
                return f"Image acceptée: {', '.join(reasons)}"
            else:
                return "Image acceptée: analyse globale positive"
        else:
            if filename_score < 0:
                return "Image rejetée: contenu non-environnemental dans le nom"
            elif color_score < 0.2:
                return "Image rejetée: absence de couleurs naturelles"
            else:
                return "Image rejetée: score environnemental insuffisant"

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
environmental_classifier = SimpleEnvironmentalClassifier()
