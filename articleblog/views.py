from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework import status,viewsets,serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Article, Comment,Category
from .serializers import ArticleSerializer, CommentSerializer, RegisterSerializer, CategorySerializer
from rest_framework_simplejwt.views import TokenObtainPairView



#  1. User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

#  2. User Login View (Token Generation)
class LoginView(TokenObtainPairView):
    """
    Uses Django Simple JWT to handle login.
    Returns access & refresh tokens.
    """
    permission_classes = [permissions.AllowAny]

#  2. User Logout View
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the token to log out the user
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)



#  3. List & Create Articles View
# ✅ View for api/articles/ → Shows ALL articles (public view)
class ArticleListCreateView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Allow viewing for everyone, restrict creation

    def get_queryset(self):
        """
        If a category filter is applied, return only articles that belong to at least one of the provided categories.
        Otherwise, return all articles.
        """
        queryset = Article.objects.all()  # Fetch all articles

        category_ids = self.request.query_params.get('category')  # Get categories from query params

        if category_ids:
            category_ids = category_ids.split(",")
            queryset = queryset.filter(categories__id__in=category_ids).distinct()  # Filter by category IDs
            queryset = queryset.exclude(categories=None)
        return queryset

    def perform_create(self, serializer):
        """
        Assign the logged-in user as the author when creating an article.
        """
        serializer.save(author=self.request.user)  # Assign the logged-in user as the author


# ✅ View for api/user/articles/ → Shows only the logged-in user’s articles
class UserArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def get_queryset(self):
        """
        Ensure users only see their own articles and can filter by category.
        """
        user = self.request.user  # Get logged-in user
        queryset = Article.objects.filter(author=user)  # Show only user's articles

        category = self.request.query_params.get('category')  # Check for category filter
        if category:
            queryset = queryset.filter(category__name=category)

        return queryset


#  4. Retrieve, Update, Delete Article View
class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensure users can only access their own articles.
        Optionally filter by category if provided in request.
        """
        queryset = Article.objects.filter(author=self.request.user)  # Only user's articles

        # Get category filter from request
        category_ids = self.request.query_params.getlist('category')
        if category_ids:
            queryset = queryset.filter(categories__id__in=category_ids).distinct() # Filter by category name

        return queryset

#  5. Create a Comment on an Article
    # ✅ Allow users to comment on any article (including their own)
from rest_framework.response import Response
from rest_framework import status

class ArticleCommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        article_id = self.kwargs.get('article_id')
        try:
            article = Article.objects.get(id=article_id)  # Get the article
            serializer.save(user=self.request.user, article=article)  # Use 'user' instead of 'author'
        except Article.DoesNotExist:
            raise serializers.ValidationError({"detail": "Article not found."})

    # ✅ View to list all comments on a specific article


class ArticleCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')

        # Debugging logs
        print(f"Looking for article ID: {article_id}")

        if not Article.objects.filter(id=article_id).exists():
            print("Article not found!")  # This will show in the terminal
            raise NotFound("Article not found")

        queryset = Comment.objects.filter(article_id=article_id)

        if not queryset.exists():
            print("No comments found!")  # This will show in the terminal
            raise NotFound("No comments found for this article")

        return queryset

    # ✅ View to flag/unflag a comment (only on articles posted by the logged-in user)
class FlagCommentView(generics.UpdateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can flag

    def patch(self, request, *args, **kwargs):
        article_id = kwargs.get('article_id')
        comment_id = kwargs.get('pk')

        try:
            article = Article.objects.get(id=article_id)
            comment = Comment.objects.get(id=comment_id, article=article)  # Ensure comment belongs to the article

            # Ensure the logged-in user owns the article
            if article.author != request.user:
                return Response(
                    {"detail": "You can only flag comments on your own articles."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Toggle 'flagged' status
            comment.flagged = not comment.flagged
            comment.save()
            return Response(
                {"detail": f"Comment flagged: {comment.flagged}"},
                status=status.HTTP_200_OK
            )

        except Article.DoesNotExist:
            return Response({"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found in this article."}, status=status.HTTP_404_NOT_FOUND)

# Category
class CategoryViewSet(viewsets.ModelViewSet):  # Supports GET, POST, PUT, DELETE
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ArticleListByCategoryView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        return Article.objects.filter(category__name=category_name, published=True)