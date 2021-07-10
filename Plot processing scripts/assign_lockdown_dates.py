# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 22:11:10 2021

@author: Farah
"""
import os
import datetime

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
data_directory_name = 'Collated Data Sets'
collated_data_path = os.path.join(current_directory, data_directory_name)

filename_suffix = '_' + 'collated' + '_' + 'year' + '.csv'

for ixp in ixp:
    if os.path.isfile(os.path.join(collated_data_path, ixp + filename_suffix)):
        
        if ixp == 'ANIX - Albanian Neutral Internet eXchange':
            #Source: https://web.archive.org/web/20200311132130/https://www.tiranatimes.com/?p=144535
            lockdown_date = datetime.datetime(2020, 3, 12, 0, 0, 0)
            
        elif ixp == 'TorIX':
            #Source: https://globalnews.ca/news/6688074/ontario-doug-ford-coronavirus-covid-19-march-17/
            lockdown_date = datetime.datetime(2020, 3, 17, 0, 0, 0)
            
        elif ixp == 'MIX-IT':
            #Source: https://www.theguardian.com/world/2020/mar/08/coronavirus-italy-quarantine-virus-reaches-washington-dc
            lockdown_date = datetime.datetime(2020, 3, 8, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) São Paulo':
            #State: São Paulo
            #Source: https://www.bbc.com/news/world-latin-america-52040205
            lockdown_date = datetime.datetime(2020, 3, 24, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Rio de Janeiro':
            #State: Rio de Janeiro
            #Source: https://www.reuters.com/article/us-health-coronavirus-brazil-lockdown/brazil-lockdowns-attacked-by-bolsonaro-begin-to-slip-idUSKCN21R30B
            lockdown_date = datetime.datetime(2020, 3, 23, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Fortaleza':
            #State: Ceará
            #Source: https://www.tandfonline.com/doi/pdf/10.1080/22221751.2020.1785337
            lockdown_date = datetime.datetime(2020, 5, 8, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Porto Alegre':
            #State: Rio Grande do Sul
            #Source: https://g1.globo.com/rs/rio-grande-do-sul/noticia/2020/03/19/governo-decreta-situacao-de-calamidade-publica-no-rs-devido-ao-coronavirus.ghtml
            lockdown_date = datetime.datetime(2020, 3, 19, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Brasília':
            #State: Federal District
            #Source: https://www.mayerbrown.com/-/media/files/perspectives-events/publications/2020/03/temporary-measures-to-deter-the-spread-of-covid19-in-brazil_v2.pdf
            lockdown_date = datetime.datetime(2020, 3, 19, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Salvador':
            #State: Bahia
            #Source: https://www.mayerbrown.com/-/media/files/perspectives-events/publications/2020/03/temporary-measures-to-deter-the-spread-of-covid19-in-brazil_v2.pdf
            lockdown_date = datetime.datetime(2020, 3, 16, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Belém':
            #State: Pará
            #Source: https://www.mayerbrown.com/-/media/files/perspectives-events/publications/2020/03/temporary-measures-to-deter-the-spread-of-covid19-in-brazil_v2.pdf
            lockdown_date = datetime.datetime(2020, 3, 16, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Campinas':
            #State: São Paulo
            #Source: https://www.bbc.com/news/world-latin-america-52040205
            lockdown_date = datetime.datetime(2020, 3, 24, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Londrina':
            #State: Paraná
            #Source: https://www.mayerbrown.com/-/media/files/perspectives-events/publications/2020/03/temporary-measures-to-deter-the-spread-of-covid19-in-brazil_v2.pdf
            lockdown_date = datetime.datetime(2020, 3, 19, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Recife':
            #State: Pernambuco
            #Source: https://www.mayerbrown.com/-/media/files/perspectives-events/publications/2020/03/temporary-measures-to-deter-the-spread-of-covid19-in-brazil_v2.pdf
            lockdown_date = datetime.datetime(2020, 3, 20, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Belo Horizonte':
            #State: Minas Gerais
            #Source: https://www.mayerbrown.com/-/media/files/perspectives-events/publications/2020/03/temporary-measures-to-deter-the-spread-of-covid19-in-brazil_v2.pdf
            lockdown_date = datetime.datetime(2020, 3, 19, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Natal':
            #State: Rio Grande do Norte
            #Source: https://g1.globo.com/rn/rio-grande-do-norte/noticia/2020/03/20/governo-do-rn-decreta-calamidade-publica-por-causa-do-coronavirus.ghtml
            lockdown_date = datetime.datetime(2020, 3, 20, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Florianópolis':
            #State: Santa Catarina
            #Source: https://g1.globo.com/sc/santa-catarina/noticia/2020/03/29/casos-de-pacientes-com-coronavirus-sobe-para-197-em-sc-e-governo-prorroga-quarentena.ghtml
            lockdown_date = datetime.datetime(2020, 3, 17, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Maceió':
            #State: Alagoas
            #Source: https://www.mayerbrown.com/-/media/files/perspectives-events/publications/2020/03/temporary-measures-to-deter-the-spread-of-covid19-in-brazil_v2.pdf
            lockdown_date = datetime.datetime(2020, 3, 19, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Vitória':
            #State: Espírito Santo
            #Source: https://www.mayerbrown.com/-/media/files/perspectives-events/publications/2020/03/temporary-measures-to-deter-the-spread-of-covid19-in-brazil_v2.pdf
            lockdown_date = datetime.datetime(2020, 3, 19, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Maringá':
            #State: Paraná
            #Source: https://www.mayerbrown.com/-/media/files/perspectives-events/publications/2020/03/temporary-measures-to-deter-the-spread-of-covid19-in-brazil_v2.pdf
            lockdown_date = datetime.datetime(2020, 3, 16, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Goiânia':
            #State: Goiás
            #Source: https://www.mayerbrown.com/-/media/files/perspectives-events/publications/2020/03/temporary-measures-to-deter-the-spread-of-covid19-in-brazil_v2.pdf
            lockdown_date = datetime.datetime(2020, 3, 20, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Santa Maria':
            #State: Rio Grande do Sul
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Foz do Iguaçu':
            #State: Paraná
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) São José do Rio Preto':
            #State: São Paulo
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Manaus':
            #State: Amazonas
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Cuiabá':
            #State: Mato Grosso
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'IX.br (PTT.br) Caxias do Sul':
            #State: Rio Grande do Sul
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'LONAP':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'BCIX':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'MASS-IX':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'IXPN Lagos':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'IIX-Bali':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'DE-CIX Frankfurt':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'DE-CIX Munich':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'DE-CIX Hamburg':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'DE-CIX Istanbul':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'DE-CIX Madrid':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'DE-CIX Marseille':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'DE-CIX New York':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'DE-CIX Dallas':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'JPNAP Osaka':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'JPNAP Tokyo':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'GrenoblIX':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)
            
        elif ixp == 'SAIX':
            #Source:
            lockdown_date = datetime.datetime(2020, 0, 0, 0, 0, 0)

        