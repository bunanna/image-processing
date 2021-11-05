# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 14:57:17 2021

@author: User
"""

import pickle
import synth_control_and_interpolation as synth
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import datetime
import json

selected_ixp = 'DE-CIX New York'

pkl_2020_08_01_2020_12_31 = pickle.load(open("2020-08-01_2020-12-31_all.pkl", "rb"))

'''
plt.figure(figsize=(16,10))

for ixp in list(pkl_2020_08_01_2020_12_31.keys()):
    
    plt.plot(pkl_2020_08_01_2020_12_31[ixp]['year']['dates'], pkl_2020_08_01_2020_12_31[ixp]['year']['values'], label = ixp)
    
plt.legend(loc="upper left")
plt.show()
'''
plt.figure(figsize=(8,5))
plt.plot(pkl_2020_08_01_2020_12_31[selected_ixp]['year']['dates'], pkl_2020_08_01_2020_12_31[selected_ixp]['year']['values'], label = 'actual behavior', linewidth = 1)

dict_to_process = {}

base_lat = pkl_2020_08_01_2020_12_31[selected_ixp]['latitude']
base_long = pkl_2020_08_01_2020_12_31[selected_ixp]['longitude']

dist_limit = 8500
for ixp in list(pkl_2020_08_01_2020_12_31.keys()):
    new_lat = pkl_2020_08_01_2020_12_31[ixp]['latitude']
    new_long = pkl_2020_08_01_2020_12_31[ixp]['longitude']
    
    if ixp == selected_ixp or geodesic((base_lat, base_long), (new_lat, new_long)).kilometers < dist_limit:
        dict_to_process[ixp] = pkl_2020_08_01_2020_12_31[ixp]
        
        
synth.apply_synthetic_control(dict_to_process, selected_ixp)

dataframes = synth.process_dataframes(dict_to_process, selected_ixp)

plt.title(selected_ixp + ' Throughput')
plt.ylabel('Throughput in Gb/s')
plt.axvline(x = datetime.datetime(2020, 3, 1), color = 'black')

plt.show()




