import csv
#clears output.csv so that you don't have to keep deleting it manually. Can be removed if not wanted.
refresh = open(r"output.csv",'w')

reader = csv.reader(open(r"input.csv"),delimiter=',', quotechar='"')
data = list(reader)
#get columns number of the two needed columns. Every column before status is assumed to be needed.
status_position = data[0].index('ZB Status')
gender_position = data[0].index('ZB Gender')

#outputs list of required columns for each row.
def row_generator(status, gender):
    out = []
    for x in range(status+1):
        out.append(row[x])
    out.append(row[gender])
    return out

#checks if status is not equal to invalid. If it's not, writes filtered row to output.csv.
reader = csv.reader(open(r"input.csv"),delimiter=',', quotechar='"')
for row in reader:
    if row[status_position] != 'invalid':
        csv.writer(open(r"output.csv",'a', newline='')).writerow(row_generator(status_position, gender_position))