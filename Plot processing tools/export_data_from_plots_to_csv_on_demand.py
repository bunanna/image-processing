# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 17:35:48 2020

@author: User
"""
import plot_data_to_dict
import datetime
import csv
import os
import shutil
import sys

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

excluded = ['EPIX.Katowice',
            'EPIX.Warszawa-KIX',]

current_directory = os.getcwd()

input_ixp = input('Input desired IXP. Input all for all included IXPs: ')
input_type = ''
ixps_to_use = []

if input_ixp == 'all':
    ixps_to_use = ixps
else:
    ixps_to_use = [input_ixp]
    input_type = input('Input desired plot type. Input all for all available types: ')

start_year = input('Input starting year: ')
start_month = input('Input starting month: ')
start_day = input('Input starting day: ')

current_date = datetime.date(int(start_year), int(start_month), int(start_day))

end_year = input('Input ending year: ')
end_month = input('Input ending month: ')
end_day = input('Input ending day: ')

end_date = datetime.date(int(end_year), int(end_month), int(end_day))

while current_date <= end_date:
    directory_name = str(current_date) + '_data_sets'
    
    if not os.path.isdir(directory_name):
        os.makedirs(directory_name)
        
    zip_file_name = str(current_date) + "_archive.zip"
    if os.path.isfile(zip_file_name) and not os.path.isdir(str(current_date)):
        shutil.unpack_archive(zip_file_name, str(current_date))
    
    if input_ixp == 'all' and input_type == '':
        output_filename = str(current_date) + '.txt'
    elif input_ixp != 'all' and input_type == 'all':
        output_filename = str(current_date) + '_' + input_ixp + '.txt'
    elif input_ixp != 'all' and input_type != 'all':
        output_filename = str(current_date) + '_' + input_ixp + '_' + input_type + '.txt'
    
    sys.stdout = open(output_filename, 'w')
    sys.stderr = sys.stdout
        
    for selected_ixp in ixps_to_use:
        
        data = plot_data_to_dict.get_data_no_loop(selected_ixp, current_date.year, current_date.month, current_date.day)
        stitched_dict = plot_data_to_dict.stitched_data_to_dict(data)
        ixp_data = stitched_dict[selected_ixp]
        keys = list(ixp_data.keys())
        
        if input_type in keys and input_type != '':
            keys_to_use = [input_type]
        else:
            keys_to_use = keys
            
        csv_columns = ["Dates", "Values (Gb)"]
        
        os.chdir(directory_name)
        
        for data_type in keys_to_use:
            file_string = str(current_date) + '_' + selected_ixp.replace(' ', '_') + '_' + data_type
            csv_name = file_string + ".csv"
            rows = zip(ixp_data[data_type]['dates'], ixp_data[data_type]['values'])
        
            with open(csv_name, 'w', newline='') as output_file:
                csv_output = csv.writer(output_file)
                csv_output.writerow(csv_columns)
                
                for row in rows:
                    csv_output.writerow(row)
                
        os.chdir(current_directory)

    print('Data extraction completed for this day.')
    
    sys.stdout.close()
    sys.stderr.close()
    
    current_date += datetime.timedelta(days = 1)