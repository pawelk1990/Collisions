from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .processing import file_processing
from .forms import RobotForm, RobotChooseForm, LoginForm
from .models import Robot, RobotData, RobotError
from .output import creating_output, robot_details
from django_tables2 import RequestConfig
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import zipfile


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
                if zipfile.is_zipfile(f):
                    file_processing(f, request.user)   
                else:
                    return HttpResponse("Wrong file, <a href=\"\">try again</a>")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

@staff_member_required(login_url = '/login')
def form_compare(request, robot_name):
    form_class = RobotChooseForm(request.POST, request = request, robot = robot_name)

    if request.method == 'POST':
        if form_class.is_valid():
            robot_to_compare = request.POST.get('choice')
            collision_on = request.POST.get('collision_on')
            coll = None
            if collision_on!=None:
                coll = True
            else:
                coll = False
            return redirect('/'+ robot_name + '/'+ str(Robot.objects.get(pk = robot_to_compare))+'/'+str(coll))
        else:
            raise Http404 

    return render(request, 'uploadingData/compare.html', {'form': form_class, 'robot_name': robot_name})

   
@staff_member_required(login_url = '/login')
def compare_robots_page(request, first, second, collision_on): 
    ref_f = Robot.objects.get(author = request.user, robot_name = first)
    ref_s = Robot.objects.get(author = request.user, robot_name = second)   
    
    contex = {'programs':creating_output(ref_f, ref_s, collision_on).to_html(classes=["table table-bordered table-responsive text-center"]), 'first': first, 'second': second}
    return render(request, "uploadingData/compare_robots.html", contex)  

@staff_member_required(login_url = '/login')
def robot_detail_page(request, robot_name):
    ref = Robot.objects.get(author = request.user, robot_name = robot_name)
    errors = RobotError.objects.filter(robot_name = ref)
    context = {'programs': robot_details(ref).to_html(classes=["table table-responsive table-bordered text-center"]), 'robot_name': robot_name, 'errors': errors }
    return render(request, "uploadingData/robot_detail.html", context)

@staff_member_required(login_url = '/login')
def form_page(request):
    return render(request, "uploadingData/form.html")

@staff_member_required(login_url = '/login')
def robots_page(request):
    robots = Robot.objects.filter(author = request.user).values('robot_name').distinct()
    context = {'robots': robots}
    return render(request, "uploadingData/robots.html", context)

@staff_member_required(login_url = '/login')
def robot_delete_page(request, robot_name):
    obj = Robot.objects.get(author = request.user, robot_name=robot_name)    
    obj.delete()
    return redirect('/robots')

def login(request):  
    form_class = LoginForm()

    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(username = login, password = password)      

        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            return redirect('/login')


    return render(request, "uploadingData/login.html", {'form': form_class})

@staff_member_required(login_url = '/login')
def logout(request):    
    auth_logout(request)
    return redirect('/login')
    





