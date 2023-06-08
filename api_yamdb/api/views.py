from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import viewsets
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import filters, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from .permissions import (
    IsAdminOrIsSuperUser,
    AdminOrReadOnly,
    ReviewCommentPermission
)
from .mixins import GenreCategoryModelViewSet
from reviews.models import Comment, Genre, Category, Review, Title, User
from .serializers import (
    CommentSerializer,
    GenreSerializer,
    CategorySerializer,
    UserSerializer,
    UserRegisterSerializer,
    UserRecieveTokenSerializer,
    ReviewSerializer,
    TitleWatchSerializer,
    TitleCreateSerializer,
)
from .utils import send_confirmation_code
from .filters import TitleFilterSet


class GenreViewSet(GenreCategoryModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleWatchSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        queryset = Review.objects.filter(title=title)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        author = self.request.user

        serializer.save(title=title, author=author)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (permissions.IsAuthenticated, IsAdminOrIsSuperUser)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def get_me_data(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True,
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        try:
            user = User.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email'),
            )
            send_confirmation_code(
                email=user.email,
                confirmation_code=default_token_generator.make_token(user),
            )
            return Response(request.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            serializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.create(**serializer.validated_data)
            send_confirmation_code(
                email=user.email,
                confirmation_code=default_token_generator.make_token(user),
            )
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserReceiveTokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserRecieveTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Код подтверждения невалиден'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermission,)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        queryset = Comment.objects.filter(
            review__title_id=title_id, review_id=review_id
        )
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, id=review_id)
        author = self.request.user

        serializer.save(review=review, author=author)
