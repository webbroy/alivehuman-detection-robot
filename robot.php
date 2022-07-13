<?php
system("gpio mode 6 out");
system("gpio mode 4 out");
system("gpio mode 3 out");
system("gpio mode 2 out");
if (isset($_GET["pin"])){
	$pin=strip_tags ($_GET["pin"]);
	
	if(is_numeric($pin)){
		if($pin==70){
			system("gpio write 6 0");
			system("gpio write 4 0");
			system("gpio write 3 0");
			system("gpio write 2 0");
			echo('Stop');
			}
		if($pin==71){
			system("gpio write 2 1");
			system("gpio write 4 1");
			system("gpio write 3 0");
			system("gpio write 6 0");
			echo('start');
			}
		if($pin==72){
			system("gpio write 2 1");
			system("gpio write 3 0");
			system("gpio write 4 0");
			system("gpio write 6 0");
			echo('right');
			}
		if($pin==73){
			system("gpio write 4 1");
			system("gpio write 3 0");
			system("gpio write 2 0");
			system("gpio write 6 0");
			echo('left');
			}
		if($pin==74){
			system("gpio write 3 1");
			system("gpio write 6 1");
			system("gpio write 4 0");
			system("gpio write 2 0");
			echo('back');
			}
	}
}
