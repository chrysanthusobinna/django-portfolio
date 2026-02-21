class SubdomainMiddleware:
    """
    Sets request.subdomain when host is like: <username>.<BASE_DOMAIN>
    Sets request.custom_domain_user when host is a custom domain
    """
    def __init__(self, get_response):
        self.get_response = get_response

        # Import settings to get BASE_DOMAIN
        from django.conf import settings
        self.base_domain = getattr(settings, 'BASE_DOMAIN')

        # Subdomains not acting as usernames
        self.reserved = {"www", "admin", "api", "static", "media"}

    def __call__(self, request):
        host = request.get_host().split(":")[0].lower()  # remove port

        request.subdomain = None
        request.custom_domain_user = None

        # Check if this is localhost - skip all processing
        if self._is_localhost(host):
            return self.get_response(request)

        # Check if it's a subdomain of base domain
        if host.endswith("." + self.base_domain):
            sub = host[: -(len(self.base_domain) + 1)]
            if sub and sub not in self.reserved:
                request.subdomain = sub
        else:
            # This might be a custom domain (not base domain itself)
            if not self._is_base_domain(host):
                user = self._get_custom_domain_user(host)
                if user:
                    request.custom_domain_user = user

        return self.get_response(request)

    def _is_localhost(self, host):
        """Check if host is localhost or 127.0.0.1"""
        return host in ['localhost', '127.0.0.1']

    def _is_base_domain(self, host):
        """Check if host is the base domain"""
        return host == self.base_domain or host.endswith("." + self.base_domain)

    def _get_custom_domain_user(self, host):
        """Check if host is a custom domain and return the associated user"""
        try:
            from .models import CustomDomain
            custom_domain = CustomDomain.objects.get(domain=host, is_verified=True)
            return custom_domain.user
        except CustomDomain.DoesNotExist:
            return None
