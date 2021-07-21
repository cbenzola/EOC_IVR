#!/usr/bin/python3

import cgi, cgitb, os, sys, requests
import sys, urllib
from datetime import date, datetime

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
    get_date = form.getfirst('date')
    
    # Format the date in mm-dd format
    format_date = '-'.join([get_date[:2], get_date[2:4]])
    
    # Convert the formatted date into a date object
    d = datetime.strptime(format_date, '%m-%d')
    
    # Now we need to get the year and time so we can add it into the filename #
    # The time is needed, so that we do not have any duplicate files #
    
    # This is where it may get confusing. If a caller schedules a ride for next year, we have to make sure we increment the year
    # So to do that, I had to do a little trickery 
    

    # The now variable gets the todays date and time
    now = datetime.now()
    # Time gets the current hour and minutes. We will insert this into the filename to, to ensure that there are no duplicates
    time = now.strftime('%H_%M')
    # The today variable grabs the current month #   
    today = datetime.now().month
    # get_year grabs the current year from the now variable and converts it into a string. This will be used when we are renaming the file
    get_year =now.strftime("%Y")
    # I created another year variable, because when we have to increment the year, it cannot be a string
    year = date.today().year
    
    # increment_year gets todays date, but takes the year variable that we set before and adds 1 to it 
    increment_year = date.today().replace(year + 1)
    
    # If the month that the user entered has already passed, increment the year. If it isn't, keep the year the same
    if d.month < today:
        get_year= increment_year
    else:
        get_year = now
        
    # form_file grabs the submitted audio file from the system #
    # sound_variable is the name of the input that the phone system stores the audio file in when it sent to us #
    form_file = form['sound_variable']
    
    # Validate that a file was sent to us #
    if form_file.file:
        # If it was, insert the file into our audio directory #
        fn = os.path.basename(form_file.filename)
        open( '../audio/' + fn, 'wb').write(form_file.file.read())
        
        # When the file is inserted, rename it in ssn_mm-dd-yyyy_H_M.wav format #
        os.rename('../audio/' + fn, '../audio/' + ssn + '_' + format_date + '-' + get_year.strftime("%Y") + '_' + time + '.wav')

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
