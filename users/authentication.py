from datetime import datetime  # Importa a classe datetime do módulo datetime
from rest_framework import permissions  # Importa o módulo permissions do Django REST framework
from rest_framework.permissions import BasePermission  # Importa a classe BasePermission do Django REST framework
from rest_framework_jwt.authentication import JSONWebTokenAuthentication  # Importa a classe JSONWebTokenAuthentication do rest_framework_jwt.authentication
from rest_framework_jwt.settings import api_settings  # Importa as configurações do JWT do rest_framework_jwt.settings

from users.serializers import UserUsernameAndIdSerializer  # Importa o serializador UserUsernameAndIdSerializer do aplicativo users

# Define uma classe JwtExactritr que herda de JSONWebTokenAuthentication
class JwtExactritr(JSONWebTokenAuthentication):
    def get_jwt_value(self, request):
        pass

# Define uma função jwt_payload_handler para criar um payload personalizado para o token JWT
def jwt_payload_handler(user):
    """ Custom payload handler
    Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    return {
        'user_id': user.pk,
        'username': user.username,
        'email': user.email,
        "iss": "http://melardev.com",
        'roles': ['ROLE_ADMIN' if user.is_staff else 'ROLE_USER'],
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        # 'orig_iat': timegm(datetime.utcnow().utctimetuple())
    }

# Define uma função jwt_response para criar a resposta personalizada para as visualizações de login e atualização do JWT
def jwt_response(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    roles = []
    if user.is_staff:
        roles.append('ROLE_ADMIN')
    else:
        roles.append('ROLE_USER')
    user_dto = UserUsernameAndIdSerializer(user, context={'request': request}).data
    user_dto.update({'roles': roles})
    return {
        "success": True,
        'user': user_dto,
        'token': token,
        'catson': 'Estou a entender'
    }

# Define uma função de teste chamada test
def test(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

# Define uma classe de permissão chamada IsAdminOrReadOnly
class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS or
                (request.user and
                 request.user.is_staff)
        )

# Define uma classe de permissão chamada IsAdminOrOwnerOrReadOnly
class IsAdminOrOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and (request.user.is_staff or obj.user == request.user)
