
from django.contrib import admin
from django.urls import path
from .views import (
    home_page,
    form_page,
    FileFieldView,
    robots_page, 
    ComparePage
)

urlpatterns = [
    path('', FileFieldView.as_view()),
    path('home', home_page),
    path('robot', robots_page),
    path('<str:robot_name>/compare', ComparePage.as_view()),
    path('<str:robot_name>', home_page),
]
