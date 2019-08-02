
from django.contrib import admin
from django.urls import path
from .views import (
    form_page,
    FileFieldView,
    robots_page, 
    ComparePage,
    robot_detail_page,
    compare_robots_page,
    robot_delete_page
)

urlpatterns = [
    path('', FileFieldView.as_view()),
    path('robots', robots_page),
    path('<str:robot_name>', robot_detail_page),
    path('<str:robot_name>/delete', robot_delete_page),
    path('<str:robot_name>/compare', ComparePage.as_view()),
    path('<str:first>/<str:second>', compare_robots_page),
]
