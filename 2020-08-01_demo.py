# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 17:35:48 2020

@author: User
"""
import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from PIL import Image

import plot_image_processing
import synth_control_and_interpolation
import data_stitching

selected_ixp = 'DE-CIX Munich'
filter_amount = 0.75

stitched_dict = data_stitching.stitched_data_to_dict(data_stitching.get_data())
ixps = list(stitched_dict.keys())
new_ixps = ixps.copy()

test = synth_control_and_interpolation.process_dataframes(ixps, selected_ixp, stitched_dict, filter_amount)

pickle.dump(stitched_dict, open("save.pkl", "wb"))
pickle_test = pickle.load(open("save.pkl", "rb"))



        