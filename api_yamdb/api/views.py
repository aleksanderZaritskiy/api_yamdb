from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    ReadTitleSerializer,
    CreateTitleSerializer,
    ReviewsSerializer,
    CommentsSerializer,
)
from .permissions import IsAuthorAdminSuperUserPermissions, IsAdminOrReadOnly
from .filters import TitleFilter
from .mixins import MixinsSet


class CategoryViewSet(MixinsSet):
    """Category endpoint"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class GenreViewSet(MixinsSet):
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

    queryset = Title.objects.all().annotate(rating=Avg('title_review__score'))
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
        return self.get_title_id().title_review.all()

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
        return self.get_review_id().review_comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title_id(),
            review=self.get_review_id(),
        )
