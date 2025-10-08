'''
This python module preserves the user-defined variables and funcs to use 
during transformation stage
'''

import pandas as pd
import numpy as np
from datetime import datetime
# geodata
from geopy.geocoders import Nominatim

# importing package's modules
import gtd_util.load as ld
from .misc import get_memo_use


#>>>>>>>>>>>>>>>>>> HANDLING GEODATA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# creating an API client to use for geodata extraction
geolocator = Nominatim(user_agent="coordinates_to_country")

def get_geodata(*args):
  '''
  USAGE: this func transforms coordinates to country
  INPUT:
    args, float : coordinates (latitude, longitude)
  OUTPUT:
    country name, string
  '''

  lat, lon = args[0], args[1] # unpack the arguments

  input_data = f'{lat},{lon}' # creating a string variable to feed the locator

  location = geolocator.reverse(input_data, language='en', timeout=10) # extracting geodata

  if location:
      return location.address.split(',')[-1].strip() # extracting the country from geodata
  else:
      return np.nan
      




#>>>>>>>>>>>>>>>>>>>> USER-DEFINED VARIABLES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# naming conventions
alt_country_names = {'Bosnia And Herzegovina'     :'Bosnia and Herzegovina',
                     'Bosnia-Herzegovina'         :'Bosnia and Herzegovina',
                     'Czech Republic'             :'Czechia',
                     'Holy See'                   : 'Vatican City',
                     'Macedonia'                  :'North Macedonia',
                     'Moldova, Republic of'       : 'Moldova',
                     'Netherlands, Kingdom of the' : 'Netherlands',
                     'Russian Federation'         : 'Russia',
                     'Slovak Republic'            :'Slovakia',
                     'Soviet Union'               :'Russia',
                     'Türkiye'                    : 'Turkiye',
                     'Turkey'                     : 'Turkiye',
                     'United Kingdom of Great Britain and Northern Ireland' : 'United Kingdom'}


col_alt_dict = {'eventid'           : 'id',
                'iyear'             : 'year',
                'imonth'            : 'month',
                'iday'              : 'day',
                'country_txt'       : 'country',
                'provstate'         : 'province_state',
                'latitude'          : 'lat',
                'longitude'         : 'lon',
                'gname'             : 'terr_group',
                'success'           : 'is_success',
                'suicide'           : 'is_suicide',
                'claimed'           : 'is_claimed',
                'attacktype1_txt'   : 'attack_type',
                'targtype1_txt'     : 'target_type',
                'targsubtype1_txt'  : 'target_subtype',
                'natlty1_txt'       : 'target_nationality',
                'weaptype1_txt'     : 'weapon_type',
                'weapsubtype1_txt'  : 'weapon_subtype',
                'nkill'             : 'fatalities_total',
                'nkillter'          : 'fatalities_terrorists',
                'nwound'            : 'wounded_total',
                'nwoundte'          : 'wounded_terrorists',
                'property'          : 'is_property_damaged',
                'ishostkid'         : 'is_hostage',
                'nhostkid'          : 'hostages_total',
                'nhours'            : 'hostage_hours',
                'kidhijcountry'     : 'kid_hij_country',
                'ndays'             : 'hostage_days',
                'ransom'            : 'is_ransom'}


replace_attacktype = {'Unknown'                           :'UKN',
                      'Hostage Taking (Kidnapping)'       :'Hostage Kidnapping',
                      'Hostage Taking (Barricade Incident)':'Barricade Hostage',
                      'Facility/Infrastructure Attack'    :'Infrastructure Attack',
                      'Bombing/Explosion'                 : 'Bombing'}

