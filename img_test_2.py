# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 17:29:03 2020

@author: brian
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
from skimage import io
mpl.rcParams['figure.dpi'] = 300
current_img = 'day.png'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


'''
from: https://stackoverflow.com/a/33507138
'''
def remove_alpha_channel(img):
    png = Image.open(img).convert('RGBA')
    background = Image.new('RGBA', png.size, (255,255,255))
    alpha_composite = Image.alpha_composite(background, png)
    alpha_composite.convert('RGB')

    return alpha_composite    

def get_top_colors(img):
    color_count = 3
    index = 0
    process_list = []
    color_list = []

    im = Image.open(img)
    channels = list(im.getbands())

    if 'A' in channels:
        im = remove_alpha_channel(img)

    quantized_im = im.quantize(colors=color_count,method=2)
    new_quantized_im = quantized_im.convert('RGB')
    top_color_list = quantized_im.getpalette()[:(color_count * 3)]

    for entry in top_color_list:
        process_list.append(entry)

        if index != 2:
            index+=1
        else:
            color_list.append(tuple(process_list))
            process_list = []
            index = 0

    return color_list, new_quantized_im, im

def ident_chars(img):
    scale_factor = 2
    tolerance = 5
    im = get_top_colors(img)[2]
    constructed_num = []
    reconstructed_nums = {}
    index = 0
    thresh = 200
    fn = lambda x : 255 if x > thresh else 0
    
    enhanced_im = im.resize((im.size[0]*scale_factor, im.size[1]*scale_factor)).convert('L').point(fn, mode='1')#.filter(ImageFilter.ModeFilter(3))
    
    text = pytesseract.image_to_string(enhanced_im).splitlines()
    text_num = pytesseract.image_to_string(enhanced_im, config='digits').splitlines()
    box = pytesseract.image_to_boxes(enhanced_im).splitlines()
    box_num = pytesseract.image_to_boxes(enhanced_im, config='digits').splitlines()
    
    '''
    for string in box_num:
        current_box_list = string.split()
        
        if index == 0:
            current_number_str = current_box_list[0]
            top_left_corner_x = int(current_box_list[1])
            top_left_corner_y = int(current_box_list[2])
            bottom_right_corner_x = int(current_box_list[3])
            bottom_right_corner_y = int(current_box_list[4])
            constructed_num.append(current_number_str)
        
        else:
            
            prev_top_left_corner_x = top_left_corner_x
            prev_top_left_corner_y = top_left_corner_y
            prev_bottom_right_corner_x = bottom_right_corner_x
            prev_bottom_right_corner_y = bottom_right_corner_y
            
            current_number_str = current_box_list[0]
            top_left_corner_x = int(current_box_list[1])
            top_left_corner_y = int(current_box_list[2])
            bottom_right_corner_x = int(current_box_list[3])
            bottom_right_corner_y = int(current_box_list[4])
            
            if top_left_corner_y in range(prev_top_left_corner_y - tolerance, prev_top_left_corner_y + tolerance):
                constructed_num.append(current_number_str)
            else:
                new_num = ''.join(constructed_num)
                reconstructed_nums[new_num] = ((bottom_right_corner_y - top_left_corner_y) // (2*scale_factor)) + (top_left_corner_y // scale_factor)
                constructed_num = []
                constructed_num.append(current_number_str)
                index = 0
                    
        index += 1
            
    return reconstructed_nums
    '''    
    
    return scale_factor, text, text_num, box, box_num, enhanced_im


def get_heights(img):
    color_dict = {}
    res = get_top_colors(img)
    top_colors = res[0]
    quantized_im = res[1]
    original_im = Image.open(img, 'r')
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

def process_heights(img):
    color_info = get_heights(img)
    color_dict = color_info[0]
    top_colors = color_info[1]
    new_color_dict = {}
    
    for color_tuple in top_colors:
        index = 0
        current_dict = color_dict[color_tuple]
        x_val_list = current_dict['x values high']
        
        for value in x_val_list:
            if index != 0 and x_val_list[index] != x_val_list[index - 1] + 1:
                break
            else:
                index += 1
                
        new_color_dict[color_tuple] = {
            'x values high': current_dict['x values high'][index:],
            'x values low': current_dict['x values low'][index:],
            'all highs': current_dict['all highs'][index:] ,
            'all lows': current_dict['all lows'][index:]
        }
            
    return new_color_dict
