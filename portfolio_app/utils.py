from django.contrib import messages

def validate_image_file(request, file_field_name, label_name, allowed_extensions=('jpg', 'jpeg', 'png', 'gif')):
    """
    Validates if the uploaded file is an image with an allowed extension.
    """
    if file_field_name in request.FILES:
        file = request.FILES[file_field_name]
        if not file.name.lower().endswith(allowed_extensions):
            error_message = f"Invalid file type for {label_name}. Only {', '.join(allowed_extensions)} files are allowed."
            return False, error_message
    return True, None


from django.core.mail import send_mail
from django.conf import settings

def send_contact_email(subject, message, recipient_list):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
        return True, None  
    except Exception as e:
        error_message = f"Error sending email: {e}"
        print(f"Error sending email: {e}")
        return False, error_message   
