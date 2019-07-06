from .serializers import UserSerializerWithToken,UserSerializer


def my_jwt_response(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }

