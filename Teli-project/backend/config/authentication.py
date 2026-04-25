from rest_framework.authentication import TokenAuthentication, get_authorization_header


class LenientTokenAuthentication(TokenAuthentication):
    """
    Accept both the standard "Token <key>" value and the malformed
    "Authorization: Token <key>" value some clients send as header content.
    """

    keyword = "Token"

    def authenticate(self, request):
        header = get_authorization_header(request)
        if header:
            normalized = header.strip()
            if normalized.lower().startswith(b"authorization: token "):
                request.META["HTTP_AUTHORIZATION"] = normalized.split(b":", 1)[1].strip().decode("utf-8")
        return super().authenticate(request)
