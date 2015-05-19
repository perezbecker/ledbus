from bart_api import BartApi

bart = BartApi()

data=[]

all_predictions=bart.etd('MCAR')

for i in xrange(len(all_predictions)):
    times=[]
    destination=all_predictions[i]['abbreviation']
    times.append(destination)
    for j in xrange(len(all_predictions[i]['estimates'])):
        # print all_predictions[i]['estimates'][j]["minutes"]
        times.append(all_predictions[i]['estimates'][j]["minutes"])
    data.append(times)

print data
