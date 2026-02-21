# Environment Variables Configuration
# Copy this file to env.py and fill in your actual values

# Database Configuration
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=localhost
DATABASE_PORT=3306

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Vertex AI Configuration (for CV parsing)
VERTEXAI_PROJECT_ID=your_google_cloud_project_id
VERTEXAI_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json

# Cloudflare Configuration (for custom domain management)
# Get your API token from: https://dash.cloudflare.com/profile/api-tokens
# Required permissions: Zone:Zone:Edit, Zone:Zone:Read, Account:Account:Read
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id

# Domain Configuration
BASE_DOMAIN=mifolio.live

# Security
SECRET_KEY=your_django_secret_key
DEBUG=False

# Site Configuration
SITE_NAME=MIfolio
