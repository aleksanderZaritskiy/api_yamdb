from http import HTTPStatus

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view, permission_classes

from api.permissions import IsAdmin
from .serializers import (
    SignUpSerializer,
    UsersSerializer,
    TokenSerializer,
)
from .models import MyUser


class SignUpView(CreateAPIView):
    queryset = MyUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_user = MyUser.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email'),
        ).exists()
        current_email = MyUser.objects.filter(
            email=request.data.get('email')
        ).exists()
        current_name = MyUser.objects.filter(
            username=request.data.get('username')
        ).exists()

        if not current_user and (current_email or current_name):
            return Response(
                'Пользователь с такими именем или почтой уже существует',
                status=HTTPStatus.BAD_REQUEST,
            )

        user, exists = MyUser.objects.get_or_create(
            **serializer.validated_data
        )

        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Регистрация',
            message=f'Код подтверждения: {confirmation_code}',
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )

        user.confirmation_code = confirmation_code
        user.save()
        return Response(data=serializer.data, status=HTTPStatus.OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        MyUser, username=serializer.validated_data['username']
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
    serializer_class = UsersSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    @action(
        methods=[
            'get',
            'patch',
        ],
        detail=False,
        url_path='me',
        url_name='me',
        permission_classes=[permissions.IsAuthenticated],
    )
    def owner_profile(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = SignUpSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=HTTPStatus.OK)
        serializer = SignUpSerializer(user)
        return Response(serializer.data, status=HTTPStatus.OK)
