from django.conf import settings
from rest_framework import serializers

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comments,
)
from users.models import User
from reviews.constants import LENGTH_USER_NAME, LENGTH_EMAIL


class SignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=LENGTH_USER_NAME,
    )

    email = serializers.EmailField(
        max_length=LENGTH_EMAIL,
    )
    bio = serializers.CharField(
        required=False,
        write_only=True,
    )
    first_name = serializers.CharField(
        max_length=LENGTH_USER_NAME,
        required=False,
        write_only=True,
    )
    last_name = serializers.CharField(
        max_length=LENGTH_USER_NAME,
        required=False,
        write_only=True,
    )

    def create(self, validated_data):

        current_user = User.objects.filter(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
        ).exists()
        current_email = User.objects.filter(
            email=validated_data.get('email')
        ).exists()
        current_name = User.objects.filter(
            username=validated_data.get('username')
        ).exists()

        if current_user:
            return User.objects.get(**validated_data)

        if not current_user and (current_email or current_name):
            raise serializers.ValidationError(
                'Пользователь с таким именем или почтой уже существует'
            )

        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.last_name = validated_data.get(
            "last_name", instance.last_name
        )
        instance.bio = validated_data.get("bio", instance.bio)
        instance.save()
        return instance

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Данное имя запрещенно')
        return value


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
    username = serializers.CharField(required=True, max_length=150)
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
