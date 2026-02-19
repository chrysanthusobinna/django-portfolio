class SubdomainMiddleware:
    """
    Sets request.subdomain when host is like: <username>.mifolio.live
    """
    def __init__(self, get_response):
        self.get_response = get_response

        # domain
        self.base_domain = "mifolio.live"

        # Subdomains  not acting as usernames
        self.reserved = {"www", "admin", "api", "static", "media"}

    def __call__(self, request):
        host = request.get_host().split(":")[0].lower()  # remove port

        request.subdomain = None

        # Only match: *.mifolio.live
        if host.endswith("." + self.base_domain):
            sub = host[: -(len(self.base_domain) + 1)]  # remove ".mifolio.live"
            if sub and sub not in self.reserved:
                request.subdomain = sub

        return self.get_response(request)
