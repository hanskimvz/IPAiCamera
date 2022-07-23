<?
$file = '../config/dl_confidence.conf';

// post
if (isset($_POST['confidenceData'])) {
  $updatedData = $_POST['confidenceData'];
  file_put_contents($file, $updatedData);
  echo 'success';
}
?>