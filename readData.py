import gpib
	import time
	tds= gpib.find("tds744") # define in /etc/gpib.conf
	 
	def query(handle, command, numbytes=100000):
		gpib.write(handle,command)
		#time.sleep(0.1)
		response = gpib.read(handle,numbytes)
		print response
	#line from ievgen 
        #line 2
	#line 3
	gpib.write(tds,"DATA:ENCDG ASCI") #read data in ASCI 
	gpib.write(tds,"DATA:WIDTH 1") #read numbers in 1 byte (-128 .. 128 range)
	query(tds,"*IDN?")

	 
	gpib.close(tds)
