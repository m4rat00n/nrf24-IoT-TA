<?php
require_once "connect.php";
   if(function_exists($_GET['function'])){
        $_GET['function']();
   }
  function get_data(){
        global $connect;
        $query = $connect->query("SELECT * FROM sensor_dt");
        while($row = mysqli_fetch_object($query)){
              $data[] = $row;
        }
        $response = array('status' => 1, 'message' => 'Success', 'data' => $data);
        header('Content-Type: application/json');
        echo json_encode($response);
  }

  function add_data(){
        global $connect;
        $check = array('pckt_send'=>'', 'pckt_recv' => '','chiper_len' => '', 'plain_len' => '' ,'delay' => '', 'kec_angin' => '', 'curah_hujan' => '', 'Temp' => '', 'Humidity' => '', 'soil_mois' => '', 'Jarak' => '');
        $check_match = count(array_intersect_key($_POST, $check));
        if($check_match == count($check)){
              $result = mysqli_query($connect, "INSERT INTO sensor_dt SET pckt_send = '$_POST[pckt_send]', pckt_recv = '$_POST[pckt_recv]' , chiper_len = '$_POST[chiper_len]', plain_len = '$_POST[plain_len]', delay = '$_POST[delay]', kec_angin = '$_POST[kec_angin]', curah_hujan = '$_POST[curah_hujan]', Temp = '$_POST[Temp]', Humidity = '$_POST[Humidity]', soil_mois = '$_POST[soil_mois]', Jarak = '$_POST[Jarak]'");
              if($result){
                    $response = array('status' => 1, 'message' => 'Upload Success');
              }
              else{
                    $response = array('status' => 0, 'message' => 'Upload Failed');
              }
        }
        else{
              $response = array('status' => 0, 'message' => 'Wrong Params');
        }
        header('Content-Type: application/json');
        echo json_encode($response);
  }
  function update_data(){
  	global $connect;
	$check = array('delay'=>'','kec_angin'=>'','curah_hujan'=>'','temp'=>'','humidity'=>'','soil_mois'=>'');
	$check_match = count(array_intersect_key($_POST, $check));
	if($check_match == count($check)){
		$result = mysqli_query($connect, "UPDATE monitoring SET delay = '$_POST[delay]', kec_angin = '$_POST[kec_angin]', curah_hujan = '$_POST[curah_hujan]', temp = '$_POST[temp]', humidity = '$_POST[humidity]', soil_mois = '$_POST[soil_mois]' WHERE id=1");
		if($result){
			$response = array('status'=>1, 'message'=>'Update Success');
		}
		else{
			$response = array('status'=>0, 'message'=>'Update Failed');
		}
	}
	else{
		$response = array('status'=>0, 'message'=>'Wrong Params');
	}
	header('Content-Type: application/json');
        echo json_encode($response);
  }
?>

