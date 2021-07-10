# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 17:35:48 2020

@author: User
"""
import synth_control_and_interpolation
import data_stitching
import pickle
import datetime
import csv
import os

selected_ixp = 'DE-CIX Munich'

'''
excluded = ['EPIX.Katowice',
            'EPIX.Warszawa-KIX',]

all_ixps = ['ANIX - Albanian Neutral Internet eXchange',
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
'''

all_ixps = ['DE-CIX Munich']

start_year = 2020
start_month = 9
start_day = 1

current_directory = os.getcwd()
directory_name = str(datetime.date(start_year, start_month, start_day)) + ' Data Sets'

if not os.path.isdir(directory_name):
    os.makedirs(directory_name)
    
data = data_stitching.get_data_no_loop(selected_ixp, start_year, start_month, start_day, all_ixps)
stitched_dict = data_stitching.stitched_data_to_dict(data)
ixp_data = stitched_dict[selected_ixp]
keys = list(ixp_data.keys())
csv_columns = ["Dates", "Values"]

os.chdir(directory_name)

for data_type in keys:
    file_string = str(datetime.date(start_year, start_month, start_day)) + '_' + selected_ixp + '_' + data_type
    csv_name = file_string + ".csv"
    rows = zip(ixp_data[data_type]['dates'], ixp_data[data_type]['values'])

    with open(csv_name, 'w', newline='') as output_file:
        csv_output = csv.writer(output_file)
        csv_output.writerow(csv_columns)
        
        for row in rows:
            csv_output.writerow(row)
            
os.chdir(current_directory)