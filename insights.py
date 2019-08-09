import json
import requests
import datetime

def get_post():

url_post = “https://graph.facebook.com/v4.0/”<span style=”color: rgb(255, 0, 0);” data-mce-style=”color: #ff0000;”>Your Post Name</span>”/?fields=posts.limit(99)%7Btype%2Ccreated_time%2Cid%2Cpermalink_url%2Cmessage%7D&amp;access_token=” + key
count = 0
rows_post = []
rows_post.append([“id”,”post_type”,”created_time”,”permalink_url”,”message”,”impression”,”like”,”comment”,”share”,”click”])
while True:
response_post = requests.get(url_post)
response_post.raise_for_status()
FBPost = json.loads(response_post.text)
if count &gt; 20: # Set time out = 20 (times) calling Facebook API. Maximum post the program can handle is 99 * 20 = 1980
return rows_post
elif count == 0:
for item in FBPost[“posts”][“data”]:

temp_post_type = item.get(“type”,””)
temp_createdtime = item.get(“created_time”,””)
temp_id = item.get(“id”,””)
temp_permlink = item.get(“permalink_url”,””)
temp_message = item.get(“message”,””)
temp = [temp_id,temp_post_type,temp_createdtime,temp_permlink,temp_message]
print(temp)
dateObject = datetime.strptime(temp_createdtime,’%Y-%m-%dT%H:%M:%S+0000′) # Parse time format – originated from stackoverflow
if dateObject &lt; startDate:
return rows_post
rows_post.append(temp)
url_post = FBPost[“posts”][“paging”][“next”] # Using the “next” field to be the new url
count = count + 1
else:
for item in FBPost[“data”]:

temp_post_type = item.get(“type”,””)
temp_createdtime = item.get(“created_time”,””)
temp_id = item.get(“id”,””)
temp_permlink = item.get(“permalink_url”,””)
temp_message = item.get(“message”,””)
temp_message = temp_message.translate(non_bmp_map) # Using transition table to replacing non-BMP
temp = [temp_id,temp_post_type,temp_createdtime,temp_permlink,temp_message]
print(temp)
dateObject = datetime.strptime(temp_createdtime,’%Y-%m-%dT%H:%M:%S+0000′) # Copy from stackoverflow
if dateObject &lt; startDate:
return rows_post
rows_post.append(temp)
url_post = FBPost[“paging”][“next”] # Using the “next” field to be the new url
count = count + 1
[/code]

# The other one is to retrieve all the required metrics for a specific post. The facebook API actually allows for getting multiple metrics and bundles them together in one call.  Here I used three:  Impression(post_impressions), Engagement(post_story_adds_by_action_type) and Clicks(post_consumptions_by_type_unique).
# [code language=”python”]
def get_post_metrics(post_id):

metric1 = ‘post_impressions’
metric2 = ‘post_story_adds_by_action_type’
metric3 = ‘post_consumptions_by_type_unique’
url = ‘https://graph.facebook.com/v2.9/’ + post_id + ‘/insights/’ + metric1 + ‘,’ + metric2 + ‘,’ + metric3 + ‘?access_token=’ + key
response = requests.get(url)
response.raise_for_status()
post_metrics = json.loads(response.text)
impression = 0
like = 0
comment = 0
share = 0
click = 0
fb_impression = post_metrics[‘data’][0] # Parse impression metric
if fb_impression[‘name’]==’post_impressions’:
impression = fb_impression[‘values’][0].get(“value”,0)

fb_engagement = post_metrics[‘data’][1] # Parse engagement metrics: like, share, comments
if fb_engagement[‘name’]==’post_story_adds_by_action_type’:
like = fb_engagement[‘values’][0][‘value’].get(“like”,0)
comment = fb_engagement[‘values’][0][‘value’].get(“comment”,0)
share = fb_engagement[‘values’][0][‘value’].get(“share”,0)

fb_click = post_metrics[‘data’][2] # Parse clicks metric
if fb_click[‘name’]==’post_consumptions_by_type_unique’:
click = fb_click[‘values’][0][‘value’].get(“link clicks”,0)

Print([impression, like, comment, share, click]) 