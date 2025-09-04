from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class EnvironmentalData(models.Model):
    """Modèle pour stocker les données environnementales"""
    CATEGORY_CHOICES = [
        ('pollution', 'Pollution'),
        ('climat', 'Climat'),
        ('biodiversite', 'Biodiversité'),
        ('energie', 'Énergie'),
        ('dechets', 'Déchets'),
        ('eau', 'Eau'),
        ('air', 'Air'),
        ('foret', 'Forêt'),
        ('ocean', 'Océan'),
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    keyword = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField()
    source = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'keyword']
    
    def __str__(self):
        return f"{self.category} - {self.keyword}"

class ChatHistory(models.Model):
    """Modèle pour stocker l'historique des conversations"""
    session_id = models.CharField(max_length=100, blank=True, null=True)
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Chat Histories"
    
    def __str__(self):
        return f"Chat {self.session_id} - {self.timestamp}"
from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField()
    images = models.JSONField(default=list, blank=True)  # URLs des images
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()  # via related_name

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # Nouveau : système de likes pour les commentaires
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)
    # Nouveau : système de réponses aux commentaires
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def replies_count(self):
        return self.replies.count()

    class Meta:
        ordering = ['created_at']
