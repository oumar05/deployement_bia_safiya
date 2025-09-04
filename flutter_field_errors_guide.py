#!/usr/bin/env python3
"""
Exemples de réponses d'erreur par champ pour Flutter
"""

# Structure de réponse d'erreur maintenant retournée par l'API
FIELD_ERROR_EXAMPLES = {
    
    "email_invalide": {
        "email": ["Veuillez entrer une adresse email valide."]
    },
    
    "email_existe": {
        "email": ["Cette adresse email est déjà utilisée."]
    },
    
    "username_court": {
        "username": ["Le nom d'utilisateur doit contenir au moins 3 caractères."]
    },
    
    "username_existe": {
        "username": ["Ce nom d'utilisateur est déjà pris."]
    },
    
    "password_court": {
        "password": ["Le mot de passe doit contenir au moins 8 caractères."]
    },
    
    "password_mismatch": {
        "password2": ["Les mots de passe ne correspondent pas."]
    },
    
    "erreurs_multiples": {
        "email": ["Veuillez entrer une adresse email valide."],
        "username": ["Ce nom d'utilisateur est déjà pris."],
        "password": ["Le mot de passe doit contenir au moins 8 caractères."],
        "password2": ["Les mots de passe ne correspondent pas."]
    }
}

# Code Flutter pour gérer ces erreurs par champ
FLUTTER_ERROR_HANDLING_CODE = '''
// Dans votre classe State Flutter :
String? emailError;
String? usernameError;
String? passwordError;
String? password2Error;

void _handleRegistrationResponse(Map<String, dynamic> response) {
  // Réinitialiser les erreurs
  setState(() {
    emailError = null;
    usernameError = null;
    passwordError = null;
    password2Error = null;
  });
  
  if (response.containsKey('email')) {
    setState(() {
      emailError = response['email'][0]; // Premier message d'erreur
    });
  }
  
  if (response.containsKey('username')) {
    setState(() {
      usernameError = response['username'][0];
    });
  }
  
  if (response.containsKey('password')) {
    setState(() {
      passwordError = response['password'][0];
    });
  }
  
  if (response.containsKey('password2')) {
    setState(() {
      password2Error = response['password2'][0];
    });
  }
}

// Dans vos TextField widgets :
TextField(
  controller: emailController,
  decoration: InputDecoration(
    hintText: 'Email',
    errorText: emailError, // L'erreur s'affiche sous le champ
    errorStyle: TextStyle(color: Colors.red),
  ),
),

TextField(
  controller: usernameController,
  decoration: InputDecoration(
    hintText: 'Nom d\'utilisateur',
    errorText: usernameError, // L'erreur s'affiche sous le champ
    errorStyle: TextStyle(color: Colors.red),
  ),
),

TextField(
  controller: passwordController,
  decoration: InputDecoration(
    hintText: 'Mot de passe',
    errorText: passwordError, // L'erreur s'affiche sous le champ
    errorStyle: TextStyle(color: Colors.red),
  ),
),

TextField(
  controller: password2Controller,
  decoration: InputDecoration(
    hintText: 'Confirmer le mot de passe',
    errorText: password2Error, // L'erreur s'affiche sous le champ
    errorStyle: TextStyle(color: Colors.red),
  ),
),
'''

print("📱 Format des erreurs par champ pour Flutter")
print("=" * 50)

print("\n✅ MAINTENANT CHAQUE ERREUR VA SOUS SON CHAMP :")
print("-" * 50)

for error_type, error_data in FIELD_ERROR_EXAMPLES.items():
    print(f"\n🔸 {error_type.replace('_', ' ').title()}:")
    for field, messages in error_data.items():
        print(f"   {field}: {messages[0]}")

print("\n📱 CÔTÉ FLUTTER :")
print("-" * 20)
print("• emailError → TextField email")
print("• usernameError → TextField username")  
print("• passwordError → TextField password")
print("• password2Error → TextField confirmation")

print("\n🎯 RÉSULTAT :")
print("-" * 15)
print("✅ Email invalide → erreur sous le champ email")
print("✅ Username pris → erreur sous le champ username")
print("✅ Password court → erreur sous le champ password")
print("✅ Passwords différents → erreur sous le champ confirmation")

print("\n🌱 Interface utilisateur améliorée pour Bia Savia ! 🌱")
