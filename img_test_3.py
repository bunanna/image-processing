# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 17:29:03 2020

@author: brian
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pytesseract
import os
import datetime
from dateutil.relativedelta import relativedelta
from collections import Counter
from PIL import Image, ImageFilter, ImageEnhance
mpl.rcParams['figure.dpi'] = 300
mpl.rcParams.update({'font.size': 5})
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

'''
from: https://stackoverflow.com/a/33507138
'''
def remove_alpha_channel(img):
    png = img.convert('RGBA')
    background = Image.new('RGBA', png.size, (255,255,255))
    alpha_composite = Image.alpha_composite(background, png)
    alpha_composite.convert('RGB')

    return alpha_composite    

def get_top_colors(img):
    index = 0
    color_count = 10
    process_list = []
    color_list = []
    channels = list(img.getbands())

    if 'A' in channels:
        im = remove_alpha_channel(img)
    else:
        im = img

    quantized_im = im.quantize(colors=color_count,method=2)
    new_quantized_im = quantized_im.convert('RGB')
    top_color_list = quantized_im.getpalette()[:(color_count * 3)]

    for entry in top_color_list:
        process_list.append(entry)

        if index != 2:
            index+=1
        else:
            red = process_list[0]
            green = process_list[1]
            blue = process_list[2]
            
            if red == green and red == blue:
                process_list = []
                index = 0
            else:
                color_list.append(tuple(process_list))
                process_list = []
                index = 0
            
    return color_list, new_quantized_im, im

def get_heights(img):
    color_dict = {}
    res = get_top_colors(img)
    top_colors = res[0]
    quantized_im = res[1]
    original_im = res[2]
    max_x, max_y = original_im.size

    for entry in top_colors:
        color_dict[entry] = {
        'highest in current column': 10000,
        'lowest in current column': 0,
        'current high': 'n/a',
        'current low': 'n/a',
        'x values high': [],
        'x values low': [],
        'all highs': [] ,
        'all lows': []
        }

    for x in range(max_x):
        for y in range(max_y):

            position_tuple = tuple([x, y])
            current_pixel = quantized_im.getpixel(position_tuple)

            if current_pixel in top_colors:

                current_dict = color_dict[current_pixel]

                if current_dict['current high'] == 'n/a':

                    if y < current_dict['highest in current column']:
                        current_dict['current high'] = y

                else:

                    if y < current_dict['current high']:
                        current_dict['current high'] = y

                if current_dict['current low'] == 'n/a':

                    if y > current_dict['lowest in current column']:
                        current_dict['current low'] = y

                else:

                    if y > current_dict['current low']:
                        current_dict['current low'] = y

        for color_tuple in top_colors:

            current_dict = color_dict[color_tuple]

            if current_dict['current high'] != 'n/a':
                current_dict['all highs'].append(current_dict['current high'])
                current_dict['x values high'].append(x)

            if current_dict['current low'] != 'n/a':
                current_dict['all lows'].append(current_dict['current low'])
                current_dict['x values low'].append(x)
            
            current_dict['current high'] = 'n/a'
            current_dict['current low'] = 'n/a'
            current_dict['highest in current column'] = 10000
            current_dict['lowest in current column'] = 0

    return color_dict, top_colors

def process_heights(img, is_removable_key):
    color_info = get_heights(img)
    color_dict = color_info[0]
    top_colors = color_info[1]
    new_color_dict = {}
    
    for color_tuple in top_colors:
        index = 0
        counter = 0
        current_dict = color_dict[color_tuple]
        x_val_list = current_dict['x values high']
        
        if is_removable_key == True:
            for value in x_val_list:
                if index != 0 and x_val_list[index] != x_val_list[index - 1] + 1 and counter < 20:
                    counter = 0
                    break
                else:
                    index += 1
                    counter += 1
                   
            new_color_dict[color_tuple] = {
                'x values': current_dict['x values high'][index:],
                'highs': current_dict['all highs'][index:] ,
                'lows': current_dict['all lows'][index:]
            }
        
        else:
            new_color_dict[color_tuple] = {
                'x values': current_dict['x values high'],
                'highs': current_dict['all highs'],
                'lows': current_dict['all lows']
            }
            
        
    for color in top_colors:
        if len(new_color_dict[color]['x values']) < 10:
            del new_color_dict[color]
            
    return new_color_dict

