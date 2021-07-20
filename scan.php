<?php 
/********************************************************/

// scan.php is used for scanning the audio directory for when a user wants to review their scheduled rides or delete a scheduled ride

//1) Phones system sends SSN to script

//2) Then we need to scan wav file directory for all file names that begin with that SSN and return the quantity (3 files return 3 as a variable)  

//3) The Phone system will then have it ask the user to listen to your first ride press 1, second ride 2, 3rd 3, etc. 

//4) When caller presses 1 we return the full name of the first wav file, 2 returns second, 3 returns 3rd, etc, so the system can play the wav file from URL

//5) When a user presses the option for cancel we delete that wav file(Line 116)

header("Content-type: text/xml;charset=utf-8"); 

// We will first declare the variables that we will be grabbing from the URL //

// Like the other PHP files, $ssn just grabs the entered SSN from the URL
$ssn= $_GET['ssn'];

/*$file_name returns the URL variable num passed from the phone system. 
$_GET[num] represents the number the user presses on the phone. So lets say the user has 3 future rides, 
the phone system will ask what ride they want to review, thus 1 will return the first ride, 2 will the second ride, etc.*/
$file_name = $_GET['num'];

/*$delete_file is only passed to the URL if the user wants to cancel their ride. If they do cancel, the word 'True' will be
passed to delete_file */
$delete_file = $_GET['delete_file'];

// Set file count to 0. This will be called to count the number of files in the directory //
$file_count = 0;

// Scan the audio directory for files starting with the entered SSN. This returns an array
$return_files = glob('audio/'.$ssn.'_*.wav');

// $files is used to return just the name of file, instead of the full path
$files = str_replace('audio/', '', $return_files);

/* $file just returns the name of the selected file.
  And since $return_files returns an array of the files, we have to subtract 1 from the user input. 
  So when they press 1 to review the first ride, the code will grab the first file which is stored at 0 in the array  */
$file = $file_name -1 ;

// Check to see if there are files in the directory, if there is, count them
if($files){
  $file_count = count($files);
}

/* $cut_wav cuts the .wav off of the file name and $cut_audio cuts the audio/ and SSN .
This is so we can return the date of the ride back to the system */
$cut_wav = substr_replace($return_files, '',-10);
$cut_audio = substr_replace($cut_wav, '', -26, -10);

// $get_month returns the month in the file name. This is so we can later convert the month to month name. 
$get_month = substr($cut_audio[$file], 0,2);

/* $replace_dash replaces the hyphens with slashes in the date. 
    This will be used for when we convert the date to epoch */
$replace_dash = str_replace('-','/',$cut_audio, );

//  $trim_zero trims the leading zero in the month(if there is one). This is because to convert the date it must be between 1-12, not 01-12
$trim_zero = ltrim($get_month, '0');

// $monthName converts the month from the filename to the full month name. i.e 1-01-2021 turns into January-01-2021 etc
$monthName = date('F', mktime(0, 0, 0, $trim_zero, 10));

// Finally, $month_conversion replaces the month number in the filename with the month name
$month_conversion = substr_replace($cut_audio, $monthName, -11, -8);

// $file_date just replaces the hyphens in the month, so it is easier to read.
$file_date = str_replace("-"," ",$month_conversion);

/* $epoch_conversion converts the date of the filename into epoch time, for the system to say back to the customer.
This is because the phone system can only read the date, if it is in epoch time */
$epoch_conversion = strtotime($replace_dash[$file]);

// $epoch_date changes the timezone from local time to GMT(Greenwich Mean Time), which is the timezone of the phone system. 
$epoch_date = $epoch_conversion +14400;

// XML response to send variables back to phone system 
echo '<?xml version="1.0" encoding="utf-8"?>';  
  echo  '<response  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../xml/scan.xsd"> 
  <result>
     <ivr_info>
        <variables>
           <variable>
              <name>file_count</name>
              <value>'.$file_count.'</value>
           </variable>
           <variable>
              <name>file</name>
              <value>'.$files[$file].'</value>
           </variable>
           <variable>
              <name>file_date</name>
              <value>'.$file_date[$file].'</value>
           </variable>
           <variable>
              <name>epoch_date</name>
              <value>'.$epoch_date.'</value>
           </variable>
           <variable>
              <name>delete_file</name>
              <value>'.$delete_file.'</value>
           </variable>
        </variables>
     </ivr_info>
  </result>
</response>
  ';

/* Finally, check to see if $delete_file is set to True.
  If it is to True, delete the selected file in the directory */
if ($delete_file){
  switch($delete_file){
    case 'True':
       unlink($return_files[$file]);
       break;
  }
}
?>



