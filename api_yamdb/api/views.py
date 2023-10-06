from http import HTTPStatus

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view, permission_classes

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
)
from users.models import User
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    ReadTitleSerializer,
    CreateTitleSerializer,
    ReviewsSerializer,
    CommentsSerializer,
    SignUpSerializer,
    UsersSerializer,
    TokenSerializer,
    UserUpdateSerializer,
)
from .permissions import (
    IsAuthorAdminSuperUserPermissions,
    IsAdminOrReadOnly,
    IsAdmin,
)
from .filters import TitleFilter
from .viewsets_parrents import ViewSet


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        print('1')

        serializer = SignUpSerializer(data=request.data)

        print('2')
        serializer.is_valid(raise_exception=True)

        print(f'is_valid : {serializer.is_valid()}')

        user = serializer.save()

        print('3')

        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Регистрация',
            message=f'Код подтверждения: {confirmation_code}',
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response(data=serializer.data, status=HTTPStatus.OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=HTTPStatus.OK)

    return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
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
            serializer = UserUpdateSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        else:
            serializer = UsersSerializer(user)
        return Response(serializer.data, status=HTTPStatus.OK)


class CategoryViewSet(ViewSet):
    """Category endpoint"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class GenreViewSet(ViewSet):
    """Genre endpoint"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Title endpoint"""

    queryset = Title.objects.all().annotate(rating=Avg('review__score'))
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadTitleSerializer
        return CreateTitleSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """Reviews endpoint"""

    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthorAdminSuperUserPermissions,)
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_title_id(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title_id().review.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title_id())


class CommentsViewsSet(viewsets.ModelViewSet):
    """Comments endpoint"""

    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorAdminSuperUserPermissions,)
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_title_id(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_review_id(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review_id().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title_id(),
            review=self.get_review_id(),
        )
