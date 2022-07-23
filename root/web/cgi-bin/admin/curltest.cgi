<?php
  if(isset($_GET['smtp']) && isset($_POST['test']))
  {
    $x=$_POST['test'];
    $contextFile = "testfile.txt";
    $emailFile = fopen($contextFile, "w");
    $txt = "From:" . $x['sender'] . "\r\nTo:" . $x['receiver'] . "\r\nSubject:" . $x['title'] . "\r\n\r\n" . $x['message'];
    fwrite($emailFile, $txt);
    fclose($emailFile);

    $array_reciver = explode(';', $x['receiver']);
    $mail_rcpts = "";
    foreach ($array_reciver as $recv)
    {
      //recv is not empty
      if (empty($recv) == 0)
      {
        //ex) --mail-rcpt 'abc@a.com' --mail-rcpt 'abc@b.com'
        $mail_rcpts .= " --mail-rcpt '$recv'";
      }
    }

    if($x['ssl_enable'] == '1') {
      $string = "curl --max-time 20 --url 'smtps://" . $x['smtp_addr'] . ":" . $x['ssl_port'] . "' --ssl-reqd --mail-from '" . $x['sender'] . "' $mail_rcpts --upload-file " . $contextFile . " --user '" . $x['id'] . ":" . $x['pass'] . "' --insecure";
    }
    else {
      $string = "curl --max-time 20 --url 'smtp://" . $x['smtp_addr'] . ":" . $x['smtp_port'] . "' --mail-from '" . $x['sender'] . "' $mail_rcpts --upload-file " . $contextFile . " --user '" . $x['id'] . ":" . $x['pass'] . "' --insecure";
    }
    $ret = exec($string . " 2>&1", $output, $status);
    if($status == 0) //Success
      echo "Success to test mail.\r\nPlease check that the recipient has received the email.\r\nThen press 'Apply' to save.";
    else { //Fail
      echo "Failed : ";
      if(strpos($ret, "(" . $status . ")")) { // status error code 
        $tmp = strstr($ret, "(" . $status . ")"); //remove status error code
        if(strpos($tmp, "Login")) { // Login denied
          $tmp .= ". Please check if the User ID or the password or the port is correct.";
        }
        if(strpos($tmp, "routines")) { // SSL failed
          $tmp = "() SSL failed. Please check if the Mode and port are correct.";
        }
        echo strstr($tmp, " ") . "\r\n";
      }
      else
        echo $ret . "\r\n";
    }
  }
?>