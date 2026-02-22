import os


# for local development
os.environ["DATABASE_NAME"] = "hotel_booking"
os.environ["DATABASE_USER"] = "postgres"
os.environ["DATABASE_PASSWORD"] = "root"
os.environ["DATABASE_HOST"] = "localhost"
os.environ["DATABASE_PORT"] = "5432"

# # POSTGRESQL URL
# os.environ.setdefault(
#     "DATABASE_URL", "<put DATABASE_URL here>"
# )

# DJANGO SECRET_KEY
os.environ.setdefault(
    "SECRET_KEY", "<put DJANGO SECRET KEY here>"
)

# CLOUDINARY URL
os.environ.setdefault(
    "CLOUDINARY_URL", "cloudinary://<put api_key here>:<put api_secret here>@<put cloud_name here>"
)

# Email settings
os.environ.setdefault("EMAIL_HOST", "<put smtp server here>")
os.environ.setdefault("EMAIL_PORT", "<put email port here>")
os.environ.setdefault("EMAIL_HOST_USER", "<put your-email-address here>")
os.environ.setdefault("EMAIL_HOST_PASSWORD", "<put your-email-password here>")

# Google OAuth
os.environ.setdefault("GOOGLE_CLIENT_ID", "<put Google OAuth client ID here>")
os.environ.setdefault("GOOGLE_CLIENT_SECRET", "<put Google OAuth client secret here>")

# Vertex AI Configuration (replace with your actual values)
VERTEXAI_PROJECT_ID = os.environ.get("VERTEXAI_PROJECT_ID", "your-project-id-here")
VERTEXAI_LOCATION = os.environ.get("VERTEXAI_LOCATION", "us-central1")

# Google Cloud credentials (set this to the path of your service account key)
os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", "/path/to/your/service-account-key.json")

# Base Domain for Subdomain URLs
os.environ.setdefault("BASE_DOMAIN", "mifolio.live")

# Google reCAPTCHA v2 Configuration
# Get these keys from: https://www.google.com/recaptcha/admin/create
os.environ.setdefault("RECAPTCHA_SITE_KEY", "<put reCAPTCHA site key here>")
os.environ.setdefault("RECAPTCHA_SECRET_KEY", "<put reCAPTCHA secret key here>")

# Debug mode for development
os.environ.setdefault("DEBUG", "True")