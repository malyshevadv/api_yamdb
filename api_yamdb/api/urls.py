from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet, UserMe, UserViewSet, get_token, signup


router = DefaultRouter()

router.register(
    r'titles\/(?P<title_id>\d+)\/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles\/(?P<title_id>\d+)\/reviews/(?P<review_id>\d+)\/comments',
    CommentViewSet,
    basename='comments'
)

router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
    path('v1/users/me/', UserMe.as_view(), name='profile'),
    path('v1/', include(router.urls))
]
