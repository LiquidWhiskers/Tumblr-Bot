import csv
text = ""
badChars = ['*', '$', '%', '(', ')','+','-','/']
with open('Data.csv', 'r', encoding="utf-8") as file:
    text = file.read()
text = str(text)
for badChar in badChars:
    print(badChar)
    text = text.replace(badChar, "") 
text = text.replace("“","\"")
text = text.replace("”","\"")  
text =text.replace("„",',,')
import csv
temp = []

csvfile = open('Data.csv', newline='',encoding='utf-8')
reader = csv.reader(csvfile, delimiter=',', quotechar='|')
for row in reader:
    temp.append(row) 
csvfile.close()
print(len(temp))
for index in range(len(temp)):
    try:
        entry = temp[index][0]
    except IndexError:
        pass;
    print(entry)
    temp[index] = entry[1:len(entry)]                
def listToCsv(list, output):
    csvfile = open(output, 'w', newline='', encoding='utf-8') 
    writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for item in list:
        writer.writerow([item])      
    csvfile.close()
    



listToCsv(temp, 'Data.csv')