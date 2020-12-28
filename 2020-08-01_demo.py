# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 17:35:48 2020

@author: User
"""
import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

import plot_image_processing
import synth_control_and_interpolation

directory = os.getcwd()
start_year = 2020
start_month = 8
start_day = 1
selected_ixp = 'DE-CIX Dallas'

start_ixp = [selected_ixp]

all_ixps = ['JPNAP Osaka',
            'LONAP',
            'BCIX',
            'MASS-IX',
            'TorIX',
            'IXPN Lagos',
            'IX.br (PTT.br) Brasília',
            'MIX-IT',
            'IX.br (PTT.br) São Paulo',
            'GrenoblIX',
            'DE-CIX Dallas',
            'DE-CIX Frankfurt',
            'DE-CIX Munich', 
            'DE-CIX Hamburg',
            'DE-CIX Istanbul',
            'DE-CIX Madrid',
            'DE-CIX Marseille',
            'DE-CIX New York',]

end_ixp = [selected_ixp]
all_ixps.remove(selected_ixp)
ixp_list = start_ixp + all_ixps + end_ixp
new_ixp_list = ixp_list.copy()

non_de_cix_and_frankfurt = ['JPNAP Osaka',
                            'LONAP',
                            'BCIX',
                            'MASS-IX',
                            'TorIX',
                            'IXPN Lagos',
                            'IX.br (PTT.br) Brasília',
                            'MIX-IT',
                            'IX.br (PTT.br) São Paulo',
                            'GrenoblIX',
                            'DE-CIX Frankfurt']


ixp_count = 0
before_crop = 0
after_crop = 0

for date_file in directory:

    start_date = datetime.date(start_year, start_month, start_day)
    start_date_time = datetime.datetime(start_year, start_month, start_day)
    
    if not os.path.isdir(str(start_date) + ' ' + 'Generated Images'):
        os.makedirs(str(start_date) + ' ' + 'Generated Images')
    os.chdir(str(start_date) + ' ' + 'Generated Images')
    
    date_directory = os.path.join(directory, str(start_date))
    
    for test_ixp in ixp_list:
        
        os.chdir(os.path.join(directory, str(start_date) + ' ' + 'Generated Images'))
        
        if not os.path.isdir(test_ixp):
            os.makedirs(test_ixp)
        os.chdir(test_ixp)
        
        ixp_directory = os.path.join(date_directory, str(start_date) + ' ' + test_ixp)
        plot_type = ''
            
        for filename in os.listdir(ixp_directory):
            graph_type = ''
                
            if 'year' in filename and 'peers' not in filename and 'prefixes' not in filename and '2' not in filename and '5' not in filename:
                
                if 'day' in filename:
                    plot_type = 'day'
                elif '5year' in filename:
                    plot_type = '5year'
                elif '2year' in filename:
                    plot_type = '2year'
                elif 'twoyear' in filename:
                    plot_type = '2year'
                elif 'year' in filename:
                    plot_type = 'year'
                
                current_img = Image.open(os.path.join(ixp_directory, filename))

                axes = plot_image_processing.crop_axes(test_ixp, current_img, plot_type)
                main_color = axes[5]
                removable_key = axes[6]
                ixp_type = axes[7]
                filter_type = axes[8]
                
                x_axis = axes[0]
                y_axis = axes[1]
                scale_factor = axes[4]
                
                left_x_axis = axes[2][0]
                top_x_axis = axes[2][1]
                right_x_axis = axes[2][2]
                bottom_x_axis = axes[2][3]
                
                left_y_axis = axes[3][0]
                top_y_axis = axes[3][1]
                right_y_axis = axes[3][2]
                bottom_y_axis = axes[3][3]
                
                x_axis_chars = plot_image_processing.ident_chars(x_axis, scale_factor, 'x', filter_type)
                y_axis_chars = plot_image_processing.ident_chars(y_axis, scale_factor, 'y', filter_type)
                
                #x_axis_chars[2].show()
                #y_axis_chars[2].show()
                
                if '5year' in filename and 'DE-CIX New York' in test_ixp:
                    x_chars = plot_image_processing.process_chars(x_axis_chars[0], x_axis_chars[1], True, False)
                    y_chars = plot_image_processing.process_chars(y_axis_chars[0], y_axis_chars[1], True, True)
                else:
                    x_chars = plot_image_processing.process_chars(x_axis_chars[0], x_axis_chars[1], False, False)
                    y_chars = plot_image_processing.process_chars(y_axis_chars[0], y_axis_chars[1], False, True)
                
                y_chars = plot_image_processing.process_chars(y_axis_chars[0], y_axis_chars[1], True, True)
        
                scaled_x = plot_image_processing.map_boxes(x_chars, scale_factor, x_axis_chars[3], left_x_axis, top_x_axis, 'x')
                scaled_y = plot_image_processing.map_boxes(y_chars, scale_factor, y_axis_chars[3], left_y_axis, top_y_axis, 'y')

                colors = plot_image_processing.process_heights(current_img, removable_key)
                scaled_y_vals = plot_image_processing.map_y_values(colors, scaled_y)
                
                fig,axes = plt.subplots(figsize=(10,5))
                
                plot_info = synth_control_and_interpolation.plot_data(filename, test_ixp, scaled_y_vals, scaled_x, start_date_time, start_date, main_color, ixp_type)
                
                all_dict = plot_info[0]
                list_length = len(ixp_list)
                
                if test_ixp == selected_ixp and ixp_count == 0:
                    before_crop = len(plot_info[1])
                    after_crop = len(plot_info[2])
                    x_scale = plot_info[3]
                    new_scaled_x = x_scale[:after_crop]
                    
                if 'Frankfurt' in selected_ixp or 'MIX-IT' in selected_ixp or 'São Paulo' in selected_ixp:
                    
                    if selected_ixp in test_ixp:
                        df_selected_before_jan = plot_info[1][:before_crop] * 1000
                        df_selected_after_jan = plot_info[2][:after_crop] * 1000
                        selected_before_dates = plot_info[4]
                        selected_after_dates = plot_info[3]
                        selected_before_vals = plot_info[5]
                        selected_after_vals = plot_info[6]
                        
                elif selected_ixp in test_ixp:
                    df_selected_before_jan = plot_info[1][:before_crop]
                    df_selected_after_jan = plot_info[2][:after_crop]
                    selected_before_dates = plot_info[4]
                    selected_after_dates = plot_info[3]
                    selected_before_vals = plot_info[5]
                    selected_after_vals = plot_info[6]
                    
                elif 'Frankfurt' in test_ixp or 'MIX-IT' in test_ixp or 'São Paulo' in test_ixp:
                    df_new_before_jan = plot_info[1][:before_crop] * 1000
                    df_new_after_jan = plot_info[2][:after_crop] * 1000
                    new_before_dates = plot_info[4]
                    new_after_dates = plot_info[3]
                    new_before_vals = plot_info[5]
                    new_after_vals = plot_info[6]
                    
                else:
                    df_new_before_jan = plot_info[1][:before_crop]
                    df_new_after_jan = plot_info[2][:after_crop]
                    new_before_dates = plot_info[4]
                    new_after_dates = plot_info[3]
                    new_before_vals = plot_info[5]
                    new_after_vals = plot_info[6]
                    
                if test_ixp in non_de_cix_and_frankfurt and ixp_count > 0:
                    nan_filler_before = synth_control_and_interpolation.nan_fill(selected_before_dates, new_before_dates, new_before_vals)
                    nan_filler_after = synth_control_and_interpolation.nan_fill(selected_after_dates, new_after_dates, new_after_vals)
                    
                    if 'Frankfurt' in test_ixp or 'MIX-IT' in test_ixp or 'São Paulo' in test_ixp:
                        df_new_before_jan = pd.DataFrame({test_ixp: nan_filler_before[0][:before_crop]*1000})
                        df_new_after_jan = pd.DataFrame({test_ixp: nan_filler_after[0][:after_crop]*1000})
                    else:
                        df_new_before_jan = pd.DataFrame({test_ixp: nan_filler_before[0][:before_crop]})
                        df_new_after_jan = pd.DataFrame({test_ixp: nan_filler_after[0][:after_crop]})
                        
                if ixp_count == 0:
                    result_before_jan = df_selected_before_jan
                    result_after_jan = df_selected_after_jan
                    
                elif test_ixp != ixp_list[list_length - 1]:
                    
                    if (df_new_before_jan.isna().sum()[test_ixp] / len(df_new_before_jan)) > 0.7 or (df_new_after_jan.isna().sum()[test_ixp] / len(df_new_after_jan)) > 0.7:
                        new_ixp_list.remove(test_ixp)
                    else:
                    
                        result_before_jan = pd.concat([result_before_jan, 
                                                       df_new_before_jan],
                                                       axis=1, sort=False)
                        
                        result_after_jan = pd.concat([result_after_jan, 
                                                       df_new_after_jan],
                                                       axis=1, sort=False)
                    
                if test_ixp == ixp_list[list_length - 1] and ixp_count > 0:   
                    result_before_jan = result_before_jan.interpolate(method='linear')
                    result_after_jan= result_after_jan.interpolate(method='linear')
                
                    new_ixp_list.remove(selected_ixp)
                    new_ixp_list.remove(selected_ixp)
                    ixp_list_synth = new_ixp_list
                    
                    synth_control_and_interpolation.synthetic_control(result_before_jan, result_after_jan, new_scaled_x, selected_before_dates, selected_ixp, ixp_list_synth)
                    axes.relim()
                    axes.autoscale()
                    axes.grid()
                    axes.set_ylim(bottom=0)
                    plt.legend()
                    
                ixp_count += 1
                
    start_day += 1
    os.chdir(directory)
    
    if start_day == 12 or start_day == 28:
        start_day += 1
    elif start_day == 2 or start_day == 3:
        break