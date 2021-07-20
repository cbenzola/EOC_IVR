<?php
/************************************************************************* 
 SV_EOCS_RESULT_COUNT.PHP  
This file is used to Validate if the SSN that the user entered is valid               
             
**************************************************************************/


/*********************************************************************

Create Function That Creates XML Response For Phone System to Read Back To Server. 
$valid is defined in if statement below this block function

***********************************************************************/

header("Content-type: text/xml;charset=utf-8");  

// Get and Declare Social Security Variable That User Entered //
$ssn = $_GET['ssn'];

// If SSN That User Entered Is Not Empty Execute Following Block //
if ($ssn != '' )
{
   // Include Database Credentials from defines.php // 
    include("defines.php");

    // Create Connection To Database //
    try{
        $pdo = new PDO("mysql:host=$host;dbname=$dbname", $user, $password);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Build our SQL Query For Checking if SSN is in Database. Returns 0 if SSN is not in database and 1 if SSN is in Database //
        $sql = "SELECT IFNULL( (SELECT CASE WHEN SS_NO = SS_NO THEN 1 END FROM transact2 WHERE SS_NO = :ssn LIMIT 1) ,0) AS 'valid';";

        // Prepare Query //
        $stmt = $pdo->prepare($sql);

        // Bind Entered SSN Variable To Query //
        $stmt->bindValue(':ssn', $ssn);

        // Execute Query //
        $stmt->execute();

        // Fetch Query Results //
        $results = $stmt->fetch();

        // Get Result of 1 or 0 from Query //
        $valid = $results["valid"]; 

      echo '<?xml version="1.0" encoding="utf-8"?>';  
      
  // Return our XML response 
  // valid is the only variable we pass back to switchvox
      echo '<response xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="php/xml.xsd"> 
      <result>
        <ivr_info>
          <variables>
            <variable>
            <name>valid</name> 
          <value>'.$valid.'</value>
            </variable>
          </variables>
        </ivr_info>
      </result> 
      </response>
      ';

      //  echo sendResponse($valid);

     // If Connection to Database Fails, Throw Error //    
    }catch(PDOException $e)
    {
      echo "Connection failed: " . $e->getMessage();
    }
 // If No SSN is Entered //   
}else{
    echo 'Invalid SSN';
  }

// Close Database Connection //  
$pdo=null;

?>