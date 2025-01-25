from django.conf import settings


def site_info(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_CONTACT_EMAIL_ADDRESS': settings.SITE_CONTACT_EMAIL_ADDRESS,
        'SITE_CONTACT_PHONE_NUMBER': settings.SITE_CONTACT_PHONE_NUMBER,
        'SITE_CONTACT_LINKEDIN_URL': settings.SITE_CONTACT_LINKEDIN_URL,
    }
