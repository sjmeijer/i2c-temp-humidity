import subprocess
import time
import sys

while(1):
	result = subprocess.check_output("python getTempHumidity.py", shell=True)
	sys.stdout.write(str(result)+"\r")
	#		 "temp: %03.3f, humidity: %03.3f"
	
	time.sleep(2)
	
	sys.stdout.flush()
	#sys.stdout.write("\033[K")
	
