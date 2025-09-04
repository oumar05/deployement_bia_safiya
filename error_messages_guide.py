#!/usr/bin/env python3
"""
Guide des messages d'erreur user-friendly pour Bia Savia
"""

# Messages d'erreur améliorés pour l'inscription
ERROR_MESSAGES = {
    # Erreurs d'email
    "email_required": "L'adresse email est obligatoire.",
    "email_invalid": "Veuillez entrer une adresse email valide (ex: nom@domaine.com).",
    "email_exists": "Cette adresse email est déjà utilisée. Essayez de vous connecter ou utilisez une autre adresse.",
    
    # Erreurs de nom d'utilisateur
    "username_required": "Le nom d'utilisateur est obligatoire.",
    "username_exists": "Ce nom d'utilisateur est déjà pris. Essayez un autre nom.",
    "username_too_short": "Le nom d'utilisateur doit contenir au moins 3 caractères.",
    "username_too_long": "Le nom d'utilisateur ne peut pas dépasser 30 caractères.",
    "username_invalid_chars": "Le nom d'utilisateur ne peut contenir que des lettres, chiffres, tirets (-) et underscores (_).",
    
    # Erreurs de mot de passe
    "password_required": "Le mot de passe est obligatoire.",
    "password_too_short": "Le mot de passe doit contenir au moins 8 caractères.",
    "password_mismatch": "Les mots de passe ne correspondent pas. Vérifiez votre saisie.",
    
    # Erreurs générales
    "server_error": "Une erreur est survenue. Veuillez réessayer dans quelques instants.",
    "validation_error": "Veuillez corriger les erreurs ci-dessous.",
    "network_error": "Problème de connexion. Vérifiez votre internet et réessayez.",
}

# Exemples de réponses API améliorées
EXAMPLE_RESPONSES = {
    "success_registration": {
        "success": True,
        "message": "Compte créé avec succès ! Bienvenue sur Bia Savia. 🌱",
        "user": {
            "id": 1,
            "username": "ahmed_ben",
            "email": "ahmed@example.com"
        }
    },
    
    "error_email_exists": {
        "success": False,
        "message": "Veuillez corriger les erreurs ci-dessous.",
        "errors": {
            "email": "Cette adresse email est déjà utilisée. Essayez de vous connecter ou utilisez une autre adresse."
        }
    },
    
    "error_password_weak": {
        "success": False,
        "message": "Veuillez corriger les erreurs ci-dessous.",
        "errors": {
            "password": "Le mot de passe doit contenir au moins 8 caractères et au moins un chiffre."
        }
    },
    
    "error_multiple_fields": {
        "success": False,
        "message": "Veuillez corriger les erreurs ci-dessous.",
        "errors": {
            "email": "Veuillez entrer une adresse email valide (ex: nom@domaine.com).",
            "username": "Ce nom d'utilisateur est déjà pris. Essayez un autre nom.",
            "password2": "Les mots de passe ne correspondent pas."
        }
    }
}

# Guide pour l'application mobile Flutter
FLUTTER_ERROR_HANDLING = """
// Dans l'application Flutter, gérer les erreurs ainsi :

void _handleRegistrationError(Map<String, dynamic> response) {
  if (response['success'] == false) {
    String mainMessage = response['message'] ?? 'Une erreur est survenue';
    Map<String, dynamic> errors = response['errors'] ?? {};
    
    // Afficher le message principal
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(mainMessage),
        backgroundColor: Colors.red,
      ),
    );
    
    // Afficher les erreurs spécifiques sous chaque champ
    setState(() {
      emailError = errors['email'];
      usernameError = errors['username'];
      passwordError = errors['password'];
      password2Error = errors['password2'];
    });
  }
}
"""

print("✅ Messages d'erreur user-friendly configurés pour Bia Savia")
print("\n📧 Exemples de messages :")
print(f"Email invalide: {ERROR_MESSAGES['email_invalid']}")
print(f"Mot de passe faible: {ERROR_MESSAGES['password_too_short']}")
print(f"Nom d'utilisateur pris: {ERROR_MESSAGES['username_exists']}")

print("\n🎯 Maintenant les utilisateurs verront des messages clairs en français !")
