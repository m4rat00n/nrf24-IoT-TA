<?php
$hostname = "localhost";
$database = "sensorData";
$username = "ody";
$password = "123";

$connect = mysqli_connect($hostname, $username, $password, $database);

if(!$connect){
   die("tidak terhubung: " . mysqli_connect_error());
}
?>
