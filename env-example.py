import os

# POSTGRESQL URL
os.environ.setdefault(
    "DATABASE_URL", "<put DATABASE_URL here>"
)

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
