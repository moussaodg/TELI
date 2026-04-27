import logging

from rest_framework.authentication import TokenAuthentication, get_authorization_header


class LenientTokenAuthentication(TokenAuthentication):
    """
    Accept standard "Token <key>" and "Bearer <key>" values.
    Also normalize malformed headers that include the full authorization
    prefix in the header value.
    """

    keyword = "Token"

    def authenticate(self, request):
        header = get_authorization_header(request)
        logging.getLogger(__name__).debug('LenientTokenAuthentication header=%r', header)
        if header:
            parsed = self._normalize_authorization_header(header)
            if parsed is not None:
                logging.getLogger(__name__).debug('LenientTokenAuthentication parsed=%r', parsed)
                request.META["HTTP_AUTHORIZATION"] = parsed.decode("utf-8")
        return super().authenticate(request)

    def _normalize_authorization_header(self, header: bytes) -> bytes | None:
        header = header.strip()
        lower = header.lower()

        if lower.startswith(b"authorization:"):
            _, value = header.split(b":", 1)
            return self._normalize_authorization_header(value.strip())

        if lower.startswith(b"authorization bearer "):
            token = header.split(b" ", 2)[2].strip()
            return b"Token " + token

        if lower.startswith(b"authorization token "):
            token = header.split(b" ", 2)[2].strip()
            return b"Token " + token

        if lower.startswith(b"authorization "):
            _, value = header.split(b" ", 1)
            return self._normalize_authorization_header(value.strip())

        if lower.startswith(b"bearer "):
            token = header.split(b" ", 1)[1].strip()
            if token.lower().startswith(b"authorization"):
                return self._normalize_authorization_header(token)
            return b"Token " + token

        if lower.startswith(b"token "):
            return header

        return None
