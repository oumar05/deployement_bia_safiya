from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

# Inscription
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True,
        error_messages={
            'required': 'Le mot de passe est obligatoire.',
            'blank': 'Le mot de passe ne peut pas être vide.',
        }
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        error_messages={
            'required': 'La confirmation du mot de passe est obligatoire.',
            'blank': 'La confirmation du mot de passe ne peut pas être vide.',
        }
    )
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'L\'adresse email est obligatoire.',
            'invalid': 'Veuillez entrer une adresse email valide.',
            'blank': 'L\'adresse email ne peut pas être vide.',
        }
    )
    username = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Le nom d\'utilisateur est obligatoire.',
            'blank': 'Le nom d\'utilisateur ne peut pas être vide.',
        }
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')

    def validate_email(self, value):
        """Validation personnalisée pour l'email"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cette adresse email est déjà utilisée.")
        return value

    def validate_username(self, value):
        """Validation personnalisée pour le nom d'utilisateur"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà pris.")
        
        if len(value) < 3:
            raise serializers.ValidationError("Le nom d'utilisateur doit contenir au moins 3 caractères.")
        
        if len(value) > 30:
            raise serializers.ValidationError("Le nom d'utilisateur ne peut pas dépasser 30 caractères.")
        
        # Vérifier que le nom d'utilisateur ne contient que des caractères autorisés
        import re
        if not re.match("^[a-zA-Z0-9_-]+$", value):
            raise serializers.ValidationError("Le nom d'utilisateur ne peut contenir que des lettres, chiffres, tirets et underscores.")
        
        return value

    def validate_password(self, value):
        """Validation personnalisée pour le mot de passe"""
        if len(value) < 8:
            raise serializers.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        
        return value

    def validate(self, attrs):
        """Validation globale"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password2": "Les mots de passe ne correspondent pas."
            })
        return attrs

    def create(self, validated_data):
        """Création de l'utilisateur"""
        try:
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email']
            )
            user.set_password(validated_data['password'])
            user.save()
            
            # Envoyer un email de bienvenue
            try:
                from .email_service import EmailService
                EmailService.send_welcome_email(user.email, user.username)
            except Exception as e:
                # Ne pas faire échouer l'inscription si l'email ne s'envoie pas
                print(f"Erreur envoi email de bienvenue: {e}")
            
            return user
        except Exception as e:
            raise serializers.ValidationError({
                "non_field_errors": ["Une erreur est survenue lors de la création du compte. Veuillez réessayer."]
            })

# Profil utilisateur
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail

# Mot de passe oublié
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Aucun utilisateur avec cet email.")
        return value

    def save(self):
        request = self.context.get('request')
        email = self.validated_data['email']
        user = User.objects.get(email=email)

        # Générer token
        token_generator = PasswordResetTokenGenerator()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        # Créer deep link vers l'application Flutter
        # Format: biasavia://reset-password?uid=<uid>&token=<token>
        reset_url = f"biasavia://reset-password?uid={uid}&token={token}"
        
        # Utiliser le service d'email
        from .email_service import EmailService
        
        # Envoyer l'email avec le service
        success = EmailService.send_password_reset_email(
            user_email=email,
            reset_token=token,
            reset_url=reset_url
        )
        
        if success:
            return True
        else:
            raise serializers.ValidationError("Erreur lors de l'envoi de l'email.")
        
        return True


# Confirmation réinitialisation
class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        error_messages={
            'required': 'Le nouveau mot de passe est obligatoire.',
            'blank': 'Le nouveau mot de passe ne peut pas être vide.',
        }
    )
    new_password2 = serializers.CharField(
        write_only=True,
        error_messages={
            'required': 'La confirmation du nouveau mot de passe est obligatoire.',
            'blank': 'La confirmation du nouveau mot de passe ne peut pas être vide.',
        }
    )
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate_new_password(self, value):
        """Validation personnalisée pour le nouveau mot de passe"""
        if len(value) < 8:
            raise serializers.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                "new_password2": "Les mots de passe ne correspondent pas."
            })
        return attrs

    def save(self):
        uid = self.validated_data['uidb64']
        token = self.validated_data['token']
        password = self.validated_data['new_password']

        # Décoder l'UID
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Lien invalide.")

        # Vérifier token
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise serializers.ValidationError("Token invalide ou expiré.")

        # Changer mot de passe
        user.set_password(password)
        user.save()
        return user


# Serializers pour les posts et commentaires
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    likes_users = UserSerializer(source='likes', many=True, read_only=True)
    replies_count = serializers.IntegerField(source='replies.count', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at', 'likes_count', 'likes_users', 'replies_count', 'replies', 'parent']

    def get_replies(self, obj):
        # Retourner les réponses directes à ce commentaire
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True, context=self.context).data
        return []

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    likes = serializers.IntegerField(source='likes_count', read_only=True)
    likes_users = UserSerializer(source='likes', many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'images', 'author', 'created_at', 'likes', 'likes_users', 'comments_count', 'comments']
