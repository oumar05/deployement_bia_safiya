from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import (
    RegisterView, UserProfileView, PasswordResetView, PasswordResetConfirmView,
    LikePostView, PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView, ImageUploadView,
    CommentListCreateView, CommentDeleteView, LikeCommentView, ReplyToCommentView, CommentRepliesView,
    chatbot_view
)
from .ai_views import classify_image, classify_batch, ai_status, initialize_ai

urlpatterns = [
    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Auth
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/profile/', UserProfileView.as_view(), name='profile'),

    # Password oubli
    path('api/password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('api/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('chatbot/', chatbot_view, name='chatbot'),

    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
    path('upload-image/', ImageUploadView.as_view(), name='upload-image'),
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    # Nouvelles routes pour les commentaires
    path('comments/<int:pk>/like/', LikeCommentView.as_view(), name='like-comment'),
    path('comments/<int:pk>/reply/', ReplyToCommentView.as_view(), name='reply-to-comment'),
    path('comments/<int:pk>/replies/', CommentRepliesView.as_view(), name='comment-replies'),
    
    # IA Endpoints
    path('api/ai/classify/', classify_image, name='ai-classify'),
    path('api/ai/classify-batch/', classify_batch, name='ai-classify-batch'),
    path('api/ai/status/', ai_status, name='ai-status'),
    path('api/ai/initialize/', initialize_ai, name='ai-initialize'),
    # Ajoute ici d'autres routes si besoin
]
