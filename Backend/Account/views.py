from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.http import Http404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=["post"],
        url_path="register",
        permission_classes=[AllowAny],
    )
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User created successfully"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def login(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            # return Response({"token": token.key})
            return Response({"token": token.key, "id": user.id})

        else:
            return Response(
                {"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["post"])
    def logout(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            return Response(
                {"detail": "You do not have permission to update this user."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def change_password(self, request, pk=None):
        try:
            user = self.get_object()
        except Http404:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if request.user != user:
            return Response(
                {
                    "detail": "You do not have permission to change this user's password."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not user.check_password(old_password):
            return Response(
                {"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST
            )
        if user.check_password(new_password):
            return Response(
                {"new_password": "New password cannot be the same as old password."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(new_password)
        user.save()
        return Response(
            {"detail": "Password updated successfully."}, status=status.HTTP_200_OK
        )

    # @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    # def reset_password(self, request):
    #     email = request.data.get("email")
    #     user = User.objects.filter(email=email).first()
    #     if user:
    #         token = default_token_generator.make_token(user)
    #         uid = urlsafe_base64_encode(force_bytes(user.pk))
    #         mail_subject = 'Reset your password'
    #         message = render_to_string('reset_password_email.html', {
    #             'user': user,
    #             'domain': 'your-domain.com',
    #             'uid': uid,
    #             'token': token,
    #         })
    #         send_mail(mail_subject, message, 'noreply@your-domain.com', [email])
    #     return Response({"detail": "Password reset email has been sent."}, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ["login", "create", "register"]:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
