from django.conf import settings


def site_info(request):
    # Determine the main domain URL
    if 'localhost' in request.get_host() or '127.0.0.1' in request.get_host():
        main_domain_url = 'http://localhost:8000'
    else:
        main_domain_url = f'https://{settings.BASE_DOMAIN}'
    
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_CONTACT_EMAIL_ADDRESS': settings.SITE_CONTACT_EMAIL_ADDRESS,
        'SITE_CONTACT_PHONE_NUMBER': settings.SITE_CONTACT_PHONE_NUMBER,
        'SITE_CONTACT_LINKEDIN_URL': settings.SITE_CONTACT_LINKEDIN_URL,
        'MAIN_DOMAIN_URL': main_domain_url,
        'BASE_DOMAIN': settings.BASE_DOMAIN,
    }
