from .models import Robot, RobotData
import itertools
import pandas as pd
def creating_output(first, second): #TODO logger.info/logging.info 
    f = list(RobotData.objects.filter(robot_name = first ).values_list('program_name', flat=True).distinct())
    s = list(RobotData.objects.filter(robot_name = second).values_list('program_name', flat=True).distinct())  

    print(f)
    print(s)
    
    pos = (list(itertools.product(f, s)))
    df = pd.DataFrame(columns = s, index = f)
    for p in pos:
        col_f = set(RobotData.objects.filter(robot_name = first, program_name = p[0]).values_list('collision_number', flat=True).distinct())
        col_s = set(RobotData.objects.filter(robot_name = second, program_name = p[1]).values_list('collision_number', flat=True).distinct())
        df.set_value(p[0], p[1], col_f.intersection(col_s))

        print(p, col_f, col_s, col_f.intersection(col_s))

    print(df)
    return df

