# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 17:29:03 2020

@author: Brianna Barrow (bmb2193)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
import pandas as pd
import ruptures as rpt
from tslib.src import tsUtils
from tslib.src.synthcontrol.syntheticControl import RobustSyntheticControl
from tslib.tests import testdata

import plot_image_processing

def find_peak_ranges(processed_x_values, processed_y_values, ixp):
    '''
    Uses ruptures to find breakpoints (areas where the series of data changes
    suddenly) and highlight regions of interest.

    Args:
        processed_y_values: A dictionary mapping colors to the x and y values 
        of their pixels in actual units.

    Returns: The three regions of interest with the highest averages.

    '''
    date_numpy = np.array(processed_x_values)
    throughput_numpy = np.array(processed_y_values)
    maximum = np.max(throughput_numpy)
    
    print("Currently processing " + ixp)
    algo = rpt.Pelt(model='rbf').fit(throughput_numpy)
    result = algo.predict(pen=5)
    breakpoint_amt = len(result)
    #rpt.display(throughput_numpy, result, figsize=(10, 6))
    
    start_index_in_result = 0
    end_index_in_result = 1
    start_index = 0
    end_index = 0
    count = 0
    january_index = 0
    breakpoint_avg_list = []
    avg_index_list = []
    
    for date in date_numpy:
        if date.year == 2020 and date.month == 1:
            january_index = count
            break
        count += 1;
    
    before_stretch = 1
    after_stretch = 1
        
    before_january_old = throughput_numpy[0:january_index]
    before_january_date = date_numpy[0:january_index]
    before_january = np.repeat(before_january_old,before_stretch, axis=0)
    
    after_january_old = throughput_numpy[january_index:]
    after_january_date = date_numpy[january_index:]
    after_january = np.repeat(after_january_old,after_stretch, axis=0) 
    
    last_year_mean = np.mean(before_january)
    last_year_std = np.std(before_january)
    
    df_before_january = pd.DataFrame({ixp: before_january})
    df_after_january = pd.DataFrame({ixp: after_january})
    
    while end_index_in_result < breakpoint_amt:
        start_index = result[start_index_in_result]
        end_index = result[end_index_in_result]
        new_numpy = throughput_numpy[start_index:end_index]
        
        if np.mean(new_numpy) > last_year_mean + 1*(last_year_std):
            breakpoint_avg_list.append(int(np.mean(new_numpy)))
            
            avg_index_list.append((start_index, end_index))
        start_index_in_result += 1
        end_index_in_result += 1
        
    list_to_sort = zip(breakpoint_avg_list, avg_index_list)
    sorted_list = sorted(list_to_sort)
    tuples = zip(*sorted_list)
    
    avg, indices = [list(tuple) for tuple in tuples]
    
    return indices[len(indices)-3:len(indices)], last_year_mean, last_year_std, maximum, df_before_january, df_after_january, after_january_date, before_january_date, before_january_old, after_january_old

def synthetic_control(before_january_data, after_january_data, after_january_dates, before_january_dates, selected_ixp, other_ixps):
    singvals = 4
    trainDF = pd.DataFrame(data=before_january_data)
    testDF = pd.DataFrame(data=after_january_data[other_ixps])
    rscModel = RobustSyntheticControl(selected_ixp, singvals, len(trainDF), probObservation=1.0, modelType='svd', svdMethod='numpy', otherSeriesKeysArray=other_ixps)
    rscModel.fit(trainDF)
    denoisedDF = rscModel.model.denoisedDF()
    print(rscModel.model.weights)
    
    predictions = []
    predictions = np.dot(testDF[other_ixps], rscModel.model.weights)
    model_fit = np.dot(trainDF[other_ixps][:], rscModel.model.weights)
    
    plt.plot(after_january_dates, predictions, color = 'red', label = "counterfactual", linewidth = 1)
    plt.plot(before_january_dates, model_fit, color = 'green', label = "fitted model", linewidth = 1)
    
