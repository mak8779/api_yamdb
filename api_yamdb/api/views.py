from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from api.serializers import SignupSerializer, TokenSerializer
from django.contrib.auth import get_user_model
import random

User = get_user_model()


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            confirmation_code = str(random.randint(100000, 999999))

            user, created = User.objects.get_or_create(
                username=username,
                email=email,
                defaults={'confirmation_code': confirmation_code}
            )

            if not created:
                user.confirmation_code = confirmation_code
                user.save()

            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {confirmation_code}',
                'noreply@yamdb.com',
                [email],
                fail_silently=False,
            )

            return Response(
                {'email': email, 'username': username},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(generics.CreateAPIView):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(
                username=serializer.validated_data['username']
            )

            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
