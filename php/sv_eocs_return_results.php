<?php

/************************************************************************* 
  
This file is used to see if the user has any rides left for the month             
             
**************************************************************************/


/*********************************************************************

Create Function That Creates XML Response For Phone System to Read Back. 
$count is defined in if statement below this block

***********************************************************************/

header("Content-type: text/xml;charset=utf-8"); 

// Declare Social Security Variable That User Entered //
$ssn = $_GET['ssn'];

// If SSN User Entered Is Not Empty Execute Following Block //
if ($ssn != '' )
{
  // Include Database Credentials from defines.php //  
  include("defines.php");

  // Create Connection To Database //
  try{
      $pdo = new PDO("mysql:host=$host;dbname=$dbname", $user, $password);
      $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
      
      // Declare first day of current month and current day //
      $date1 = date("Y-m-1");
      $date2 = date("Y-m-d");

       /************************************************************************************* 
        Build SQL Query For Checking if user has any rides left for the month.
        Returns 1 if User has no rides left for month and 2 if they still have rides available 
        **************************************************************************************/
      $sql = "SELECT pl.SS_NO, count(pl.transactID), CASE WHEN COUNT(pl.TransactID) >= m.LIMIT THEN 1 ELSE 2  
                  END AS 'status'
                  FROM transact2 pl, maxride2 m
                  WHERE pl.SS_NO = :ssn AND (pl.Dater between '$date1' AND '$date2') 
                  group by pl.SS_NO;";

      // Prepare Query //
      $stmt = $pdo->prepare($sql);

      // Bind Entered SSN Variable To Query //
      $stmt->bindValue(':ssn', $ssn);

      // Execute Query //
      $stmt->execute();

      // Fetch Query Results //
      $results = $stmt->fetch();

      // Get Result of 1 or 2 from Query //
      $status = $results["status"]; 

      // Call Function //
      echo '<?xml version="1.0" encoding="utf-8"?>';  
// Return our XML response 
  // status is the only variable we pass back to switchvox
  // Attach XML Schema(xml.xsd) to response element //
  echo  '<response xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../xml/xml.xsd">
  <result>
    <ivr_info>
      <variables>
        <variable>
        <name>status</name> 
      <value>'.$status.'</value>
        </variable>
      </variables>
    </ivr_info>
  </result> 
  </response>
  ';

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