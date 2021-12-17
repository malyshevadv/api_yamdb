from django.contrib.auth import get_user_model
from rest_framework import validators, serializers

from reviews.models import Category, Comment, Genre, Review, Titles


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='Вы уже писали отзыв на это произведение.'
            )
        ]
