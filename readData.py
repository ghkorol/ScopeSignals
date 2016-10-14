import gpib
import time
tds= gpib.find("tds744") # define in /etc/gpib.conf

def query(handle, command, numbytes=100000):
	gpib.write(handle,command)
	#time.sleep(0.1)
	response = gpib.read(handle,numbytes)
	print response

query(tds,"*IDN?") #ask for ID, simple test if the scope does response (page 2-21 of Programmer Manual)
gpib.write(tds,"FAC") #Reset to factory default (p. 2-21)
gpib.write(tds,"DATA:ENCDG ASCI") #set the convenient data reading format(p. 2-34, p.2-35)
gpib.write(tds,"DATA:WIDTH 1") #1 byte for reading numbers (-128 .. 128 range)(p. 2-34, p.2-35)


	
gpib.close(tds)
