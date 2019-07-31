from django import forms

class RobotForm (forms.Form):
    robot_name = forms.CharField(label='Robot name', max_length=100)
    robot_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))