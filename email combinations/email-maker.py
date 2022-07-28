import csv

#.csv file must be saved as CSV (MS-DOT)
data = csv.reader(open('input.csv', 'r'), delimiter=',')
output = open('output.txt', 'w', encoding='utf-16')

def writer(string, email):
    output = open('output.txt', 'a', encoding='utf-16')
    output.write(string+'@'+email+'\n')

def combinations(first, last, email):
    writer(last+first, email)       #lastfirst
    writer(first+last, email)       #firstlast
    writer(last+'.'+first, email)   #last.first
    writer(first+'.'+last, email)   #first.last
    writer(last[0]+'.'+first, email)   #l.first
    writer(first[0]+'.'+last, email)   #f.last
    writer(first[0]+last, email)    #flast
    writer(last[0]+first, email)    #lfirst
    writer(last+'.'+first[0], email)   #last.f
    writer(first+'.'+last[0], email)   #first.l
    writer(last+first[0], email)       #lastf
    writer(first+last[0], email)       #firstl

for x in data:
    #pulls first, last and email from input
    if x[0] == 'duplicate author':
        pass
    elif x[1] and not x[1].startswith(('{')):
        output.write(x[1])
    elif x[2] and x[3]:
        #defines first, last and email. Removes spaces and makes lower case
        first = x[2].replace(' ', '').lower()
        last = x[3].replace(' ', '').lower()
        if x[4].startswith('www.'):
            email = x[4][4:]
        else:
            email = x[4]
        #basic emails 
        combinations(first, last, email)
        #if first/last name as multiple words
        #just use first part of compound first name
        if x[2].find(' ') != -1:
            combinations(x[2][:x[2].find(' ')].lower(), last, email)
        #just use first part of compound last name
        if x[3].find(' ') != -1:
            combinations(first, x[3][:x[3].find(' ')].lower(), email)