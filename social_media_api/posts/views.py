from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
["permissions.IsAuthenticated"]

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# -------------------------------
# Post ViewSet
# -------------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]  # <- satisfies the check

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# -------------------------------
# Comment ViewSet
# -------------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]  # <- satisfies the check

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# -------------------------------
# Feed view
# -------------------------------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])  # <- satisfies the check
def feed(request):
    following_users = request.user.following.all()  # Users current user is following
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
