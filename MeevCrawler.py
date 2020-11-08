import requests
import json
import time

#Auth and Tumblr
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""
blog_url = "meevs.net"

#Probe for Initial Total Posts 
url = 'https://api.tumblr.com/v2/blog/{}/posts/text?api_key={}&notes_info=true&limit{}&offset={}'.format(
     blog_url, CONSUMER_KEY, str(1),str(0))
probe = requests.get(url)
probe = probe.json()
initalTotalPosts = probe['response']['total_posts']
current_pages = initalTotalPosts
print ("Total Posts:" + str(initalTotalPosts))
current_requests = 0 


#0 is first post, ~totalPosts Last
def retrieve(absolute_start, absolute_end, total_posts):

    #Calculate relative posts from Absolute posts and pages
    relative_posts = absolute_end - absolute_start
    pages = int((relative_posts - (relative_posts % 20))/20) 
    
    # Prints how many pages and posts it is downloading
    if relative_posts % 20 > 0:
        actual_pages = pages + 1
    else:
        actual_pages = pages
    print ("Downloading " + str(actual_pages) + " page(s), Posts: " + str(absolute_start) + "-" + str(absolute_end))
    
    #Process for all full pages
    for page in range(pages):
        #Calculate start, end, and offset based on total minus something.
        limit = 20
        start = absolute_start + (limit * (page))
        end = absolute_start + (limit * (page)+ limit)   
        offset = total_posts - (limit*(page+1))
        
        download(page, start, end, limit, offset)
        
    #Process Exceptions
    limit = relative_posts - (pages)*20
    end = pages * 20 
    if end != absolute_end:
        
        #Process for not full pages
        if absolute_start % 20 == 0:
            start = (20 * (pages)) + (absolute_start - (absolute_start % 20))
            offset = total_posts - (limit+pages*20)
            
        #Process if absolute start was not on a multiple of 20
        else:
            start = absolute_end - (absolute_end - absolute_start) % 20
            offset = total_posts - (limit+pages*20)

        
        #Make things right
        end = absolute_end 
        
    download(page, start, end, limit, offset)
    
    
def download(page, start, end, limit, offset):
    #Print current status of pages and posts 
    print ("Page: " + str(page+1) + "/" + str(current_pages) + " Current Posts: " + 
           str(start) + "-" + str((end)) + 
           " Offset: " + str(offset) + " Limit: " + str(limit))
    
    #Generate url
    url = 'https://api.tumblr.com/v2/blog/{}/posts/text?api_key={}&notes_info=true&limit={}&offset={}'.format(
    blog_url, CONSUMER_KEY, str(limit), str(offset))
    
    #Download Page
    raw_json = requests.get(url)
    raw_json = raw_json.json()
    current_pages = raw_json['response']['total_posts']
    
    
    #Save JSON output 
    with open(str(start) + "-" 
              + str(end) + ".json", 'w') as fp:
        json.dump(raw_json, fp)
    current_requests = current_requests + 1
    
    #Handles if API calls exceed rate limit
    if raw_json['meta']['status'] != 200 or current_requests >= 1000:
        time.sleep(10)
        
#Function Call
retrieve(0, initalTotalPosts, initalTotalPosts)

