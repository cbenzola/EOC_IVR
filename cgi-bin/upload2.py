#!/usr/bin/python3

import cgi, cgitb, os, sys, requests
import sys, urllib
from datetime import date, datetime
from pytz import timezone
from dateutil.relativedelta import relativedelta

# This is the CGI script that uploads and renames the audio file to the server #

def save_uploaded_file():
    print ('Content-Type: text/html; charset=UTF-8')
    print ('''
    <html>
    <head>
    <title>Upload File</title>
    </head>
    <body>
    ''')
    
    # Initialize the field storage class to grab the submitted URL parameters #
    form = cgi.FieldStorage()
    
    # Grab the SSN from URL #
    ssn = form.getfirst('ssn')
    
    # Grab the date from the URL #
    date = form.getfirst('date')
    
    # Format the date in mm-dd format
    d = '-'.join([date[:2], date[2:4], date[4:]])
    
    # Now we need to get the year and time so we can add it into the filename #
    # The time is needed, so that we do not have any duplicate files #
    
    # The today variable grabs the current date and time #
    # But since we only care about getting the year and time, we will have today2 format it in yyyy_hour_minute format 
    tz= timezone('EST')
    today = datetime.now(tz)
    
    today2 =today.strftime("%Y_%H_%M")
    
    if d < today.strftime("%m-%d-%Y"):
       today2 += relativedelta(years=1)
    
    # form_file grabs the submitted audio file from the system #
    # sound_variable is the name of the input that the phone system stores the audio file in when it sent to us #
    form_file = form['sound_variable']
    
    # Validate that a file was sent to us #
    if form_file.file:
        # If it was, insert the file into our audio directory #
        fn = os.path.basename(form_file.filename)
        open( '../audio/' + fn, 'wb').write(form_file.file.read())
        
        # When the file is inserted, rename it in ssn_mm-dd-yyyy_H_M.wav format #
        os.rename('../audio/' + fn, '../audio/' + ssn + '_' + d + today2 + '.wav')

        message = 'The file "' + fn + '" was uploaded successfully'
    else:
        message = 'No file was uploaded'

    print("<hr>")
    print("</body>")
    print("<h1>")
    print("</h1>")
    print("</html>".format( message))


cgitb.enable()
save_uploaded_file()
