from datetime import date

from django.conf import settings
from django.db.models import Avg
from rest_framework import serializers

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comments,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CreateTitleSerializer(serializers.ModelSerializer):
    """Create title"""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'genre',
            'category',
            'description',
        )
        read_only_fields = ('pub_date',)

    def validate(self, data):
        today = date.today()
        if data.get('year') and data.get('year') > today.year:
            raise serializers.ValidationError(
                'Нельзя добавить произведение ещё не вышедшее'
            )
        return data


class ReadTitleSerializer(serializers.ModelSerializer):
    """Read title"""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        read_only_fields = ('pub_date',)

    def get_rating(self, obj):
        reviews = obj.title_reviews.aggregate(Avg('score'))
        if reviews.get('score__avg'):
            return int((reviews.get)('score__avg'))
        return None

    def validate(self, data):
        today = date.today()
        if data.get('year') > today.year:
            raise serializers.ValidationError(
                'Нельзя добавить произведение ещё не вышедшее'
            )
        return data


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    score = serializers.ChoiceField(choices=settings.CHOICES)

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'author', 'pub_date')
        read_only_fields = ('title', 'author')

    def validate(self, data):
        exists_reviews = Review.objects.filter(
            author=self.context.get('request').user,
            title=self.context.get('view').kwargs.get('title_id'),
        ).exists()

        if self.context['request'].method == 'POST' and exists_reviews:
            raise serializers.ValidationError(
                'Вы уже оценили произведение',
            )
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('title', 'review')
