from rest_framework import permissions, exceptions
from core.models import AuthSession


class AuthPermission(permissions.BasePermission):
    def authenticate(self, request):
        token = self.get_token_from_request(request)

        if not token:
            return None

        jwt_session = AuthSession.find_by_token(token)

        if not jwt_session:
            raise exceptions.AuthenticationFailed('Invalid or expired token')

        return (jwt_session.user, None)

    def has_permission(self, request, view):
        user = request.user  # The user is set by the authentication process

        # TODO: Check if user is active / role is allowed to access this endpoint

        return True  # You can customize this based on your permission logic

    def get_token_from_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]

        return None
