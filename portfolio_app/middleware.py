class SubdomainUsernameMiddleware:
    """
    If request is to <username>.mifolio.live, set request.subdomain_username.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(":")[0].lower()  # remove port
        base = "mifolio.live"  # change if needed

        request.subdomain_username = None

        if host.endswith("." + base):
            sub = host[: -(len(base) + 1)]  # everything before .mifolio.live
            # ignore common subdomains
            if sub and sub not in ("www", "api"):
                request.subdomain_username = sub
                print(f"DEBUG: Subdomain detected - username: {sub}")

        return self.get_response(request)
