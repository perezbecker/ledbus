# Super simple NextBus display thing (prints to console).

import time
from predict import predict
import string

localdir="/home/pi/ledbus/"

# List of bus lines/stops to predict.  Use routefinder.py to look up
# lines/stops for your location, copy & paste results here.  The 4th
# element on each line can then be edited for brevity if desired.
stops = [
( 'sf-muni', 'N', '3915', 'to Downtown' ),
( 'sf-muni', '6', '5898', 'to Downtown' ),
( 'sf-muni', 'N', '3912', 'to Wastelands' ),
( 'sf-muni', '33', '4963', 'to Final del Infinito' ),
#( 'sf-muni', '7', '4720', 'to Downtown' ),
]

# Populate a list of predict objects from stops[].  Each then handles
# its own periodic NextBus server queries.  Can then read or extrapolate
# arrival times from each object's predictions[] list (see code later).
predictList = []
for s in stops:
	predictList.append(predict(s))

# time.sleep(1) # Allow a moment for initial results

LetterTime=["A","B","C","D","E","F"]


#Colorschema 1
#nextbuscolor=["w","b","c","g","y","r"]
#white 0 to 4:59 min
#blue 5 to 9:59 min
#cyan 10 to 14:59 min
#green 15 to 19:59 min
#yellow 20 to 24:59 min
#red> 25 min 
#pink no_bus/error


#Colorshema 2
nextbuscolor=["w","g","y","y","r","r"]
#white 0 to 4:59
#green 5 to 9:59
#yellow 10 to 19:59
#red > 20

bus1_color="p"
bus2_color="p"

time_since_last_response = 0

while (time_since_last_response < 60):

    currentTime = time.time()


    ledspot=0
    ledtext=""
    #lastquery=0

 
    time_since_last_response_array=[]




    for pl in predictList:
        
	time_since_last_response_array.append(int(time.time()-pl.lastQueryTime))

	busorder=0
        print pl.data[1] + ' ' + pl.data[3] + ':'
        if pl.predictions: # List of arrival times, in seconds
            #print min(pl.predictions)
            
            if(len(pl.predictions)>1):
                delta_t1=pl.predictions[1]-pl.predictions[0]
            
                if(delta_t1 > 0 and delta_t1 < 1500):
                    bus1_color=nextbuscolor[int(delta_t1/300)]
                elif(delta_t1 >= 1500):
                    bus1_color=nextbuscolor[5]
                else:
                    bus1_color="p"
            else:
                bus1_color="p"
            
            if(len(pl.predictions)>2):
                delta_t2=pl.predictions[2]-pl.predictions[1]

                if(delta_t2 > 0 and delta_t2 < 1500):
                    bus2_color=nextbuscolor[int(delta_t2/300)]
                elif(delta_t2 >= 1500):
                    bus2_color=nextbuscolor[5]
                else:
                    bus2_color="p"
            else:
                bus2_color="p"
            
        
            for p in pl.predictions:
                # Extrapolate from predicted arrival time,
                # current time and time of last query,
                # display in whole minutes.
                t = p - (currentTime - pl.lastQueryTime)
                print '\t' + str(int(t/60)) + ' minutes'
                # print '\t' + str(t/60) + ' min'
                if(ledspot != 1):
                    if(busorder == 0):
                        
                        if(t<600 and t>=0):
                            ledtext=ledtext+str(int(t/60))+LetterTime[int((t%60)/10)]+bus1_color
                        
                        elif(t<0):
                            ledtext=ledtext+"<0"+bus1_color
                        elif(t>5940):
			    ledtext=ledtext+"++"+bus1_color                     
			else:
                            ledtext=ledtext+str(int(t/60))+bus1_color
                        ledspot=ledspot+1
                else:
                    if(busorder == 1):
                        if(t<600 and t>=0):
                            ledtext=ledtext+str(int(t/60))+LetterTime[int((t%60)/10)]+bus2_color
                        
                        elif(t<0):
                            ledtext=ledtext+"<0"+bus2_color
			elif(t>5940):
			    ledtext=ledtext+"++"+bus2_color                        
                        else:
                            ledtext=ledtext+str(int(t/60))+bus2_color
                        ledspot=ledspot+1
                            
                busorder=busorder+1    
        else:
            print '\tNo predictions'
            ledtext=ledtext+"--"+"p"
        
	#lastquery=pl.lastQueryTime
    

    time_since_last_response = max(time_since_last_response_array)
    
    if(time_since_last_response < 100):
    	ledtext=ledtext+str(time_since_last_response).zfill(2)+"c"
    else:
	ledtext=ledtext+"99c"
     

    print ledtext,time_since_last_response
    ledtext=ledtext.translate(string.maketrans('0','O'))
    
    if (time_since_last_response < 57):
        f = open(localdir+"bustimes",'w')
        #f.write(ledtext[0:6]+"\n") # python will convert \n to os.linesep
        #f.write(ledtext[6:12]+"\n") # python will convert \n to os.linesep
	f.write(ledtext+"\n")
	f.close()
    else:
        f = open(localdir+"bustimes",'w')
        f.write("XXpXXpXXpXXpXXpXXp\n") # python will convert \n to os.linesep
        #f.write("XXXXXX") # python will convert \n to os.linesep
	f.close()
    	
	g = open(localdir+"buserrors",'a')
	g.write("Time:"+str(time.time())+" last response:"+str(time_since_last_response)+"\n")
	g.close()


    prevTime = currentTime;
    time.sleep(1) # Refresh every ~5 seconds
