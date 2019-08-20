import zipfile
import re
from .models import Robot, RobotData, RobotError

def populate_database(robot_name, program_name, collision_number, on_or_off, user):
    if not Robot.objects.filter(author = user, robot_name=robot_name).exists():
        obj = Robot.objects.create(author = user, robot_name=robot_name)
        RobotData.objects.create(robot_name = obj, 
        program_name =program_name, collision_number = collision_number, on_or_off =on_or_off)
    else: 
        obj = Robot.objects.get(author = user, robot_name=robot_name)
        RobotData.objects.create(robot_name = obj, 
        program_name =program_name, collision_number = collision_number, on_or_off =on_or_off)


# COLLSTOP( 8, 1 )means start collision number 8, COLLSTOP( 8, 2 )means end collision number 8
def detect_COLLSTOP_standart(zip_file, src_file, collision_string, user):
    collision_data = re.search("(\d*?), (\d)", collision_string)
    robot_name = zip_file.filename.split(".")[0]
    program_name = src_file.split('/')[-1]

    if collision_data:
        collision_number = int(collision_data.group(1))
        enabling_collision = collision_data.group(2)    
        if enabling_collision == '1':
            enabling_collision = True
        elif  enabling_collision == '2':
            enabling_collision = False  
        else: 
            enabling_collision = None 
        populate_database(robot_name, program_name, collision_number, enabling_collision, user)        
    else:
        if not Robot.objects.filter(author = user, robot_name=robot_name).exists():
            obj = Robot.objects.create(author = user, robot_name=robot_name)
            RobotError.objects.create(robot_name = obj, 
            program_name = program_name, robot_error = collision_string)
        else:
            obj = Robot.objects.get(author = user, robot_name=robot_name)
            RobotError.objects.create(robot_name = obj, 
            program_name = program_name, robot_error = collision_string)

        
    
def read_file(zip_file, src_file, user):
    with zip_file.open(src_file) as sf:
        for line in sf:
            if b'COLLSTOP' in line:
                detect_COLLSTOP_standart(zip_file, src_file, line.decode('UTF-8'), user)

def file_processing(uploaded_file, user):
    zf = zipfile.ZipFile(uploaded_file)
    data = zipfile.ZipFile.namelist(zf)
    for d in data:
        if  d.split('.')[1] =='src':
            read_file(zf, d, user)



