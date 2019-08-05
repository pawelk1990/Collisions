from django.contrib import admin
from .models import Robot, RobotData, RobotError
from .list_filters import RobotNameFilter, RobotProgramFilter
# Register your models here.


@admin.register(RobotData)
class RobotDataAdmin(admin.ModelAdmin):
    list_filter = (RobotNameFilter, RobotProgramFilter)


@admin.register(RobotError)
class RobotErrorAdmin(admin.ModelAdmin):
    list_filter = (RobotNameFilter, )