
from django.contrib import admin
from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from .views import (
    form_page,
    FileFieldView,
    robots_page, 
    robot_detail_page,
    compare_robots_page,
    robot_delete_page, 
    form_compare,
    login,
    logout
)

urlpatterns = [
    path('', staff_member_required(FileFieldView.as_view(), login_url = '/login')),
    path('login', login),
    path('logout', logout),
    path('robots', robots_page),
    path('<str:robot_name>', robot_detail_page),
    path('<str:robot_name>/delete', robot_delete_page),
    path('<str:robot_name>/compare', form_compare),
    path('<str:first>/<str:second>/<str:collision_on>', compare_robots_page),
]
