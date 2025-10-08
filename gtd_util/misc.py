'''
This python file preserves other functions
to use during the ETL process
'''

import pandas as pd
import numpy as np
from datetime import datetime #datetime formating for the log file

project_name = 'gtd_project'

def compute_value_diff_prcnt(new_value, old_value):
  '''
  USAGE: this func computes the percentage difference between two values

  INPUT:
    new_value, float : new value
    old_value, float : old value
  OUTPUT:
    prcnt_diff, float : percentage difference between two values
  '''

  prcnt_diff = ((new_value - old_value) / old_value) * 100

  return prcnt_diff


def get_memo_use(df):
  '''
  USAGE: To compute the memory usage of a dataframe

  INPUT:
    df, dataframe : the dataframe to compute the memory usage
  OUTPUT:
    memory_usage, float : memory usage in MB
  '''
  memory_usage = df.memory_usage(deep=True).sum()  / 1024 / 1024
  
  return memory_usage
  



#Creating a log function to log our ETL sequence. 
def log(msg, path):

  # getting the current timestamp
  now = datetime.now()

  # the format we're going to use for our timestamp : Year-Monthname-Day-Hour-Minute-Second
  timestamp_format = '%Y-%h-%d-%H:%M:%S'

  # formating the current timestamp to our favor
  timestamp = now.strftime(timestamp_format)

  # append the timestamp of the running process to a log file
  with open(path + "logfile.txt", "a") as f:
      f.write(timestamp + ',' + msg + '\n')
      




def compute_duration(fin, st):
  '''
  USAGE: this func computes the duration between two
          timestamps in hours, mins, and secs
  INPUT:
    fin, float: the finish timestamp
    st, float: the start timestamp
  OUTPUT:
    hours, int: the hours computed
    mins, int: the ninutes computed
    secs, float: the seconds computed
  '''
  duration = fin - st
  hours = int(duration // 3600)
  mins = int((duration % 3600) // 60)
  secs = round((duration % 60), 2)
  return hours, mins, secs
  
  
  
  
  
  
def find_project_directory(pj_name=project_name):

    # addressing the project's path to work with
    # NOT necessary if you already working the project's directory
    project_paths = glob(f'**/{pj_name}', recursive=True)
    
    # Check if the project directory was found
    if project_paths:
        project_path = project_paths[0]
        # Change the current working directory to the project path
        os.chdir(project_path)
        print(f'Current working directory -> {os.getcwd()}')
    else:
        print(f"Error: '{pj_name}' directory not found. \nPlease ensure the notebook is run from a location that contains this directory.") 