# Table of contents

CONTENTS OF THIS FILE
----------------------------------
* Introduction
* Overview
* Requirements
* PHP Files
* Python Files
* CGI
* Additional Files

# Introduction

I justed to wanted to provide a bit of a breakdown of this project, where files are located, the use of them and what is needed for this project.

# Overview

Quick Breakdown of where the IVR variables are sent

1. sv_eocs_result_count.php validates the caller's SSN
2. sv_eocs_return_results.php checks if the caller has any rides left for the month
3. If the user wants to review or cancel a future ride, all of the URL variables from the IVR are then sent to scan.php
4. After the call is over, the audio file gets sent to upload.py in the cgi-bin folder

# Requirements

The newest versions of Python and PHP are reccommended for this project to run correctly. I also wanted 
to highlight some of the important Python modules that are used in the scripts you will need. I have also created a requirements.txt file for reference, but you most likely will not need every one of those

## dbfpy3

dbfpy3 is a python-only module for reading and writing DBF-files. This package allows us to transform the foxpro files into MySQL data.

### Installastion

```bash
pip install dbfpy3
```

#### Heads Up

I had some trouble getting this to work properly using pip, so that is why I just added the whole folder into the scripts directory instead


# PHP Files

## defines.php

### Usage

defines.php defines our database credentials to include in our other files to reduce redundancy and increase security( Did not include it the repository for security purposes)

## Sv_eocs_result_count.php

### Usage

This is the first file that the IVR uses. It is used to check the validate that the SSN the user entered is in the database

## Sv_eocs_return_results.php

### Usage

This file is used see if the user has anymore rides left for the month

## Date_validation.php

### Usage

This file is used to validate the date that the user entered is correct

## Scan.php

### Usage

This file is used to scan the audio directory so the user can review future rides and cancel future rides.

# Python Files

## Transact.py

### Usage

transact.py is used to convert EOC's transact foxpro table into a MySQL table and then inserts it into our MySQL database

## Maxride.py

### Usage

transact.py is used to convert EOC's transact foxpro table into a MySQL table and then inserts it into our MySQL database

## Monitor.py

### Usage

monitor.py is used to monitor the directory that we have EOC's database files located in. When EOC updates their database, the file in our directory is also updated and the monitor script sees that and triggers transact.py and maxride.py to run, so the database is always up to date.

# CGI

For the audio files to be updated from the phone system to our server, we must send them to a CGI script. In our case, we used Python CGI

## Upload.py

### Usage

When a user is finished with their call, the audio is recorded and sent to our script upload.py.
When the audio is sent, upload.py uploads and renames the file to our audio directory

# Additional Files

## Defines.yml

### Usage

This is where we store our database credentials for our python files( Did not include it the repository for security purposes)

## Xml.xsd and Scan.xsd

### Usage

These two files located in the xml directory are just the schemas that our xml responses to send back to the system use.
Every php file uses xml.xsd except for scan.php, which uses scan.xsd# Table of contents

## Purge_audio.sh

### Usage

This file is used as a cron job and deletes the audio file the day after the user has taken their ride, based on the date in the file name. 
