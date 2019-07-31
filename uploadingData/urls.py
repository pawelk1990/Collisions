
from django.contrib import admin
from django.urls import path
from .views import (
    home_page,
    form_page,
    FileFieldView,
    robots_page
)

urlpatterns = [
    path('', FileFieldView.as_view()),
    path('home', home_page),
    path('robot', robots_page, name = 'r')
]
