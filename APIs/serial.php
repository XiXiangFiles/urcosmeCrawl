<?php 
	$s_id=@$_POST['s_id'];
	$brandName=@$_POST['brandName'];
	$serialName=@$_POST['serialName'];
	$className=@$_POST['className'];

	$servername = "localhost";
	$username = "pi";
	$password = "nccutest";
	$dbname = "kekeproject";
	$conn = new mysqli($servername, $username, $password,$dbname);
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	}
	$checkTable="SELECT `b_id` FROM`brand` where `name`='$brandName'";
	$result = $conn->query($checkTable);
	if ($result->num_rows > 0) {
		$doubleCheck="SELECT * FROM `category` WHERE (SELECT `b_id` FROM `brand` WHERE `name` ='$brandName') = b_id and `className`='$className'";
		$result = $conn->query($doubleCheck);
		if ($result->num_rows > 0){
			$row = $result->fetch_assoc();
			$insertData="INSERT INTO `serial`(`s_id`, `c_id`, `serialName`) VALUES ($s_id,".$row['c_id'].", '$serialName')";
			$conn->query($insertData);
			echo 'true';
		}else{
			echo 'false';
		}
	}else{
		echo 'false';

	}		 
	$conn->close();
?>
