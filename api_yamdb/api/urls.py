from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, SignupView, TokenView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view(), name='token'),
]
