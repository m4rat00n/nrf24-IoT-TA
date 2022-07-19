<?php
  $link = mysqli_connect("127.0.0.1", "ody", "123", "sensorData");
  if($link) {
    $query = mysqli_query($link, "SELECT * FROM monitoring");
    while($array = mysqli_fetch_array($query)) {
      echo $array['delay']."<br />";
    } 
  }
  else {
    echo "MySQL error :".mysqli_error();
  }
?>
