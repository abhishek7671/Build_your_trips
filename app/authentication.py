from rest_framework_simplejwt.authentication import JWTAuthentication as JWTA

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from rest_framework.exceptions import AuthenticationFailed




class JWTAuthentication(JWTA):

    """
    This custom wrapper skip all the public urls from authentication.
    """




    def authenticate(self, request):
        res = super().authenticate(request)
        
        if res is None:
            return res
        user, token = res
        refersh_token=OutstandingToken.objects.filter(user=user).latest("id")
        if BlacklistedToken.objects.filter(token=refersh_token).exists():
            raise AuthenticationFailed('Your Token is Expired')
        print(refersh_token.token)
        return (user,token)
