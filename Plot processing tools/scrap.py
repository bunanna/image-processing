# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 01:58:13 2021

@author: User
"""

ixps = ['angonix',
        'ANIX - Albanian Neutral Internet eXchange',
        'BCIX',
        'DE-CIX Dallas',
        'DE-CIX Frankfurt',
        'DE-CIX Hamburg',
        'DE-CIX Istanbul',
        'DE-CIX Madrid',
        'DE-CIX Marseille',
        'DE-CIX Munich',
        'DE-CIX New York', 
        'GrenoblIX',
        'IIX-Bali',
        'IX.br (PTT.br) BelÃ©m',
        'IX.br (PTT.br) Belo Horizonte',
        'IX.br (PTT.br) BrasÃ­lia',
        'IX.br (PTT.br) Campinas',
        'IX.br (PTT.br) Caxias do Sul',
        'IX.br (PTT.br) CuiabÃ¡',
        'IX.br (PTT.br) FlorianÃ³polis',
        'IX.br (PTT.br) Fortaleza',
        'IX.br (PTT.br) Foz do IguaÃ§u',
        'IX.br (PTT.br) GoiÃ¢nia',
        'IX.br (PTT.br) Londrina',
        'IX.br (PTT.br) MaceiÃ³',
        'IX.br (PTT.br) Manaus',
        'IX.br (PTT.br) MaringÃ¡',
        'IX.br (PTT.br) Natal',
        'IX.br (PTT.br) Porto Alegre',
        'IX.br (PTT.br) Recife',
        'IX.br (PTT.br) Rio de Janeiro',
        'IX.br (PTT.br) Salvador',
        'IX.br (PTT.br) Santa Maria',
        'IX.br (PTT.br) SÃ£o JosÃ© do Rio Preto',
        'IX.br (PTT.br) SÃ£o Paulo',
        'IX.br (PTT.br) VitÃ³ria',
        'IXPN Lagos',
        'JPNAP Osaka',
        'JPNAP Tokyo',
        'LONAP',
        'MASS-IX',
        'MIX-IT',
        'SAIX'
        'TorIX']

group_6 = [
    'IX.br (PTT.br) São Paulo',
    'IX.br (PTT.br) Teresina',
    'IX.br (PTT.br) Vitória'
]

group_6 = [
    'IX.br (PTT.br) Belém',
    'IX.br (PTT.br) Belo Horizonte',
    'IX.br (PTT.br) Brasília',
    'IX.br (PTT.br) Campina Grande',
    'IX.br (PTT.br) Campinas',
    'IX.br (PTT.br) Campo Grande',
    'IX.br (PTT.br) Cascavel',
    'IX.br (PTT.br) Caxias do Sul',
    'IX.br (PTT.br) Cuiabá',
    'IX.br (PTT.br) Curitiba',
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
    'IX.br (PTT.br) Vitória'
]

    
    '''
    
    elif 'Netnod' in ixp:
        for char in key_list[key_amount - 1]:
            if char.isdigit() == True:
                end_week_number_string_list.append(char)
                
        end_week_number_label = ''.join(end_week_number_string_list)
        
        while current_date.isocalendar()[1] != int(end_week_number_label) or current_date.weekday != 3:
            current_date -= datetime.timedelta(days = 1)
        
        end_time = datetime.datetime.combine(current_date, datetime.time(12, 0))
        print(end_time)
        
        for char in key_list[0]:
            if char.isdigit() == True:
                start_week_number_string_list.append(char)
    
        start_week_number_label = ''.join(start_week_number_string_list)
        start_time = end_time - datetime.timedelta(weeks = end_time.isocalendar()[1] - int(start_week_number_label))
        
        start_location = x_axis_dict[key_list[first_tag]]['vertical midline']
        end_location = x_axis_dict[key_list[key_amount - 1]]['vertical midline']
        
        time_scale = (end_time.isocalendar()[1] - int(start_week_number_label)) * 7 * 24 * 60 * 60
    '''   
    