replace_targettype = {# CIVILIAN SOFT-TARGETS
                      'Private Citizens & Property'  : 'Civilian',
                      'Business'                     : 'Civilian',
                      'Tourists'                     : 'Civilian',

                      # GOVERNMENT & STATE
                      'Government (General)'         : 'Government',
                      'Government (Diplomatic)'      : 'Government',

                      # MILITARY & SECURITY FORCES
                      'Military'                     : 'Security',
                      'Police'                       : 'Security',

                      # ARMED NON-STATE ACTORS
                      'Terrorists/Non-State Militia' : 'Militant',
                      'Violent Political Party'      : 'Militant',

                      # CRITICAL INFRASTRUCTURE / SERVICES
                      'Telecommunication'            : 'Infrastructure',
                      'Utilities'                    : 'Infrastructure',
                      'Food or Water Supply'         : 'Infrastructure',

                      # TRANSPORT SYSTEMS
                      'Transportation'               : 'Transport',
                      'Airports & Aircraft'          : 'Transport',
                      'Maritime'                     : 'Transport',

                      # SOCIETAL INSTITUTIONS
                      'Educational Institution'      : 'Education',
                      'Religious Figures/Institutions': 'Religious',
                      'Journalists & Media'          : 'Media',
                      'NGO'                          : 'NGO',

                      # UNKNOWN / OTHER
                      'Other'                        : 'Other',
                      'Unknown'                      : 'UKN'}

replace_target_nationality = {'Multinational' : 'International'}

