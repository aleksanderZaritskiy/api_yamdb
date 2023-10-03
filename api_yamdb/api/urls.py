from django.urls import path, include
from rest_framework.routers import SimpleRouter

from users.views import UserViewSet, SignUpView, get_jwt_token
from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewsViewSet,
    CommentsViewsSet,
)


VERSION_API = 'v1'

router_v1 = SimpleRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewsSet,
    basename='comment',
)

urlpatterns = [
    path(f'{VERSION_API}/', include(router_v1.urls)),
    path(f'{VERSION_API}/auth/signup/', SignUpView.as_view(), name='signup'),
    path(f'{VERSION_API}/auth/token/', get_jwt_token, name='token'),
]
