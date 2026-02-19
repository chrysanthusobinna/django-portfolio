class SubdomainMiddleware:
    """
    Sets request.subdomain when host is like: <username>.<BASE_DOMAIN>
    """
    def __init__(self, get_response):
        self.get_response = get_response

        # Import settings to get BASE_DOMAIN
        from django.conf import settings
        self.base_domain = getattr(settings, 'BASE_DOMAIN')

        # Subdomains  not acting as usernames
        self.reserved = {"www", "admin", "api", "static", "media"}

    def __call__(self, request):
        host = request.get_host().split(":")[0].lower()  # remove port

        request.subdomain = None

        if host.endswith("." + self.base_domain):
            sub = host[: -(len(self.base_domain) + 1)]
            if sub and sub not in self.reserved:
                request.subdomain = sub

        return self.get_response(request)
