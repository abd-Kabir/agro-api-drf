from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ObtainAuthTokeAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.filter(user=user).first()
        if token:
            token.delete()
        token = Token(user=user)
        token.save()
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.user.auth_token
        if token:
            token.delete()
        return Response({"message": "Logged out", "status": status.HTTP_200_OK})


class RegisterUser(APIView):
    model = User

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get("username")
        password: str = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        user = User(username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email)
        user.set_password(password)
        user.save()

        return Response({
            "message": "Successfully",
            "status": status.HTTP_200_OK,
            "user_id": user.id})
