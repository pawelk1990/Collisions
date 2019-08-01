from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .processing import file_processing
from .forms import RobotForm, RobotChooseForm
from .models import Robot
from .output import creating_output
# Create your views here.

class FileFieldView(FormView):
    form_class = RobotForm
    template_name = 'uploadingData/form.html'  # Replace with your template.
    success_url = 'robot'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        Robot.objects.all().delete()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('robot_files')
        if form.is_valid():  

            for f in files:
                file_processing(f)
            
            creating_output()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class ComparePage(FormView):
    form_class = RobotChooseForm
    template_name = 'uploadingData/compare.html'
    success_url = 'robot'
   
  

def home_page(request, robot_name):
    programs = Robot.objects.filter(robot_name = robot_name).values('program_name').distinct()
    context = {'programs': programs, 'robot_name':robot_name }
    return render(request, "uploadingData/home.html", context)

def form_page(request):
    return render(request, "uploadingData/form.html")

def robots_page(request):
    robots = Robot.objects.values('robot_name').distinct()
    context = {'robots': robots}
    return render(request, "uploadingData/robots.html", context)



