import json
import os
import csv
from bs4 import BeautifulSoup

cwd = os.getcwd()
files = []

def locate(files, absolute_start, absolute_end):
    relative_posts = absolute_end - absolute_start
    pages = int((relative_posts - (relative_posts % 20))/20) 
    
    #Repeat Process for all full pages
    for page in range(pages):
        #Calculate start, end, and offset based on total minus something.
        limit = 20
        start = absolute_start + (limit * (page))
        end = absolute_start + (limit * (page)+ limit)   
        files.append((start, end))
    
    #Process Exceptions
    limit = relative_posts - (pages)*20
    end = pages * 20 
    if end != absolute_end:
        
        #Process for not full pages
        if absolute_start % 20 == 0:
            start = (20 * (pages)) + (absolute_start - (absolute_start % 20))
            
        #Process if absolute start was not on a multiple of 20
        else:
            start = absolute_end - (absolute_end - absolute_start) % 20
            
        #Make things right
        end = absolute_end     
        files.append((start, end))
    
def load(start, end):
    locate(files, start, end)
    for item in files:
        print(str(item[0]) + "-" + str(item[1]))
        with open(cwd + "\\JSONs\\" + str(item[0]) + "-" + str(item[1]) + ".json") as data_file:
            data = json.load(data_file)
        with open('Data.csv', 'a', newline='\n') as csvfile:
            for post in range(item[1]-item[0]):
                writer = csv.writer(csvfile, delimiter=' ', quotechar=' ',
                                     quoting=csv.QUOTE_MINIMAL)
                for trail in range(10):
                    try:
                        row = data['response']['posts'][post]['trail'][trail]['content_raw']
                        soup = BeautifulSoup(row, "html.parser")
                        soup = soup.string
                        if soup != "" and soup != " ":
                            writer.writerow([soup.string])
                        else:
                            pass
                    except:
                        pass
load(0, 23573)

    