# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 22:59:50 2021

@author: User
"""

import datetime
import os

current_directory = os.getcwd()

start_date_year = input('Input start year: ')
start_date_month = input('Input start month: ')
start_date_day = input('Input start day: ')

end_date_year = input('Input end year: ')
end_date_month = input('Input end month: ')
end_date_day = input('Input end day: ')

current_date = datetime.date(int(start_date_year), int(start_date_month), int(start_date_day))
end_date = datetime.date(int(end_date_year), int(end_date_month), int(end_date_day))

while current_date < end_date:
    file_string = str(current_date) + ' Archive.zip'
    
    if os.path.isfile(file_string):
        os.rename(file_string, str(current_date) + '_archive.zip')
        
    current_date += datetime.timedelta(days = 1)
    