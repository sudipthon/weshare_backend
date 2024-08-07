from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.shortcuts import get_list_or_404
from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Prefetch, Count


class IsAuthenticatedCustom(IsAuthenticated):
    message = "You need to login for this action."


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
        # self.pagination_class = CustomPageNumberPagination  # set the custom pagination class

        base_query = Post.objects.filter(Q(post_type="Giveaway") & Q(flag=None))
        if request.user.is_authenticated:
            giveaway = base_query.exclude(author=request.user)
        else:
            giveaway = base_query

        page = self.paginate_queryset(giveaway)

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):
        """Return a list of comments for a specific post."""
        post = self.get_object()
        comments = Comment.objects.filter(post=post, reply=None)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path="exchange")
    def list_exchanges(self, request, *args, **kwargs):
        """Return a list of exchange posts."""
        base_query = Post.objects.filter(Q(post_type="Exchange") & Q(flag=None))
        if request.user.is_authenticated:
            exchanges = base_query.exclude(author=request.user)
        else:
            exchanges = base_query
        page = self.paginate_queryset(exchanges)

        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    # @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    # def my_posts(self, request):
    #     """Return a list of posts created by the current user."""
    #     my_posts = Post.objects.filter(author=request.user)
    #     page = self.paginate_queryset(my_posts)
    #     if not my_posts:
    #         return Response(
    #             {"message": "No posts by this user."}, status=status.HTTP_404_NOT_FOUND
    #         )
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     serializer = self.get_serializer(my_posts, many=True)
    #     return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def user_posts(self, request,pk=None):
        """Return a list of posts created by the current user."""

        user = User.objects.get(id=pk)
        posts = Post.objects.filter(author=user)
        page = self.paginate_queryset(posts)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def search(self, request):
        """Return a list of posts that match the search query."""
        query = request.query_params.get("query", "")
        post_type = request.query_params.get("post_type", "")
        # try:
        posts = Post.objects.filter(
            (
                Q(author__username__icontains=query)
                | Q(content__icontains=query)
                | Q(tags__name__icontains=query)
            )
            & Q(post_type=post_type)
            & Q(flag=None),
        )
        page = self.paginate_queryset(posts)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

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
        super().update(request, *args, **kwargs)
        return Response({"message": "Post Updated"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticatedCustom])
    def upvote(self, request, pk=None):
        post = self.get_object()
        post.upvotes.add(request.user)
        return Response({"status": "Post upvoted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def undo_upvote(self, request, pk=None):
        post = self.get_object()
        post.upvotes.remove(request.user)
        return Response({"status": "upvote removed"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {"error": "You are not the author of this post."},
                status=status.HTTP_403_FORBIDDEN,
            )
        post.comments.all().delete()
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Post deleted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def set_flag(self, request, *args, **kwargs):
        flag = request.data.get("flag")
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {"error": "You are not the author of this post."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if post.flag != None:
            return Response(
                {"error": "Post already flagged."},
                status=status.HTTP_428_PRECONDITION_REQUIRED,
            )
        # if post.post_type == flag:
        post.flag = flag
        post.save()

        return Response({"message": f"Post flagged {flag}"}, status=status.HTTP_200_OK)

    def get_permissions(self):
        """Instantiates and returns the list of permissions."""

        if self.action in ["create", "update", "partial_update", "my_posts"]:
            self.permission_classes = [IsAuthenticatedCustom, IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in [
            "list_giveaways",
            "list_exchanges",
            "search",
            "user_posts",
            "comments",
        ]:
            self.permission_classes = []

        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    # queryset = Comment.objects.filter(reply=None)

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(reply=None)

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
        parent_id = request.data.get("reply")
        reply = None
        if parent_id is not None:
            try:
                reply = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist:
                return Response(
                    {"error": "Parent comment does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        comment = Comment.objects.create(
            author=request.user, post=post, text=text, reply=reply
        )
        serializer = self.get_serializer(comment)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "Comment added"}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(pk=kwargs["pk"])
        except Comment.DoesNotExist:
            return Response(
                {"error": "Comment does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if comment.author != request.user:
            return Response(
                {"error": "You are not the author of this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        comment.delete()
        return Response({"message": "Comment deleted"}, status=status.HTTP_200_OK)


class ReportsViewSet(viewsets.ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer
    permission_classes = [IsAuthenticated]

    # def create(self, serializer):
    def create(self, request, *args, **kwargs):
        user = self.request.user
        post_id = request.data.get("post_id")
        post = Post.objects.get(id=post_id)
        if Reports.objects.filter(author=user, post=post).exists():
            return Response(
                {"error": "You have already reported this post."},
                # status=status.HTTP_400_BAD_REQUEST,
                status=status.HTTP_403_FORBIDDEN,
            )
        report = Reports.objects.create(
            author=user, post=post, reason=request.data.get("reason")
        )
        serializer = self.get_serializer(report)
        return Response(
            {"message": "Report added succesfully"}, status=status.HTTP_201_CREATED
        )
