# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 17:35:48 2020

@author: User
"""
import data_stitching
import datetime
import csv
import os
import shutil
import sys

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

excluded = ['EPIX.Katowice',
            'EPIX.Warszawa-KIX',]



current_directory = os.getcwd()
x = datetime.datetime.now()
current_year = x.year
current_month = x.month
current_day = x.day

directory_name = str(datetime.date(current_year, current_month, current_day)) + ' Data Sets'

if not os.path.isdir(directory_name):
    os.makedirs(directory_name)
    
zip_file_name = str(datetime.date(current_year, current_month, current_day)) + " Archive.zip"
if os.path.isfile(zip_file_name) and not os.path.isdir(str(datetime.date(current_year, current_month, current_day))):
    shutil.unpack_archive(zip_file_name, str(datetime.date(current_year, current_month, current_day)))

output_filename = str(datetime.date(current_year, current_month, current_day)) + '.txt'

sys.stdout = open(output_filename, 'w')
sys.stderr = sys.stdout
    
for selected_ixp in ixps:
    
    data = data_stitching.get_data_no_loop(selected_ixp, current_year, current_month, current_day)
    stitched_dict = data_stitching.stitched_data_to_dict(data)
    ixp_data = stitched_dict[selected_ixp]
    keys = list(ixp_data.keys())
    csv_columns = ["Dates", "Values (Gb)"]
    
    os.chdir(directory_name)
    
    for data_type in keys:
        file_string = str(datetime.date(current_year, current_month, current_day)) + '_' + selected_ixp + '_' + data_type
        csv_name = file_string + ".csv"
        rows = zip(ixp_data[data_type]['dates'], ixp_data[data_type]['values'])
    
        with open(csv_name, 'w', newline='') as output_file:
            csv_output = csv.writer(output_file)
            csv_output.writerow(csv_columns)
            
            for row in rows:
                csv_output.writerow(row)
            
    os.chdir(current_directory)

if os.path.isdir(str(datetime.date(current_year, current_month, current_day))):
    print('Now deleting extracted folder.')
    shutil.rmtree(os.path.join(current_directory, str(datetime.date(current_year, current_month, current_day))))

print('Now moving log file.')
shutil.move(os.path.join(current_directory, output_filename), os.path.join(current_directory, directory_name, output_filename))

print('Daily data extraction complete.')