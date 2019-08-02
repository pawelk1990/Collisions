from django import forms
from .models import Robot

class RobotForm (forms.Form):
    robot_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class RobotChooseForm(forms.Form):
    choice = forms.ModelChoiceField(queryset = Robot.objects.all())