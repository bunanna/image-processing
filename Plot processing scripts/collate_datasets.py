# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 23:07:54 2021

@author: Farah
"""
import datetime
import csv
import os
import sys
import pandas

ixps = ['ANIX - Albanian Neutral Internet eXchange',
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
        'SAIX']

current_directory = os.getcwd()
column_names = ["Dates", "Values (Gb)"]

start_year = input('Input starting year: ')
start_month = input('Input starting month: ')
start_day = input('Input starting day: ')

start_date = datetime.date(int(start_year), int(start_month), int(start_day))
print(str(start_date))

end_year = input('Input ending year: ')
end_month = input('Input ending month: ')
end_day = input('Input ending day: ')

end_date = datetime.date(int(end_year), int(end_month), int(end_day))
print(str(end_date))

input_ixp = input('Input desired IXP. Input all for all included IXPs: ')
ixps_to_use = []

if input_ixp == 'all':
    ixps_to_use = ixps
else:
    ixps_to_use = [input_ixp]
    
input_type = input('Input desired plot type. Input all for all available types: ')
type_to_use = []

if input_type == 'all':
    type_to_use = ['year', 'month']
else:
    type_to_use = [input_type]
    
for ixp in ixps_to_use:
    
    for plot_type in type_to_use:
        
        csv_filename = ixp + '_' + 'collated' + '_' + plot_type + '.csv'
        
        if not os.path.isfile(csv_filename):
            
            found_start = False
            found_end = False
            found_no_start = False
            found_no_end = False
            found_start_date = None
            found_end_date = None
            base_dates = []
            base_values = []
            dates_to_add = []
            values_to_add = []
            collated_dates = []
            collated_values = []
            
            while found_start == False and found_no_start == False:
                
                start_directory_name = str(start_date) + ' Data Sets'
                complete_directory = os.path.join(current_directory, start_directory_name)
                
                if not os.path.isdir(complete_directory):
                    if start_date < end_date:
                        print('{} data set directory not found. Checking next day.'.format(str(start_date)))
                        start_date += datetime.timedelta(days = 1)
                    else:
                        found_no_start = True
                        print('Invalid start date.')
                else:
                    print('{} data set directory found!'.format(str(start_date)))
                    os.chdir(complete_directory)
                    file_to_find = file_string = str(start_date) + '_' + ixp + '_' + plot_type + '.csv'
                    
                    if not os.path.isfile(os.path.join(complete_directory, file_to_find)):
                        if start_date < end_date:
                            print('{} data set for {} plots of type {} not found. Checking next day.'.format(str(start_date), ixp, plot_type))
                            start_date += datetime.timedelta(days = 1)
                        else:
                            found_no_start = True
                            print('Invalid start date.')
                    else:
                        found_start = True
                        print('{} data set for {} plots of type {} found!'.format(str(start_date), ixp, plot_type))
                        found_start_date = start_date
                        start_data = pandas.read_csv(file_to_find)
                        start_data_dates = start_data[column_names[0]].tolist()
                        start_data_values = start_data[column_names[1]].tolist()
                        
                        start_data_dates_parsed = []
                        
                        for str_date in start_data_dates:
                            datetime_object = datetime.datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
                            start_data_dates_parsed.append(datetime_object)
            
            os.chdir(current_directory)
            start_date = datetime.date(int(start_year), int(start_month), int(start_day))

            while found_end == False and found_no_end == False:
                
                end_directory_name = str(end_date) + ' Data Sets'
                complete_directory = os.path.join(current_directory, end_directory_name)
                
                if not os.path.isdir(complete_directory):
                    if end_date > start_date:
                        print('{} data set directory not found. Checking previous day.'.format(str(end_date)))
                        end_date -= datetime.timedelta(days = 1)
                    else:
                        found_no_end = True
                        print('Invalid end date.')
                else:
                    print('{} data set directory found!'.format(str(end_date)))
                    os.chdir(complete_directory)
                    file_to_find = file_string = str(end_date) + '_' + ixp + '_' + plot_type + '.csv'
                    
                    if not os.path.isfile(os.path.join(complete_directory, file_to_find)):
                        if end_date > start_date:
                            print('{} data set for {} plots of type {} not found. Checking previous day.'.format(str(end_date), ixp, plot_type))
                            end_date -= datetime.timedelta(days = 1)
                        else:
                            found_no_end = True
                            print('Invalid end date.')
                    else:
                        found_end = True
                        print('{} data set for {} plots of type {} found!'.format(str(end_date), ixp, plot_type))
                        found_end_date = end_date
                        end_data = pandas.read_csv(file_to_find)
                        end_data_dates = end_data[column_names[0]].tolist()
                        end_data_values = end_data[column_names[1]].tolist()
                        
                        end_data_dates_parsed = []
                        
                        for str_date in end_data_dates:
                            datetime_object = datetime.datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
                            end_data_dates_parsed.append(datetime_object)
            
            collated_directory = os.path.join(current_directory, 'Collated Data Sets')
            
            if not os.path.isdir(collated_directory):
                os.makedirs(collated_directory)
                
            end_date = datetime.date(int(end_year), int(end_month), int(end_day))
            
            base_dates = start_data_dates_parsed
            base_values = start_data_values
            base_dates_last = base_dates[len(base_dates) - 1]
            end_counter = 0
            
            for date in end_data_dates_parsed:
                if date > base_dates_last:
                    break
                else:
                    end_counter += 1
                    
            dates_to_add = end_data_dates_parsed[end_counter:]
            values_to_add = end_data_values[end_counter:]
            
            collated_dates = base_dates + dates_to_add
            collated_values = base_values + values_to_add
            
            rows = zip(collated_dates, collated_values)
            
            os.chdir(collated_directory)
            
            with open(csv_filename, 'w', newline='') as output_file:
                csv_output = csv.writer(output_file)
                csv_output.writerow(column_names)
                
                for row in rows:
                    csv_output.writerow(row)
            
            print('{} data set of {} plots was created using data from {} and {} data.'.format(ixp, plot_type, str(found_start_date), str(found_end_date)))
            os.chdir(current_directory)
            
        else:
            
            found_end = False
            found_no_end = False
            found_end_date = None
            dates_to_add = []
            values_to_add = []
            collated_dates = []
            collated_values = []
            
            while found_end == False and found_no_end == False:
                
                end_directory_name = str(end_date) + ' Data Sets'
                complete_directory = os.path.join(current_directory, end_directory_name)
                
                if not os.path.isdir(complete_directory):
                    if end_date > start_date:
                        print('{} data set directory not found. Checking previous day.'.format(str(end_date)))
                        end_date -= datetime.timedelta(days = 1)
                    else:
                        found_no_end = True
                        print('Invalid end date.')
                else:
                    print('{} data set directory found!'.format(str(end_date)))
                    os.chdir(complete_directory)
                    file_to_find = file_string = str(end_date) + '_' + ixp + '_' + plot_type + '.csv'
                    
                    if not os.path.isfile(os.path.join(complete_directory, file_to_find)):
                        if end_date > start_date:
                            print('{} data set for {} plots of type {} not found. Checking previous day.'.format(str(end_date), ixp, plot_type))
                            end_date -= datetime.timedelta(days = 1)
                        else:
                            found_no_end = True
                            print('Invalid end date.')
                    else:
                        found_end = True
                        print('{} data set for {} plots of type {} found!'.format(str(end_date), ixp, plot_type))
                        found_end_date = end_date
                        end_data = pandas.read_csv(file_to_find)
                        end_data_dates = end_data[column_names[0]].tolist()
                        end_data_values = end_data[column_names[1]].tolist()
                        
                        end_data_dates_parsed = []
                        
                        for str_date in end_data_dates:
                            datetime_object = datetime.datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
                            end_data_dates_parsed.append(datetime_object)
            
            collated_directory = os.path.join(current_directory, 'Collated Data Sets')
            
            if not os.path.isdir(collated_directory):
                sys.exit('There is no directory for collated data sets.')
            else:
                os.chdir(collated_directory)
            
                end_date = datetime.date(int(end_year), int(end_month), int(end_day))
                
                base_data = pandas.read_csv(csv_filename)
                base_dates = base_data[column_names[0]].tolist()
                base_values = base_data[column_names[1]].tolist()
                
                base_dates_parsed = []
                
                for str_date in base_dates:
                    datetime_object = datetime.datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
                    base_dates_parsed.append(datetime_object)
                    
                base_dates_last = base_dates_parsed[len(base_dates) - 1]
                
                end_counter = 0
                
                for date in end_data_dates_parsed:
                    if date > base_dates_last:
                        break
                    else:
                        end_counter += 1
                        
                dates_to_add = end_data_dates_parsed[end_counter:]
                values_to_add = end_data_values[end_counter:]
                
                collated_dates = base_dates_parsed + dates_to_add
                collated_values = base_values + values_to_add
                
                rows = zip(collated_dates, collated_values)
                
                with open(csv_filename, 'w', newline='') as output_file:
                    csv_output = csv.writer(output_file)
                    csv_output.writerow(column_names)
                    
                    for row in rows:
                        csv_output.writerow(row)
                
                print('{} data set of {} plots was created using preexisting data and {} data.'.format(ixp, plot_type, str(found_end_date)))
                os.chdir(current_directory)