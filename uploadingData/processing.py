import zipfile
import re
from .models import Robot

def populate_database(robot_name, program_name, collision_number, on_or_off):
    Robot.objects.create(robot_name=robot_name, program_name =program_name, collision_number = collision_number, on_or_off =on_or_off)

# COLLSTOP( 8, 1 )means start collision number 8, COLLSTOP( 8, 2 )means end collision number 8
def detect_COLLSTOP_standart(zip_file, src_file, collision_string):
    if re.findall(" \d*,", collision_string) and re.findall(", \d*", collision_string):
        collision_number = int(re.findall(" \d*,", collision_string)[0][:-1])
        enabling_collision = int(re.findall(", \d*", collision_string)[0][1:])
        if enabling_collision == 1:
            enabling_collision = True
        elif  enabling_collision == 2:
            enabling_collision = False  
        else: 
            enabling_collision = None 
        populate_database(zip_file.filename, src_file.split('/')[-1], collision_number, enabling_collision)        
    else:
        pass
        #print(zip_file.filename, src_file.split('/')[-1], collision_string)
    
def read_file(zip_file, src_file):
    with zip_file.open(src_file) as sf:
        collisions = [detect_COLLSTOP_standart(zip_file, src_file, line.decode('UTF-8')) for line in sf if b'COLLSTOP' in line] 

def file_processing(uploaded_file):
    zf = zipfile.ZipFile(uploaded_file)
    data = zipfile.ZipFile.namelist(zf)
    [read_file(zf, i) for i in data if i.split('.')[1] =='src' ]


