# 🌐 Interface d'Administration BiaSaviya

Interface web moderne et complète pour administrer l'application BiaSaviya.

## 🏗️ Architecture

```
admin_interface/
├── templates/          # Templates HTML
│   ├── base_admin.html     # Template de base
│   ├── admin_login.html    # Connexion admin
│   ├── admin_dashboard.html # Tableau de bord
│   ├── admin_users.html    # Gestion utilisateurs
│   ├── admin_posts.html    # Gestion posts
│   └── chat_analytics.html # Analytics chat
├── views.py           # Logique métier
├── urls.py           # Routes URL
└── apps.py           # Configuration de l'app
```

## 🚀 Installation Rapide

```bash
# Exécuter le script d'installation
./setup_admin_interface.sh

# Ou manuellement :
cd backend/backend
pip install django djangorestframework django-cors-headers python-dotenv
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## 📍 Accès

- **Interface Admin Custom**: http://localhost:8000/admin-panel/login/
- **Django Admin**: http://localhost:8000/admin/

## 🔑 Identifiants par défaut

- **Email**: admin@biasaviya.com
- **Mot de passe**: admin123

## 🎨 Fonctionnalités

### 📊 Tableau de Bord
- Statistiques temps réel
- Graphiques d'évolution des utilisateurs
- Métriques d'activité générale
- Sessions mobiles Flutter

### 👥 Gestion des Utilisateurs
- Liste complète avec recherche et filtres
- Activation/désactivation de comptes
- Gestion des rôles (Admin/Utilisateur)
- Historique des connexions

### 📝 Gestion des Posts
- Modération des publications
- Système de signalement
- Gestion des images multiples
- Statistiques de popularité

### 🤖 Analytics du Chatbot
- Analyse des conversations
- Catégorisation automatique
- Métriques de performance
- Graphiques de tendances

## 🛠️ Technologies Utilisées

- **Backend**: Django 5.x
- **Frontend**: Bootstrap 5, Chart.js
- **Base de données**: SQLite (dev) / PostgreSQL (prod)
- **APIs**: Django REST Framework

## 🎯 Modèles de Données

### CustomUser
- Système d'authentification par email
- Rôles et permissions
- Historique des connexions

### UserSession & UserInteraction
- Tracking des sessions utilisateur
- Analytics comportementales
- Support mobile Flutter

### Post & Comment
- Système de posts avec images
- Commentaires et likes
- Modération intégrée

### ChatHistory
- Historique des conversations
- Catégorisation intelligente
- Analytics de performance

## 🔧 Configuration

### Variables d'environnement (.env)
```bash
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Permissions
```python
# Dans views.py
@login_required
@user_passes_test(is_admin)
def admin_view(request):
    # Seuls les admins peuvent accéder
```

## 📈 Analytics Temps Réel

L'interface se met à jour automatiquement toutes les 30 secondes avec :
- Nouveaux utilisateurs
- Posts publiés
- Conversations chatbot
- Sessions actives

## 🎨 Personnalisation

### Couleurs (CSS Variables)
```css
:root {
    --primary-color: #2d5a27;
    --secondary-color: #4a7c59;
    --accent-color: #6ba368;
}
```

### Ajout de nouvelles pages
1. Créer le template dans `templates/`
2. Ajouter la vue dans `views.py`
3. Configurer l'URL dans `urls.py`
4. Ajouter au menu dans `base_admin.html`

## 🐛 Dépannage

### Erreur de module manquant
```bash
pip install -r requirements.txt
```

### Erreur de migration
```bash
python manage.py makemigrations --empty admin_interface
python manage.py migrate
```

### Problème de permissions
```bash
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.get(email='admin@biasaviya.com')
>>> user.is_staff = True
>>> user.is_superuser = True
>>> user.save()
```

## 📚 Documentation API

### Endpoints disponibles
- `GET /admin-panel/api/stats/` - Statistiques temps réel
- `POST /admin-panel/api/toggle-user/<id>/` - Activer/désactiver utilisateur
- `POST /admin-panel/api/delete-post/<id>/` - Supprimer un post

## 🚀 Déploiement

### Production
1. Configurer PostgreSQL
2. Configurer les variables d'environnement
3. Collecter les fichiers statiques : `python manage.py collectstatic`
4. Utiliser un serveur web (Nginx + Gunicorn)

## 📞 Support

Pour toute question ou problème :
1. Vérifier la documentation
2. Consulter les logs Django
3. Contacter l'équipe de développement