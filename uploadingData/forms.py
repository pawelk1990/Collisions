from django import forms
from .models import Robot

class LoginForm(forms.Form):
    login =  forms.CharField(label='Login', max_length=100)
    password =  forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)

class RobotForm (forms.Form):
    robot_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class RobotChooseForm(forms.Form):
    choice = forms.ModelChoiceField(queryset = Robot.objects.all())
    collision_on = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        robot = kwargs.pop("robot")
        super(RobotChooseForm, self).__init__(*args, **kwargs)
        self.fields['choice'].queryset = Robot.objects.filter(author = self.request.user).exclude(robot_name = robot)
    
   


    