"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from portfolio_app.views import custom_signup_view

# Custom error handlers
handler404 = 'portfolio_app.views.custom_404'
handler500 = 'portfolio_app.views.custom_500'

urlpatterns = [
    path('admin-panel/', admin.site.urls),
    path('', include('portfolio_app.urls')),
    # Custom signup with reCAPTCHA - must come before allauth.urls
    path('accounts/signup/', custom_signup_view, name='account_signup'),
    path("accounts/", include("allauth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