replace_targetsub = {#>>>>> CIVILIAN SOFT-TARGETS <<<<<

                      # Private Citizens & Property
                      'House/Apartment/Residence'               : 'Residence',
                      'Race/Ethnicity Identified'               : 'Race_Ethnicity',
                      'Political Party Member/Rally'            : 'Political_Assembly',
                      'Unnamed Civilian/Unspecified'            : 'Civilian_Unspec',
                      'Museum/Cultural Center/Cultural House'   : 'Cultural_Site',
                      'Religion Identified'                     : 'Religious_Group',
                      'Laborer (General)/Occupation Identified' : 'Laborer',
                      'Named Civilian'                          : 'Civilian_Named',
                      'Vehicles/Transportation'                 : 'Private_Vehicle',
                      'Marketplace/Plaza/Square'                : 'Public_Area',
                      'Public Area (garden, parking lot, garage, beach, public building, camp)' 
                                                                : 'Public_Area',
                      'Labor Union Related'                     : 'Labor_Union',
                      'Refugee (including Camps/IDP/Asylum Seekers)'  
                                                                : 'Refugee',
                      'Student'                                 : 'Student',
                      'Procession/Gathering (funeral, wedding, birthday, religious)' 
                                                                : 'Gathering',
                      'Farmer'                                  : 'Agricultural_Personnel',
                      'Memorial/Cemetery/Monument'              : 'Memorial_Site',
                      'Alleged Informant'                       : 'Informant',
                      'Village/City/Town/Suburb'                : 'Built-up_Area',
                      'Protester'                               : 'Protester',

                      # Business
                      'Retail/Grocery/Bakery'                   : 'Retail_Facility',
                      'Bank/Commerce'                           : 'Finance_Facility',
                      'Restaurant/Bar/Café'                     : 'Food_Beverage',
                      'Hotel/Resort'                            : 'Hospitality',
                      'Multinational Corporation'               : 'Corporation',
                      'Construction'                            : 'Construction_Site', 
                      'Gas/Oil/Electric'                        : 'Energy_Infrastructure', 
                      'Entertainment/Cultural/Stadium/Casino'   : 'Entertainment_Venue',
                      'Industrial/Textiles/Factory'             : 'Industrial_Facility',
                      'Farm/Ranch'                              : 'Agricultural_Site',
                      'Medical/Pharmaceutical'                  : 'Medical_Facility',
                      'Private Security Company/Firm'           : 'Private_Security',
                      'Mining'                                  : 'Mining_Site',
                      'Legal Services'                          : 'Legal_Services',

                      # Turists
                      'Tour Bus/Van'                            : 'Tour_Vehicle',
                      'Tourist'                                 : 'Tourist',
                      'Other Facility'                          : 'Tourist_Facility',
                      'Tourism Travel Agency'                   : 'Travel_Agency',

                      #>>>>> GOVERNMENT & STATE <<<<<
                      #Government (General)
                      'Government Personnel (excluding police, military)'     
                                                                : 'Gov_Personnel',
                      'Politician or Political Party Movement/Meeting/Rally'
                                                                : 'Political_Assembly',
                      'Government Building/Facility/Office'     : 'Gov_Facility',
                      'Judge/Attorney/Court'                    : 'Judicial_Facility',
                      'Intelligence'                            : 'Intelligence_Entity',
                      'Election-related'                        : 'Election_Event',
                      'Head of State'                           : 'Head-of-State',
                      'Royalty'                                 : 'Royalty',

                      # Government (Diplomatic)
                      'Diplomatic Personnel (outside of embassy, consulate)'
                                                                : 'Diplomatic_Personnel',
                      'International Organization (peacekeeper, aid agency, compound)'
                                                                : 'Intl_Organization',
                      'Embassy/Consulate'                       : 'Diplomatic_Facility',

                      #>>>>> MILITARY & SECURITY FORCES <<<<<
                      # Military
                      'Military Barracks/Base/Headquarters/Checkpost'           : 'Military_Facility',
                      'NATO'                                                    : 'NATO',
                      'Military Personnel (soldiers, troops, officers, forces)' : 'Military_Personnel',
                      'Military Unit/Patrol/Convoy'                             : 'Military_Unit',
                      'Military Aircraft'                                       : 'Military_Aircraft',
                      'Military Checkpoint'                                     : 'Military_Post',
                      'Military Transportation/Vehicle (excluding convoys)'     : 'Military_Vehicle',

                      'Military Recruiting Station/Academy'                     : 'Military_Facility',
                      'Non-combatant Personnel'                                 : 'Civilian_Staff',
                      'Military Maritime'                                       : 'Military_Maritime',
                      'Military Weaponry'                                       : 'Military_Weaponry',

                      # Police
                      'Police Building (headquarters, station, school)' : 'Police_Facility',
                      'Police Security Forces/Officers'                 : 'Police_Personnel',
                      'Police Checkpoint'                               : 'Police_Post',
                      'Police Patrol (including vehicles and convoys)'  : 'Police_Unit',
                      'Prison/Jail'                                     : 'Correctional_Facility',

                      #>>>>> ARMED NON‑STATE ACTORS <<<<<
                      'Paramilitary'                             : 'Paramilitary',
                      'Non-State Militia'                        : 'Paramilitary',
                      'Terrorist'                                : 'Terrorist',
                      'Party Office/Facility'                    : 'V_Party_Facility',
                      'Party Official/Candidate/Other Personnel' : 'V_Party_Personnel',

                      #>>>>> CRITICAL INFRASTRUCTURE / SERVICES <<<<<
                      # Telecommunication
                      'Multiple Telecommunication Targets'  : 'Telecom_Infrastructure',
                      'Television'                          : 'Television_Infrastructure',
                      'Telephone/Telegraph'                 : 'Telecom_Infrastructure',
                      'Radio'                               : 'Radio_Infrastructure',

                      # Utilities
                      'Gas'         : 'Energy_Infrastructure',
                      'Oil'         : 'Energy_Infrastructure',
                      'Electricity' : 'Energy_Infrastructure',

                      # Food or Water Supply
                      'Water Supply': 'Water_Infrastructure',

                      #>>>>> TRANSPORT SYSTEMS <<<<<
                      # Transportation
                      'Train/Train Tracks/Trolley'        : 'Rail_System',
                      'Bus (excluding tourists)'          : 'Public_Bus',
                      'Bus Station/Stop'                  : 'Bus_Station',
                      'Bridge/Car Tunnel'                 : 'Bridge_Tunnel',
                      'Subway'                            : 'Subway',
                      'Highway/Road/Toll/Traffic Signal'  : 'Road_Infrastructure',
                      'Taxi/Rickshaw'                     : 'Taxi_Service',

                      # Airports & Aircraft
                      'Airline Officer/Personnel'         : 'Airline_Personnel',
                      'Airport'                           : 'Airport_Facility',
                      'Aircraft (not at an airport)'      : 'Aircraft_In-Flight',

                      # Maritime
                      'Commercial Maritime'               : 'Maritime_Commercial',
                      'Civilian Maritime'                 : 'Maritime_Civilian',

                      #>>>>> SOCIETAL INSTITUTIONS <<<<<
                      # Educational Institution
                      'School/University/Educational Building'  : 'Educational_Facility',
                      'Teacher/Professor/Instructor'            : 'Educator',
                      'Other Personnel'                         : 'Misc_Personnel',

                      # Religious Figures/Institutions
                      'Place of Worship'        : 'Religious_Site',
                      'Religious Figure'        : 'Religious_Figure',
                      'Affiliated Institution'  : 'Affiliated_Institution',

                      # Journalists & Media
                      'Newspaper Journalist/Staff/Facility'     : 'Media_Newspaper',
                      'Radio Journalist/Staff/Facility'         : 'Media_Radio',
                      'Television Journalist/Staff/Facility'    : 'Media_Television',
                      'Other (including online news agencies)'  : 'Media_Online',

                      # NGO
                      'International NGO' : 'NGO_International',
                      'Domestic NGO'      : 'NGO_Domestic',

                      #>>>>> UNKNOWN / OTHER <<<<<
                      # Other
                      'Fire Fighter/Truck' : 'Fire_Service',
                      'Ambulance'          : 'Ambulance_Service',
                      #Unknown
                      'Unknown' : 'UKN'
}


