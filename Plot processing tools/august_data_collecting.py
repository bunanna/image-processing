# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 17:35:48 2020

@author: User
"""
import synth_control_and_interpolation
import data_stitching
import pickle
import datetime

selected_ixp = 'DE-CIX Munich'

excluded = ['EPIX.Katowice',
            'EPIX.Warszawa-KIX',
            'IX.br (PTT.br) Campinas',]

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


start_year = 2020
start_month = 8
start_day = 1

end_year = 2020
end_month = 8
end_day = 32

data = data_stitching.get_data(selected_ixp, start_year, start_month, start_day, all_ixps, end_day, end_month, end_year)

stitched_dict = data_stitching.stitched_data_to_dict(data)

file_string = str(datetime.date(start_year, start_month, start_day)) + '_' + str(datetime.date(end_year, end_month, end_day - 1))

pickle.dump(stitched_dict, open(file_string + ".pkl", "wb"))
