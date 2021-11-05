# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 11:47:03 2021

@author: User
"""
import pickle
import datetime
from opencage.geocoder import OpenCageGeocode

pkl_2020_08_01_2020_08_31 = pickle.load(open("2020-08-01_2020-08-31.pkl", "rb"))

pkl_2020_09_01_2020_09_30 = pickle.load(open("2020-09-01_2020-09-30.pkl", "rb"))

pkl_2020_10_01_2020_10_31 = pickle.load(open("2020-10-01_2020-10-31.pkl", "rb"))

pkl_2020_11_01_2020_11_30 = pickle.load(open("2020-11-01_2020-11-30.pkl", "rb"))

pkl_2020_12_01_2020_12_31 = pickle.load(open("2020-12-01_2020-12-31.pkl", "rb"))

ixps = list(pkl_2020_08_01_2020_08_31.keys())

key = 'bd6e1524012a4459bc142002b0ab8617'
geocoder = OpenCageGeocode(key)

collected_dict = {}

def stitcher(current_list_dates, current_list_vals, starting_list_dates, starting_list_vals):
    crop_index = 0
    cropped_list_dates = []
    cropped_list_vals = []
    
    for current_date in current_list_dates:
        if current_date > starting_list_dates[len(starting_list_dates) - 1]:
            cropped_list_dates = current_list_dates[crop_index:]
            cropped_list_vals = current_list_vals[crop_index:]
            starting_list_dates += cropped_list_dates
            starting_list_vals += cropped_list_vals
            break
        else:
            crop_index += 1
            
    return starting_list_dates, starting_list_vals

for ixp in ixps:
    
    collected_dict[ixp] = {}
    collected_dict[ixp]['city'] = pkl_2020_08_01_2020_08_31[ixp]['city']
    collected_dict[ixp]['country'] = pkl_2020_08_01_2020_08_31[ixp]['country']
    collected_dict[ixp]['country_code'] = pkl_2020_08_01_2020_08_31[ixp]['country_code']
    collected_dict[ixp]['continent'] = pkl_2020_08_01_2020_08_31[ixp]['continent']
    
    keys_1 = list(pkl_2020_08_01_2020_08_31[ixp].keys())
    keys_2 = list(pkl_2020_09_01_2020_09_30[ixp].keys())
    keys_3 = list(pkl_2020_10_01_2020_10_31[ixp].keys())
    keys_4 = list(pkl_2020_11_01_2020_11_30[ixp].keys())
    keys_5 = list(pkl_2020_12_01_2020_12_31[ixp].keys())
    print(ixp)
    
    if 'week' in keys_1 and 'week' in keys_2 and 'week' in keys_3 and 'week' in keys_4 and 'week' in keys_5:
        week_2020_08_01_2020_08_31 = pkl_2020_08_01_2020_08_31[ixp]['week']
        base_list_dates = week_2020_08_01_2020_08_31['dates']
        base_list_vals = week_2020_08_01_2020_08_31['values']
        starting_list_dates = base_list_dates
        starting_list_vals = base_list_vals
        ####################################################################
        week_2020_09_01_2020_09_30 = pkl_2020_09_01_2020_09_30[ixp]['week']
        current_list_dates = week_2020_09_01_2020_09_30['dates']
        current_list_vals = week_2020_09_01_2020_09_30['values']

        result_to_2020_09_30 = stitcher(current_list_dates, current_list_vals, starting_list_dates, starting_list_vals)
        ####################################################################
        week_2020_10_01_2020_10_31 = pkl_2020_10_01_2020_10_31[ixp]['week']
        current_list_dates = week_2020_10_01_2020_10_31['dates']
        current_list_vals = week_2020_10_01_2020_10_31['values']
        
        result_to_2020_10_31 = stitcher(current_list_dates, current_list_vals, result_to_2020_09_30[0], result_to_2020_09_30[1])
        ####################################################################
        week_2020_11_01_2020_11_30 = pkl_2020_11_01_2020_11_30[ixp]['week']
        current_list_dates = week_2020_11_01_2020_11_30['dates']
        current_list_vals = week_2020_11_01_2020_11_30['values']
        
        result_to_2020_11_30 = stitcher(current_list_dates, current_list_vals, result_to_2020_10_31[0], result_to_2020_10_31[1])
        ####################################################################
        week_2020_12_01_2020_12_31 = pkl_2020_12_01_2020_12_31[ixp]['week']
        current_list_dates = week_2020_12_01_2020_12_31['dates']
        current_list_vals = week_2020_12_01_2020_12_31['values']
        
        result_to_2020_12_31 = stitcher(current_list_dates, current_list_vals, result_to_2020_11_30[0], result_to_2020_11_30[1])
        ####################################################################
        collected_dict[ixp]['week'] = {
            'dates': result_to_2020_12_31[0],
            'values': result_to_2020_12_31[1]
        }
        
    if 'month' in keys_1 and 'month' in keys_2 and 'month' in keys_3 and 'month' in keys_4 and 'month' in keys_5:
        month_2020_08_01_2020_08_31 = pkl_2020_08_01_2020_08_31[ixp]['month']
        base_list_dates = month_2020_08_01_2020_08_31['dates']
        base_list_vals = month_2020_08_01_2020_08_31['values']
        starting_list_dates = base_list_dates
        starting_list_vals = base_list_vals
        ####################################################################
        month_2020_09_01_2020_09_30 = pkl_2020_09_01_2020_09_30[ixp]['month']
        current_list_dates = month_2020_09_01_2020_09_30['dates']
        current_list_vals = month_2020_09_01_2020_09_30['values']

        result_to_2020_09_30 = stitcher(current_list_dates, current_list_vals, starting_list_dates, starting_list_vals)
        ####################################################################
        month_2020_10_01_2020_10_31 = pkl_2020_10_01_2020_10_31[ixp]['month']
        current_list_dates = month_2020_10_01_2020_10_31['dates']
        current_list_vals = month_2020_10_01_2020_10_31['values']
        
        result_to_2020_10_31 = stitcher(current_list_dates, current_list_vals, result_to_2020_09_30[0], result_to_2020_09_30[1])
        ####################################################################
        month_2020_11_01_2020_11_30 = pkl_2020_11_01_2020_11_30[ixp]['month']
        current_list_dates = month_2020_11_01_2020_11_30['dates']
        current_list_vals = month_2020_11_01_2020_11_30['values']
        
        result_to_2020_11_30 = stitcher(current_list_dates, current_list_vals, result_to_2020_10_31[0], result_to_2020_10_31[1])
        ####################################################################
        month_2020_12_01_2020_12_31 = pkl_2020_12_01_2020_12_31[ixp]['month']
        current_list_dates = month_2020_12_01_2020_12_31['dates']
        current_list_vals = month_2020_12_01_2020_12_31['values']
        
        result_to_2020_12_31 = stitcher(current_list_dates, current_list_vals, result_to_2020_11_30[0], result_to_2020_11_30[1])
        ####################################################################
        collected_dict[ixp]['month'] = {
            'dates': result_to_2020_12_31[0],
            'values': result_to_2020_12_31[1]
        }
        
    if 'year' in keys_1 and 'year' in keys_2 and 'year' in keys_3 and 'year' in keys_4 and 'year' in keys_5:
        year_2020_08_01_2020_08_31 = pkl_2020_08_01_2020_08_31[ixp]['year']
        base_list_dates = year_2020_08_01_2020_08_31['dates']
        base_list_vals = year_2020_08_01_2020_08_31['values']
        starting_list_dates = base_list_dates
        starting_list_vals = base_list_vals
        ####################################################################
        year_2020_09_01_2020_09_30 = pkl_2020_09_01_2020_09_30[ixp]['year']
        current_list_dates = year_2020_09_01_2020_09_30['dates']
        current_list_vals = year_2020_09_01_2020_09_30['values']

        result_to_2020_09_30 = stitcher(current_list_dates, current_list_vals, starting_list_dates, starting_list_vals)
        ####################################################################
        year_2020_10_01_2020_10_31 = pkl_2020_10_01_2020_10_31[ixp]['year']
        current_list_dates = year_2020_10_01_2020_10_31['dates']
        current_list_vals = year_2020_10_01_2020_10_31['values']
        
        result_to_2020_10_31 = stitcher(current_list_dates, current_list_vals, result_to_2020_09_30[0], result_to_2020_09_30[1])
        ####################################################################
        year_2020_11_01_2020_11_30 = pkl_2020_11_01_2020_11_30[ixp]['year']
        current_list_dates = year_2020_11_01_2020_11_30['dates']
        current_list_vals = year_2020_11_01_2020_11_30['values']
        
        result_to_2020_11_30 = stitcher(current_list_dates, current_list_vals, result_to_2020_10_31[0], result_to_2020_10_31[1])
        ####################################################################
        year_2020_12_01_2020_12_31 = pkl_2020_12_01_2020_12_31[ixp]['year']
        current_list_dates = year_2020_12_01_2020_12_31['dates']
        current_list_vals = year_2020_12_01_2020_12_31['values']
        
        result_to_2020_12_31 = stitcher(current_list_dates, current_list_vals, result_to_2020_11_30[0], result_to_2020_11_30[1])
        ####################################################################
        collected_dict[ixp]['year'] = {
            'dates': result_to_2020_12_31[0],
            'values': result_to_2020_12_31[1]
        }
        
del collected_dict['IX.br (PTT.br) Maceió']
del collected_dict['IXPN Lagos']
del collected_dict['IX.br (PTT.br) Rio de Janeiro']
del collected_dict['DE-CIX Frankfurt']
del collected_dict['MIX-IT']

ixps = list(collected_dict.keys())

for ixp in ixps:
    query = collected_dict[ixp]['city']
    results = geocoder.geocode(query)
    collected_dict[ixp]['latitude'] = results[0]['geometry']['lat']
    collected_dict[ixp]['longitude'] = results[0]['geometry']['lng']
    
start_year = 2020
start_month = 8
start_day = 1

end_year = 2021
end_month = 1
end_day = 1

file_string = str(datetime.date(start_year, start_month, start_day)) + '_' + str(datetime.date(end_year, end_month, end_day) - datetime.timedelta(days = 1))

pickle.dump(collected_dict, open(file_string + ".pkl", "wb"))
        