from django.urls import path
from .views import ListPost, DetailPost

urlpatterns = [
    path('', ListPost.as_view()),
    path('<int:pk>/', DetailPost.as_view()),
]
