from rest_framework import authentication, permissions, exceptions
from core.models import AuthSession


class AuthPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # TODO: Implement role based permission
        return True


class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Extract the token from the request's Authorization header
        token = self.get_token_from_request(request)

        if not token:
            raise exceptions.AuthenticationFailed(
                'Authenticaton token not provided')

        # Find the user associated with the token
        user = self.get_user_from_token(token)

        if not user:
            raise exceptions.AuthenticationFailed(
                'Invalid or expired token')

        return (user, None)

    def get_token_from_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]

        return None

    def get_user_from_token(self, token):
        try:
            # Find the user associated with the token
            jwt_session = AuthSession().find_by_token(token)
            if jwt_session:
                return jwt_session.user
            
            return None  # Token is invalid or expired
        except Exception as e:
            raise exceptions.NotFound(e)
