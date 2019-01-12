<?php 
	$id=@$_POST['b_id'];
	$name=@$_POST['name'];
	$servername = "localhost";
	$username = "pi";
	$password = "nccutest";
	$dbname = "kekeproject";
	$conn = new mysqli($servername, $username, $password,$dbname);
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	} 
	$checkTable  = "SELECT `b_id`,`name` FROM `brand` WHERE `b_id` ='$id' and `name`= '$name'";
	$result = $conn->query($checkTable);
	if ($result->num_rows > 0) {
		echo "false";
	}else{
		$insertData = "INSERT INTO `brand`(`b_id`, `name`) VALUES ($id,'$name')";
		$conn->query($insertData);
		echo 'true';
	}	
	$conn->close();	
?>
