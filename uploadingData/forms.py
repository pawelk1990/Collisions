from django import forms
from .models import Robot

class RobotForm (forms.Form):
    robot_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class RobotChooseForm(forms.Form):
    choice = forms.ModelChoiceField(queryset = Robot.objects.all())
    collision_on = forms.BooleanField(required=False)

    def __init__(self, *args,**kwargs):
        user = kwargs.pop('user')
        super(RobotChooseForm,self).__init__(*args,**kwargs)
        print(user)



    