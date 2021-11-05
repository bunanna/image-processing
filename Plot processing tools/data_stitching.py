# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 19:15:23 2021

@author: Brianna Barrow (bmb2193)
"""
import datetime
import os
from PIL import Image
import traceback
import matplotlib.pyplot as plt

import plot_image_processing

def create_all_ixp_dict(filename, ixp, scaled_y_vals, scaled_x, start_date_time, start_date, main_color, ixp_type, horizontal_offset):
    '''
    Function that invokes the x value mapping function from plot_image_processing to collect the y-values and associated dates in one dictionary.

    Args:
        filename: The plot image filename.

        ixp: The IXP that the plot image was collected from.

        scaled_y_vals: The y-values after being scaled according to the units and y-values on the y-axis of the plot image.

        scaled_x: The x-values after being scaled according to the times on the x-axis of the plot image. 

        start_date_time: Datetime object of the start date selected by the operator.

        start_date: Date object of the start date selected by the operator.

        main_color: The main color of the plotted data, determined using the get_main_color function in plot_image_processing.

        ixp_type: The format of the axis scale units, used in mapping y-values for specific plots (mainly month plots)

        horizontal_offset: The distance, in pixels, between the left edge of the image and the start of the plotted data.

    Returns:
        data_dict: A dictionary collecting the y-values and associated dates (as strings and datetime objects) for the selected IXP.
    '''
    
    data_dict = {}
    data_dict[ixp] = {}
    data_dict[ixp][str(start_date)] = {}
    
    if 'day' in filename:
        scaled_x_vals = plot_image_processing.map_x_values_day(scaled_y_vals, scaled_x, start_date_time, ixp, horizontal_offset)
        dict_string = 'day'
    
    elif 'week' in filename:
        scaled_x_vals = plot_image_processing.map_x_values_week(scaled_y_vals, scaled_x, start_date_time, ixp, horizontal_offset)
        dict_string = 'week'
        
    elif 'month' in filename:
        scaled_x_vals = plot_image_processing.map_x_values_month(scaled_y_vals, scaled_x, start_date_time, ixp_type, ixp, horizontal_offset)
        dict_string = 'month'

    data_dict[ixp][str(start_date)][dict_string] = {}
    
    data_dict[ixp][str(start_date)][dict_string]['values'] = scaled_x_vals[main_color]['y values']
    data_dict[ixp][str(start_date)][dict_string]['dates'] = scaled_x_vals[main_color]['string dates']
    data_dict[ixp][str(start_date)][dict_string]['raw dates'] = scaled_x_vals[main_color]['raw dates']
    
    return data_dict

def create_all_ixp_dict_year(filename, ixp, scaled_y_vals, scaled_x, start_date_time, start_date, main_color, horizontal_offset):
    '''
    Function that invokes the x value mapping function from plot_image_processing to collect the y-values and associated dates in one dictionary for year plots.

    Args:
        filename: The plot image filename.

        ixp: The IXP that the plot image was collected from.

        scaled_y_vals: The y-values after being scaled according to the units and y-values on the y-axis of the plot image.

        scaled_x: The x-values after being scaled according to the times on the x-axis of the plot image. 

        start_date_time: Datetime object of the start date selected by the operator.

        start_date: Date object of the start date selected by the operator.

        main_color: The main color of the plotted data, determined using the get_main_color function in plot_image_processing.

        horizontal_offset: The distance, in pixels, between the left edge of the image and the start of the plotted data.

    Returns:
        data_dict: A dictionary collecting the y-values and associated dates (as strings and datetime objects) for the selected IXP.
    '''
    
    data_dict = {}
    data_dict[ixp] = {}
    data_dict[ixp][str(start_date)] = {}

    if '5year' in filename and 'Frankfurt' in ixp:
        dict_string = '5year'
        scaled_x_vals = plot_image_processing.map_x_values_year(scaled_y_vals, scaled_x, start_date_time, True, ixp, dict_string, horizontal_offset)
    elif 'twoyear' in filename and 'Netnod' in ixp:
        dict_string = '2year'
        scaled_x_vals = plot_image_processing.map_x_values_year(scaled_y_vals, scaled_x, start_date_time, False, ixp, dict_string, horizontal_offset)
    else:
        if '5year' in filename:
            dict_string = '5year'
        elif 'twoyear' in filename:
            dict_string = '2year'
        elif '2year' in filename:
            dict_string = '2year'
        elif 'year' in filename:
            dict_string = 'year'
        scaled_x_vals = plot_image_processing.map_x_values_year(scaled_y_vals, scaled_x, start_date_time, False, ixp, dict_string, horizontal_offset)
    
    data_dict[ixp][str(start_date)][dict_string] = {}
    
    data_dict[ixp][str(start_date)][dict_string]['values'] = scaled_x_vals[main_color]['y values']
    data_dict[ixp][str(start_date)][dict_string]['dates'] = scaled_x_vals[main_color]['string dates']
    data_dict[ixp][str(start_date)][dict_string]['raw dates'] = scaled_x_vals[main_color]['raw dates']
    
    return data_dict

def get_data_no_loop(selected_ixp, start_year, start_month, start_day):
    '''
    Processes the selected IXP plot image, extracts the plotted information, and collects the data into a dictionary.

    Args:
    selected_ixp: The IXP that the plot images should be retrieved from.

    start_year: The year to start looking for plot images from.

    start_month: The month to start looking for plot images from.

    start_day: The day to start looking for plot images from.

    Returns:
    -------
    all_dict: A dictionary that collects the y-values and their associated dates, expressed as datetime objects.
    '''
    
    directory = os.getcwd()
    directory = r'C:\Users\User\Desktop\Research\Plot images'

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
                    folder_name = str(current_date) + ' ' + selected_ixp
        
                    axes = plot_image_processing.crop_axes(folder_name, current_img, plot_type)
                    
                    x_axis = axes[0]
                    y_axis = axes[1]
                    
                    left_x_axis = axes[2][0]
                    top_x_axis = axes[2][1]
                    
                    left_y_axis = axes[3][0]
                    top_y_axis = axes[3][1]
                    
                    scale_factor = axes[4]
                    
                    ixp_type = axes[5]
                    filter_type = axes[6]
                    
                    cropped_plot_box = axes[7]
                    cropped_plot = axes[8]
                    
                    day_time_combined = axes[9]
                    weekday_day_month_combined = axes[10]
                    day_month_combined = axes[11]
                    
                    x_axis_chars = plot_image_processing.ident_chars(x_axis, scale_factor, 'x', filter_type)
                    y_axis_chars = plot_image_processing.ident_chars(y_axis, scale_factor, 'y', filter_type)
                    
                    if '5year' in filename and 'DE-CIX New York' in selected_ixp:
                        x_chars = plot_image_processing.process_chars(x_axis_chars[0], x_axis_chars[1], True, False)
                        y_chars = plot_image_processing.process_chars(y_axis_chars[0], y_axis_chars[1], True, True)
                    else:
                        x_chars = plot_image_processing.process_chars(x_axis_chars[0], x_axis_chars[1], False, False)
                        y_chars = plot_image_processing.process_chars(y_axis_chars[0], y_axis_chars[1], False, True)
                    
                    y_chars = plot_image_processing.process_chars(y_axis_chars[0], y_axis_chars[1], True, True)
            
                    scaled_x = plot_image_processing.map_boxes(x_chars, scale_factor, x_axis_chars[3], left_x_axis, top_x_axis, 'x', day_time_combined, weekday_day_month_combined, day_month_combined)
                    scaled_y = plot_image_processing.map_boxes(y_chars, scale_factor, y_axis_chars[3], left_y_axis, top_y_axis, 'y', False, False, False)
                    
                    removable_key = plot_image_processing.get_removable_key(str(current_date) + ' ' + selected_ixp, plot_type)
        
                    colors = plot_image_processing.process_heights(cropped_plot, selected_ixp)
                    scaled_y_vals = plot_image_processing.map_y_values(colors, scaled_y, cropped_plot_box[1])
                    main_color = plot_image_processing.get_main_color(folder_name, colors)
        
                    if plot_type == 'year':
                        plot_info = create_all_ixp_dict_year(filename, selected_ixp, scaled_y_vals, scaled_x, current_date_time, current_date, main_color, cropped_plot_box[0])
        
                        all_dict[str(current_date)][selected_ixp][plot_type] = {
                            'dates': plot_info[selected_ixp][str(current_date)][plot_type]['raw dates'],
                            'values': plot_info[selected_ixp][str(current_date)][plot_type]['values']
                        }
                        
                    else:
                        plot_info = create_all_ixp_dict(filename, selected_ixp, scaled_y_vals, scaled_x, current_date_time, current_date, main_color, ixp_type, cropped_plot_box[0])
        
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
    starting_list_dates = []
    starting_list_vals = []
            
    for date in date_list:
        crop_index = 0
        cropped_list_dates = []
        cropped_list_vals = []
        
        if plot_type in dict_data[date][ixp].keys():
            
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
        
        if '5year' in types:
            year_result = plot_data_stitching(dates_list, '5year', dict_data, ixp)
                            
            stitched_dict[ixp]['5year'] = {
                'dates': year_result[0],
                'values': year_result[1]
            }
            
        if '2year' in types:
            year_result = plot_data_stitching(dates_list, '2year', dict_data, ixp)
                            
            stitched_dict[ixp]['2year'] = {
                'dates': year_result[0],
                'values': year_result[1]
            }
            
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
    start_day = 1
    
    end_year = 2020
    end_month = 8
    end_day = 3
    
    all_data = {}
    
    current_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)
    
    ixp_example = 'DE-CIX New York'
    
    while current_date < end_date:
        if current_date != datetime.date(2020, 8, 12) and current_date != datetime.date(2020, 8, 28):
            data = get_data_no_loop(ixp_example, current_date.year, current_date.month, current_date.day)
            current_key = list(data.keys())[0]
            all_data[current_key] = data[current_key]
            
        current_date += datetime.timedelta(days = 1)
        
    stitched_dict = stitched_data_to_dict(all_data)
    
    '''
    plt.rcParams.update({'font.size': 4})
    plt.grid()
    plt.plot(stitched_dict[ixp_example]['month']['dates'], stitched_dict[ixp_example]['month']['values'], linewidth = 0.5)
    '''