# reCAPTCHA v2 Setup Instructions

This project now includes Google reCAPTCHA v2 protection on the registration form to prevent bot signups.

## Installation Steps

### 1. Install the Package
```bash
pip install django-recaptcha==4.0.0
```

### 2. Get reCAPTCHA Keys
1. Go to [Google reCAPTCHA Admin Console](https://www.google.com/recaptcha/admin/create)
2. Fill in the form:
   - **Label**: Your project name (e.g., "Django Portfolio")
   - **reCAPTCHA type**: reCAPTCHA v2 ("I'm not a robot" Checkbox)
   - **Domains**: Add your domains (localhost for development, your production domain)
3. Accept the terms of service
4. Copy your **Site Key** (public key) and **Secret Key** (private key)

### 3. Configure Environment Variables
Add these to your environment or `env.py` file:

```python
# reCAPTCHA Configuration
os.environ.setdefault("RECAPTCHA_PUBLIC_KEY", "your-site-key-here")
os.environ.setdefault("RECAPTCHA_PRIVATE_KEY", "your-secret-key-here")
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Test the Setup
1. Run your development server: `python manage.py runserver`
2. Go to the signup page: `http://localhost:8000/account/signup/`
3. You should see the "I'm not a robot" checkbox
4. Test both successful and failed reCAPTCHA validation

## Configuration Details

### Settings Added
- `RECAPTCHA_PUBLIC_KEY`: Your reCAPTCHA site key
- `RECAPTCHA_PRIVATE_KEY`: Your reCAPTCHA secret key  
- `RECAPTCHA_VERSION = 2`: Use reCAPTCHA v2

### Form Integration
The `CustomSignupForm` now includes:
```python
captcha = ReCaptchaField()
```

### Security Notes
- **Never commit your secret keys to version control**
- Use environment variables in production
- Test with different reCAPTCHA scores in development
- Monitor reCAPTCHA analytics in Google Admin Console

## Troubleshooting

### Common Issues

1. **"Invalid site key" error**
   - Check your RECAPTCHA_PUBLIC_KEY is correct
   - Ensure your domain is registered in reCAPTCHA admin console

2. **"Invalid secret key" error**
   - Check your RECAPTCHA_PRIVATE_KEY is correct
   - Verify no extra spaces or characters

3. **reCAPTCHA not showing**
   - Check JavaScript is enabled in browser
   - Verify internet connection
   - Check browser console for errors

4. **Form submission fails**
   - Ensure django-recaptcha is installed
   - Check migrations are run
   - Verify keys are properly set

### Development Tips
- Use test keys for initial setup
- Test both valid and invalid reCAPTCHA responses
- Check network tab in browser for reCAPTCHA API calls

## Production Deployment
- Add reCAPTCHA keys to your hosting environment variables
- Ensure your production domain is registered in Google reCAPTCHA
- Monitor reCAPTCHA analytics and adjust security settings as needed
