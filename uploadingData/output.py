from .models import Robot

def creating_output():
    ob = Robot.objects.all()
    print(ob)

