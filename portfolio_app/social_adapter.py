from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter to prevent duplicate accounts and link social accounts 
    to existing accounts with the same email address.
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        This hook is invoked before a social login is processed.
        We check if there's an existing user with the same email and link them.
        """
        # Only process if the social account doesn't have a user yet
        if sociallogin.is_existing:
            return
            
        # Get email from social account
        email = sociallogin.account.extra_data.get('email')
        if not email:
            return
            
        # Try to find existing user with this email
        try:
            user = User.objects.get(email=email)
            
            # Link the social account to the existing user
            sociallogin.connect(request, user)
            
            # Add a success message
            messages.success(
                request, 
                f"Your Google account has been linked to your existing account ({email})."
            )
            
            # Redirect to prevent the normal flow from continuing
            raise ImmediateHttpResponse(redirect('account_login'))
            
        except User.DoesNotExist:
            # No existing user found, continue with normal signup
            logger.info(f"No existing user found for email: {email}")
            return
            
        except Exception as e:
            logger.error(f"Error in pre_social_login: {e}")
            return
    
    def save_user(self, request, sociallogin, form=None):
        """
        Override save_user to ensure consistent user creation.
        """
        user = super().save_user(request, sociallogin, form=form)
        
        # Ensure user has a proper username (Google might not provide one)
        if not user.username:
            # Generate username from email or create a unique one
            base_username = sociallogin.account.extra_data.get('email', '').split('@')[0]
            username = base_username
            counter = 1
            
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1
                
            user.username = username
            user.save()
        
        return user
