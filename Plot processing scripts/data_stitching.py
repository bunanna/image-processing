# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 19:15:23 2021

@author: Brianna Barrow (bmb2193)
"""
import datetime
import os
from PIL import Image
import traceback

import plot_image_processing
import synth_control_and_interpolation

def get_data_no_loop(selected_ixp, start_year, start_month, start_day):
    directory = os.getcwd()

    current_date = datetime.date(start_year, start_month, start_day)
    current_date_time = datetime.datetime(start_year, start_month, start_day)
    
    all_dict = {}
    
    if current_date <= datetime.date(2020, 9, 23):
        date_directory = os.path.join(directory, str(current_date))
    elif current_date <= datetime.date(2020, 10, 18):
        date_directory = directory
    else:
        date_directory = os.path.join(directory, str(current_date))
        
    all_dict[str(current_date)] = {}
    all_dict[str(current_date)][selected_ixp] = {}
    
    ixp_directory = os.path.join(date_directory, str(current_date) + ' ' + selected_ixp)
    
    if os.path.isdir(ixp_directory) == True:
        
        for filename in os.listdir(ixp_directory):
        
            try:
                plot_type = ''
                  
                #if '1year' in filename:
                if ('year' in filename or 'month' in filename or 'week' in filename and 'peers' not in filename) and 'prefixes' not in filename and '2' not in filename and '5' not in filename and 'two' not in filename:
                    
                    if 'day' in filename:
                        plot_type = 'day'
                    elif 'month' in filename:
                        plot_type = 'month'
                    elif 'week' in filename:
                        plot_type = 'week'
                    elif '5year' in filename:
                        plot_type = '5year'
                    elif '2year' in filename:
                        plot_type = '2year'
                    elif 'twoyear' in filename:
                        plot_type = '2year'
                    elif 'year' in filename:
                        plot_type = 'year'
                        
                    display_string = 'Now processing {} plot for {} on {}.'.format(plot_type, selected_ixp, str(current_date))
                    print(display_string)
                    
                    current_img = Image.open(os.path.join(ixp_directory, filename))
        
                    axes = plot_image_processing.crop_axes(selected_ixp, current_img, plot_type)
                    main_color = axes[5]
                    removable_key = axes[6]
                    ixp_type = axes[7]
                    filter_type = axes[8]
                    
                    x_axis = axes[0]
                    y_axis = axes[1]
                    scale_factor = axes[4]
                    
                    left_x_axis = axes[2][0]
                    top_x_axis = axes[2][1]
                    
                    left_y_axis = axes[3][0]
                    top_y_axis = axes[3][1]
                    
                    x_axis_chars = plot_image_processing.ident_chars(x_axis, scale_factor, 'x', filter_type)
                    y_axis_chars = plot_image_processing.ident_chars(y_axis, scale_factor, 'y', filter_type)
                    
                    if '5year' in filename and 'DE-CIX New York' in selected_ixp:
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
        
                    if plot_type == 'year':
                        plot_info = synth_control_and_interpolation.plot_data_year(filename, selected_ixp, scaled_y_vals, scaled_x, current_date_time, current_date, main_color)
        
                        all_dict[str(current_date)][selected_ixp][plot_type] = {
                            'dates': plot_info[selected_ixp][str(current_date)][plot_type]['raw dates'],
                            'values': plot_info[selected_ixp][str(current_date)][plot_type]['values']
                        }
                        
                    else:
                        plot_info = synth_control_and_interpolation.plot_data(filename, selected_ixp, scaled_y_vals, scaled_x, current_date_time, current_date, main_color, ixp_type)
        
                        all_dict[str(current_date)][selected_ixp][plot_type] = {
                            'dates': plot_info[selected_ixp][str(current_date)][plot_type]['raw dates'],
                            'values': plot_info[selected_ixp][str(current_date)][plot_type]['values']
                        }
                        
            except:
                print('An exception occured when processing the {} plot of {} on {}. Try checking the characters on the x and y axes.'.format(plot_type, selected_ixp, str(current_date)))
                traceback.print_exc()
                continue
                
    else:
        print('The selected IXP was not found.')
                    
    os.chdir(directory)
    
    return all_dict
    
def plot_data_stitching(date_list, plot_type, dict_data, ixp):
    
    base_list_dates = dict_data[date_list[0]][ixp][plot_type]['dates']
    base_list_vals = dict_data[date_list[0]][ixp][plot_type]['values']
            
    for date in date_list:
        crop_index = 0
        cropped_list_dates = []
        cropped_list_vals = []
        
        if date == date_list[0]:
            starting_list_dates = base_list_dates
            starting_list_vals = base_list_vals
        else:
            current_list_dates = dict_data[date][ixp][plot_type]['dates']
            current_list_vals = dict_data[date][ixp][plot_type]['values']
            
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
    
def stitched_data_to_dict(dict_data):
    
    dates = dict_data.keys()
    dates_list = list(dates)
    ixps = dict_data[dates_list[0]].keys()
    ixps_list = list(ixps)
    stitched_dict = {}
    
    for ixp in ixps:
        stitched_dict[ixp] = {}
    
    for ixp in ixps_list:
        types = dict_data[dates_list[0]][ixp].keys()
        
        if 'year' in types:
            year_result = plot_data_stitching(dates_list, 'year', dict_data, ixp)
                            
            stitched_dict[ixp]['year'] = {
                'dates': year_result[0],
                'values': year_result[1]
            }
        
        if 'month' in types:
            month_result = plot_data_stitching(dates_list, 'month', dict_data, ixp)
                            
            stitched_dict[ixp]['month'] = {
                'dates': month_result[0],
                'values': month_result[1]
            }
        
        if 'week' in types:
            week_result = plot_data_stitching(dates_list, 'week', dict_data, ixp)
                            
            stitched_dict[ixp]['week'] = {
                'dates': week_result[0],
                'values': week_result[1]
            }
                            
    return stitched_dict

if __name__ == "__main__":
    
    start_year = 2020
    start_month = 8
    start_day = 6
    
    end_year = 2020
    end_month = 8
    end_day = 8
    
    start_date = datetime.date(start_year, start_month, start_day)
    current_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)
    
    ixp_example = 'DE-CIX Munich'
    
    while current_date < end_date:
        data = get_data_no_loop(ixp_example, start_year, start_month, start_day)
        stitched_dict = stitched_data_to_dict(data)
        current_date += datetime.timedelta(days = 1)