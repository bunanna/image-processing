# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 19:15:23 2021

@author: Brianna Barrow (bmb2193)
"""
import datetime
import os
from PIL import Image

import plot_image_processing
import synth_control_and_interpolation

def get_data(selected_ixp, start_year, start_month, start_day, all_ixps, end_day, end_month, end_year):
    directory = os.getcwd()
    ixp = [selected_ixp]

    other_ixps = all_ixps.copy()
    other_ixps.remove(selected_ixp)
    ixp_list = ixp + other_ixps
    
    current_date = datetime.date(start_year, start_month, start_day)
    current_date_time = datetime.datetime(start_year, start_month, start_day)
    
    all_dict = {}

    for date_file in directory:

        if not os.path.isdir(str(current_date) + ' ' + 'Generated Images'):
            os.makedirs(str(current_date ) + ' ' + 'Generated Images')
        
        os.chdir(str(current_date) + ' ' + 'Generated Images')
        date_directory = os.path.join(directory, str(current_date))
        all_dict[str(current_date)] = {}
        
        for ixp in ixp_list:
            all_dict[str(current_date)][ixp] = {}
            
        for test_ixp in ixp_list:
            
            os.chdir(os.path.join(directory, str(current_date) + ' ' + 'Generated Images'))
            
            if not os.path.isdir(test_ixp):
                os.makedirs(test_ixp)
            os.chdir(test_ixp)
            
            ixp_directory = os.path.join(date_directory, str(current_date) + ' ' + test_ixp)
                
            for filename in os.listdir(ixp_directory):
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
                        
                    display_string = 'Now processing {} plot for {} on {}.'.format(plot_type, test_ixp, str(current_date))
                    print(display_string)
                    
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
                    
                    left_y_axis = axes[3][0]
                    top_y_axis = axes[3][1]
                    
                    x_axis_chars = plot_image_processing.ident_chars(x_axis, scale_factor, 'x', filter_type)
                    y_axis_chars = plot_image_processing.ident_chars(y_axis, scale_factor, 'y', filter_type)
                    
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

                    if plot_type == 'year':
                        plot_info = synth_control_and_interpolation.plot_data_year(filename, test_ixp, scaled_y_vals, scaled_x, current_date_time, current_date, main_color)
    
                        all_dict[str(current_date)][test_ixp][plot_type] = {
                            'dates': plot_info[test_ixp][str(current_date)][plot_type]['raw dates'],
                            'values': plot_info[test_ixp][str(current_date)][plot_type]['values']
                        }
                        
                    else:
                        plot_info = synth_control_and_interpolation.plot_data(filename, test_ixp, scaled_y_vals, scaled_x, current_date_time, current_date, main_color, ixp_type)
    
                        all_dict[str(current_date)][test_ixp][plot_type] = {
                            'dates': plot_info[test_ixp][str(current_date)][plot_type]['raw dates'],
                            'values': plot_info[test_ixp][str(current_date)][plot_type]['values']
                        }
                        
        os.chdir(directory)
        
        current_date += datetime.timedelta(days = 1)
        current_date_time += datetime.timedelta(days = 1)
    
        if (current_date.month == 8 and current_date.day == 12) or (current_date.month == 8 and current_date.day == 28):
            if current_date.day == end_day:
                break
            else:
                current_date += datetime.timedelta(days = 1)
                current_date_time += datetime.timedelta(days = 1)
            
        elif current_date.day == end_day:
            break
        
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
    
    selected_ixp = 'DE-CIX Munich'
    
    start_year = 2020
    start_month = 8
    start_day = 6
    
    end_year = 2020
    end_month = 8
    end_day = 7
    
    all_ixps = ['EPIX.Katowice',
                'EPIX.Warszawa-KIX',
                'ANIX - Albanian Neutral Internet eXchange',
                'TorIX',
                'MIX-IT',
                'IX.br (PTT.br) São Paulo',
                'IX.br (PTT.br) Rio de Janeiro',
                'IX.br (PTT.br) Fortaleza',
                'IX.br (PTT.br) Porto Alegre',
                'IX.br (PTT.br) Brasília',
                'IX.br (PTT.br) Salvador',
                'IX.br (PTT.br) Belém',
                'IX.br (PTT.br) Campinas',
                'IX.br (PTT.br) Londrina',
                'IX.br (PTT.br) Recife',
                'IX.br (PTT.br) Belo Horizonte',
                'IX.br (PTT.br) Natal',
                'IX.br (PTT.br) Florianópolis',
                'IX.br (PTT.br) Maceió',
                'IX.br (PTT.br) Vitória',
                'IX.br (PTT.br) Maringá',
                'IX.br (PTT.br) Goiânia',
                'IX.br (PTT.br) Santa Maria',
                'IX.br (PTT.br) Foz do Iguaçu',
                'IX.br (PTT.br) São José do Rio Preto',
                'IX.br (PTT.br) Manaus',
                'IX.br (PTT.br) Cuiabá',
                'IX.br (PTT.br) Caxias do Sul',
                'LONAP',
                'BCIX',
                'MASS-IX',
                'IXPN Lagos',
                'IIX-Bali',
                'DE-CIX Frankfurt',
                'DE-CIX Munich', 
                'DE-CIX Hamburg',
                'DE-CIX Istanbul',
                'DE-CIX Madrid',
                'DE-CIX Marseille',
                'DE-CIX New York', 
                'DE-CIX Dallas',
                'JPNAP Osaka',
                'JPNAP Tokyo',
                'GrenoblIX', 
                'SAIX',]
    
    all_ixps = ['IX.br (PTT.br) Rio de Janeiro',
                'DE-CIX Munich']
    
    data = get_data(selected_ixp, start_year, start_month, start_day, all_ixps, end_day, end_month, end_year)
    stitched_dict = stitched_data_to_dict(data)