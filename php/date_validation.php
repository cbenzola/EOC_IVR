<?php

/*********** ********************************************************************************
This file is to validate the date that the user entered is correct, so that the name of the wav file can never be incorrect 

*********************************************************************************************/

header("Content-type: text/xml;charset=utf-8"); 

// Grab the date variable from the URL
$date = $_GET['date'];

// Format the date in mm-dd format
$date_slash =substr($date, 0, 2) . '/' . substr($date, 2, 2);

// Initialize the variable that we will pass back to the phone system to 0
$date_valid = 0;

// Create a REGEX expression to make sure the date that user entered is in the correct format
if (preg_match('/(0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01])/',$date_slash)) {
   
    // If it is valid, initialize $date_valid to 1 and pass that back to the system
    $date_valid = 1;
    echo '<?xml version="1.0" encoding="utf-8"?>';  
    echo  '<response xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../xml/xml.xsd">
    <result>
      <ivr_info>
        <variables>
          <variable>
          <name>date_valid</name> 
        <value>'.$date_valid.'</value>
          </variable>
          <variable>
          <name>date</name> 
        <value>'.$date_slash.'</value>
          </variable>
        </variables>
      </ivr_info>
    </result> 
    </response>
    ';
} else {
    // If it is not valid, pass back a 0 to the phone system
    echo '<?xml version="1.0" encoding="utf-8"?>';  
   
      echo  '<response xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../xml/xml.xsd">
      <result>
        <ivr_info>
          <variables>
            <variable>
            <name>date_valid</name> 
          <value>'.$date_valid.'</value>
            </variable>
            <variable>
            <name>date</name> 
          <value>'.$date_slash.'</value>
            </variable>
          </variables>
        </ivr_info>
      </result> 
      </response>
      ';
}
?>