'''
This python module preserves the user-defined variables and functions
to use during extraction stage
'''

import pandas as pd
import gtd_util.load as ld
from .misc import get_memo_use

#----------------------- user-defined variables ------------------------------------
# data resources file paths --ORDER MATTERS FOR THE EXTRACTION STAGE
file_paths = ['source_files/european_countries.csv',
              'source_files/countries_iso_codes.csv',
              'source_files/included_features.txt',
              'source_files/globalterrorismdb_1970_2020.xlsx']

# years to filter 
YEAR = 2000




#------------------------------- functions ----------------------------------------

# func to extract data from .csv files
def get_csv_data(file_path):
    df = pd.read_csv(file_path)
    return df
    
    
# func to extract the features we're going to use from a .txt file
def get_features(file_path):
    use_colmns = []

    with open(file_path, 'r') as file:
      for line in file:
        use_colmns.append(line.strip())
        
    return use_colmns
    

# func to extract the gtd data we're going to use from a .xlsx file
def get_excel_data(file_path, use_cols, year):
    df = pd.read_excel(file_path, usecols=use_cols)
    df = df[df.iyear >= year].reset_index(drop=True)
    return df


# func that implements the data extraction stage from the resources 
def extract():
    # retrieve european countries to use from .csv file
    extracted_countries = get_csv_data(file_paths[0])
    
    # retrieve countries' iso-3 codes from .csv file
    extracted_iso_codes = pd.read_csv(file_paths[1])
    
    # get the features to retrieve
    use_cols = get_features(file_paths[2])
    
    extracted_gtd = get_excel_data(file_paths[3], use_cols, YEAR)
    
    print(f'Data extraction, Finished!')
    
    init_gtd_memory_usage = get_memo_use(extracted_gtd)
    print(f'\t-Initial GTD memory usage: {init_gtd_memory_usage:.2f} MB')
    print(f'\t-Extracted {len(extracted_gtd)} GTD records from year {YEAR} to {extracted_gtd.iyear.max()}')
    
    return extracted_countries, extracted_iso_codes, extracted_gtd, init_gtd_memory_usage
