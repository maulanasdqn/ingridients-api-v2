from django.urls import path
from . import views

urlpatterns = [
    path("", views.IngridientView.as_view()),
    path('<str:pk>/', views.IngridientDetail.as_view())
]