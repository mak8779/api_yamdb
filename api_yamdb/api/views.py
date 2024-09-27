# from rest_framework.pagination import LimitOffsetPagination
import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly, IsModeratorOrOwner
from api.serializers import (CategorySerializer, GenreSerializer, MeSerializer,
                             SignupSerializer, TitleSerializer,
                             TitleViewSerializer, TokenSerializer,
                             UserSerializer)
from reviews.models import Category, Genre, Title

User = get_user_model()


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет групп категорий."""

    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    # pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет групп жанров."""

    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    # pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет групп произведений."""
    queryset = Title.objects.all().order_by('name')
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    # pagination_class = PageNumberPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleViewSerializer
        return TitleSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        required_fields = ['username', 'email']
        missing_fields = [
            field for field in required_fields if field not in request.data
        ]

        if missing_fields:
            error_response = {
                field: ['Обязательное поле.'] for field in missing_fields
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']

            if username.lower() == 'me':
                return Response(
                    {'username': ['Юзернейм "me" не разрешен.']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            email = serializer.validated_data['email']

            user = User.objects.filter(username=username, email=email).first()

            if user:
                confirmation_code = str(random.randint(100000, 999999))
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

            confirmation_code = str(random.randint(100000, 999999))
            user = User.objects.create(
                username=username,
                email=email,
                confirmation_code=confirmation_code
            )

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

        if 'username' not in request.data:
            return Response(
                {'detail': 'Username - обязательное поле.'},
                status=status.HTTP_400_BAD_REQUEST
            )

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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    def list(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_admin:
            return Response(status=status.HTTP_403_FORBIDDEN)
        username = kwargs.get('pk')
        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        username = kwargs.get('pk')
        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        username = kwargs.get('pk')
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated, IsModeratorOrOwner],
        url_path='me'
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = MeSerializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            if 'role' in request.data:
                return Response(
                    {"detail": "Роль нельзя изменить."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = MeSerializer(
                request.user,
                data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