def plot_data(filename, ixp, scaled_y_vals, scaled_x, start_date_time, start_date, main_color, ixp_type):
    
    data_dict = {}
    data_dict[ixp] = {}
    data_dict[ixp][str(start_date)] = {}
    
    if 'day' in filename:
        scaled_x_vals = plot_image_processing.map_x_values_day(scaled_y_vals, scaled_x, start_date_time)
        dict_string = 'day'
        title_string = ' - Incoming traffic for last day'
        file_string = 'day'
    
    elif 'week' in filename:
        scaled_x_vals = plot_image_processing.map_x_values_week(scaled_y_vals, scaled_x, start_date_time)
        dict_string = 'week'
        title_string = ' - Incoming traffic for last week'
        file_string = 'week'
        
    elif 'month' in filename:
        scaled_x_vals = plot_image_processing.map_x_values_month(scaled_y_vals, scaled_x, start_date_time, ixp_type)
        dict_string = 'month'
        title_string = ' - Incoming traffic for last month'
        file_string = 'month'
      
    elif 'year' in filename:
        mpl.rcParams.update({'font.size': 10})
        if '5year' in filename and 'Frankfurt' in ixp:
            dict_string = '5year'
            title_string = ' - Incoming traffic for last 5 years'
            file_string = '5years'
            scaled_x_vals = plot_image_processing.map_x_values_year(scaled_y_vals, scaled_x, start_date_time, True, ixp, dict_string)
        elif 'twoyear' in filename and 'Netnod' in ixp:
            dict_string = '2year'
            title_string = ' - Incoming traffic for last 2 years'
            file_string = '2years'
            scaled_x_vals = plot_image_processing.map_x_values_year(scaled_y_vals, scaled_x, start_date_time, False, ixp, dict_string)
        else:
            if '5year' in filename:
                dict_string = '5year'
                title_string = ' - Incoming traffic for last 5 years'
                file_string = '5years'
            elif 'twoyear' in filename:
                dict_string = '2year'
                title_string = ' - Incoming traffic for last 2 years'
                file_string = '2years'
            elif '2year' in filename:
                dict_string = '2year'
                title_string = ' - Incoming traffic for last 2 years'
                file_string = '2years'
            elif 'year' in filename:
                dict_string = 'year'
                title_string = ' - Incoming traffic for last year'
                file_string = 'year'
            scaled_x_vals = plot_image_processing.map_x_values_year(scaled_y_vals, scaled_x, start_date_time, False, ixp, dict_string)
        
    plt.plot(scaled_x_vals[main_color]['raw dates'], scaled_x_vals[main_color]['y values'], linewidth = 1, label = 'actual')
    plt.ylabel('Incoming traffic in ' + scaled_x_vals[main_color]['unit'] + 'bits per second')

    data_dict[ixp][str(start_date)][dict_string] = {}
    data_dict[ixp][str(start_date)][dict_string] = {}
    data_dict[ixp][str(start_date)][dict_string]['values'] = scaled_x_vals[main_color]['y values']
    data_dict[ixp][str(start_date)][dict_string]['dates'] = scaled_x_vals[main_color]['string dates']
    
    get_standard = find_peak_ranges(scaled_x_vals[main_color]['raw dates'], data_dict[ixp][str(start_date)][dict_string]['values'], ixp)
    
    plt.axvline(x = datetime.datetime(2020, 1, 1), color = 'black')

    '''
    test = get_standard[0]
    
    start_1, end_1 = test[len(test) - 1]
    plt.axvspan(scaled_x_vals[main_color]['raw dates'][start_1 - 1], scaled_x_vals[main_color]['raw dates'][end_1 - 1], facecolor='r', alpha = 0.5, zorder=-100)
    
    axes.text(0, -0.1, "Red peak date range: " + data_dict[ixp][str(start_date)][dict_string]['dates'][start_1 - 1][0:10] + " to " + data_dict[ixp][str(start_date)][dict_string]['dates'][end_1 - 1][0:10], transform=axes.transAxes, fontsize=10, verticalalignment='top')
    
    if len(test) == 2:
        start_2, end_2 = test[len(test) - 2]
        plt.axvspan(scaled_x_vals[main_color]['raw dates'][start_2 - 1], scaled_x_vals[main_color]['raw dates'][end_2 - 1], facecolor='y', alpha = 0.5, zorder=-100)
        axes.text(0, -0.2, "Yellow peak date range: " + data_dict[ixp][str(start_date)][dict_string]['dates'][start_2 - 1][0:10] + " to " + data_dict[ixp][str(start_date)][dict_string]['dates'][end_2 - 1][0:10], transform=axes.transAxes, fontsize=10, verticalalignment='top')
        
    elif len(test) == 3:
        start_2, end_2 = test[len(test) - 2]
        plt.axvspan(scaled_x_vals[main_color]['raw dates'][start_2 - 1], scaled_x_vals[main_color]['raw dates'][end_2 - 1], facecolor='y', alpha = 0.5, zorder=-100)
        
        start_3, end_3 = test[len(test) - 3]
        plt.axvspan(scaled_x_vals[main_color]['raw dates'][start_3 - 1], scaled_x_vals[main_color]['raw dates'][end_3 - 1], facecolor='b', alpha = 0.5, zorder=-100)
        
        axes.text(0, -0.2, "Yellow peak date range: " + data_dict[ixp][str(start_date)][dict_string]['dates'][start_2 - 1][0:10] + " to " + data_dict[ixp][str(start_date)][dict_string]['dates'][end_2 - 1][0:10], transform=axes.transAxes, fontsize=10, verticalalignment='top')
        axes.text(0, -0.3, "Blue peak date range: " + data_dict[ixp][str(start_date)][dict_string]['dates'][start_3 - 1][0:10] + " to " + data_dict[ixp][str(start_date)][dict_string]['dates'][end_3 - 1][0:10], transform=axes.transAxes, fontsize=10, verticalalignment='top')
        
    axes.text(0, -0.5, "Maximum value of throughput is: " + str(get_standard[3]), transform=axes.transAxes, fontsize=10, verticalalignment='top')
    
    plt.axhline(y = get_standard[1], color = 'blue', zorder=-50)
    axes.text(0, -0.6, "Pre-January plot mean (blue line): " + str(get_standard[1]), transform=axes.transAxes, fontsize=10, verticalalignment='top')
    plt.axhline(y = get_standard[1] + get_standard[2], color = 'purple', zorder=-50)
    axes.text(0, -0.7, "Standard deviation (one per line above mean): " + str(get_standard[2]), transform=axes.transAxes, fontsize=10, verticalalignment='top')
    plt.axhline(y = get_standard[1] + get_standard[2]*2, color = 'green', zorder=-50)
    plt.axhline(y = get_standard[1] + get_standard[2]*3, color = 'red', zorder=-50)
    
    '''
    plt.title(ixp + title_string)
    
    
    #plt.savefig(str(start_date) + ' ' + ixp + ' ' + file_string + ' peaks' + '.png', bbox_inches = 'tight')
    #plt.savefig(str(start_date) + ' ' + ixp + ' ' + file_string + ' peaks' + '.pdf', bbox_inches = 'tight')
    
    #plt.savefig(str(start_date) + ' ' + ixp + ' ' + file_string + '.png')
    #plt.savefig(str(start_date) + ' ' + ixp + ' ' + file_string + '.pdf')

    #plt.cla()
    #plt.close()
    
    return data_dict, get_standard[4], get_standard[5], get_standard[6], get_standard[7], get_standard[8], get_standard[9]

