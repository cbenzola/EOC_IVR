#!/usr/bin/python3

import cgi, cgitb, os, sys, requests
import sys, urllib
from datetime import date, datetime
from pytz import timezone
from dateutil.relativedelta import relativedelta

# This is the CGI script that uploads and renames the audio file to the server #



date = '0406'

d2 = '-'.join([date[:2], date[2:4]])
print(d2)
# Format the date in mm-dd format

d = datetime.strptime(d2, '%m-%d')
# Now we need to get the year and time so we can add it into the filename #
# The time is needed, so that we do not have any duplicate files #

# The today variable grabs the current date and time #
# But since we only care about getting the year and time, we will have today2 format it in yyyy_hour_minute format 
tz= timezone('EST')
now = datetime.now()
today = datetime.now().month

today2 =now.year 

if d.month < today:
   today2 = now+ relativedelta(years = 1)

print(today2.strftime("%Y_%H_%M"))    