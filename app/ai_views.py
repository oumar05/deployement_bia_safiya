from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.conf import settings
import os
import tempfile
import logging
from .simple_environmental_ai import environmental_classifier

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def classify_image(request):
    """
    API endpoint pour classifier une image
    """
    import asyncio
    
    try:
        if 'image' not in request.FILES:
            return Response({
                'error': 'Aucune image fournie'
            }, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']
        
        # Vérifier le type de fichier (plus souple sur la détection MIME)
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/pjpeg']
        file_extension = image_file.name.lower().split('.')[-1] if '.' in image_file.name else ''
        allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
        
        # Accepter si le type MIME est valide OU si l'extension est valide
        if (image_file.content_type not in allowed_types and 
            file_extension not in allowed_extensions):
            return Response({
                'error': f'Type de fichier non supporté: {image_file.content_type}. Utilisez JPG, PNG ou WebP.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier la taille du fichier (max 10MB)
        if image_file.size > 10 * 1024 * 1024:
            return Response({
                'error': 'Fichier trop volumineux. Maximum 10MB.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Sauvegarder temporairement l'image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            for chunk in image_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        try:
            # Classifier l'image (utiliser run pour les fonctions async)
            result = asyncio.run(environmental_classifier.classify_image(temp_file_path))
            
            # Nettoyer le fichier temporaire
            os.unlink(temp_file_path)
            
            return Response({
                'success': True,
                'is_environmental': result.get('is_environmental', False),
                'confidence': result.get('confidence', 0.0),
                'explanation': result.get('explanation', ''),
                'details': result.get('top_predictions', [])
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Nettoyer le fichier temporaire en cas d'erreur
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise e

    except Exception as e:
        logger.error(f"Erreur lors de la classification: {e}")
        return Response({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def classify_batch(request):
    """
    API endpoint pour classifier plusieurs images en lot
    """
    import asyncio
    
    try:
        if 'images' not in request.FILES:
            return Response({
                'error': 'Aucune image fournie'
            }, status=status.HTTP_400_BAD_REQUEST)

        images = request.FILES.getlist('images')
        
        if len(images) > 10:
            return Response({
                'error': 'Maximum 10 images par lot'
            }, status=status.HTTP_400_BAD_REQUEST)

        temp_files = []
        results = []

        try:
            # Sauvegarder toutes les images temporairement
            for image_file in images:
                # Vérifications de base (même logique souple que classify_image)
                allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/pjpeg']
                file_extension = image_file.name.lower().split('.')[-1] if '.' in image_file.name else ''
                allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
                
                if (image_file.content_type not in allowed_types and 
                    file_extension not in allowed_extensions):
                    results.append({
                        'filename': image_file.name,
                        'error': 'Type de fichier non supporté'
                    })
                    continue

                if image_file.size > 10 * 1024 * 1024:
                    results.append({
                        'filename': image_file.name,
                        'error': 'Fichier trop volumineux'
                    })
                    continue

                # Sauvegarder temporairement
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                    for chunk in image_file.chunks():
                        temp_file.write(chunk)
                    temp_files.append(temp_file.name)

            # Classifier toutes les images valides
            if temp_files:
                batch_result = asyncio.run(environmental_classifier.batch_classify(temp_files))
                
                # Formater les résultats
                for i, detail in enumerate(batch_result['details']):
                    results.append({
                        'filename': images[i].name,
                        'is_environmental': detail['result'].get('is_environmental', False),
                        'confidence': detail['result'].get('confidence', 0.0),
                        'explanation': detail['result'].get('explanation', '')
                    })

            # Nettoyer les fichiers temporaires
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)

            return Response({
                'success': True,
                'total': len(images),
                'results': results,
                'summary': {
                    'accepted': sum(1 for r in results if r.get('is_environmental', False)),
                    'rejected': sum(1 for r in results if not r.get('is_environmental', False))
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Nettoyer les fichiers temporaires en cas d'erreur
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            raise e

    except Exception as e:
        logger.error(f"Erreur lors de la classification en lot: {e}")
        return Response({
            'success': False,
            'error': 'Erreur interne du serveur',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def ai_status(request):
    """
    API endpoint pour vérifier le statut du système d'IA
    """
    try:
        return Response({
            'success': True,
            'ai_ready': environmental_classifier.is_loaded,
            'model_info': {
                'name': 'MobileNetV2',
                'source': 'TensorFlow Hub',
                'categories': 'ImageNet (1000 classes)',
                'environmental_filtering': True
            },
            'capabilities': {
                'image_formats': ['JPEG', 'JPG', 'PNG', 'WebP'],
                'max_file_size': '10MB',
                'batch_processing': True,
                'max_batch_size': 10
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Erreur lors de la vérification du statut: {e}")
        return Response({
            'success': False,
            'error': 'Erreur interne du serveur'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def initialize_ai(request):
    """
    API endpoint pour initialiser le modèle d'IA
    """
    import asyncio
    
    try:
        success = asyncio.run(environmental_classifier.load_model())
        
        return Response({
            'success': success,
            'message': 'Modèle chargé avec succès' if success else 'Échec du chargement du modèle',
            'ai_ready': environmental_classifier.is_loaded
        }, status=status.HTTP_200_OK if success else status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation: {e}")
        return Response({
            'success': False,
            'error': 'Erreur lors de l\'initialisation du modèle d\'IA',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
