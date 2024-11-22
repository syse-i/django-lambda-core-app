from django.urls import path
from rest_framework import routers

from lambda_core.user_profile.views import UserViewSet, GroupViewSet, ProfileAPIView

router = routers.SimpleRouter()

router.register('users/', UserViewSet, basename='user')
router.register('groups/', GroupViewSet, basename='group')

app_name = 'user_profile_api'

urlpatterns = [
    path('', ProfileAPIView.as_view(), name='profile'),
] + router.urls
