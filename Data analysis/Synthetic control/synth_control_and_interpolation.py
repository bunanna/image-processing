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
from tslib.src.synthcontrol.syntheticControl import RobustSyntheticControl

#import plot_image_processing
#import data_stitching





'''
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
    result = algo.predict(pen=1)
    breakpoint_amt = len(result)
    #rpt.display(throughput_numpy, result, figsize=(10, 6))
    
    start_index_in_result = 0
    end_index_in_result = 1
    start_index = 0
    end_index = 0
    count = 0
    breakpoint_avg_list = []
    avg_index_list = []
    
    for date in date_numpy:
        if date.year == 2020 and date.month == 3:
            interv_index = count
            break
        count += 1;
        
    before_interv = throughput_numpy[0:interv_index]
    after_interv = throughput_numpy[interv_index:]
    
    last_year_mean = np.mean(before_interv)
    last_year_std = np.std(before_interv)
    
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
    
    return indices[len(indices)-3:len(indices)], last_year_mean, last_year_std, maximum

def divide_by_date(processed_x_values, processed_y_values, ixp):
    date_numpy = np.array(processed_x_values)
    throughput_numpy = np.array(processed_y_values)
    count = 0
    
    for date in date_numpy:
        if date.year == 2020 and date.month == 3:
            interv_index = count
            break
        count += 1;
    
    before_interv_date = date_numpy[0:interv_index]
    before_interv = throughput_numpy[0:interv_index]
    
    after_interv_date = date_numpy[interv_index:]
    after_interv = throughput_numpy[interv_index:]
    
    df_before_interv = pd.DataFrame({ixp: before_interv})
    df_after_interv = pd.DataFrame({ixp: after_interv})
    
    df_before_interv_dates = pd.DataFrame({ixp: before_interv_date})
    df_after_interv_dates = pd.DataFrame({ixp: after_interv_date})
    
    return df_before_interv, df_after_interv, before_interv, after_interv, df_before_interv_dates, df_after_interv_dates, before_interv_date, after_interv_date

def synthetic_control(before_interv_data, after_interv_data, after_interv_dates, before_interv_dates, selected_ixp, other_ixps):
    singvals = 4
    trainDF = pd.DataFrame(data=before_interv_data)
    testDF = pd.DataFrame(data=after_interv_data[other_ixps])
    rscModel = RobustSyntheticControl(selected_ixp, singvals, len(trainDF), probObservation=1.0, modelType='svd', svdMethod='numpy', otherSeriesKeysArray=other_ixps)
    rscModel.fit(trainDF)
    denoisedDF = rscModel.model.denoisedDF()
    print(rscModel.model.weights)
    
    predictions = []
    predictions = np.dot(testDF[other_ixps], rscModel.model.weights)
    model_fit = np.dot(trainDF[other_ixps][:], rscModel.model.weights)

    plt.plot(after_interv_dates, predictions, color = 'red', label = "counterfactual", linewidth = 1)
    plt.plot(before_interv_dates, model_fit, color = 'green', label = "fitted model", linewidth = 1)


def nan_fill(compare_dates, base_dates, base_vals):
    
    fixed_array = np.empty(compare_dates.shape)
    fixed_array[:] = np.NaN
    
    base_val_index = 0
    fixed_array_index = 0
    find_date_index = 0
    crop_index = 0
    
    if (compare_dates[0].month > base_dates[0].month and compare_dates[0].year == base_dates[0].year) or compare_dates[0].year > base_dates[0].year or (compare_dates[0].day > base_dates[0].day and compare_dates[0].month == base_dates[0].month and compare_dates[0].year == base_dates[0].year):
        
        for date in base_dates:
            if date.year == compare_dates[0].year and date.month == compare_dates[0].month and date.day == compare_dates[0].day:
                crop_index = find_date_index
                break
            find_date_index += 1
            
        base_dates_modify = base_dates[crop_index:]
        base_vals_modify = base_vals[crop_index:]
            
    else:
        base_dates_modify = np.copy(base_dates)
        base_vals_modify = np.copy(base_vals)
    
    for base_date in base_dates_modify:
        fixed_array_index = 0
        for compare_date in compare_dates:
            if compare_date.year == base_date.year and compare_date.month == base_date.month and compare_date.day == base_date.day:
                if np.isnan(fixed_array[fixed_array_index]):
                    fixed_array[fixed_array_index] = base_vals_modify[base_val_index]
                    break
            fixed_array_index += 1
        base_val_index += 1
            
    return fixed_array, base_dates_modify, base_vals_modify
'''
def plot_data(filename, ixp, scaled_y_vals, scaled_x, start_date_time, start_date, main_color, ixp_type):
    
    data_dict = {}
    data_dict[ixp] = {}
    data_dict[ixp][str(start_date)] = {}
    
    if 'day' in filename:
        scaled_x_vals = plot_image_processing.map_x_values_day(scaled_y_vals, scaled_x, start_date_time, ixp)
        dict_string = 'day'
        title_string = ' - Incoming traffic for last day'
        file_string = 'day'
    
    elif 'week' in filename:
        scaled_x_vals = plot_image_processing.map_x_values_week(scaled_y_vals, scaled_x, start_date_time, ixp)
        dict_string = 'week'
        title_string = ' - Incoming traffic for last week'
        file_string = 'week'
        
    elif 'month' in filename:
        scaled_x_vals = plot_image_processing.map_x_values_month(scaled_y_vals, scaled_x, start_date_time, ixp_type, ixp)
        dict_string = 'month'
        title_string = ' - Incoming traffic for last month'
        file_string = 'month'

    data_dict[ixp][str(start_date)][dict_string] = {}
    
    data_dict[ixp][str(start_date)][dict_string]['values'] = scaled_x_vals[main_color]['y values']
    data_dict[ixp][str(start_date)][dict_string]['dates'] = scaled_x_vals[main_color]['string dates']
    data_dict[ixp][str(start_date)][dict_string]['raw dates'] = scaled_x_vals[main_color]['raw dates']
    
    return data_dict