def crop_axes(folder_name, img):
    left_x_axis = 0
    top_x_axis = 0
    right_x_axis = 0
    bottom_x_axis = 0
    
    left_y_axis = 0
    top_y_axis = 0
    right_y_axis = 0
    bottom_y_axis = 0

    '''
    group 1 (blue):
    dimensions: 500x135
    '''
    group_1 = [
        'angonix',
        'ArmIX',
        'BCIX', 
        'CIX', 
        'IIX-Bali', 
        'IIX-Jogja',
        'IXPN Lagos',
        'LyonIX', 
        'MASS-IX', 
        'MUS-IX', 
        'RIX', 
        'SAIX'
    ]
    
    group_2 = [
        'LONAP'
    ]
    
    if folder_name in group_1:
        left_x_axis = 75
        top_x_axis = 118
        right_x_axis = img.width - 1
        bottom_x_axis = 132
        
        left_y_axis = 25
        top_y_axis = 0
        right_y_axis = 75
        bottom_y_axis = 132
        
        scale_factor = 3
        
    elif folder_name in group_2:
        left_x_axis = 75
        top_x_axis = 168
        right_x_axis = img.width - 1
        bottom_x_axis = 182
        
        left_y_axis = 25
        top_y_axis = 0
        right_y_axis = 75
        bottom_y_axis = 132
        
        scale_factor = 6
        
    x_axis_box = tuple([left_x_axis, top_x_axis, right_x_axis, bottom_x_axis])    
    y_axis_box = tuple([left_y_axis, top_y_axis, right_y_axis, bottom_y_axis])
    
    x_axis = img.crop(tuple(x_axis_box))
    y_axis = img.crop(tuple(y_axis_box))
    
    return x_axis, y_axis, x_axis_box, y_axis_box, scale_factor

def ident_chars(img, scale_factor, axis):
    thresh = 200
    fn = lambda x : 255 if x > thresh else 0
    '''
    img_1 = img.convert('L')
    img_2 = img_1.resize((img_1.size[0]*scale_factor, img_1.size[1]*scale_factor))
    img_3 = img_2.point(fn, mode='1')
    enhanced_img = img_3.filter(ImageFilter.DETAIL)
    '''
    img_1 = img.convert('L')
    img_2 = img_1.resize((img_1.size[0]*scale_factor, img_1.size[1]*scale_factor))
    img_3 = img_2.point(fn, mode='1')
    img_4 = img_3.filter(ImageFilter.ModeFilter(3))
    #img_5 = img_4.filter(ImageFilter.MaxFilter(3))
    enhanced_img = img_4.filter(ImageFilter.DETAIL)
    
    '''
    img_4 = img_3.filter(ImageFilter.ModeFilter(3))
    enhanced_img = img_4.filter(ImageFilter.MaxFilter(3))
    
    .filter(ImageFilter.GaussianBlur(2))
    '''
    
    if axis == 'x':
        text = pytesseract.image_to_string(enhanced_img,lang='eng', config='--psm 6 --oem 3').split()
    elif axis == 'y':
        text = pytesseract.image_to_string(enhanced_img,lang='eng', config='--psm 6 --oem 3').splitlines()
        
    box = pytesseract.image_to_boxes(enhanced_img, lang='eng', config='--psm 6 --oem 3').splitlines()
    text[:] = (string for string in text if string != '')
    text[:] = (string for string in text if string != '|')
    
    '''
    text_num = pytesseract.image_to_string(enhanced_img, lang='eng', config='digits --psm 6 --oem 3').splitlines()
    box_num = pytesseract.image_to_boxes(enhanced_img, lang='eng', config='digits --psm 6 --oem 3').splitlines()
    text_num[:] = (string for string in text_num if string != '')
    
    return scale_factor, text, text_num, box, box_num, enhanced_img
    '''
    
    return text, box, enhanced_img, img_1.size[1]

