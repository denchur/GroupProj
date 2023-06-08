import re
from rest_framework import serializers
from rest_framework import validators

from reviews.models import Category, Comment, Genre, Review, Title, User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleWatchSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField()
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')

    def validate_score(self, value):
        if not 0 < value < 11:
            raise serializers.ValidationError('Score дожен быть от 1 до 10!')
        return value

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            author = self.context['request'].user
            title_id = self.context['view'].kwargs['title_id']

            existing_review = Review.objects.filter(author=author,
                                                    title_id=title_id).exists()
            if existing_review:
                message = 'Already review this title.'
                raise serializers.ValidationError(message)

            return attrs
        return attrs


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=150,
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message=('Пользователь с таким email уже существует'),
            )
        ],
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True,
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message=('Пользователь с таким username уже существует'),
            )
        ],
    )

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


class UserRegisterSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if re.match(r'[Mm][Ee]$', data.get('username')):
            raise serializers.ValidationError('Использовать имя me запрещено')
        return data


class UserRecieveTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$', max_length=150, required=True
    )
    confirmation_code = serializers.CharField(max_length=150, required=True)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
