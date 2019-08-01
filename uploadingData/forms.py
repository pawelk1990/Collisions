from django import forms
from .models import Robot

class RobotForm (forms.Form):
    robot_name = forms.CharField(label='Robot name', max_length=100)
    robot_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class RobotChooseForm(forms.Form):
    pass
    #Robots = dict(Robot.objects.values_list('robot_name').distinct())
    #Robots = ((i.id, i) for i in Robot.objects.values_list('robot_name').distinct())
    #choice = forms.ChoiceField(choices = Robots)