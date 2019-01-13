<?php 
	$c_id=@$_POST['c_id'];
	$b_id=@$_POST['b_id'];
	$brandName=@$_POST['brandName'];
	$className=@$_POST['className'];

	$servername = "localhost";
	$username = "pi";
	$password = "nccutest";
	$dbname = "kekeproject";
	$conn = new mysqli($servername, $username, $password,$dbname);
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	}
	$checkTable="SELECT * FROM `category` WHERE `c_id`= $c_id and `b_id` = (SELECT `b_id` FROM`brand` where `name`='$brandName' )and `className`='$className'";
	$result = $conn->query($checkTable);
	if ($result->num_rows > 0) {
		echo "false";
	}else{
		$doubleCheck='SELECT `b_id` FROM`brand` where `name`="'.$brandName.'"';
		$result = $conn->query($doubleCheck);
		if ($result->num_rows > 0){
			$insertData="INSERT INTO `category`(`c_id`, `b_id`, `className`) VALUES ($c_id, $b_id, '$className')";
			echo $insertData;
			$conn->query($insertData);
			echo 'true';
		}else{
			echo 'false';
		}
	}		 
	$conn->close();
?>
