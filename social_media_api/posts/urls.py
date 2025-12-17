from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, feed

# Router for ViewSets
router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('comments', CommentViewSet, basename='comment')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),   # /posts/ and /comments/
    path('feed/', feed, name='feed'), # /feed/
]
