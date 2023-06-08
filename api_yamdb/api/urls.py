from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    UserViewSet,
    UserRegisterView,
    UserReceiveTokenView,
    ReviewViewSet,
    TitleViewSet,
)

router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UserViewSet, basename='users')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='review')
comments_url = r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments'
router.register(comments_url,
                CommentViewSet, basename='comment')
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', UserRegisterView.as_view(), name='signup'),
    path('v1/auth/token/', UserReceiveTokenView.as_view(), name='get_token')
]
