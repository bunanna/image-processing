# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 23:58:49 2021

@author: User
"""

import datetime
import shutil
import os

start_date = datetime.date(2020, 7, 25)
end_date = datetime.date(2020, 9, 23)

current_date = start_date

while current_date <= end_date:
    if os.path.isdir(str(current_date)) == True:
        shutil.make_archive(str(current_date) + '_archive', 'zip', str(current_date))
        current_date += datetime.timedelta(days = 1)