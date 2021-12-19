from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .permissions import (
    IsAdmin, IsAuthor, IsModerator, ReadOnly, IsAuthenticated
)
from .serializers import (CommentSerializer, MeSerializer, ReviewSerializer,
                          SignUpSerializer, TokenSerializer, UserSerializer)


def send_confirmation(user):
    """Отправляет письмо пользователю."""
    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        'Email confirmation',
        f'Ваш код для подтверждения почты: {confirmation_code}',
        'admin@me.to',
        [user.email]
    )


class UserViewSet(ModelViewSet):
    """ViewSet для ресурса users."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = [IsAuthenticated & IsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['username']


class UserMe(RetrieveAPIView, UpdateAPIView):
    """View для users/me/."""

    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Регистрация пользователя.

    Создает нового пользователя, отправляет на указанный email код
    подтверждения.
    Если пользователь с полученными username и email уже существует -
    отправляет ему код подтверждения.
    """
    user = User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')
    ).first()

    if user:
        send_confirmation(user)
        return Response('Мы отправили код подтверждения на вашу почту.',
                        status=status.HTTP_200_OK)
    else:
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            send_confirmation(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Получение JWT-токена.

    Если полученный код подтверждения валиден - отправляет юзеру JWT-токен.
    """
    serializer = TokenSerializer(data=request.data)

    if serializer.is_valid():
        user = get_object_or_404(User, username=request.data.get('username'))

        token_valid = default_token_generator.check_token(
            user, request.data.get('confirmation_code')
        )

        if token_valid:
            jwt_token = RefreshToken.for_user(user).access_token

            return Response({'token': str(jwt_token)},
                            status=status.HTTP_200_OK)

        return Response(
            'Token is invalid or expired. Please request another '
            'confirmation email by signing in.',
            status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticated
        & (IsAuthor | IsModerator | IsAdmin)
        | ReadOnly
    ]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        get_object_or_404(Title, pk=title_id)
        review = get_object_or_404(Review, pk=review_id)
        comments_list = review.comments.all()
        return comments_list

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        get_object_or_404(Title, pk=title_id)
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review, author=self.request.user)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticated
        & (IsAuthor | IsModerator | IsAdmin)
        | ReadOnly
    ]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        review_list = title.reviews.all()
        return review_list

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        author = self.request.user
        if Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже писали отзыв на это произведение.'
            )
        else:
            serializer.save(title=title, author=author)
