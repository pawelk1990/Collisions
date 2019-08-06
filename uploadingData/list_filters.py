from .models import RobotData, Robot
from django.contrib import admin


class RobotNameFilter(admin.SimpleListFilter):
    title = 'Robot name filter'
    parameter_name = 'robot_name'

    def lookups(self, request, model_admin):
       return set([(r['robot_name'],r['robot_name']) for r in RobotData.objects.values('robot_name').distinct()])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(robot_name = self.value()).order_by('program_name')
        else: 
           return queryset

class RobotProgramFilter(admin.SimpleListFilter):
    title = 'Robot program filter'
    parameter_name = 'program_name'
    
    def lookups(self, request, model_admin):
  
        if request.GET.__contains__("robot_name"):
            return set([(r['program_name'],r['program_name']) for r in RobotData.objects.filter(robot_name= request.GET["robot_name"]).values('program_name').distinct()])
        else:
            return set([(r['program_name'],r['program_name']) for r in RobotData.objects.values('program_name').distinct()])

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(program_name = self.value())
        else: 
           return queryset