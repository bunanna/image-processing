# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 17:29:03 2020

@author: Brianna Barrow (bmb2193)
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
import ruptures as rpt

mpl.rcParams['figure.dpi'] = 300
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def remove_alpha_channel(img):
    '''
    from: https://stackoverflow.com/a/33507138
    
    Removes the alpha channel by creating a white image matching the 
    dimensions of the input image and forming a composite with the white image 
    and the original image without the alpha channel.
    
    Args:
        img: Image with alpha channel in png format.
        
    Returns:
        alpha_composite: Image composite without alpha channel.
    '''
    
    png = img.convert('RGBA')
    background = Image.new('RGBA', png.size, (255,255,255))
    alpha_composite = Image.alpha_composite(background, png)
    alpha_composite.convert('RGB')

    return alpha_composite    


def get_top_colors(img):
    '''
    Quantizes the image, which maps all distinct colors to a palette of 256
    colors.
    
    Args:
        img: Image in png format.
        
    Returns:
        color_list: A list of the desired number of colors as RGB tuples.
    
        new_quantized_im: The image with all colors changed to those in the 
        palette that they resemble.
        
        im: The original image.
    '''
    
    index = 0
    color_count = 20
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
    '''
    Iterates over the input image's pixels and finds the x-values and highest 
    and lowest y-values for pixels of specific colors.
    
    Args:
        img: Image in png format.
        
    Returns:
        color_dict: A dictionary of each color leading to a dictionary of the
        highest and lowest y-values per color, as well as x-values, for pixels 
        of that color.
        
        top_colors: A list of the desired number of colors as RGB tuples.
    '''
    
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
    '''
    Remaps the color dictionary from the function above to fewer keys for each
    color. Also filters out any y-values belonging to keys next to the plot 
    and any colors with less than 10 x-values associated with them.
    
    Args:
        img: Image in png format.
            
        is_removable_key: A boolean specifying if the plot has a key that can 
        be removed by filtering out beginning x-values that correspond to 
        unchanging consecutive y-values.
        
    Returns:
        new_color_dict: A dictionary of each color leading to a dictionary of 
        the highest and lowest y-values per color, as well as x-values, for 
        pixels of that color.
    '''
    
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
    '''
    Crops the x and y axes from the image and identifies the IX the image is 
    from to generate information needed for further processing by subsequent 
    functions.
    
    Args:
        folder_name: The name of the folder in which img is found. Used to 
        determine the IXP name.
            
        img: Image in png format.
        
    Returns:
        x_axis: The x-axis cropped from img.
            
        y_axis: The y-axis cropped from img.
            
        x_axis_box: The bounding box used to crop out the x-axis.
            
        y_axis_box: The bounding box used to crop out the y-axis.
            
        scale_factor: The scale factor used to increase the size of the axes 
        to increase Tesseract's accuracy.
            
        primary_color: The primary color for the incoming traffic plot for 
        each IX.
            
        removable_key: Boolean for if the IX's plots have keys that can be 
        filtered out from the list of x-values.
            
        plot_type: The format of the axis scale units, used in mapping 
        y-values for specific plots (mainly month plots).
            
        filter_type: The list of filters that work well for each IX.
    '''
    
    left_x_axis = 0
    top_x_axis = 0
    right_x_axis = 0
    bottom_x_axis = 0
    
    left_y_axis = 0
    top_y_axis = 0
    right_y_axis = 0
    bottom_y_axis = 0
    
    removable_key = False
    plot_type = 0
    filter_type = 0
    primary_color = ()

    '''
    group 1 (blue):
    dimensions: 500x135, 600x135, 700x135
    no features below x-axis
    '''
    group_1 = [
        'angonix',
        'ArmIX',
        'BCIX', 
        'CIX',
        'GrenoblIX',
        'IIX-Bali', 
        'IIX-Jogja',
        'IXPN Lagos',
        'KAZ-GOV-IX',
        'LONAP',
        'LyonIX', 
        'MASS-IX', 
        'MUS-IX', 
        'RIX', 
        'SAIX'
    ]
    
    '''
    group 2 (yellow):
    dimensions: 
    '''
    group_2 = [
        'DE-CIX Dallas',
        'DE-CIX Hamburg',
        'DE-CIX Istanbul',
        'DE-CIX Madrid',
        'DE-CIX Marseille',
        'DE-CIX Munich',
        'DE-CIX New York',
        'DE-CIX Palermo'
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
        
        scale_factor = 4
        plot_type = 1
        filter_type = 1
        removable_key = False

        if 'GrenoblIX' in folder_name:
            left_y_axis = 21
            scale_factor = 6
            filter_type = 2
        elif 'KAZ-GOV-IX' in folder_name:
            top_x_axis = 168
            bottom_x_axis = 182
            bottom_y_axis = 182
            scale_factor = 6
        elif 'LONAP' in folder_name:
            top_x_axis = 168
            bottom_x_axis = 182
            bottom_y_axis = 182
            scale_factor = 6
          
        if 'IXPN Lagos' in folder_name:
            primary_color = (4, 192, 4)
        elif 'LONAP' in folder_name:
            primary_color = (84, 190, 239) 
        else:    
            primary_color = (0, 204, 0)

    elif folder_name in group_2:
        left_x_axis = 46
        top_x_axis = 434
        right_x_axis = img.width - 1
        bottom_x_axis = 451
        
        left_y_axis = 10
        top_y_axis = 0
        right_y_axis = 46
        bottom_y_axis = 451
        
        scale_factor = 6
        
        plot_type = 2
        filter_type = 1
        removable_key = True
        
        primary_color = (246, 217, 15)
        
    x_axis_box = tuple([left_x_axis, top_x_axis, right_x_axis, bottom_x_axis])    
    y_axis_box = tuple([left_y_axis, top_y_axis, right_y_axis, bottom_y_axis])
    
    x_axis = img.crop(tuple(x_axis_box))
    y_axis = img.crop(tuple(y_axis_box))
    
    return x_axis, y_axis, x_axis_box, y_axis_box, scale_factor, primary_color, removable_key, plot_type, filter_type


def ident_chars(img, scale_factor, axis, filter_set):
    '''
    Takes the cropped axes from the function above and processes them using a 
    list of filters, with the filters used determined by which IX the plot
    comes from, then uses Tesseract OCR to find the characters used in the
    axis scales.

    Args:
        img: Image as a Pillow Image object.
            
        scale_factor: The scale factor used to increase the size of the axes 
        to increase Tesseract's accuracy.
            
        axis: The axis, x or y, that is being processed.
            
        filter_set: An integer that picks between lists of filter settings, as
        determined based on the IX the image is from.
    
    Returns:
        text: The strings in the image, as determined by Tesseract.
            
        box: The characters and box coordinates that surround them, as
        determined by Tesseract.
            
        enhanced_img: The image of the axis with the selected filters applied.
            
        img_1.size[1]: The height of the original image.
    '''
    
    thresh = 200
    fn = lambda x : 255 if x > thresh else 0

    if filter_set == 1:
        img_1 = img.convert('L')
        img_2 = img_1.resize((img_1.size[0]*scale_factor, img_1.size[1]*scale_factor))
        img_3 = img_2.point(fn, mode='1')
        img_4 = img_3.filter(ImageFilter.ModeFilter(3))
        img_5 = img_4.filter(ImageFilter.MaxFilter(3))
    
        enhanced_img = img_5.filter(ImageFilter.DETAIL)
    elif filter_set == 2:
        img_1 = img.convert('L')
        img_2 = img_1.resize((img_1.size[0]*scale_factor, img_1.size[1]*scale_factor))
        img_3 = img_2.point(fn, mode='1')
        img_4 = img_3.filter(ImageFilter.ModeFilter(3))
    
        enhanced_img = img_4.filter(ImageFilter.DETAIL)
    
    if axis == 'x':
        text = pytesseract.image_to_string(enhanced_img,lang='eng', config='--psm 6 --oem 3').split()
    elif axis == 'y':
        text = pytesseract.image_to_string(enhanced_img,lang='eng', config='--psm 6 --oem 3').splitlines()
        
    box = pytesseract.image_to_boxes(enhanced_img, lang='eng', config='--psm 6 --oem 3').splitlines()
  
    box[:] = (string for string in box if string[0] != '')
    box[:] = (string for string in box if string[0] != '|')
    box[:] = (string for string in box if string[0] != '—')
    
    text[:] = (string for string in text if string != '')
    text[:] = (string for string in text if string != '|')
    text[:] = (string for string in text if string != '—')
    
    return text, box, enhanced_img, img_1.size[1]

def process_chars(str_list, box_list):
    '''
    Associates strings with the boxes and characters that form them.
    
    Args:
        str_list: A list of the strings in the image being processed, as
        determined by Tesseract.
            
        box_list: A list of the boxes and associated characters, as determined
        by Tesseract.
    
    Returns:
        word_box_dict: A dictionary mapping strings in the image to their
        constituent characters and associated boxes.
    '''
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
    '''
    Uses box information to determine the coordinates (expressed as midlines) 
    of each string found by Tesseract. If the axis being processed is the 
    y-axis, it also finds the unit the number strings are in.
    
    Args:
        word_box_dict: A dictionary mapping strings in the image to their
        constituent characters and associated boxes.
            
        scale: The scale factor used to scale up the image, now used to return
        the coordinates scaled to the original image.
            
        height: The original height (before scaling) of the axis image.
            
        shift_right: An integer used to offset and correct the x coordinates. 
            
        shift_down: An integer used to offset and correct the y coordinates.
            
        axis: The axis, x or y, currently being processed.
            
    Returns:
        char_box_dict: Dictionary mapping strings to their coordinates, as
        determined by their characters' constituent boxes. If the axis being 
        processed is the y-axis, the keys will be integers corresponding to
        values on the y-axis.
    '''
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
    '''
    Scales the y-values in the input dictionary to the actual y-values on the
    plot by determining the pixel y-value of the highest and lowest values on
    the y-axis and scaling individual pixel y-values accordingly.
    
    Args:
        color_dict: A dictionary of each color leading to a dictionary of 
        the highest and lowest y-values per color, as well as x-values, for 
        pixels of that color.
            
        y_axis_dict: Dictionary mapping y-axis scale strings to their 
        coordinates, as determined by their characters' constituent boxes.

    Returns:
        y_scaled_color_dict: A dictionary that maps colors to their
        respective pixels, with each pixel's y-value being scaled to the
        actual y-value on the plot. The original x-values and y-axis unit
        values are unchanged.
    '''
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
    '''
    Takes each color in the y_units_dict and scales the x-values found in each
    color to their corresponding x-values in the x-axis time scale.
    
    Args:
        y_units_dict: A dictionary that maps colors to their
        respective pixels, with each pixel's y-value being scaled to the
        actual y-value on the plot.
            
        start_loc: The first identified label on the x-axis, used as a 
        reference for mapping pixel x-values to plot x-values.
            
        end_loc: The last identified label on the x-axis, used as a 
        reference for mapping pixel x-values to plot x-values.
            
        time_factor: The amount of seconds in the range marked by start_loc
        and end_loc.
            
        start_date: The actual date corresponding to start_loc.

    Returns:
        x_y_dict: A dictionary mapping colors to the x and y values of their 
        pixels in actual units.
    '''
    x_y_dict = {}
    
    for color in y_units_dict:
        x_values_unscaled = y_units_dict[color]['x values']
        y_values_scaled = y_units_dict[color]['scaled y values']
        y_values_kept = []
        date_list = []
        str_date_list = []
        index = 0
        
        for val in x_values_unscaled:
            
            new_val = int(((val - start_loc) / (end_loc - start_loc)) * time_factor)
            raw_date = start_date + datetime.timedelta(seconds = new_val)
            y_values_kept.append(y_values_scaled[index])
            date_list.append(raw_date)
            str_date_list.append(str(raw_date))

            index += 1
            
        x_y_dict[color] = {
            'y values' : y_values_kept,
            'unit' : y_units_dict[color]['unit'],
            'raw dates' : date_list,
            'string dates': str_date_list
        }
            
    return x_y_dict

def map_x_values_day(y_units_dict, x_axis_dict, current_date):
    '''
    Determines the start and end location for the specified day and scales the
    input x-values around the range of the specified day.

    Args:
        y_units_dict: A dictionary that maps colors to their
        respective pixels, with each pixel's y-value being scaled to the
        actual y-value on the plot.
        
        x_axis_dict: Dictionary mapping strings to their coordinates, as
        determined by their characters' constituent boxes.
            
        current_date: The actual date corresponding to start_loc.

    Returns: 
        A dictionary mapping colors to the x and y values of their pixels in 
        actual units.
    '''
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
    '''
    Determines the start and end location for the specified day's week and 
    scales the input x-values around the range of the specified days.

    Args:
        y_units_dict: A dictionary that maps colors to their
        respective pixels, with each pixel's y-value being scaled to the
        actual y-value on the plot.
        
        x_axis_dict: Dictionary mapping strings to their coordinates, as
        determined by their characters' constituent boxes.
            
        current_date: The actual date corresponding to start_loc.

    Returns:
        A dictionary mapping colors to the x and y values of their pixels in 
        actual units.
    '''
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

def map_x_values_month(y_units_dict, x_axis_dict, current_date, ixp_type):
    '''
    Determines the start and end location for the specified day's week's month
    and scales the input x-values around the range of the specified weeks.

    Args:
        y_units_dict: A dictionary that maps colors to their
        respective pixels, with each pixel's y-value being scaled to the
        actual y-value on the plot.
        
        x_axis_dict: Dictionary mapping strings to their coordinates, as
        determined by their characters' constituent boxes.
            
        current_date: The actual date corresponding to start_loc.
        
        ixp_type: Integer specifying the format the x-axis labels are in.

    Returns:
        A dictionary mapping colors to the x and y values of their pixels in 
        actual units.
    '''
    end_week_number_string_list = []
    start_week_number_string_list = []
    first_tag = 1
    key_list = list(x_axis_dict.keys())
    key_amount = len(key_list) 
    
    if ixp_type == 1:
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
        time_scale = (end_time.isocalendar()[1] - int(start_week_number_label)) * 7 * 24 * 60 * 60
        
    elif ixp_type == 2:
        end_time = datetime.datetime.combine(current_date, datetime.time(12, 0))
        
        while end_time.day != int(key_list[key_amount - 1]):
            end_time -= datetime.timedelta(days = 1)
        
        start_time = datetime.datetime(end_time.year, end_time.month - 1, int(key_list[1]), 12)
        start_location = (x_axis_dict[key_list[0]]['vertical midline'] + x_axis_dict[key_list[1]]['vertical midline']) // 2
        end_location = (x_axis_dict[key_list[key_amount - 2]]['vertical midline'] + x_axis_dict[key_list[key_amount - 1]]['vertical midline']) // 2
        time_scale = (end_time - start_time).days * 24 * 60 * 60
        
    return scale_by_color(y_units_dict, start_location, end_location, time_scale, start_time)

def map_x_values_year(y_units_dict, x_axis_dict, current_date):
    '''
    Determines the start and end location for the specified day's week's 
    month's year and scales the input x-values around the range of the 
    specified months.

    Args:
        y_units_dict: A dictionary that maps colors to their
        respective pixels, with each pixel's y-value being scaled to the
        actual y-value on the plot.
        
        x_axis_dict: Dictionary mapping strings to their coordinates, as
        determined by their characters' constituent boxes.
            
        current_date: The actual date corresponding to start_loc.

    Returns:
        A dictionary mapping colors to the x and y values of their pixels in 
        actual units.
    '''
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

def find_peak_ranges(processed_y_values):
    '''
    Uses ruptures to find breakpoints (areas where the series of data changes
    suddenly) and highlight regions of interest.

    Args:
        processed_y_values: A dictionary mapping colors to the x and y values 
        of their pixels in actual units.

    Returns: The three regions of interest with the highest averages.

    '''
    throughput_numpy = np.array(processed_y_values)                
    algo = rpt.Pelt(model='rbf').fit(throughput_numpy)
    result = algo.predict(pen=10)
    breakpoint_amt = len(result)
    
    start_index_in_result = 0
    end_index_in_result = 1
    start_index = 0
    end_index = 0
    breakpoint_avg_list = []
    avg_index_list = []
    
    while end_index_in_result < breakpoint_amt:
        start_index = result[start_index_in_result]
        end_index = result[end_index_in_result]
        new_numpy = throughput_numpy[start_index:end_index]
        breakpoint_avg_list.append(int(np.mean(new_numpy)))
        avg_index_list.append((start_index, end_index))
        start_index_in_result += 1
        end_index_in_result += 1
        
    list_to_sort = zip(breakpoint_avg_list, avg_index_list)
    sorted_list = sorted(list_to_sort)
    tuples = zip(*sorted_list)
    avg, indices = [list(tuple) for tuple in tuples]

    return indices[len(indices)-3:len(indices)]

if __name__ == "__main__":
    
    directory = r'C:\Users\brian\OneDrive\Desktop\Programming Projects\Python\COVID Internet Project\Image Processing\August Images'
    all_dict = {}
    start_year = 2020
    start_month = 8
    start_day = 1
    ixp_list = ['DE-CIX Madrid']
    
    for date_file in directory:

        start_date = datetime.date(start_year, start_month, start_day)
        start_date_time = datetime.datetime(start_year, start_month, start_day)
        date_directory = os.path.join(directory, str(start_date))
        
        for test_ixp in ixp_list:
            ixp_directory = os.path.join(date_directory, str(start_date) + ' ' + test_ixp)
            day_plot = False
            week_plot = False
            month_plot = False
            year_plot = False
            
            if test_ixp not in all_dict:
                all_dict[test_ixp] = {}
                all_dict[test_ixp][str(start_date)] = {}
                
            for filename in os.listdir(ixp_directory):
                graph_type = ''
                
                if 'year' in filename:
                    current_img = Image.open(os.path.join(ixp_directory, filename))

                    axes = crop_axes(test_ixp, current_img)
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
                    
                    x_axis_chars = ident_chars(x_axis, scale_factor, 'x', filter_type)
                    y_axis_chars = ident_chars(y_axis, scale_factor, 'y', filter_type)
                    
                    x_chars = process_chars(x_axis_chars[0], x_axis_chars[1])
                    y_chars = process_chars(y_axis_chars[0], y_axis_chars[1])
                    #x_axis.show()
                    #y_axis.show()
                    scaled_x = map_boxes(x_chars, scale_factor, x_axis_chars[3], left_x_axis, top_x_axis, 'x')
                    scaled_y = map_boxes(y_chars, scale_factor, y_axis_chars[3], left_y_axis, top_y_axis, 'y')

                    colors = process_heights(current_img, removable_key)
                    scaled_y_vals = map_y_values(colors, scaled_y)
                    
                    fig,axes = plt.subplots(figsize=(15,7))
                    
                    '''
                    if 'day' in filename:
                        day_scaled_x_vals = map_x_values_day(scaled_y_vals, scaled_x, start_date_time)
                        plt.plot(day_scaled_x_vals[main_color]['raw dates'], day_scaled_x_vals[main_color]['y values'], linewidth = 1)
                        plt.ylabel('Incoming traffic in ' + day_scaled_x_vals[main_color]['unit'] + 'bits per second')
                        axes.set_ylim(bottom=0)
                        axes.grid()
                        if '2day' in filename:
                            plt.savefig(str(start_date) + ' ' + test_ixp + ' ' + '2days' + '.pdf')
                        else:
                            plt.savefig(str(start_date) + ' ' + test_ixp + ' ' + 'day' + '.pdf')
                    
                    elif 'week' in filename:
                        week_scaled_x_vals = map_x_values_week(scaled_y_vals, scaled_x, start_date_time)
                        plt.plot(week_scaled_x_vals[main_color]['raw dates'], week_scaled_x_vals[main_color]['y values'], linewidth = 1)
                        plt.ylabel('Incoming traffic in ' + week_scaled_x_vals[main_color]['unit'] + 'bits per second')
                        axes.set_ylim(bottom=0)
                        axes.grid()
                        plt.savefig(str(start_date) + ' ' + test_ixp + ' ' + 'week' + '.pdf')
                        
                    elif 'month' in filename:
                        month_scaled_x_vals = map_x_values_month(scaled_y_vals, scaled_x, start_date_time, ixp_type)
                        plt.plot(month_scaled_x_vals[main_color]['raw dates'], month_scaled_x_vals[main_color]['y values'], linewidth = 1)
                        plt.ylabel('Incoming traffic in ' + month_scaled_x_vals[main_color]['unit'] + 'bits per second')
                        axes.set_ylim(bottom=0)
                        axes.grid()
                        plt.savefig(str(start_date) + ' ' + test_ixp + ' ' + 'month' + '.pdf')
                    '''  
                    if 'year' in filename:
                        mpl.rcParams.update({'font.size': 10})
                        year_scaled_x_vals = map_x_values_year(scaled_y_vals, scaled_x, start_date_time)
                        plt.plot(year_scaled_x_vals[main_color]['raw dates'], year_scaled_x_vals[main_color]['y values'], linewidth = 1)
                        plt.ylabel('Incoming traffic in ' + year_scaled_x_vals[main_color]['unit'] + 'bits per second')
                        axes.set_ylim(bottom=0)
                        axes.grid()

                        if '2year' in filename:
                            all_dict[test_ixp][str(start_date)]['2year'] = {}
                            all_dict[test_ixp][str(start_date)]['2year'] = {}
                            all_dict[test_ixp][str(start_date)]['2year']['values'] = year_scaled_x_vals[main_color]['y values']
                            all_dict[test_ixp][str(start_date)]['2year']['dates'] = year_scaled_x_vals[main_color]['string dates']
                            plt.title(test_ixp + ' - Incoming traffic for last 2 years')
                            
                            #plt.savefig(str(start_date) + ' ' + test_ixp + ' ' + '2years' + '.png')
                            #plt.savefig(str(start_date) + ' ' + test_ixp + ' ' + '2years' + '.pdf')
                        else:
                            all_dict[test_ixp][str(start_date)]['year'] = {}
                            all_dict[test_ixp][str(start_date)]['year'] = {}
                            all_dict[test_ixp][str(start_date)]['year']['values'] = year_scaled_x_vals[main_color]['y values']
                            all_dict[test_ixp][str(start_date)]['year']['dates'] = year_scaled_x_vals[main_color]['string dates']
                            test = find_peak_ranges(all_dict[test_ixp][str(start_date)]['year']['values'])
                            start_1, end_1 = test[0]
                            start_2, end_2 = test[1]
                            start_3, end_3 = test[2]
                            plt.axvspan(year_scaled_x_vals[main_color]['raw dates'][start_1 - 1], year_scaled_x_vals[main_color]['raw dates'][end_1 - 1], facecolor='r', alpha = 0.5, zorder=-100)
                            plt.axvspan(year_scaled_x_vals[main_color]['raw dates'][start_2 - 1], year_scaled_x_vals[main_color]['raw dates'][end_2 - 1], facecolor='g', alpha = 0.5, zorder=-100)
                            plt.axvspan(year_scaled_x_vals[main_color]['raw dates'][start_3 - 1], year_scaled_x_vals[main_color]['raw dates'][end_3 - 1], facecolor='b', alpha = 0.5, zorder=-100)
                            plt.title(test_ixp + ' - Incoming traffic for last year')
                            
                            #plt.savefig(str(start_date) + ' ' + test_ixp + ' ' + 'year' + '.png')
                            #plt.savefig(str(start_date) + ' ' + test_ixp + ' ' + 'year' + '.pdf')

                    #plt.cla()
                    #plt.close()     
                    
        start_day += 1
        
        if start_day == 12 or start_day == 28:
            start_day += 1
        elif start_day == 2:
            break