replace_weapontype = {'Unknown' :'UKN',
                      'Other'   :'UKN',
                      'Vehicle (not to include vehicle-borne explosives, i.e., car or truck bombs)':'Vehicle'}


replace_weaponsubtype = {'Unknown Explosive Type'                   :'UKN',
                         'Unknown Gun Type'                         :'UKN',
                         'Gasoline or Alcohol'                      :'Gasoline/Alcohol',
                         'Other Explosive Type'                     :'UKN',
                         'Projectile (rockets, mortars, RPGs, etc.)':'Projectile',
                         'Automatic or Semi-Automatic Rifle'        :'(Semi)Automatic Rifle',
                         'Hands, Feet, Fists'                       :'Body Compact',
                         'Knife or Other Sharp Object'              :'Sharp Object',
                         'Rifle/Shotgun (non-automatic)'            :'Rifle/Shotgun',
                         'Suicide (carried bodily by human being)'  :'Suicide Vest',
                         'Unknown Weapon Type'                      :'UKN',
                         'Other Gun Type'                           :'UKN',
                         'Rope or Other Strangling Device'          :'Strangling Device'}


cat_features = ['country', 'province_state', 'city', 'attack_type', 'target_type', 'target_subtype', 'target_nationality',
                'terr_group', 'weapon_type', 'weapon_subtype', 'region', 'alpha2', 'alpha3',
                'is_success', 'is_suicide', 'is_claimed', 'is_property_damaged', 'is_hostage', 'is_ransom']

num_features = ['fatalities_total', 'fatalities_terrorists', 'wounded_total', 'wounded_terrorists',
                'hostages_total','hostage_hours','hostage_days',
                'year', 'month', 'day']

discard_features = ['summary', 'divert', 'kid_hij_country']

coord_vals = ['lat', 'lon']

sentinels = ['Unknown', 'unknown', -9, -99, np.nan]


rearranged_cols = ['id', 'date', 'five_year', 'quarter', 'year', 'month', 'month_name', 'day',
                   'region', 'country', 'alpha2', 'alpha3', 'province_state', 'city', 'lat', 'lon',
                   'is_success', 'is_suicide', 'is_property_damaged', 'terr_group', 'is_claimed',
                   'attack_type', 'weapon_type', 'weapon_subtype', 
                   'target_type', 'target_subtype', 'target_nationality',  
                   'fatalities_total', 'fatalities_terrorists', 'wounded_total', 'wounded_terrorists',
                   'is_hostage', 'hostages_total', 'hostage_duration', 'is_ransom', 
                   ]
                   
                   

