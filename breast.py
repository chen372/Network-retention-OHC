import requests
import bs4
import json

#define functions to extract all needed variables
def username():
    users = []
    i = 1
    while i < 50:
        try:
            user = str(soup.find_all("span", { "class" : "username" })).split('<span class="username">')[i].split('</span>')[0]
            #print user
            users.append(user)
        except:
            pass
        i += 1
    return users

def posttime():
    post_times = []
    post_time = str(soup.find_all("div", { "class" : "submitted" })).split('>')[1].split('-')[0]
    post_times.append(post_time)

    i = 1
    while i < 50:
        try:
            reply_time = str(soup.find_all("span", { "class" : "submitted" })).split('<span class="submitted">')[i].split('-')[0]
            post_times.append(reply_time)
        except:
            pass
        i += 1
    return post_times

def text():
    texts = []
    i = 1
    while i < 50:
        try:
            text = str(soup.find_all("div", { "class" : "field-item even" })).split('<div class="field-item even"><p>')[i].split('</p></div>')[0]
            #print text
            texts.append(text)
        except:
            pass
        i += 1
    return texts

def postcount():
    post_counts = []
    i = 1
    while i < 50:
        try:
            s = str(soup.find_all("span", { "class" : "author-posts" })).split('Posts: ')[i]
            post_count = int(filter(str.isdigit, s))
            #print text
            post_counts.append(post_count)
        except:
            pass
        i += 1
    return post_counts

def jointime():
    join_times = []
    i = 1
    while i < 50:
        try:
            s1 = str(soup.find_all("span", { "class" : "author-regdate" })).split('Joined: ')[i]
            s2 = str(filter(str.isdigit, s1))
            join_time = s1.split()[0]+' '+s2
            join_times.append(join_time)
        except:
            pass
        i += 1
    return join_times

def reply():
    replies = []
    i = 1
    while i < 50:
        try:
            reply = {'user':users[i], 'post_time':post_times[i], 'text':texts[i]}
            replies.append(reply)
        except:
            pass
        i += 1
    return replies
	

for i in range(161,160,-1):
    posts = {}
    print i
    url = 'https://csn.cancer.org/forum/128?page='+str(i)
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text)
    links = []
    for tag in soup.find_all('a'):
        link = tag.get('href')
        try:
            if link.startswith('/node'):
                links.append(link)
        except:
            pass

    for link in links:
        url = 'https://csn.cancer.org'+link
        #print url
        resp = requests.get(url) 
        soup = bs4.BeautifulSoup(resp.text)

        #now extract all needed variables
        try:
            users = username()
            post_times = posttime()
            #post_counts = postcount()
            texts = text()
            #join_times = jointime()
            replies = reply()
        except:
            pass  
        
        try:       
            posts[link] = {'user':users[0],'post_time':post_times[0],'text':texts[0],'reply':replies}
        except:
            pass
	
	with open('D:/breast/colore_data'+str(i)+'.txt', 'w') as outfile:
		json.dump(posts, outfile)