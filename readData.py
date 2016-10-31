
nTrigs = 100 #number of triggers is going to be stored 

import os
i = 0
while os.path.exists("run%s.txt" % i):
    i += 1

#Create output file
import sys
f = open("run%s.txt" % i, "w")
#sys.stdout = f # redirect output for all prints to the file

#print data and time
from datetime import datetime
f.write(str(datetime.now())+"\n")

import gpib
import time
tds= gpib.find("tds744") # define in /etc/gpib.conf

def query(handle, command, numbytes=100000):
	gpib.write(handle,command)
	time.sleep(0.01)
	response = gpib.read(handle,numbytes)
	response = response.replace('\n','')
	return response
def write(handle, command):
  gpib.write(handle,command)
  time.sleep(2)

print query(tds,"*IDN?") #ask for ID, simple test if the scope does response (page 2-21 of Programmer Manual)

#Set Parameters
write(tds,"FAC") #Reset to factory default (p. 2-21)
time.sleep(10)
write(tds,"BELL")
write(tds,"SELECT:CH1 ON;CH2 ON;CH3 ON;CH4 OFF") #Ch on or off
write(tds,"DATA:SOURCE  CH1,CH2,CH3")#Set channel for feding data from
write(tds,"HOR:MAI:SCAl 100.0E-9") #Set Time Scale
write(tds,"CH1:SCAL 200.0E-3 ") # Set Voltage Scale
write(tds,"CH1:IMP FIF ") # SET Impedance to 50 Ohm, for 1M use MEG
write(tds,"CH1:POS 0") #y-Position

write(tds,"CH2:SCAL 1.0E-3 ") 
write(tds,"CH2:IMP FIF ") 
write(tds,"CH2:POS 0")
write(tds,"CH2:BANDWIDTH TWENTY")
write(tds,"CH2:OFFS -0.00165")

write(tds,"CH3:SCAL 1.0E-3 ") 
write(tds,"CH3:IMP FIF ") 
write(tds,"CH3:POS 0")
write(tds,"CH3:BANDWIDTH TWENTY")
write(tds,"CH3:OFFS -0.0012")


#Set Trigger
write(tds,"TRIG:MAI:EDGE:SLO FALL") #change Slope Fall or Rise
write(tds,"TRIG:MAI:EDGE:SOU CH1") #Trigger Source
write(tds,"TRIG:MAI:LEV -200.0E-3") #Trigger y-Position
#Set Data Format
write(tds,"DATA:ENCDG ASCI") #set the convenient data reading format(p. 2-34, p.2-35)
write(tds,"BELL")

time1 = time.time()
## Read data by trigger 
trigsSaved = 0
while trigsSaved<nTrigs:
  breaker = False
  AutoAuto = False
  while 0<1:
    trigState1 = query(tds,"TRIG:STATE?")
    trigState2 = query(tds,"TRIG:STATE?")
    #print trigState1, " ", trigState2
    if (trigState1 == ":TRIG:STATE AUTO" and trigState2 == ":TRIG:STATE AUTO"): AutoAuto = True
    if (trigState1 == ":TRIG:STATE AUTO" and trigState2 != ":TRIG:STATE AUTO") or (AutoAuto and trigState1 != ":TRIG:STATE AUTO" and trigState2 != ":TRIG:STATE AUTO"):
      AutoAuto = False
      breakCounter = 0
      while breakCounter<100:
	trigState3 = query(tds,"TRIG:STATE?")
	if trigState3 == ":TRIG:STATE REA":
	  gpib.write(tds,"BELL")
	  time2 = time.time()
	  f.write("timediff %s\n" % (time2 - time1) )
	  time1 = time.time()
	  f.write(query(tds,"CURVE?")+"\n")
	  breaker = True
	  break
	breakCounter += 1
      if breaker:
	trigsSaved += 1
	f.write("saved trigers: %s\n" % trigsSaved) 
	time.sleep(0.5)
	break




gpib.close(tds)
f.close()
