<?php 
	$s_id=@$_POST['s_id'];
	$productName=@$_POST['productName'];
	$grade=@$_POST['grade'];
	$articalLink=@$_POST['articalLink'];
	$price=@$_POST['price'];
	$brandName=@$_POST['brandName'];
	$serialName=@$_POST['serialName'];
	$className=@$_POST['className'];
	$marketDate=@$_POST['marketDate'];
	$info=$_POST['info'];

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
		$doubleCheck="SELECT `s_id`,`serialName` FROM `serial` WHERE (SELECT `c_id` FROM `category` WHERE (SELECT `b_id` FROM `brand` WHERE `name` ='$brandName') = b_id and `className`='$className') = c_id and `serialName`='$serialName'";
		$result = $conn->query($doubleCheck);
		if ($result->num_rows > 0){
			$row = $result->fetch_assoc();
			$trippleCheck="SELECT * FROM `products` WHERE `s_id`= ".$row['s_id']." and `name`='$productName' and `grade`='$grade' and `articalLink`='$articalLink' and `marketDate`='$marketDate' and `price`=$price ";
			$result = $conn->query($trippleCheck);
			if ($result->num_rows > 0){
				echo "false";
			}else{
				$insertData="INSERT INTO `products`(`s_id`, `name`, `grade`, `articalLink`, `marketDate`, `price`, `is_limit`, `is_discount`, `is_withdraw`, `info`) VALUES(".$row['s_id'].", '$productName', '$grade', '$articalLink', '$marketDate', $price, 0, 0, 0, '$info')";
				$result = $conn->query($insertData);
				echo 'true';
			}
		}else{
			echo 'false';
		}
	}else{
		echo 'false';

	}		 
	$conn->close();
?>