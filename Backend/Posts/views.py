from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.shortcuts import get_list_or_404
from .models import *
from .serializers import *


class IsOwner(BasePermission):
    """Permission class to check if request user is the owner of the post."""

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsCommentOwner(BasePermission):
    """Permission class to check if request user is the owner of the comment."""

    def has_object_permission(self, request, view, obj):
        return obj.comments.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        """Return a 404 response with a message suggesting the correct URLs."""
        return Response(
            {
                "message": "This URL is not available. Try http://127.0.0.1:8000/posts/giveaway or http://127.0.0.1:8000/posts/exchange"
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    @action(detail=False, url_path="giveaway")
    def list_giveaways(self, request, *args, **kwargs):
        """Return a list of giveaway posts."""
        giveaways = get_list_or_404(Post, post_type="Giveaway")
        serializer = self.get_serializer(giveaways, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path="exchange")
    def list_exchanges(self, request, *args, **kwargs):
        """Return a list of exchange posts."""
        exchanges = get_list_or_404(Post, post_type="Exchange")
        serializer = self.get_serializer(exchanges, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def my_posts(self, request):
        """Return a list of posts created by the current user."""
        my_posts = Post.objects.filter(author=request.user)
        if not my_posts:
            return Response(
                {"message": "No posts by this user."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(my_posts, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new post."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author__id != request.user:
            return Response(
                {"error": "You are not the author of this post."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {"error": "You are not the author of this post."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        """Instantiates and returns the list of permissions."""
        if self.action in ["create", "update", "partial_update", "destroy", "my_posts"]:
            self.permission_classes = [IsAuthenticated, IsOwner, IsCommentOwner]
        elif self.action in ["list_giveaways", "list_exchanges"]:
            self.permission_classes = []
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        post_id = request.data.get("post_id")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        text = request.data.get("text")
        if not text:
            return Response(
                {"error": "Text field is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        comment = Comment.objects.create(author=request.user, post=post, text=text)
        serializer = self.get_serializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