#>>>>>>>>>>>>>>>>>>>>>>>>>> USER-DEFINED TRANSFORMATION FUNCS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def fix_country_names(gtd, iso_codes):
    '''
    USAGE: 1. the purpose of this function is to find specific geografical areas
              according to nowadays' UN country names using the given coordinates
              so to retrieve current country name.
           2. modify country names for alignment
    
    INPUT:
        gtd, pd.DataFrame : the GTD dataframe
        iso_codes, pd.DataFrame : the iso-3 alpha each country codes
    OUTPUT:
        gtd, pd.DataFrame : the modified GTD dataframe
        iso_codes, pd.DataFrame : the modified iso-3 alpha codes
    '''
    
    # rename country names for alignment
    gtd.country_txt = gtd.country_txt.replace(alt_country_names)
    
    # specific country name modifications according to nowadays' UN country names
    # using the given coordinates so to retrieve current country name
    alter_countries = ['Yugoslavia', 'Serbia-Montenegro']

    for country in alter_countries:
      filt = gtd.country_txt == country
      gtd.loc[filt] = gtd.loc[filt]\
                         .apply(lambda x: x.replace(country, get_geodata(x.latitude,
                                                                         x.longitude)), axis=1)
    
    # modifying country names for alignment
    iso_codes.country = iso_codes.country.replace(alt_country_names)
    
    return gtd, iso_codes





def merge_dataframes(gtd, iso_codes, countries):
    '''
    USAGE: the purpose of this function is to merge all the retrieved data
            into a single one for further analysis
    TODO:   1. merge EUR countries with their respective iso-3 alpha codes
            2. filter the GTD dataframe on EUR countries
            3. merge GTD on EUR countries with their respective iso-3 alpha codes
    INPUT:
        gtd, pd.DataFrame :  the GTD data
        iso_codes, pd.DataFrame : The countries' iso-3 alpha codes 
        countries, pd.DataFrame : The European countries
    OUTPUT:
       merged_gtd, pd.DataFrame : the combined data we're going to use for further analysis
    '''
    
    # merging the european countries df with iso-3 codes df
    merged_countries = countries.merge(iso_codes,
                                       on='country',
                                       how='left')
                                                 
    #------------------ Filter GTD countries -----------------------

    # extracting the countries' names to filter the GTD data using the EUR countries list
    country_list = merged_countries.country.to_list()

    # finding the indices where the country in GTD data is not included
    idx_to_drop = gtd.loc[~gtd.country_txt.isin(country_list)].index

    # dropping the countries which are not included in Europe and reset the idx
    gtd.drop(idx_to_drop, inplace=True)
    gtd.reset_index(drop=True, inplace=True) 

    
    #---------------------------------------------------------------
    
    merged_gtd = gtd.merge(merged_countries,
                           left_on='country_txt',
                           right_on='country',
                           how='left')

    merged_gtd = merged_gtd.drop(['country'], axis=1) # removing exceeded columns
    
    merged_gtd = merged_gtd.rename(columns=col_alt_dict)
    
    return merged_gtd
    
    
    
    
    

def apply_feature_convensions(df):
    '''
    USAGE: the purpose of this func is to apply naming convensions 
            in categorical variables for readability and grouping some
            generalizing safely the analysis
            
    INPUT:
        df, pd.DataFrame : the gtd dataframe
    OUTPUT:
        df, pd.DataFrame : the gtd dataframe after curation
    '''
    
    # dictionary maping the columns to alter and their respective values
    replacement_maps = {'attack_type':        replace_attacktype,
                        'target_type':        replace_targettype,
                        'target_subtype':     replace_targetsub,
                        'target_nationality': replace_target_nationality,
                        'weapon_type':        replace_weapontype,
                        'weapon_subtype':     replace_weaponsubtype,
                        }

    # apply all replacements in place
    df.replace(replacement_maps, inplace=True)
    
    return df
    


