from http import HTTPStatus

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdmin
from .serializers import (SignUpSerializer, MyUserSerializer,
                          TokenSerializer, MyUserEditSerializer)
from .models import MyUser


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def singup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        MyUser,
        username=serializer.validated_data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация',
        message=f'Код подтверждения: {confirmation_code}',
        from_email=None,
        recipient_list=[user.email],
    )

    return Response(serializer.data, status=HTTPStatus.OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        MyUser,
        username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=HTTPStatus.OK)

    return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    @action(
        methods=[
            'get',
            'patch',
        ],
        detail=False,
        url_path='me',
        serializer_class=MyUserEditSerializer,
        permission_classes=[permissions.IsAuthenticated],
    )
    def owner_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=HTTPStatus.OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        return Response(status=HTTPStatus.METHOD_NOT_ALLOWED)