def nan_fill(high_sampled_dates, low_sampled_dates, low_sampled_vals):

    low_sampled_index = 0
    fixed_array_index = 0
    find_date_index = 0
    crop_index = 0

    fixed_array = np.empty(high_sampled_dates.shape)
    fixed_array[:] = np.NaN
    
    if (high_sampled_dates[0].month > low_sampled_dates[0].month and high_sampled_dates[0].year == low_sampled_dates[0].year) or high_sampled_dates[0].year > low_sampled_dates[0].year:
        
        for date in low_sampled_dates:
            if date.year == high_sampled_dates[low_sampled_index].year and date.month == high_sampled_dates[low_sampled_index].month and date.day == high_sampled_dates[low_sampled_index].day:
                crop_index = find_date_index
                break
            find_date_index += 1
            
        low_sampled_modify = low_sampled_dates[crop_index:]
        low_sampled_vals_modify = low_sampled_vals[crop_index:]
            
    else:
        low_sampled_modify = np.copy(low_sampled_dates)
        low_sampled_vals_modify = np.copy(low_sampled_vals)
    
    for date in high_sampled_dates:
        if low_sampled_index < low_sampled_modify.size:
            if date.year == low_sampled_modify[low_sampled_index].year and date.month == low_sampled_modify[low_sampled_index].month and date.day == low_sampled_modify[low_sampled_index].day:
                fixed_array[fixed_array_index] = low_sampled_vals_modify[low_sampled_index]
                low_sampled_index += 1
        fixed_array_index += 1
        
    return fixed_array, low_sampled_modify