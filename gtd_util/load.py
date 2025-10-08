'''
This python file preserves the user-defined variables and functions
to use during the loading stage
'''

import pandas as pd

# presumed that the folder is existed
dir_path = 'etl_outputs/'

  
def load_to_csv(data_in, f_name='gtd_', flg=''):  

  # where the tranformed data go to
  path_to = dir_path + f_name + f'{flg}.csv'

  # write the tranformed data to the destined file excluding the index
  data_in.to_csv(path_to, index=False)
  
  print(f'Data Loading, Finished!')
  

def load_to_pickle(data_in, f_name='gtd_', flg=''):

  # where the tranformed data go to
  path_to = dir_path + f_name + f'{flg}.pkl'

  # write the tranformed data to the destined file
  data_in.to_pickle(path_to)
  
  print(f'Data Loading, Finished!')