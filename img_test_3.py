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
from collections import Counter
from PIL import Image, ImageFilter, ImageEnhance
from skimage import io
mpl.rcParams['figure.dpi'] = 300
#current_img = 'day.png'
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
    color_count = 3
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
    first_space = False
    date_list = []
    ix_name_list = []
    for char in folder_name:
        if char == ' ' and first_space == False:
            first_space = True
        elif first_space == False:
            date_list.append(char)
        elif first_space == True:
            ix_name_list.append(char)
            
    date = ''.join(date_list)
    ix_name = ''.join(ix_name_list)
    '''
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
        'LyonIX', 
        'MASS-IX', 
        'MUS-IX', 
        'RIX', 
        'SAIX'
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
    boxes_per_string = []
    box_dict = {}
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

def map_x_values_day(y_units_dict, x_axis_dict, current_date):
    x_y_dict = {}
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

    for color in y_units_dict:
        x_values_unscaled = y_units_dict[color]['x values']
        y_values_scaled = y_units_dict[color]['scaled y values']
        y_values_kept = []
        x_values_scaled = []
        x_scaled_string = []
        date_list = []
        index = 0
        
        for val in x_values_unscaled:
            
            if val >= start_location and val < end_location:
                new_val = int(((val - start_location) / (end_location - start_location)) * hour * 60 * 60)
                raw_date = current_date + datetime.timedelta(seconds = new_val)
                val_string = str(raw_date)
                x_values_scaled.append(new_val)
                x_scaled_string.append(val_string)
                y_values_kept.append(y_values_scaled[index])
                date_list.append(raw_date)

            index += 1
            
        x_y_dict[color] = {
            'y values' : y_values_kept,
            'unit' : y_units_dict[color]['unit'],
            'x in seconds' : x_values_scaled,
            'x in hours' : x_scaled_string,
            'raw dates' : date_list
        }
            
    return x_y_dict

def map_x_values_week(y_units_dict, x_axis_dict, current_date):
    x_y_dict = {}
    key_list = list(x_axis_dict.keys())
    key_amount = len(key_list)
    end_time = datetime.datetime.combine(current_date, datetime.time(12, 0))
    start_time = end_time - datetime.timedelta(days = 7)
    start_location = x_axis_dict[key_list[0]]['vertical midline']
    end_location = x_axis_dict[key_list[key_amount - 1]]['vertical midline']
    
    for color in y_units_dict:
        x_values_unscaled = y_units_dict[color]['x values']
        y_values_scaled = y_units_dict[color]['scaled y values']
        y_values_kept = []
        x_values_scaled = []
        x_scaled_string = []
        date_list = []
        index = 0
        
        for val in x_values_unscaled:
            
            if val >= start_location and val < end_location:
                new_val = int(((val - start_location) / (end_location - start_location)) * 7 * 24 * 60 * 60)
                raw_date = start_time + datetime.timedelta(seconds = new_val)
                val_string = str(raw_date)
                x_values_scaled.append(new_val)
                x_scaled_string.append(val_string)
                y_values_kept.append(y_values_scaled[index])
                date_list.append(raw_date)

            index += 1
            
        x_y_dict[color] = {
            'y values' : y_values_kept,
            'unit' : y_units_dict[color]['unit'],
            'x in seconds' : x_values_scaled,
            'x in days' : x_scaled_string,
            'raw dates' : date_list
        }
        
    return x_y_dict

def map_x_values_month(y_units_dict, x_axis_dict, current_date):
    x_y_dict = {}
    
    
    return x_y_dict

def map_x_values_year(y_units_dict, x_axis_dict, current_date):
    x_y_dict = {}
    
    
    return x_y_dict
         
if __name__ == "__main__":
    
    directory = r'C:\Users\brian\OneDrive\Desktop\Programming Projects\Python\COVID Internet Project\Image Processing'
    start_year = 2020
    start_month = 7
    start_day = 30
    test_ixp = 'BCIX'
    start_date = datetime.date(start_year, start_month, start_day)
    start_date_time = datetime.datetime(start_year, start_month, start_day)
    date_directory = os.path.join(directory, str(start_date))
    ixp_directory = os.path.join(date_directory, str(start_date) + ' ' + test_ixp)
    
    for filename in os.listdir(ixp_directory):
        graph_type = ''
        
        if 'day' in filename:
            graph_type = 'day'
        elif 'week' in filename:
            graph_type = 'week'
        elif 'month' in filename:
            graph_type = 'month'
        elif 'year' in filename:
            graph_type = 'year'
            
        if graph_type == 'week':
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
            
            if graph_type == 'day':
                scaled_x_vals = map_x_values_day(scaled_y_vals, scaled_x, start_date_time)
            elif graph_type == 'week':
                scaled_x_vals = map_x_values_week(scaled_y_vals, scaled_x, start_date_time)
            
            x_axis_chars[2].show()
            #y_axis_chars[2].show()
