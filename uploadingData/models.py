from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

User = settings.AUTH_USER_MODEL
# Create your models here.
class Robot(models.Model):
    user = models.ForeignKey(User, default = 1, on_delete=models.CASCADE)
    robot_name =  models.CharField(max_length=50)

    def __str__(self):
        return f'{self.robot_name}'

class RobotData(models.Model):
    robot_name =  models.ForeignKey(Robot, on_delete=models.CASCADE)
    program_name =models.CharField(max_length=50)
    collision_number = models.PositiveSmallIntegerField()
    on_or_off = models.BooleanField()

    def __str__(self):
        return f'{self.robot_name}, {self.program_name}, {self.collision_number}, {self.on_or_off}' 

class RobotError(models.Model):
    robot_name =  models.ForeignKey(Robot, on_delete=models.CASCADE)
    program_name =models.CharField(max_length=50)
    robot_error = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.robot_name}, {self.program_name}'
    