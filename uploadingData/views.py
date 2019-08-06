from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .processing import file_processing
from .forms import RobotForm, RobotChooseForm
from .models import Robot, RobotData, RobotError
from .output import creating_output
from django_tables2 import RequestConfig


class FileFieldView(FormView):
    form_class = RobotForm
    template_name = 'uploadingData/form.html' 
    success_url = 'robots' 
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('robot_files')
        if form.is_valid():
            for f in files:
                file_processing(f)            
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class ComparePage(FormView):
    form_class = RobotChooseForm
    template_name = 'uploadingData/compare.html'
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)        
        if form.is_valid():             
            context = form.cleaned_data
            self.success_url = str(context["choice"])+'/'+str(context["collision_on"])
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
   
def compare_robots_page(request, first, second, collision_on):    
    errors_f = RobotError.objects.filter(robot_name = first)
    errors_s = RobotError.objects.filter(robot_name = second)
    contex = {'programs':creating_output(first, second, collision_on).to_html(), 'first': first, 'second': second,
    'errors_f':errors_f, 'errors_s':errors_s}
    return render(request, "uploadingData/compare_robots.html", contex)  

def robot_detail_page(request, robot_name):
    programs = RobotData.objects.filter(robot_name = robot_name).values('program_name').distinct()
    context = {'programs': programs, 'robot_name': robot_name }
    return render(request, "uploadingData/robot_detail.html", context)

def form_page(request):
    return render(request, "uploadingData/form.html")

def robots_page(request):
    robots = Robot.objects.values('robot_name').distinct()
    context = {'robots': robots}
    return render(request, "uploadingData/robots.html", context)

def robot_delete_page(request, robot_name):
    obj = Robot.objects.get(robot_name=robot_name)    
    obj.delete()
    return redirect('/upload/robots')





