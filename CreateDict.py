import time
start_time = time.clock() #Timer for efficiency reasons

#Working Directory:
directory = 'DictionaryFiles/'


with open(directory+'englishdictionary.txt') as f:
    content = f.readlines()


## Shove the dictionary parts into different files
i=0
while i<len(content):
    o = open(directory+'dict'+str(i)+'.txt','w')
    o.write(content[i])
    o.close()
    i+=1


## Format those aforementioned dictionary parts
i = 0
while i <= 15:
    f = open(directory+'dict'+str(i)+'.txt','r')
    currline = f.read()[1:-3]
    output = '\n'.join(currline.split('),('))
    f.close()
    o = open(directory+'dict'+str(i)+'.txt','w')
    o.write(output)
    o.close()
    i+=1






print "Complete. Took "+str(time.clock()-start_time)+" seconds"
