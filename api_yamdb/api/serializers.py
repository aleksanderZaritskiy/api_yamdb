from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from rest_framework import serializers

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comments,
)
from reviews.validators import validate_name
from users.models import User
from reviews.constants import LENGTH_USER_NAME, LENGTH_EMAIL


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=LENGTH_USER_NAME,
        validators=(
            validate_name,
            UnicodeUsernameValidator(),
        ),
    )
    email = serializers.EmailField(
        max_length=LENGTH_EMAIL,
    )

    def create(self, validated_data):
        try:
            user, exists = User.objects.get_or_create(
                email=validated_data.get('email'),
                username=validated_data.get('username'),
            )
            return user
        except IntegrityError:
            raise serializers.ValidationError(
                'Пользователь с таким именем или почтой уже существует'
            )


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=LENGTH_USER_NAME,
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


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


class ReadTitleSerializer(serializers.ModelSerializer):
    """Read title"""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )
        read_only_fields = ('pub_date',)


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
