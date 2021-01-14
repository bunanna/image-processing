# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 17:35:48 2020

@author: User
"""
import synth_control_and_interpolation
import data_stitching
import pickle

selected_ixp = 'DE-CIX Munich'
stitched_dict = data_stitching.stitched_data_to_dict(data_stitching.get_data(selected_ixp))

pickle.dump(stitched_dict, open("save.pkl", "wb"))

pickle_test = pickle.load(open("save.pkl", "rb"))

test = synth_control_and_interpolation.apply_synthetic_control(pickle_test, selected_ixp)