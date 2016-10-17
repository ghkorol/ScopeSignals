import gpib
import time
tds= gpib.find("tds744") # define in /etc/gpib.conf

def query(handle, command, numbytes=100000):
	gpib.write(handle,command)
	#time.sleep(0.1)
	response = gpib.read(handle,numbytes)
	print response

query(tds,"*IDN?") #ask for ID, simple test if the scope does response (page 2-21 of Programmer Manual)
gpib.write(tds,"DATA:ENCDG ASCI") #set the convenient data reading format(p. 2-34, p.2-35)
gpib.write(tds,"DATA:WIDTH 1") #1 byte for reading numbers (-128 .. 128 range)(p. 2-34, p.2-35)

#Set Parameters
gpib.write(tds,"FAC") #Reset to factory default (p. 2-21)
time.sleep(5)
gpib.write(tds,"BELL")
gpib.write(tds,"SELECT:CH1 ON;CH2 ON;CH3 OFF;CH4 OFF") #Ch on or off
gpib.write(tds,"HOR:MAI:SCAl 100.0E-9") #Set Time Scale
gpib.write(tds,"CH1:SCAL 500.0E-3 ") # Set Voltage Scale
gpib.write(tds,"CH1:IMP FIF ") # SET Impedance to 50 Ohm, for 1M use MEG
gpib.write(tds,"CH1:POS 0") #y-Position
gpib.write(tds,"CH2:SCAL 500.0E-3 ") 
gpib.write(tds,"CH2:IMP FIF ") 
gpib.write(tds,"CH2:POS 0")

#Set Trigger
gpib.write(tds,"TRIG:MAI:EDGE:SLO FALL") #change Slope Fall or Rise
gpib.write(tds,"TRIG:MAI:EDGE:SOU CH1") #Trigger Source
gpib.write(tds,"TRIG:MAI:LEV -100.0E-3") #Trigger y-Position
	
gpib.close(tds)