def plot_data_year(filename, ixp, scaled_y_vals, scaled_x, start_date_time, start_date, main_color):
    
    data_dict = {}
    data_dict[ixp] = {}
    data_dict[ixp][str(start_date)] = {}
    
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
    
    data_dict[ixp][str(start_date)][dict_string] = {}
    
    data_dict[ixp][str(start_date)][dict_string]['values'] = scaled_x_vals[main_color]['y values']
    data_dict[ixp][str(start_date)][dict_string]['dates'] = scaled_x_vals[main_color]['string dates']
    data_dict[ixp][str(start_date)][dict_string]['raw dates'] = scaled_x_vals[main_color]['raw dates']
    
    #plt.axvline(x = datetime.datetime(2020, 3, 1), color = 'black')
    
    #get_standard = find_peak_ranges(scaled_x_vals[main_color]['raw dates'], data_dict[ixp][str(start_date)][dict_string]['values'], ixp)
    
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
    #plt.title(ixp + title_string)
    
    
    #plt.savefig(str(start_date) + ' ' + ixp + ' ' + file_string + ' peaks' + '.png', bbox_inches = 'tight')
    #plt.savefig(str(start_date) + ' ' + ixp + ' ' + file_string + ' peaks' + '.pdf', bbox_inches = 'tight')
    
    #plt.savefig(str(start_date) + ' ' + ixp + ' ' + file_string + '.png')
    #plt.savefig(str(start_date) + ' ' + ixp + ' ' + file_string + '.pdf')

    #plt.cla()
    #plt.close()
    
    return data_dict