def handle_missing_vals(df): 
  '''
  USAGE:  the use of this func is to handle missing values and set datatypes
          in the GTD dataframe to be analysed.

  TODO:   1. drop records with missing coordinates
          2. handle missing values in categorical features
          3. handle missing values in numerical features
          4. handle zero (0) values in date features

  INPUT:
    df, pd.DataFrame: the GTD dataframe to be handled
    
  OUTPUT:
    df, pd.DataFrame: the GTD dataframe with missing values handled
  '''
  # handling lat & lon features (discard missing records)
  df = df.dropna(subset=coord_vals, how='all').reset_index(drop=True)
  df[coord_vals] = df[coord_vals].astype(float)

  # handling categorical features (replace sentinels with uknown values)
  df[cat_features] = df[cat_features].replace(sentinels, 'UKN').astype('category')

  # handling missing numerical values
  df[num_features] = df[num_features].replace(sentinels, pd.NA)

  # handling day value -> 0 (if day=0 replace with 1; there are a handful of them)
  df['day'] = df['day'].replace(0, 1)  

  return df




def fix_inconsistent_casualties(df):
  '''
  USAGE:  the use of this func is to handle missing values and set datatypes
          in the GTD dataframe to be analysed.

  TODO:   1. filter records with missing casualties in all features
          2. handle missing values in the GTD dataframe by filling them with 0
              where the filter doesn't apply (features with at least one missing value
              in each record)
          3. handle inconsistencies in fatalities and wounded personnel (eg. the total number
              of fatalities [terrorists + other people] are less than the number)

  INPUT:
    df, pd.DataFrame: the GTD dataframe to be handled
    
  OUTPUT:
    df, pd.DataFrame: the GTD dataframe with missing values handled
  '''
  
  casualties_cols = ['fatalities_total', 'fatalities_terrorists', 'wounded_total', 'wounded_terrorists']

  # -------------- fix missing casualties' values ---------------------
  filt_casualties = (df.fatalities_total.isna() & 
                     df.fatalities_terrorists.isna() &
                     df.wounded_total.isna() & 
                     df.wounded_terrorists.isna()
                     )
  
  df.loc[~filt_casualties, casualties_cols] = df.loc[~filt_casualties, casualties_cols].fillna(0)

  # ------------------ looking for inconsistencies --------------------- 
  filt_fatal = (df.fatalities_total < df.fatalities_terrorists)
  filt_wound = (df.wounded_total  < df.wounded_terrorists)
  
  if df[filt_fatal].shape[0] > 0:
    idx_f = df[filt_fatal].index
    df.loc[idx_f, 'fatalities_total'] = df.loc[idx_f, 'fatalities_terrorists']

  if df[filt_wound].shape[0] > 0:
    idx_w = df[filt_wound].index
    df.loc[idx_w, 'wounded_total'] = df.loc[idx_w, 'wounded_terrorists']
    
    
  df[casualties_cols] = df[casualties_cols].replace(pd.NA, 'UKN')

  return df





