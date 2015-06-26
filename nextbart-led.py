from bart_api import BartApi
import string

localdir="/home/pi/ledbus/"
#localdir="/Users/dperezbecker/hackday/ledbus/"

bart = BartApi()

# FIRST ROW IN DISPLAY ROCKRIDGE BART

data=[]

predictions_ROCK=bart.etd('ROCK')
for i in xrange(len(predictions_ROCK)):
    times=[]
    destination=predictions_ROCK[i]['abbreviation']
    times.append(destination)
    for j in xrange(len(predictions_ROCK[i]['estimates'])):
        # print all_predictions[i]['estimates'][j]["minutes"]
        times.append(predictions_ROCK[i]['estimates'][j]["minutes"])
    data.append(times)

# Train destinations to consider for ROCK: SFIA-y, MLBR-y
output=[]

for k in xrange(len(data)):
    if(data[k][0] == 'SFIA' or data[k][0] == 'MLBR'):
        color = 'y'
    else:
        color = 'not_of_interest'        
    for l in xrange(len(data[k])-1):
        if(data[k][l+1] != 'Leaving' and color != 'not_of_interest'):
            output.append(data[k][l+1].zfill(2)+color)
        elif(data[k][l+1] == 'Leaving' and color != 'not_of_interest'):
            output.append('00'+color)

top3 = sorted(output)            
for m in xrange(3):
    top3.append('  p')


barttimes=top3[0]+top3[1]+top3[2]


# END FIRST ROW IN DISPLAY ROCKRIDGE BART

# print data
# print top3
# print barttimes


# BEGIN SECOND ROW IN DISPLAY DOWNTOWN BERKELEY BART

data=[]

predictions_DBRK=bart.etd('DBRK')
for i in xrange(len(predictions_DBRK)):
    times=[]
    destination=predictions_DBRK[i]['abbreviation']
    times.append(destination)
    for j in xrange(len(predictions_DBRK[i]['estimates'])):
        # print all_predictions[i]['estimates'][j]["minutes"]
        times.append(predictions_DBRK[i]['estimates'][j]["minutes"])
    data.append(times)

# Train destinations to consider for DBRK: FRMT-y, DALY-r, MLBR-r
output=[]

for k in xrange(len(data)):
    if(data[k][0] == 'FRMT'):
        color = 'y'
    elif(data[k][0] == 'DALY' or data[k][0] == 'MLBR'):
        color = 'r'
    else:
        color = 'not_of_interest'        
    for l in xrange(len(data[k])-1):
        if(data[k][l+1] != 'Leaving' and color != 'not_of_interest'):
            output.append(data[k][l+1].zfill(2)+color)
        elif(data[k][l+1] == 'Leaving' and color != 'not_of_interest'):
            output.append('00'+color)

top3 = sorted(output)            
for m in xrange(3):
    top3.append('  p')
      

barttimes=barttimes+top3[0]+top3[1]+top3[2]

# print data
# print top3
# print barttimes

barttimes=barttimes.translate(string.maketrans('0','O'))

f = open(localdir+"barttimes",'w')
f.write(barttimes+"\n")
f.close()
