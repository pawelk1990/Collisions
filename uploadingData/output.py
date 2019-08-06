from .models import Robot, RobotData
import itertools
import pandas as pd


def creating_output(first, second, collision_on): 
    f = list(RobotData.objects.filter(robot_name = first ).values_list('program_name', flat=True).distinct().order_by('program_name'))
    s = list(RobotData.objects.filter(robot_name = second).values_list('program_name', flat=True).distinct().order_by('program_name'))  

    pos = (list(itertools.product(f, s)))
    df = pd.DataFrame(columns = s, index = f)

    for p in pos:
        col_f = set(RobotData.objects.filter(robot_name = first, program_name = p[0], on_or_off = collision_on).values_list('collision_number', flat=True).distinct())
        col_s = set(RobotData.objects.filter(robot_name = second, program_name = p[1], on_or_off = collision_on).values_list('collision_number', flat=True).distinct())
        df.at[p[0], p[1]] = col_f.intersection(col_s)
    
    columns_name = [(second, col) for col in df.columns]
    df.columns = pd.MultiIndex.from_tuples(columns_name)
    df.index.name =first
    
    return df