def feature_engineering(df):
  '''
  USAGE:  the purpose of this func is to create new features from the existing ones.
  TODO:   1. create a datetime feature comprised of year, month, and day
          2. create a month_name feature
          3. create a quarter feature
          4. create a 5-year feature
          5. create a captivity time feature
          6. refine the hostages
  INPUT: 
    df, pd.DataFrame: the gtd dataframe to be processed.
  OUTPUT:
    df, pd.DataFrame: the gtd dataframe with the new features.
  '''

  #----------------------------- DATETIME FEATURES -------------------------------

  # full date
  df['date'] = pd.to_datetime(dict(year=df.year,
                                  month=df.month,
                                  day=df.day))
  
  # month name
  df['month_name'] = df['date'].dt.strftime('%b')

  # quarters
  df['quarter'] = df['date'].dt.quarter.astype('Int8')

  # 5-year bins
  bins = [2000, 2005, 2010, 2015, 2020] # creating the time-points for a 5y time-span
  labels = ['2000-2005', '2006-2010', '2011-2015', '2016-2020']
  df['five_year'] = pd.cut(df['year'], bins=bins, labels=labels, right=True, include_lowest=True)

  df[['year', 'month', 'day']] = df[['year', 'month', 'day']].astype('Int16')
  
  
  #-------------------------------- CAPTIVITY DURATION -----------------------------

  both_missing_values = df['hostage_hours'].isna() & df['hostage_days'].isna() #remember which rows are totally missing
  hostage_hours = df['hostage_hours'].fillna(0) # compute with NaNs temporarily set to 0
  hostage_days  = df['hostage_days' ].fillna(0) # compute with NaNs temporarily set to 0

  df['hostage_duration'] = hostage_days * 24 + hostage_hours # compute the total captivity time (h)
  df.loc[both_missing_values, 'hostage_duration'] = pd.NA
  df['hostage_duration'] = df['hostage_duration'].round()
  
  
  
  #-------------------------------- HOSTAGE REFINEMENT -----------------------------
  
  df = df.drop(['hostage_hours', 'hostage_days'], axis=1)
  
  filt_0 = ~(df.is_hostage == 1) & (df.hostages_total.isna())
  filt_1 = (df.is_hostage == 1) & (df.hostages_total.isna())
  filt_3 = ~(df.is_hostage == 1) & (df.hostage_duration.isna())
  filt_4 = (df.is_hostage == 1) & (df.hostage_duration.isna())

  if df[filt_0].shape[0] > 0:
    idx_0 = df[filt_0].index
    df.loc[idx_0, 'hostages_total'] = 0

  if df[filt_1].shape[0] > 0:
    idx_1 = df[filt_1].index
    df.loc[idx_1, 'hostages_total'] = 'UKN'

  if df[filt_3].shape[0] > 0:
    idx_3 = df[filt_3].index
    df.loc[idx_3, 'hostage_duration'] = 0

  if df[filt_4].shape[0] > 0:
    idx_4 = df[filt_4].index
    df.loc[idx_4, 'hostage_duration'] = 'UKN'
  
  return df
  
  
  
  
  
  

def transform(gtd, iso_codes, countries):
    '''
    USAGE: the purpose of this function is to implement the data transformation stage
            of the ETL process
    TODO: 1. fix the country names
          2. merge data resources focusing in EUR
          3. apply feature conventions
          4. discard unused features
          5. drop duplicated records, if any
          6. handle missing values
          7. fix inconsistent casualties values
    INPUT:
        gtd, pd.DataFrame :  the GTD data
        iso_codes, pd.DataFrame : The countries' iso-3 alpha codes 
        countries, pd.DataFrame : The European countries
    OUTPUT:
       transf_gtd, pd.DataFrame : the transformed GTD data
    '''
    gtd, iso_codes = fix_country_names(gtd, iso_codes)
    
    merged_gtd = merge_dataframes(gtd, iso_codes, countries)
    
    transf_gtd0 = apply_feature_convensions(merged_gtd)
    
    transf_gtd1 = transf_gtd0.drop(discard_features, axis=1)
    
    transf_gtd2 = transf_gtd1.drop_duplicates()
    
    transf_gtd3 = handle_missing_vals(transf_gtd2)
    
    transf_gtd4 = fix_inconsistent_casualties(transf_gtd3)
    
    transf_gtd5 = feature_engineering(transf_gtd4)
    
    transf_gtd = transf_gtd5[rearranged_cols]
    
    print(f'Data transformation, Finished!')
    
    transf_gtd_memory_usage = get_memo_use(transf_gtd)
    print(f'\t-Final GTD memory usage: {transf_gtd_memory_usage:.2f} MB')
    print(f'\t-Transformed {len(transf_gtd)} GTD records from year {transf_gtd.year.min()} to {transf_gtd.year.max()}')
    
    return transf_gtd, transf_gtd_memory_usage