'''      
def process_dataframes(stitched_dict, selected_ixp):
    ixp_count = 0
    test_list_before_interv = []
    test_list_after_interv = []
    
    ixps = list(stitched_dict.keys())

    for ixp in ixps:
        types = list(stitched_dict[ixp].keys())
        
        if 'year' in types:
            all_dates = stitched_dict[ixp]['year']['dates']
            all_vals = stitched_dict[ixp]['year']['values']
            
            get_dataframes = divide_by_date(all_dates, all_vals, ixp)
            
            if ixp == selected_ixp and ixp_count == 0:
                new_scaled_x = get_dataframes[7]
            
            if selected_ixp == ixp:
                df_selected_before_interv = get_dataframes[0]
                df_selected_after_interv = get_dataframes[1]
                
                selected_before_vals = get_dataframes[2]
                selected_after_vals = get_dataframes[3]
                
                df_selected_before_dates = get_dataframes[4]
                df_selected_after_dates = get_dataframes[5]
                
                selected_before_dates = get_dataframes[6]
                selected_after_dates = get_dataframes[7]
                
            else:
                df_new_before_interv = get_dataframes[0]
                df_new_after_interv = get_dataframes[1]
                
                new_before_vals = get_dataframes[2]
                new_after_vals = get_dataframes[3]
                
                df_new_before_dates = get_dataframes[4]
                df_new_after_dates = get_dataframes[5]
                
                new_before_dates = get_dataframes[6]
                new_after_dates = get_dataframes[7]
                
            if ixp_count > 0:
                nan_filler_before = nan_fill(selected_before_dates, new_before_dates, new_before_vals)
                nan_filler_after = nan_fill(selected_after_dates, new_after_dates, new_after_vals)
                
                df_new_before_interv = pd.DataFrame({ixp: nan_filler_before[0]})
                df_new_after_interv = pd.DataFrame({ixp: nan_filler_after[0]})
                
                df_new_before_dates = pd.DataFrame({ixp: nan_filler_before[1]})
                df_new_after_dates = pd.DataFrame({ixp: nan_filler_after[1]})
                
            if ixp_count == 0:

                result_before_interv = df_selected_before_interv
                result_after_interv = df_selected_after_interv
                
                result_dates_before_interv = df_selected_before_dates
                result_dates_after_interv = df_selected_after_dates
                
            elif ixp_count > 0:
                            
                result_before_interv = pd.concat([result_before_interv, 
                                                  df_new_before_interv],
                                                  axis=1, sort=False)
                    
                result_after_interv = pd.concat([result_after_interv, 
                                                 df_new_after_interv],
                                                 axis=1, sort=False)
                    
                result_dates_before_interv = pd.concat([result_dates_before_interv, 
                                                        df_new_before_dates],
                                                        axis=1, sort=False)
                
                result_dates_after_interv = pd.concat([result_dates_after_interv, 
                                                       df_new_after_dates],
                                                       axis=1, sort=False)
                

        ixp_count += 1
        
    return result_before_interv, result_after_interv, new_scaled_x, selected_before_dates, result_dates_before_interv, result_dates_after_interv, ixps, selected_ixp

def apply_synthetic_control(stitched_dict, selected_ixp):

    data = process_dataframes(stitched_dict, selected_ixp)
    ixps = data[6]
    selected_ixp = data[7]
    
    interpolate_before_interv = data[0].interpolate(method='linear')
    interpolate_after_interv = data[1].interpolate(method='linear')

    new_ixp_list = ixps.copy()
    new_ixp_list.remove(selected_ixp)

    synthetic_control(interpolate_before_interv, interpolate_after_interv, data[2], data[3], selected_ixp, new_ixp_list)
'''   
if __name__ == "__main__":
    selected_ixp = 'DE-CIX Munich'
    start_year = 2020
    start_month = 8
    start_day = 5
    
    end_year = 2020
    end_month = 8
    end_day = 6
    
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
    
    data = data_stitching.get_data(selected_ixp, start_year, start_month, start_day, all_ixps, end_day, end_month, end_year)
    
    stitched_dict = data_stitching.stitched_data_to_dict(data)
    
    dataframes = process_dataframes(stitched_dict, selected_ixp)
    
    apply_synthetic_control(stitched_dict, selected_ixp)
    