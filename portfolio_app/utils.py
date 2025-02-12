from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def validate_image_file(request, file_field_name, label_name):
    allowed_extensions = ('jpg', 'jpeg', 'png', 'gif')
    error_msg = (
        "Invalid file type for {label_name}. Only "
        "{extensions} files are allowed."
    ).format(label_name=label_name, extensions=', '.join(allowed_extensions))

    # Validates if the uploaded file is an image with an allowed extension.
    if file_field_name in request.FILES:
        file = request.FILES[file_field_name]
        if not file.name.lower().endswith(allowed_extensions):
            error_message = error_msg
            return False, error_message
    return True, None


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
        return False, error_message
