<?php
	echo "MySQL - Statuslogger\n";
	
	$tmp=explode(" ",microtime());$microtime=$tmp[0]+$tmp[1];unset($tmp); // Zeitmessung Start
	
//	$server = "192.168.0.1";
	$logpath= "/var/log/"; // dump_logfile path
	$server = "localhost";
	$user   = "root";
	$pass   = "16121975";
	$path   = "/tmp/"; // temp path ending with /
	
	echo "Ermittle MySQL Client Version ... ";
	dl("mysqli.so");
	if(function_exists("mysqli_connect")) {
	    $use_ifkt = true; 
	    $mfetch = "mysqli_fetch_array";
	    $mclose = "mysqli_close";
	    echo "mysqli (PHP5)\n";
	} else {
	    $use_ifkt = false;
	    $mfetch = "mysql_fetch_array";
	    $mclose= "mysql_close";
	    echo "mysql (PHP4)\n";
	}
    
function connect() {
    GLOBAL $server, $user, $pass, $use_ifkt;
    echo "Verbinde mit DB ... ";
    if (!$use_ifkt) $con = mysql_connect($server,$user,$pass);
    else $con = mysqli_connect($server,$user,$pass);
    return $con;    
}

	$con = connect();
	if($con) {
		echo "ok\n";
		$sql = "SHOW STATUS";
		
		if(!$use_ifkt) $res = mysql_query($sql,$con);
		else $res = mysqli_query($con,$sql);	
		
		$i=0;
		$data ="";
		while ( $row = @$mfetch($res)) {
		    $data .= $row[1] . ";";
		} //# while()
	} else { echo "fehlgeschlagen!!!\n"; $status="FEHLGESCHLAGEM";}

	
	$temp=explode(" ",microtime());$microtime=$temp[0]+$temp[1]-$microtime;unset($temp); // Zeitmessung Ende

    if ($handle = fopen($logpath."mysql_status.log", "a")) {
		$data = sprintf("%02.03f;%s", $microtime, $data);
		fwrite($handle, date("YmdHis").";".$data."\n");
	    fclose($handle);
    }

#	echo $microtime;
	echo sprintf("\nFertig nach %02.03fs.\n", $microtime);
?>
