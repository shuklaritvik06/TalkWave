from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .tokens import get_tokens_for_user
from rest_framework import status
from django.forms import model_to_dict


class RegisterUser(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        username = request.data.get("username")
        if email is None or password is None:
            return Response(
                {"error": "Please provide both email and password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(email=email)
            print(user)
            if user is not None:
                return Response(
                    {"error": "Email already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except User.DoesNotExist:
            user = User.objects.create_user(email, password, username=username)
            return Response(
                {
                    "success": f"User {user.email} created successfully",
                    "data": model_to_dict(user),
                },
                status=status.HTTP_201_CREATED,
            )


class LoginUser(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response(
                {"error": "Please provide both email and password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return Response(
                    {
                        "success": f"User {user.email} logged in successfully",
                        "data": model_to_dict(user),
                        "tokens": get_tokens_for_user(user),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except User.DoesNotExist:
            return Response(
                {"error": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutUser(APIView):
    def post(self, request):
        email = request.data.get("email")
        if email is None:
            return Response(
                {"error": "Please provide email"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(email=email)
            user.auth_token.delete()
            return Response(
                {"success": f"User {user.email} logged out successfully"},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
