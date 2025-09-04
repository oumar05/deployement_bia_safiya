from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """Service pour gérer l'envoi d'emails"""
    
    @staticmethod
    def send_password_reset_email(user_email, reset_token, reset_url):
        """
        Envoie un email de réinitialisation de mot de passe
        """
        try:
            subject = 'Réinitialisation de votre mot de passe - Bia Safia'
            
            # Contenu HTML de l'email avec design moderne et professionnel
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <!--[if mso]>
                <noscript>
                    <xml>
                        <o:OfficeDocumentSettings>
                            <o:PixelsPerInch>96</o:PixelsPerInch>
                        </o:OfficeDocumentSettings>
                    </xml>
                </noscript>
                <![endif]-->
            </head>
            <body style="margin: 0; padding: 0; background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
                
                <!-- Wrapper principal -->
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f8f9fa;">
                    <tr>
                        <td align="center" style="padding: 40px 20px;">
                            
                            <!-- Container principal -->
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                                
                                <!-- Header avec logo -->
                                <tr>
                                    <td style="background: linear-gradient(135deg, #27AE60 0%, #229954 100%); border-radius: 12px 12px 0 0; padding: 40px 40px 30px 40px; text-align: center;">
                                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                            <tr>
                                                <td align="center">
                                                    <!-- Logo/Icône -->
                                                    <div style="width: 80px; height: 80px; background-color: rgba(255,255,255,0.15); border-radius: 50%; margin: 0 auto 20px auto; display: flex; align-items: center; justify-content: center;">
                                                        <div style="width: 40px; height: 40px; background-color: #ffffff; border-radius: 8px; position: relative;">
                                                            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #27AE60; font-size: 20px; font-weight: bold;">🔐</div>
                                                        </div>
                                                    </div>
                                                    
                                                    <!-- Titre principal -->
                                                    <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600; line-height: 1.2;">
                                                        Réinitialisation de mot de passe
                                                    </h1>
                                                    
                                                    <!-- Sous-titre -->
                                                    <p style="margin: 12px 0 0 0; color: rgba(255,255,255,0.9); font-size: 16px; line-height: 1.4;">
                                                        Sécurisez votre compte Bia Savia
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                
                                <!-- Contenu principal -->
                                <tr>
                                    <td style="padding: 50px 40px;">
                                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                            
                                            <!-- Message de salutation -->
                                            <tr>
                                                <td>
                                                    <h2 style="margin: 0 0 24px 0; color: #2c3e50; font-size: 22px; font-weight: 600;">
                                                        Bonjour ! 👋
                                                    </h2>
                                                    
                                                    <p style="margin: 0 0 24px 0; color: #5a6c7d; font-size: 16px; line-height: 1.6;">
                                                        Nous avons reçu une demande de réinitialisation de mot de passe pour votre compte Bia Safia.
                                                    </p>
                                                    
                                                    <p style="margin: 0 0 32px 0; color: #5a6c7d; font-size: 16px; line-height: 1.6;">
                                                        Cliquez sur le bouton ci-dessous pour créer un nouveau mot de passe sécurisé :
                                                    </p>
                                                </td>
                                            </tr>
                                            
                                            <!-- Bouton d'action principal -->
                                            <tr>
                                                <td align="center" style="padding: 20px 0 40px 0;">
                                                    <!--[if mso]>
                                                    <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="{reset_url}" style="height:56px;v-text-anchor:middle;width:280px;" arcsize="20%" strokecolor="#27AE60" fillcolor="#27AE60">
                                                    <w:anchorlock/>
                                                    <center style="color:#ffffff;font-family:sans-serif;font-size:16px;font-weight:bold;">Réinitialiser mon mot de passe</center>
                                                    </v:roundrect>
                                                    <![endif]-->
                                                    <!--[if !mso]><!-->
                                                    <a href="{reset_url}" style="display: inline-block; padding: 18px 36px; background: linear-gradient(135deg, #27AE60 0%, #229954 100%); color: #ffffff; text-decoration: none; border-radius: 12px; font-size: 16px; font-weight: 600; text-align: center; min-width: 200px; box-shadow: 0 4px 12px rgba(39, 174, 96, 0.25); transition: all 0.3s ease;">
                                                        🔐 Réinitialiser mon mot de passe
                                                    </a>
                                                    <!--<![endif]-->
                                                </td>
                                            </tr>
                                            
                                            <!-- Informations de sécurité -->
                                            <tr>
                                                <td style="background-color: #fff3cd; border-radius: 8px; padding: 20px; border-left: 4px solid #ffc107;">
                                                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                                        <tr>
                                                            <td style="width: 40px; vertical-align: top;">
                                                                <div style="width: 32px; height: 32px; background-color: #ffc107; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                                                                    <span style="color: #ffffff; font-size: 16px; font-weight: bold;">⚠️</span>
                                                                </div>
                                                            </td>
                                                            <td style="padding-left: 16px;">
                                                                <h3 style="margin: 0 0 8px 0; color: #856404; font-size: 16px; font-weight: 600;">
                                                                    Important - Sécurité
                                                                </h3>
                                                                <p style="margin: 0; color: #856404; font-size: 14px; line-height: 1.4;">
                                                                    <strong>Ce lien est valide pendant 15 minutes seulement</strong> pour votre sécurité. Après expiration, vous devrez faire une nouvelle demande.
                                                                </p>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                            
                                            <!-- Spacer -->
                                            <tr>
                                                <td style="height: 30px;"></td>
                                            </tr>
                                            
                                            <!-- Avertissement -->
                                            <tr>
                                                <td>
                                                    <p style="margin: 0; color: #7f8c8d; font-size: 14px; line-height: 1.5; text-align: center;">
                                                        Si vous n'avez pas demandé cette réinitialisation, vous pouvez ignorer cet email en toute sécurité. Votre mot de passe ne sera pas modifié.
                                                    </p>
                                                </td>
                                            </tr>
                                            
                                        </table>
                                    </td>
                                </tr>
                                
                                <!-- Footer -->
                                <tr>
                                    <td style="background-color: #f8f9fa; border-radius: 0 0 12px 12px; padding: 30px 40px;">
                                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                            <tr>
                                                <td align="center">
                                                    <!-- Logo small -->
                                                    <div style="margin-bottom: 20px;">
                                                        <span style="color: #27AE60; font-size: 24px; font-weight: bold;">🌱 Bia Safia</span>
                                                    </div>
                                                    
                                                    <!-- Informations contact -->
                                                    <p style="margin: 0 0 16px 0; color: #7f8c8d; font-size: 14px; line-height: 1.4; text-align: center;">
                                                        Votre assistant environnemental de confiance
                                                    </p>
                                                    
                                                    <!-- Copyright -->
                                                    <p style="margin: 20px 0 0 0; color: #95a5a6; font-size: 12px; text-align: center;">
                                                        © 2025 Bia Safia. Tous droits réservés.<br>
                                                        Cet email a été envoyé à votre adresse car vous possédez un compte Bia Safia.
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                
                            </table>
                            
                        </td>
                    </tr>
                </table>
                
            </body>
            </html>
            """
            
            # Contenu texte simple (fallback)
            text_content = f"""
            Bia Savia - Réinitialisation de mot de passe
            
            Bonjour,
            
            Vous avez demandé la réinitialisation de votre mot de passe sur Bia Savia.
            
            Cliquez sur le lien suivant pour créer un nouveau mot de passe :
            {reset_url}
            
            Important : Ce lien est valide pendant 15 minutes seulement.
            
            Si vous n'avez pas demandé cette réinitialisation, vous pouvez ignorer cet email.
            
            Cordialement,
            L'équipe Bia Savia
            """
            
            # Créer l'email avec contenu HTML et texte
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user_email]
            )
            email.attach_alternative(html_content, "text/html")
            
            # Envoyer l'email
            result = email.send()
            
            if result:
                logger.info(f"Email de réinitialisation envoyé avec succès à {user_email}")
                return True
            else:
                logger.error(f"Échec de l'envoi de l'email à {user_email}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email : {str(e)}")
            return False
    
    @staticmethod
    def send_welcome_email(user_email, username):
        """
        Envoie un email de bienvenue à un nouvel utilisateur
        """
        try:
            subject = 'Bienvenue sur Bia Savia !'
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white;">
                    
                    <!-- Header vert -->
                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #4CAF50;">
                        <tr>
                            <td style="padding: 40px; text-align: center; color: white;">
                                <h1 style="margin: 0; font-size: 28px; color: white; font-weight: bold;">Bienvenue sur Bia Savia !</h1>
                            </td>
                        </tr>
                    </table>
                    
                    <!-- Contenu -->
                    <table width="100%" cellpadding="0" cellspacing="0">
                        <tr>
                            <td style="padding: 40px;">
                                
                                <p style="font-size: 18px; color: #333; margin: 0 0 20px 0; font-weight: bold;">Bonjour {username},</p>
                                
                                <p style="font-size: 16px; color: #555; margin: 0 0 20px 0; line-height: 1.5;">
                                    Félicitations ! Votre compte Bia Savia a été créé avec succès.
                                </p>
                                
                                <p style="font-size: 16px; color: #555; margin: 0 0 15px 0; line-height: 1.5;">
                                    Vous pouvez maintenant :
                                </p>
                                
                                <ul style="color: #555; font-size: 16px; line-height: 1.8; margin: 0 0 30px 0; padding-left: 30px;">
                                    <li>Partager vos connaissances avec la communauté</li>
                                    <li>Poser des questions sur l'agriculture</li>
                                    <li>Découvrir des conseils et astuces</li>
                                    <li>Interagir avec d'autres agriculteurs</li>
                                </ul>
                                
                                <p style="font-size: 16px; color: #555; margin: 0 0 20px 0; line-height: 1.5;">
                                    Nous sommes ravis de vous compter parmi nous !
                                </p>
                                
                            </td>
                        </tr>
                    </table>
                    
                    <!-- Footer -->
                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8f9fa;">
                        <tr>
                            <td style="padding: 20px; text-align: center; color: #666; font-size: 14px;">
                                © 2025 Bia Savia. Tous droits réservés.
                            </td>
                        </tr>
                    </table>
                    
                </div>
            </body>
            </html>
            """
            
            text_content = f"""
            Bienvenue sur Bia Savia !
            
            Bonjour {username},
            
            Félicitations ! Votre compte Bia Savia a été créé avec succès.
            
            Vous pouvez maintenant :
            - Partager vos connaissances avec la communauté
            - Poser des questions sur l'agriculture
            - Découvrir des conseils et astuces
            - Interagir avec d'autres agriculteurs
            
            Nous sommes ravis de vous compter parmi nous !
            
            © 2025 Bia Savia. Tous droits réservés.
            """
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user_email]
            )
            email.attach_alternative(html_content, "text/html")
            
            result = email.send()
            
            if result:
                logger.info(f"Email de bienvenue envoyé avec succès à {user_email}")
                return True
            else:
                logger.error(f"Échec de l'envoi de l'email de bienvenue à {user_email}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email de bienvenue : {str(e)}")
            return False

    @staticmethod
    def send_notification_email(user_email, title, message):
        """
        Envoie un email de notification générique
        """
        try:
            subject = f'Notification Bia Savia - {title}'
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white;">
                    
                    <!-- Header vert -->
                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #4CAF50;">
                        <tr>
                            <td style="padding: 40px; text-align: center; color: white;">
                                <h1 style="margin: 0; font-size: 28px; color: white; font-weight: bold;">Bia Savia</h1>
                                <p style="margin: 10px 0 0 0; font-size: 16px; color: white;">{title}</p>
                            </td>
                        </tr>
                    </table>
                    
                    <!-- Contenu -->
                    <table width="100%" cellpadding="0" cellspacing="0">
                        <tr>
                            <td style="padding: 40px;">
                                
                                <p style="font-size: 16px; color: #555; margin: 0 0 20px 0; line-height: 1.5;">
                                    {message}
                                </p>
                                
                            </td>
                        </tr>
                    </table>
                    
                    <!-- Footer -->
                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f8f9fa;">
                        <tr>
                            <td style="padding: 20px; text-align: center; color: #666; font-size: 14px;">
                                © 2025 Bia Savia. Tous droits réservés.
                            </td>
                        </tr>
                    </table>
                    
                </div>
            </body>
            </html>
            """
            
            text_content = f"""
            {title}
            
            {message}
            
            © 2025 Bia Savia. Tous droits réservés.
            """
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user_email]
            )
            email.attach_alternative(html_content, "text/html")
            
            result = email.send()
            
            if result:
                logger.info(f"Email de notification envoyé avec succès à {user_email}")
                return True
            else:
                logger.error(f"Échec de l'envoi de l'email de notification à {user_email}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email de notification : {str(e)}")
            return False