def process_chars(str_list, box_list):
    index = 0
    copy_count = 2
    current_string_chars = []
    current_box = []
    word_box_dict = {}
    
    for string in str_list:
        for char in string:
            if char != ' ':
                current_string_chars.append(char)
                current_box.append(box_list[index])
                index += 1

        new_str = ''.join(current_string_chars)

        if new_str == 'Week':
            continue
        elif new_str in word_box_dict:
            new_str = new_str + '(' + str(copy_count) + ')'
            copy_count += 1
            word_box_dict[new_str] = current_box
            current_string_chars = []
            current_box = []
        else:
            word_box_dict[new_str] = current_box
            current_string_chars = []
            current_box = []   
        
    return word_box_dict

def map_boxes(word_box_dict, scale, height, shift_right, shift_down, axis):
    words = list(word_box_dict.keys())
    char_box_dict = {}
    
    for word in words:
        current_boxes = word_box_dict[word]
        index = 0
        vert_midline = 0
        hori_midline_avg = 0
        hori_midline = 0
        number_chars = []
        
        for box in current_boxes:
            char_box_list = box.split()
            
            if axis == 'y':
                if char_box_list[0].isdigit() or char_box_list[0] == '.':
                    number_chars.append(char_box_list[0])
                else:
                    unit = char_box_list[0]
            
            if len(current_boxes) == 1:
                left_border = (int(char_box_list[1]) // scale) + shift_right
                right_border = (int(char_box_list[3]) // scale) + shift_right
            elif index == 0:
                left_border = (int(char_box_list[1]) // scale) + shift_right
            elif index == len(current_boxes) - 1:
                right_border = (int(char_box_list[3]) // scale) + shift_right
            
            top = abs((int(char_box_list[4]) // scale) - height) + shift_down
            bottom = abs((int(char_box_list[2]) // scale) - height) + shift_down
            
            hori_midline += (bottom + top) // 2
            index += 1

        hori_midline_avg = hori_midline // len(current_boxes)
        vert_midline = (left_border + right_border) // 2
        
        if axis == 'y':
            length = len(number_chars)
            if number_chars[length - 1] == '6' and number_chars[length - 2] == '0':
                number_chars = number_chars[:(length - 1)]
                
            if '.' in number_chars:
                number = float(''.join(number_chars))
            else:
                number = int(''.join(number_chars))
            
            char_box_dict[number] = {
                "vertical midline" : vert_midline,
                "horizontal midline" : hori_midline_avg,
                "unit" : unit
            }
    
        else:
            char_box_dict[word] = {
                "vertical midline" : vert_midline,
                "horizontal midline" : hori_midline_avg
            }
           
    return char_box_dict

def map_y_values(color_dict, y_axis_dict):
    y_scaled_color_dict = {}
    y_values = list(y_axis_dict.keys())
    unit_list = []
    
    largest_val = max(y_values)
    smallest_val = min(y_values)
    
    highest_y_val = y_axis_dict[largest_val]['horizontal midline']
    lowest_y_val = y_axis_dict[smallest_val]['horizontal midline']
    
    for key in y_axis_dict:
        unit_list.append(y_axis_dict[key]['unit'])
    
    count = Counter(unit_list)
    current_unit = count.most_common(1)[0][0]

    for color in color_dict:
        y_values_colors = color_dict[color]['highs']
        y_values_scaled = []
        
        for val in y_values_colors:
            new_val = (1 - (val - highest_y_val) / (lowest_y_val - highest_y_val)) * largest_val
            y_values_scaled.append(round(new_val, 2))
            
        y_scaled_color_dict[color] = {
            'scaled y values' : y_values_scaled,
            'x values' : color_dict[color]['x values'],
            'unit' : current_unit
        }
        
    return y_scaled_color_dict

def scale_by_color(y_units_dict, start_loc, end_loc, time_factor, start_date):
    x_y_dict = {}
    
    for color in y_units_dict:
        x_values_unscaled = y_units_dict[color]['x values']
        y_values_scaled = y_units_dict[color]['scaled y values']
        y_values_kept = []
        date_list = []
        index = 0
        
        for val in x_values_unscaled:
            
            new_val = int(((val - start_loc) / (end_loc - start_loc)) * time_factor)
            raw_date = start_date + datetime.timedelta(seconds = new_val)
            y_values_kept.append(y_values_scaled[index])
            date_list.append(raw_date)

            index += 1
            
        x_y_dict[color] = {
            'y values' : y_values_kept,
            'unit' : y_units_dict[color]['unit'],
            'raw dates' : date_list
        }
            
    return x_y_dict

def map_x_values_day(y_units_dict, x_axis_dict, current_date):
    key_list = list(x_axis_dict.keys())
    key_amount = len(key_list)
    label_list = []
    zero_count = 0
    first_zero = 0
    second_zero = 0
    start_location = 0
    end_location = 0
    first_zero_index = 0
    middle_index = 0
    index = 0
    hour = 0

    for key in x_axis_dict:
        if ':' in key:
            cut_index = key.index(':')
            current_key = key[:cut_index]
        elif '(' in key:
            cut_index = key.index('(')
            current_key = key[:cut_index]            
        else:
            current_key = key

        label_list.append(current_key)   
        
        if current_key == '0' or current_key == '00':
            if zero_count == 0:
                first_zero = x_axis_dict[key]['vertical midline']
                zero_count += 1
                first_zero_index = index
            elif zero_count == 1:
                second_zero = x_axis_dict[key]['vertical midline']
                zero_count += 1
        index += 1
        
    if second_zero == 0:
        middle_index = key_amount // 2
        if first_zero_index >= middle_index:
            start_location = x_axis_dict[key_list[0]]['vertical midline']
            end_location = first_zero
            hour = 24 - int(label_list[0])
        elif first_zero_index < middle_index:
            start_location = first_zero
            end_location = x_axis_dict[key_list[key_amount - 1]]['vertical midline']
            hour = int(label_list[0])
    else:
        start_location = first_zero
        end_location = second_zero
        hour = 24
    
    return scale_by_color(y_units_dict, start_location, end_location, hour * 60 * 60, current_date)

def map_x_values_week(y_units_dict, x_axis_dict, current_date):
    key_list = list(x_axis_dict.keys())
    key_amount = len(key_list)
    
    if 'on' in key_list[key_amount - 1]:
        weekday = 1
    elif 'ue' in key_list[key_amount - 1]:
        weekday = 2
    elif 'ed' in key_list[key_amount - 1]:
        weekday = 3
    elif 'hu' in key_list[key_amount - 1]:
        weekday = 4
    elif 'ri' in key_list[key_amount - 1]:
        weekday = 5
    elif 'at' in key_list[key_amount - 1]:
        weekday = 6
    elif 'un' in key_list[key_amount - 1]:
        weekday = 7
        
    if weekday == current_date.isoweekday():
        end_time = datetime.datetime.combine(current_date, datetime.time(12, 0))
    elif weekday < current_date.isoweekday():
        end_time = datetime.datetime.combine(current_date, datetime.time(12, 0)) - datetime.timedelta(days = current_date.isoweekday() - weekday)
    elif weekday > current_date.isoweekday():
        end_time = datetime.datetime.combine(current_date, datetime.time(12, 0)) - datetime.timedelta(days = weekday - current_date.isoweekday())
    
    end_time += datetime.timedelta(days = 1)
    start_time = end_time - datetime.timedelta(days = key_amount)
    start_location = x_axis_dict[key_list[0]]['vertical midline']
    end_location = x_axis_dict[key_list[key_amount - 1]]['vertical midline']
        
    return scale_by_color(y_units_dict, start_location, end_location, (key_amount - 1) * 24 * 60 * 60, start_time)

def map_x_values_month(y_units_dict, x_axis_dict, current_date):
    end_week_number_string_list = []
    start_week_number_string_list = []
    first_tag = 1
    key_list = list(x_axis_dict.keys())
    key_amount = len(key_list) 
    week_number = current_date.isocalendar()[1]

    if str(week_number) in key_list[key_amount - 1]:
        if current_date.isoweekday() >= 4:
            end_time = datetime.datetime.combine(current_date, datetime.time(0, 0)) - datetime.timedelta(days = (current_date.isoweekday() - 4))
    else:
        for char in key_list[key_amount - 1]:
            if char.isdigit() == True:
                end_week_number_string_list.append(char)
        
        end_week_number_label = ''.join(end_week_number_string_list)
        end_time = datetime.datetime.combine(current_date, datetime.time(0, 0)) - datetime.timedelta(weeks = week_number - int(end_week_number_label))
        
        if end_time.isoweekday() > 4:
            end_time -= datetime.timedelta(days = (end_time.isoweekday() - 4))
        elif end_time.isoweekday() < 4:
            end_time += datetime.timedelta(days = (4 - end_time.isoweekday()))
            
    while 'Week' not in key_list[first_tag]:
        first_tag += 1
        
    for char in key_list[first_tag]:
        if char.isdigit() == True:
            start_week_number_string_list.append(char)
    
    start_week_number_label = ''.join(start_week_number_string_list)
    start_time = end_time - datetime.timedelta(weeks = end_time.isocalendar()[1] - int(start_week_number_label))
    start_location = x_axis_dict[key_list[first_tag]]['vertical midline']
    end_location = x_axis_dict[key_list[key_amount - 1]]['vertical midline']
     
    return scale_by_color(y_units_dict, start_location, end_location, (end_time.isocalendar()[1] - int(start_week_number_label)) * 7 * 24 * 60 * 60, start_time)

def map_x_values_year(y_units_dict, x_axis_dict, current_date):
    key_list = list(x_axis_dict.keys())
    key_amount = len(key_list)
    
    if 'an' in key_list[key_amount - 2]:
        month_num = 1
    elif 'eb' in key_list[key_amount - 2]:
        month_num = 2
    elif 'ar' in key_list[key_amount - 2]:
        month_num = 3
    elif 'pr' in key_list[key_amount - 2]:
        month_num = 4
    elif 'ay' in key_list[key_amount - 2]:
        month_num = 5
    elif 'un' in key_list[key_amount - 2]:
        month_num = 6
    elif 'ul' in key_list[key_amount - 2]:
        month_num = 7
    elif 'ug' in key_list[key_amount - 2]:
        month_num = 8
    elif 'ep' in key_list[key_amount - 2]:
        month_num = 9
    elif 'ct' in key_list[key_amount - 2]:
        month_num = 10
    elif 'ov' in key_list[key_amount - 2]:
        month_num = 11
    elif 'ec' in key_list[key_amount - 2]:
        month_num = 12
    
    if month_num == 12:
        end_time = datetime.datetime(current_date.year - 1, month_num, 15, 0, 0)
    else:
        end_time = datetime.datetime(current_date.year, month_num, 15, 0, 0)
    
    start_time = end_time - relativedelta(months = key_amount - 2)
    start_location = x_axis_dict[key_list[0]]['vertical midline']
    end_location = x_axis_dict[key_list[key_amount - 2]]['vertical midline']
    change = end_time - start_time
    
    return scale_by_color(y_units_dict, start_location, end_location, change.days * 24 * 60 * 60, start_time) 
  
if __name__ == "__main__":
    
    directory = r'C:\Users\brian\OneDrive\Desktop\Programming Projects\Python\COVID Internet Project\Image Processing\August Images'
    all_dict = {}
    start_year = 2020
    start_month = 8
    start_day = 1
    ixp_list = ['LONAP']
    
    for date_file in directory:

        start_date = datetime.date(start_year, start_month, start_day)
        start_date_time = datetime.datetime(start_year, start_month, start_day)
        date_directory = os.path.join(directory, str(start_date))
        
        for test_ixp in ixp_list:
            ixp_directory = os.path.join(date_directory, str(start_date) + ' ' + test_ixp)
            
            if test_ixp not in all_dict:
                all_dict[test_ixp] = {}
                all_dict[test_ixp][str(start_date)] = {}
                
            for filename in os.listdir(ixp_directory):
                graph_type = ''
                
                day_plot = False
                week_plot = False
                month_plot = False
                year_plot = False
                
                if 'day' in filename:
                    day_plot = True
                elif 'week' in filename:
                    week_plot = True
                elif 'month' in filename:
                    month_plot = True
                elif 'year' in filename:
                    year_plot = True
                    
                if day_plot == True or week_plot == True or month_plot == True or year_plot == True:
                    current_img = Image.open(os.path.join(ixp_directory, filename))
                    colors = process_heights(current_img, False)
                    axes = crop_axes(test_ixp, current_img)
                    
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
                    
                    x_axis_chars = ident_chars(x_axis, scale_factor, 'x')
                    y_axis_chars = ident_chars(y_axis, scale_factor, 'y')
                    
                    x_chars = process_chars(x_axis_chars[0], x_axis_chars[1])
                    y_chars = process_chars(y_axis_chars[0], y_axis_chars[1])
                    
                    scaled_x = map_boxes(x_chars, scale_factor, x_axis_chars[3], left_x_axis, top_x_axis, 'x')
                    scaled_y = map_boxes(y_chars, scale_factor, y_axis_chars[3], left_y_axis, top_y_axis, 'y')

                    scaled_y_vals = map_y_values(colors, scaled_y)
                    
                    if day_plot == True:
                        day_scaled_x_vals = map_x_values_day(scaled_y_vals, scaled_x, start_date_time)
                    elif week_plot == True:
                        week_scaled_x_vals = map_x_values_week(scaled_y_vals, scaled_x, start_date_time)
                    elif month_plot == True:
                        month_scaled_x_vals = map_x_values_month(scaled_y_vals, scaled_x, start_date_time)
                    elif year_plot == True:
                        year_scaled_x_vals = map_x_values_year(scaled_y_vals, scaled_x, start_date_time)
            
            if day_plot == True:
                fig,axes = plt.subplots(figsize=(15,5))
                plt.plot(day_scaled_x_vals[(84, 190, 239)]['raw dates'], day_scaled_x_vals[(84, 190, 239)]['y values'], linewidth = 1)
                plt.ylabel('Incoming traffic in ' + day_scaled_x_vals[(84, 190, 239)]['unit'] + 'bits per second')
                plt.tight_layout()
                plt.savefig(str(start_date) + ' ' + test_ixp + ' ' + 'day' + '.pdf')
                plt.cla()
                plt.close()
                all_dict[test_ixp][str(start_date)]['day'] = day_scaled_x_vals[(84, 190, 239)]
            
            if week_plot == True:
                fig,axes = plt.subplots(figsize=(15,5))
                plt.plot(week_scaled_x_vals[(84, 190, 239)]['raw dates'], week_scaled_x_vals[(84, 190, 239)]['y values'], linewidth = 1)
                plt.ylabel('Incoming traffic in ' + week_scaled_x_vals[(84, 190, 239)]['unit'] + 'bits per second')
                plt.tight_layout()
                plt.savefig(str(start_date) + ' ' + test_ixp + ' ' + 'week' + '.pdf')
                plt.cla()
                plt.close()
                all_dict[test_ixp][str(start_date)]['week'] = week_scaled_x_vals[(84, 190, 239)]
            
            if month_plot == True:
                fig,axes = plt.subplots(figsize=(15,5))
                plt.plot(month_scaled_x_vals[(84, 190, 239)]['raw dates'], month_scaled_x_vals[(84, 190, 239)]['y values'], linewidth = 1)
                plt.ylabel('Incoming traffic in ' + month_scaled_x_vals[(84, 190, 239)]['unit'] + 'bits per second')
                plt.tight_layout()
                plt.savefig(str(start_date) + ' ' + test_ixp + ' ' + 'month' + '.pdf')
                plt.cla()
                plt.close()
                all_dict[test_ixp][str(start_date)]['month'] = month_scaled_x_vals[(84, 190, 239)]
            
            if year_plot == True:
                fig,axes = plt.subplots(figsize=(15,5))
                plt.plot(year_scaled_x_vals[(84, 190, 239)]['raw dates'], year_scaled_x_vals[(84, 190, 239)]['y values'], linewidth = 1)
                plt.ylabel('Incoming traffic in ' + year_scaled_x_vals[(84, 190, 239)]['unit'] + 'bits per second')
                plt.tight_layout()
                plt.savefig(str(start_date) + ' ' + test_ixp + ' ' + 'year' + '.pdf')
                plt.cla()
                plt.close()
                all_dict[test_ixp][str(start_date)]['month'] = month_scaled_x_vals[(84, 190, 239)]
             
        start_day += 1
        if start_day == 12 or start_day == 28:
            start_day += 1
        elif start_day == 32:
            break