from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import MyUser


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=MyUser.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=MyUser.objects.all())]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Данное имя запрещенно')
        return value

    class Meta:
        fields = ('username', 'email',)
        model = MyUser


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)


class MyUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=MyUser.objects.all())],
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=MyUser.objects.all())]
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)
        model = MyUser


class MyUserEditSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)
        model = MyUser
        read_only_fields = ('role',)
