from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser
from .serializes import RegistrationSerializer, AuthorizationSerializer


@api_view(['POST'])
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response(
            {
                'user_token': token.key
            }
        )
    else:
        return Response(
            {
                'error': serializer.errors
            }
        )


@api_view(['POST'])
def authentication(request):
    serializer = AuthorizationSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = CustomUser.objects.get(
                email=serializer.validated_data['email']
            )
        except:
            return Response(
                {
                    'error': {
                        'code': 404,
                        'message': 'Not found'
                    }
                }
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'user_token': token.key
            }
        )
    else:
        return Response(
            {
                'error': serializer.errors
            }
        )


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def logout(request):
    request.user.auth_token.delete()
    return Response(
        {
            'data': {
                'message': 'logout'
            }
        }
    )
