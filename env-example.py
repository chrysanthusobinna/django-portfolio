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
