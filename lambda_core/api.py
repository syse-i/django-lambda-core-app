from django.urls import path, include

app_name = 'lambda_core_api'

urlpatterns = [
    path('user/', include('lambda_core.user_profile.api')),
]
