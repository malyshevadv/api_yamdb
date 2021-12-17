from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Category, Comment, Genre, Review, Titles

from .serializers import (CommentSerializer, ReviewSerializer)
from .permissions import IsAuthorAdminModerOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes =  [IsAuthor & IsAdmin & IsModerator | ReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Titles, pk=title_id)
        review = get_object_or_404(Review, pk=review_id)
        comments_list = review.comments.all()
        return comments_list

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Titles, pk=title_id)
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review, author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes =  [IsAuthor & IsAdmin & IsModerator | ReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        review_list = title.reviews.all()
        return review_list

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        serializer.save(title=title, author=self.request.user)
