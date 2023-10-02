from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, singup, get_jwt_token

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', singup, name='signup'),
    path('v1/auth/token/', get_jwt_token, name='token')
]
