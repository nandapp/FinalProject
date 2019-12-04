#Import the necessary methods from tweepy library
import tweepy
import pymysql
import time

#Variables that contains the user credentials to access Twitter API 
access_token = "1224754879-W3GemB5jCRm4VTrPPS13rgLhPGLpzoiEt1iARa8"
access_token_secret = "aJEUW4k9fBIQ5rcYYRGpH0UzzXByV6rMoYUSIJHYqxYwe"
consumer_key = "yxAbP3ypx6AbO8YfcKzsIVkdW"
consumer_secret = "hFOb7Ss4qY9mlQLwdm1A32jcO0y4ivuzG6brY2VxFORosVEw0s"

#Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Declare Connection
conn = pymysql.connect(host='localhost', port='', user='root', passwd='', db='ta_bmkg', use_unicode=True, charset="utf8mb4")
cur = conn.cursor()


#Delete Database
cur.execute("DELETE FROM tweet2pure order by no")


#Get Identity of BMKG in Twitter
user = api.get_user("108543358")
print ("Name:", user.name)
print ("Name:", user.screen_name)
print ("Number of tweets: " + str(user.statuses_count))
print ("followers_count: " + str(user.followers_count))
print ("Account location: ", user.location)
print ("Account created at: ", user.created_at)


i = 1

for Tweet in tweepy.Cursor(api.user_timeline, id=108543358).items(3500):
    text = str(Tweet.text.encode("utf-8"))
    if 'Gempa' not in text:
        continue
    print ("*****" + str(i) +"*****")
    print ("No: " + str(i))
    print ("ID: " + Tweet.id_str)
    print ("Text: " + text)
    #print ("Text: " + str(Tweet.text.encode("utf-8")))
    print ("Retweet Count: " + str(Tweet.retweet_count))
    print ("Favorite Count: " + str(Tweet.favorite_count))
    print ("Date Time: " + str(Tweet.created_at))
    print ("Geo:", Tweet.geo)
    print ("Coordinates:", Tweet.coordinates)
    print ("Retweeted:", Tweet.retweeted)
    print ("************")

    
    cur.execute("INSERT INTO tweet2pure (no, text, datetime_comp, retweet_count, favourite_count, date_time, relevance, on_time, complete) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s )",
    (str(i), str(text), str(Tweet.created_at), str(Tweet.retweet_count), str(Tweet.favorite_count), str(Tweet.created_at), str(Tweet.geo), str(Tweet.geo), str(Tweet.geo)))
    
    i = i + 1

conn.commit()
cur.close()
conn.close()

