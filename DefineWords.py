## Needed for determining how long the operation takes
import time
start_time = time.clock()
## End of time implementation until printing

directory = 'DictionaryFiles/'   ##Working Directory
Indexer = ['A', 'Babble', 'Carditis', 'Counsel', 'Doe', 'Federal', 'Haggis', 'Insulated', 'Magnificoes', 'Obey', 'Planetary', 'Reckon', 'Self-indignation', 'Stipulation', 'Trace', 'Wearisome']
## ^^^ For determining which dictionary to check, English dictionary is split
## ^^^ into 16 sections, beginning with these words.

## Reads input file and splits into list
wordlist = []
f = open("input.txt",'r').read().lower()
f = "\n".join(f.split())
for each in f.split('\n'): ##Works if separated by spaces or newlines.
    if each != '':
        wordlist.append(each)
## End of reading input (From now on file input is stored as a list)


##Clears defset.html, and prepares the file for outputting
f = open('defset.html','w')
f.write('<!DOCTYPE html>\n<html>\n <head></head>\n <body>') ##Writes necessary HTML parts
f.write('\n  <table border="1">\n   <tr>\n    <th>Word</th>\n    <th>PoS</th>\n    <th>Definition</th>\n   </tr>\n') ##Writes basics for the table
    
##Compares 2 words, returns the one that comes earlier alphabetically
def alphacompare(inp, comp, check): ##inp = inputted value, comp = value its compared to, check = digit being checked
    if inp == comp:
        return inp
    inp = inp.lower()
    comp = comp.lower()
    if len(inp)==check:    ##If 2 words have the same letters, the shorter comes 1st 
        return inp         ##ex: short < shorter
    elif len(comp)==check:
        return comp
    elif ord(inp[check])>ord(comp[check]):
        return comp
    elif ord(inp[check])<ord(comp[check]):
        return inp
    else:
        return alphacompare(inp, comp, check+1)  ##If checked letters are the same, check the next letter


##Alphabetizes a list of words, using alphacompare
def alphabetize(L): ##Wrapper for alphacompare
    aL=[]
    while len(L)>0:
        currentlow = 'ZZZZZ'
        i=0
        while i<len(L):
            currentlow = alphacompare(currentlow,L[i],0)
            i+=1
        aL.append(currentlow)
        L.remove(currentlow)
    return aL

##Alphabetizes input word list:
wordlist = alphabetize(wordlist)

##Finds which of the 16 dictionary parts a word is located within
def findmark(word):
    i = 0
    while i<16:
        if alphacompare(word,Indexer[i],0)==word:
            return i-1
        i+=1
    return 15


##MAIN Dictionary indexing function
##Consults the dictionary for the part of speech and definition
def consultdic(word):     ##Runs on a string, generates the rest
    num = str(findmark(word))      ##Picks correct dictionary file
    r = open(directory+'dict'+num+'.txt','r')
    complist = r.read().split('\n')
    i = 0
    stop = len(complist)
    while i< stop: ##Complist is a list of dictionary entries. [1] is the word, [3] is the PoS, [5] is the def
        currline = complist[i].split("'")  ##Line being read (Reads every line in dictionary section)
        currword = currline[1]             ##Word of line being read
        if currword.lower()==word.lower():  ##If the line being read is for the word being defined
            if word in wordlist:   ##If its a word that should appear on the final list (not a subdefinition)
                f.write('   <tr>\n    <td>'+currword+'</td>\n    <td>'+currline[3]+'</td>\n    <td>'+handlemulti(complist[i:])+'</td>\n   </tr>\n')
            return currword+'   '+currline[3]+'   '+handlemulti(complist[i:]) ##Returns word's entry, ends function call
        i+=1
    print 'ERROR: word "'+word+'" not found. Check Spelling.' ##Lets the user know when theres an error.
    return ''

##Handles instances of multiple definitions, combines them
def handlemulti(complist): ##Complist is a section of the dictionary
    word = complist[0].split("'")[1] ##The word being checked for alt definitions
    i = 1
    while True:   ##Keeps track of indicies of entries of the same word
        currline = complist[i].split("'")
        last = i
        if not word==currline[1]:
            break
        else:
            i+=1
        
    outp = ''
    i = 0
    while i<last:   ##Defines all instances of the word
        currline = complist[i].split("'")
        outp+= currline[5] + checkAlts(currline[5])
        if not i == last-1:
            outp = outp[:-1]
            outp+=' OR '
        i+=1
    return outp

##Fixes recursive definitions
def checkAlts(s): ##Where s is the definition of the word
    if s[:8] == 'Alt. of ':
        return ' ('+consultdic((s[8:]).lower())+')' 
    if s[:3] == 'of ':
        return ' ('+consultdic((s[3:]).lower())+')'
    else: return ''
    
##Runs program on each word in current word list
for each in wordlist: consultdic(each)

print "Done. Completed in "+str(time.clock() - start_time)+" seconds."

#Fixes the last bits of HTML       
f.write('  </table>\n </body>\n</html>')
f.close()

#So the user has time to read the errors before exiting
raw_input("Press Enter to exit.")
