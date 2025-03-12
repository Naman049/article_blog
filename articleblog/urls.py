from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    LogoutView,
    ArticleListCreateView,
    ArticleDetailView,
    ArticleCommentCreateView,
    ArticleCommentListView,
    FlagCommentView,
    CategoryViewSet,
    ArticleListByCategoryView,
    UserArticleListView

)

category_list = CategoryViewSet.as_view({'get': 'list', 'post': 'create'})
category_detail = CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})


urlpatterns = [
    # ✅ Authentication Routes
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ Article Routes
    path('articles/', ArticleListCreateView.as_view(), name='article-list'),
    path('user/articles/', UserArticleListView.as_view(), name='user-article-list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),

    # ✅ Comment Routes
    # Endpoint for adding a comment to an article
    path('articles/<int:article_id>/comments/', ArticleCommentCreateView.as_view(), name='article-comments'),

    # Endpoint for listing all comments on a specific article
    path('articles/<int:article_id>/all-comments/', ArticleCommentListView.as_view(), name='article-comments'),

    # Endpoint for flagging/unflagging a comment
    path('articles/<int:article_id>/comments/<int:pk>/flag/', FlagCommentView.as_view(), name='flag-comment'),

    # Categories
    path('categories/', category_list, name='category-list'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),
    path('articles/category/<str:category_name>/', ArticleListByCategoryView.as_view(), name='articles-by-category'),
]

