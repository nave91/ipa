from oauthlib.oauth1 import rfc5849

class OAuth1(object):
    def __init__(self, client_key, client_secret, resource_owner_key, resource_owner_secret):
        self._oauth_client = rfc5849.Client(
            client_key=client_key,
            client_secret=client_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret
        )

    def __call__(self, request):
        request.url, request.headers, request.body = self._oauth_client.sign(
            unicode(request.url),
            unicode(request.method),
            request.body,
            request.headers
        )

    
    
