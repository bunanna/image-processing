# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 01:36:21 2021

@author: User
"""
import os
import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
import copy
import sklearn

from tslib.src import tsUtils
from tslib.src.synthcontrol.syntheticControl import RobustSyntheticControl

'''
IXPs that we have data for.
'''

ixps = ['angonix',
        'ANIX - Albanian Neutral Internet eXchange',
        'BALT-IX',
        'BCIX',
        'DE-CIX Dallas',
        'DE-CIX Dusseldorf',
        'DE-CIX Frankfurt',
        'DE-CIX Hamburg',
        'DE-CIX Istanbul',
        'DE-CIX Madrid',
        'DE-CIX Marseille',
        'DE-CIX Munich', 
        'DE-CIX New York',
        'DE-CIX Palermo',
        'GrenoblIX',
        'Hopus',
        'IIX-Bali',
        'IIX-Jogja',
        'IX.br (PTT.br) Belém',
        'IX.br (PTT.br) Belo Horizonte',
        'IX.br (PTT.br) Brasília',
        'IX.br (PTT.br) Campina Grande',
        'IX.br (PTT.br) Campinas',
        'IX.br (PTT.br) Campo Grande',
        'IX.br (PTT.br) Cascavel',
        'IX.br (PTT.br) Caxias do Sul',
        'IX.br (PTT.br) Cuiabá',
        'IX.br (PTT.br) Florianópolis',
        'IX.br (PTT.br) Fortaleza',
        'IX.br (PTT.br) Foz do Iguaçu',
        'IX.br (PTT.br) Goiânia',
        'IX.br (PTT.br) João Pessoa',
        'IX.br (PTT.br) Lajeado',
        'IX.br (PTT.br) Londrina',
        'IX.br (PTT.br) Maceió',
        'IX.br (PTT.br) Manaus',
        'IX.br (PTT.br) Maringá',
        'IX.br (PTT.br) Natal',
        'IX.br (PTT.br) Porto Alegre',
        'IX.br (PTT.br) Recife',
        'IX.br (PTT.br) Rio de Janeiro',
        'IX.br (PTT.br) Salvador',
        'IX.br (PTT.br) Santa Maria',
        'IX.br (PTT.br) São José do Rio Preto',
        'IX.br (PTT.br) São José dos Campos',
        'IX.br (PTT.br) São Luís',
        'IX.br (PTT.br) São Paulo',
        'IX.br (PTT.br) Teresina',
        'IX.br (PTT.br) Vitória',
        'IXPN Lagos',
        'JPNAP Osaka',
        'JPNAP Tokyo',
        'LONAP',
        'MASS-IX',
        'MIX-IT',
        'Netnod Copenhagen',
        'Netnod Gothenburg',
        'Netnod Lulea',
        'Netnod Stockholm',
        'Netnod Sundsvall',
        'SAIX',
        'TahoeIX'
        'TorIX',
        'YYCIX']

one_day_average_ixps = ['angonix',
                        'GrenoblIX',
                        'IIX-Bali',
                        'IIX-Jogja',
                        'IX.br (PTT.br) Belém',
                        'IX.br (PTT.br) Belo Horizonte',
                        'IX.br (PTT.br) Brasília',
                        'IX.br (PTT.br) Campinas',
                        'IX.br (PTT.br) Caxias do Sul',
                        'IX.br (PTT.br) Cuiabá',
                        'IX.br (PTT.br) Florianópolis',
                        'IX.br (PTT.br) Fortaleza',
                        'IX.br (PTT.br) Foz do Iguaçu',
                        'IX.br (PTT.br) Lajeado',
                        'IX.br (PTT.br) Londrina',
                        'IX.br (PTT.br) Maceió',
                        'IX.br (PTT.br) Maringá',
                        'IX.br (PTT.br) Porto Alegre',
                        'IX.br (PTT.br) Recife',
                        'IX.br (PTT.br) Rio de Janeiro',
                        'IX.br (PTT.br) Salvador',
                        'IX.br (PTT.br) Santa Maria',
                        'IX.br (PTT.br) São José do Rio Preto',
                        'IXPN Lagos',
                        'LONAP',
                        'MASS-IX',
                        'MIX-IT']

column_names = ["Dates", "Values (Gb)"]

def load_data(file_location):
    '''
    Loads the CSV data for each IXP and assembles the data into dictionaries.

    Args:
        file_location: Folder name where the CSV files are located.

    Returns:
        data_dict: The data extracted from the CSV files, with an entry for each IXP.
    '''
    
    current_directory = os.getcwd()
    
    data_dict = {}

    os.chdir(file_location)
    
    for filename in os.listdir(file_location):
        
        for ixp in one_day_average_ixps:
            
            if ixp.replace(' ', '_').replace('é', 'e').replace('á', 'a').replace('í', 'i').replace('ç', 'c').replace('ó', 'o').replace('ã', 'a') in filename:
                data = pandas.read_csv(filename)
                data_dates = data[column_names[0]].tolist()
                data_values = data[column_names[1]].tolist()
                
                data_dict[ixp] = {
                    'dates': data_dates,
                    'values': data_values
                }
                
                continue
            
    os.chdir(current_directory)
    
    keys = list(data_dict.keys())
    
    for key in keys:
        current_date_list = data_dict[key]['dates']
        new_date_list = []
        
        for date in current_date_list:
            new_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            new_date_list.append(new_date)
            
        data_dict[key]['dates'] = new_date_list
    
    return data_dict

def get_latest_start_date_and_crop(ixp_dict):
    '''
    Finds the latest start date among all IXPs in the dictionary and crops the y-value and date list for each IXP so that they start after this latest date.

    Args:
        ixp_dict: The IXP data dictionary generated in load_data.

    Returns:
        ixp_dict: The IXP data dictionary passed as input, modified according to the function description.
    '''
    
    keys = list(ixp_dict.keys())
    latest_date = datetime.date(2000, 1, 1)
    index = 0
    
    for key in keys:
        current_date_list = ixp_dict[key]['dates']
        first_date = current_date_list[0].date()
        
        if first_date > latest_date:
            latest_date = first_date
        
    for key in keys:
        current_date_list = ixp_dict[key]['dates']
        current_val_list = ixp_dict[key]['values']
        new_date_list = []
        new_val_list = []
        index = 0
        
        for date in current_date_list:
            if date.date() == latest_date:
                new_date_list = current_date_list[index:]
                new_val_list = current_val_list[index:]
                break
            index += 1
            
        ixp_dict[key]['dates'] = new_date_list
        ixp_dict[key]['values'] = new_val_list
                
    return ixp_dict

def get_earliest_end_date_and_crop(ixp_dict):
    '''
    Finds the earliest date among all IXPs in the dictionary and crops the y-value and date list for each IXP so that they start after this latest date.

    Args:
        ixp_dict: The IXP data dictionary generated in load_data or get_latest_start_date_and_crop (if operating the two functions in tandem).

    Returns:
        ixp_dict: The IXP data dictionary passed as input, modified according to the function description.
    '''
    
    keys = list(ixp_dict.keys())
    earliest_date = datetime.date(2030, 1, 1)
    index = 0
    
    for key in keys:
        current_date_list = ixp_dict[key]['dates']
        last_date = current_date_list[len(current_date_list) - 1].date()
        
        if last_date < earliest_date:
            earliest_date = last_date
        
    for key in keys:
        current_date_list = ixp_dict[key]['dates']
        current_val_list = ixp_dict[key]['values']
        new_date_list = []
        new_val_list = []
        index = 0
        
        for date in current_date_list:
            if date.date() == earliest_date:
                new_date_list = current_date_list[:index - 1]
                new_val_list = current_val_list[:index - 1]
                break
            index += 1
            
        ixp_dict[key]['dates'] = new_date_list
        ixp_dict[key]['values'] = new_val_list
                
    return ixp_dict

def resample(ixp_dict):
    '''
    Uses the resample function in pandas to generate a dataframe in which all IXP data is synchronized to the same frequency.

    Args:
        ixp_dict: An IXP dictionary in which each IXPs' data starts and ends on the same date.

    Returns:
        final_dataframe: A dataframe containing all of the IXP data matched to the same frequency.
    '''
    
    keys = list(ixp_dict.keys())
    
    new_dict = {
        keys[0]: ixp_dict[keys[0]]['values'],
        'dates': ixp_dict[keys[0]]['dates']
    }
    
    filled_dataframe = pandas.DataFrame.from_dict(new_dict).set_index('dates').resample('D').mean()
    
    for key in keys:
        if key == keys[0]:
            continue
        else:
            new_dict = {
                key: ixp_dict[key]['values'],
                'dates': ixp_dict[key]['dates']
            }
            
            new_dataframe = pandas.DataFrame.from_dict(new_dict).set_index('dates')
            resampled = new_dataframe.resample('D').mean()
            
            filled_dataframe = pandas.concat([filled_dataframe, resampled], axis=1, sort=False)
            
    final_dataframe = filled_dataframe.bfill()
    
    return final_dataframe

def synthetic_control(ixp_dataframe, desired_ixp, start_date, train_end_date, end_date, intervention_day):
    all_ixps = list(np.unique(ixp_dataframe.columns.values))
    all_dates = ixp_dataframe.index
    
    days = np.delete(all_dates, [0])
    all_ixps.remove(desired_ixp)
    other_ixps = all_ixps
    
    sing_vals = 1
    p = 1.0
    
    training_days = []
    for val in range(0, (train_end_date - start_date).days):
        training_days.append(start_date + datetime.timedelta(days = val))
        
    test_days = []
    for val in range(0, (end_date - train_end_date).days):
        test_days.append(train_end_date + datetime.timedelta(days = val))
        
    train_data_master_dict = {}
    train_data_dict = {}
    test_data_dict = {}
    
    for ixp in other_ixps:
        series = ixp_dataframe[ixp]
        train_data_master_dict.update({ixp: series[training_days].values})
        (train_data, p_observation) = tsUtils.randomlyHideValues(copy.deepcopy(train_data_master_dict[ixp]), p)
        train_data_dict.update({ixp: train_data})
        test_data_dict.update({ixp: series[test_days].values})
        
    series = ixp_dataframe[desired_ixp]
    train_data_master_dict.update({desired_ixp: series[training_days].values})
    train_data_dict.update({desired_ixp: series[training_days].values})
    test_data_dict.update({desired_ixp: series[test_days].values})

    train_master_df = pandas.DataFrame(data = train_data_master_dict)
    train_df = pandas.DataFrame(data = train_data_dict)
    test_df = pandas.DataFrame(data = test_data_dict)
    
    rsc_model = RobustSyntheticControl(desired_ixp, sing_vals, len(train_df), probObservation = 1.0,  modelType = 'svd', svdMethod = 'numpy', otherSeriesKeysArray = other_ixps)
    rsc_model.fit(train_df)
    
    denoised_df = rsc_model.model.denoisedDF()
    predictions = rsc_model.predict(test_df)
    
    #days_to_plot = training_days + test_days
    
    #plt.plot(days_to_plot, np.append(train_master_df[desired_ixp], test_df[desired_ixp], axis=0), color = 'red', label = 'observations')
    #plt.plot(days_to_plot, np.append(denoised_df[desired_ixp], predictions, axis = 0), color = 'blue', label = 'synthetic control')
    #plt.axvline(x = intervention_day, linewidth = 1, color = 'black', label = 'Intervention')
    #plt.legend(loc = 'lower left', shadow = True)
    #plt.title(desired_ixp)
    #plt.show()
    
    
    return predictions, test_df[desired_ixp], training_days, test_days, denoised_df[desired_ixp], rsc_model, other_ixps, train_master_df[desired_ixp]

def mean_model(ixp_dataframe, desired_ixp, window_size, start_date, train_end_date, end_date, intervention_day):
    training_days = []
    for val in range(0, (train_end_date - start_date).days):
        training_days.append(start_date + datetime.timedelta(days = val))
        
    test_days = []
    for val in range(0, (end_date - train_end_date).days):
        test_days.append(train_end_date + datetime.timedelta(days = val))
        
    training_values = ixp_dataframe[desired_ixp][training_days].values
    test_values = ixp_dataframe[desired_ixp][test_days].values
    
    all_rates_of_change = []
    for val in range(len(training_values) - 1):
        current_rate_of_change = (training_values[val + 1] - training_values[val]) / ((training_days[val + 1] - training_days[val]).days)
        all_rates_of_change.append(current_rate_of_change)
        
    avg_rate = np.mean(all_rates_of_change)
    
    result_values = []
    limit = len(training_values) // 10
    
    relevant_days = test_days[:limit - 1]
    
    index = 1
    for day in relevant_days:
        new_val = training_values[-1] + (avg_rate * index)
        result_values.append(new_val)
        index += 1;
    
    prediction_values = np.array(result_values)
    
    #days_to_plot = training_days + test_days
    
    #train_and_test = np.append(training_values, test_values, axis = 0)
    #train_and_prediction = np.append(training_values, prediction_values, axis=0)
    
    #plt.plot(days_to_plot, train_and_test, color = 'red', label = 'observations')
    #plt.plot(days_to_plot, train_and_prediction, color = 'green', label = 'linear model')
    #plt.legend(loc = 'lower left', shadow = True)
    #plt.title(desired_ixp)
    #plt.show()
    return prediction_values, test_values, training_days, test_days, training_values, relevant_days, limit - 1
    
if __name__ == "__main__":
    start_date = datetime.datetime(2019, 8, 8, 0, 0, 0)
    intervention_day = datetime.datetime(2019, 10, 31, 0, 0, 0)
    train_end_date = datetime.datetime(2019, 11, 1, 0, 0, 0)
    end_date = datetime.datetime(2019, 12, 31, 0, 0, 0)
    
    folder_name = r'C:\Users\User\Desktop\Research\Data\collated_data_sets_2020-11-30'
    all_dict = load_data(folder_name)
    test_1 = get_latest_start_date_and_crop(all_dict)
    test_2 = get_earliest_end_date_and_crop(test_1)
    df = resample(test_2)
    
    synthetic_control_predictions, synthetic_control_actual, synthetic_control_training_days, synthetic_control_test_days, synthetic_control_denoised_data, synthetic_control_model, synthetic_control_other_ixps, synthetic_control_training_values = synthetic_control(df, 'LONAP', start_date, train_end_date, end_date, intervention_day)
    mean_model_predictions, mean_model_actual, mean_model_training_days, mean_model_test_days, mean_model_training_values, mean_model_relevant_days, crop_length = mean_model(df, 'LONAP', 3, start_date, train_end_date, end_date, intervention_day)
    
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    
    ax[0].barh(synthetic_control_other_ixps, synthetic_control_model.model.weights/np.max(synthetic_control_model.model.weights), color=list('rgbkymc'))
    ax[0].set_title('LONAP Weights')
    
    ax[1].plot(synthetic_control_training_days + synthetic_control_test_days[:crop_length], np.append(synthetic_control_training_values, synthetic_control_predictions[:crop_length]), label = 'synthetic control', linestyle = 'dotted')
    ax[1].plot(mean_model_training_days + mean_model_relevant_days, np.append(mean_model_training_values, mean_model_predictions), label = 'mean model', linestyle = 'dashed')
    ax[1].plot(mean_model_training_days + mean_model_test_days[:crop_length], np.append(mean_model_training_values, mean_model_actual[:crop_length]), label = 'actual')
    ax[1].legend(loc = 'lower left', shadow = True)
    ax[1].axvline(x = intervention_day, linewidth = 1, color = 'black', label = 'intervention')
    ax[1].set_title('LONAP mean model, synthetic control, and actual')
    
    rms_synthetic_control_test = sklearn.metrics.mean_squared_error(synthetic_control_actual[:crop_length], synthetic_control_predictions[:crop_length], squared = False)
    rms_mean_model_test = sklearn.metrics.mean_squared_error(mean_model_actual[:crop_length], mean_model_predictions[:crop_length], squared = False)
    
    text_str = '\n'.join(('Synthetic control RMSE: %.2f' % (rms_synthetic_control_test, ), 'Mean model RMSE: %.2f' % (rms_mean_model_test, )))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax[1].text(0.05, 0.95, text_str, fontsize=14, verticalalignment='top', bbox=props)
    
    plt.show()
    
    
    '''
    fig, ax = plt.subplots()
    plt.grid()
    ax.plot(all_dict['IX.br (PTT.br) Florianópolis']['dates'], all_dict['IX.br (PTT.br) Florianópolis']['values'], linewidth = 0.5)
    plt.show()
    '''