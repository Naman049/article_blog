from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Article, Comment, Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(**data)
        if user:
            refresh = RefreshToken.for_user(user)
            return {'refresh': str(refresh), 'access': str(refresh.access_token)}
        raise serializers.ValidationError("Invalid credentials")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'article', 'user', 'flagged','created_at']
        read_only_fields = ['user', 'created_at','flagged']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ArticleSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),many=True)  # Accepts only category ID
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'published', 'author', 'categories']
        read_only_fields = ['author']  # Prevent user from modifying author

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])  # Extract categories
        article = Article.objects.create(**validated_data)  # Create article
        article.categories.set(categories)  # Assign categories
        return article

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', None)  # Get categories if provided
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if categories is not None:
            instance.categories.set(categories)  # Update categories only if provided

        return instance

    class Meta:
        model = Article
        fields = '__all__'
