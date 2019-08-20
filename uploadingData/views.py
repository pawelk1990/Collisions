from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .processing import file_processing
from .forms import RobotForm, RobotChooseForm
from .models import Robot, RobotData, RobotError
from .output import creating_output
from django_tables2 import RequestConfig
from django.contrib.admin.views.decorators import staff_member_required


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
                file_processing(f, request.user)            
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
   
@staff_member_required
def compare_robots_page(request, first, second, collision_on): 
    ref_f = Robot.objects.get(author = request.user, robot_name = first)
    ref_s = Robot.objects.get(author = request.user, robot_name = second)   
    errors_f = RobotError.objects.filter(robot_name = ref_f)
    errors_s = RobotError.objects.filter(robot_name = ref_s)
    contex = {'programs':creating_output(ref_f, ref_s, collision_on).to_html(), 'first': first, 'second': second,
    'errors_f':errors_f, 'errors_s':errors_s}
    return render(request, "uploadingData/compare_robots.html", contex)  

@staff_member_required
def robot_detail_page(request, robot_name):
    ref = Robot.objects.get(author = request.user, robot_name = robot_name)
    programs = RobotData.objects.filter(robot_name = ref).values('program_name').distinct()
    context = {'programs': programs, 'robot_name': robot_name }
    return render(request, "uploadingData/robot_detail.html", context)

@staff_member_required
def form_page(request):
    return render(request, "uploadingData/form.html")

@staff_member_required
def robots_page(request):
    robots = Robot.objects.filter(author = request.user).values('robot_name').distinct()
    print(request.user)
    context = {'robots': robots}
    return render(request, "uploadingData/robots.html", context)

@staff_member_required
def robot_delete_page(request, robot_name):
    obj = Robot.objects.get(author = request.user, robot_name=robot_name)    
    obj.delete()
    return redirect('/upload/robots')





