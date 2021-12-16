from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserMe, UserViewSet, get_token, signup


router = SimpleRouter()

router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
    path('v1/users/me/', UserMe.as_view(), name='profile'),
    path('v1/', include(router.urls))
]
