# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 15:36:21 2021

@author: User
"""
import os
import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime

mpl.rcParams.update({'font.size': 8})

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

current_directory = os.getcwd()
folder_name = r'C:\Users\User\Desktop\Research\Data analysis\collated_data_sets_2020-11-30'
num_bins = 20

data_dict = {}

os.chdir(folder_name)

for filename in os.listdir(folder_name):
    
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

keys_in_dict = list(data_dict.keys())
fig, ax = plt.subplots()
plt.grid()

data = data_dict['MASS-IX']['values']
data_dates = data_dict['MASS-IX']['dates']
dates = []

for date in data_dates:
    new_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    dates.append(new_date)

ax.plot(dates, data, linewidth = 1)
ax.set_title('MASS-IX')
ax.set_xlabel('Date')
ax.set_ylabel('Throughput in Gb/s')
plt.show()

'''
for key in keys_in_dict:
    data = data_dict[key]['values']
    counts, bin_edges = np.histogram(data, bins=num_bins)
    pdf = counts / sum(counts)
    cdf = np.cumsum(pdf)
    ax.plot(bin_edges[1:], cdf, label = key, linewidth = 1)

plt.margins(0.01)
plt.legend(prop={'size': 6})    
plt.show()
'''
