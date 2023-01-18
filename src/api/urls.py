from django.urls import path, include
from .views import  MyTokenObtainPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView
from src.views import IngridientView, IngridientDetail


urlpatterns = [
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('ingridient/', include("src.urls"))
]