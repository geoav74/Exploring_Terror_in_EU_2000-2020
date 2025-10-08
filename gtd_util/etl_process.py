'''
  The purpose of this module is to implement the
  ETL process.
  
  To run this ETL process the python package should be 
  in the same directory in our project and have the following
  structure:
  (project directory)
  - source_files/
  - etl_outputs/
  
'''

from .extract import extract 
from .transform import transform
from .load import load_to_pickle
from .misc import compute_value_diff_prcnt, log, compute_duration 
from time import time

log_dir = 'etl_outputs/'



def run_etl():
  #>>>>>>>>>>>>>>>>>> ETL PROCESS <<<<<<<<<<<<<<<<<<<

  start = time()

  #------------------- Extraction -------------------
  log('Extraction Start', log_dir)
  extr_countries, extr_iso_codes, extr_gtd, init_mu = extract()
  log('Extraction Finished', log_dir)


  #------------------ Transformation ----------------
  log('Transformation Start', log_dir)
  gtd_transf, fin_mu = transform(extr_gtd, extr_iso_codes, extr_countries)
  log('Transformation Finished', log_dir)


  #--------------------- Loading --------------------
  log('Loading Start', log_dir)
  load_to_pickle(gtd_transf, flg='final')
  log('Loading Finished', log_dir)

  end = time()
  hours, mins, secs = compute_duration(end, start)
  print(f'\nETL Process, Complete!\n')

  memo_diff = compute_value_diff_prcnt(fin_mu, init_mu)
  print(f'-ETL Duration: {hours}hrs - {mins}mins - {secs}secs')
  print(f'-Percentage difference in memory usage: {memo_diff:.2f}%')
  print(f'-The shape of the dataframe is: {gtd_transf.shape}')



