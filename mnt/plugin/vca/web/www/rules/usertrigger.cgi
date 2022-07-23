<?
$file = '../config/trigger.conf';
$tag = "rule";
$trigger = "trigger";
$begin = "begin";
$end = "end";
$trgVal = '0';
$bgVal = '0';
$edVal = '0';
$json = json_decode(file_get_contents($file),TRUE);
if (isset($_GET[$trigger]) && isset($_GET[$begin]) && isset($_GET[$end])) {
  $trgVal = $_GET[$trigger];
  $bgVal = $_GET[$begin];
  $edVal = $_GET[$end];

  if ($_GET[$trigger]!="") {
    if(!ctype_digit($trgVal)) {
      $trgVal = '0';
    }
  }
  else $trgVal = '0';
  if ($_GET[$begin]!="") {
    echo $bgVal;
    echo var_dump(!ctype_digit($bgVal) && $bgVal!=1);
    if(!ctype_digit($bgVal)) {
      $bgVal = '0';
    } else if($bgVal != 1) {
      $bgVal = '0';
    }
  }else $bgVal = '0';
  if ($_GET[$end]!="") {
    if(!ctype_digit($edVal)) {
      $edVal = '0';
    }else if($bgVal != 1) {
      $bgVal = '0';
    }
  }else $edVal = '0';
}
if (isset($_GET[$tag]) && $_GET[$tag]!="") {
  $value = $_GET[$tag];
  if(isset($_GET["add"])) {
    if(!isset($json[$value])) {
      $json[$value]['type'] = $trgVal;
      $json[$value]['begin'] = $bgVal;
      $json[$value]['end'] = $edVal;
    }
    else {
      $json[$value]['type'] = $trgVal;
      $json[$value]['begin'] = $bgVal;
      $json[$value]['end'] = $edVal;
    }
    file_put_contents($file, json_encode($json, JSON_FORCE_OBJECT | JSON_UNESCAPED_SLASHES));
    echo $tag . "=" . $value . " : " . print_r($json[$value]);
    unset($json);
  }
  else if(isset($_GET["del"])) {
    echo var_dump(isset($json[$value]) && $json[$value] != "");
    if(isset($json[$value]) && $json[$value] != "") {
      unset($json[$value]);
      file_put_contents($file, json_encode($json, JSON_FORCE_OBJECT | JSON_UNESCAPED_SLASHES));
    }
    echo print_r($json);
    echo $tag . "=" . $value;
    unset($json);
  }
}
?>