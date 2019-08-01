from django.db import models

# Create your models here.
class Robot(models.Model):
    robot_name =  models.CharField(max_length=50,  primary_key=True, unique = True)

    def __str__(self):
        return '%s' % (self.robot_name)

class RobotData(models.Model):
    robot_name =  models.ForeignKey(Robot, on_delete=models.CASCADE)
    program_name =models.CharField(max_length=50)
    collision_number = models.IntegerField()
    on_or_off = models.BooleanField()

    def __str__(self):
        return '%s %s %d' % (self.robot_name, self.program_name, self.collision_number )
    