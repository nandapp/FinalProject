#Import the necessary methods from tweepy library
import tweepy
import pymysql
import nltk
from unidecode import unidecode
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

#Variables that contains the user credentials to access Twitter API 
access_token = "1224754879-W3GemB5jCRm4VTrPPS13rgLhPGLpzoiEt1iARa8"
access_token_secret = "aJEUW4k9fBIQ5rcYYRGpH0UzzXByV6rMoYUSIJHYqxYwe"
consumer_key = "yxAbP3ypx6AbO8YfcKzsIVkdW"
consumer_secret = "hFOb7Ss4qY9mlQLwdm1A32jcO0y4ivuzG6brY2VxFORosVEw0s"

#Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#define stopword
factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()

#define stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

#Declare Connection
conn = pymysql.connect(host='localhost', port='', user='root', passwd='', db='tes_coba', use_unicode=True, charset="utf8mb4")
cur = conn.cursor()

#get data from database
cur.execute("SELECT user FROM `rt6`")
row = cur.fetchall()

n=1
for text in row:
    textfix = unidecode(str(text)).lower()          #lower text
    text_token = (nltk.word_tokenize(str(textfix))) #tokenize
    text_stop = stopword.remove(str(text_token))    #stopword
    text_stem = stemmer.stem(str(text_stop))        #stemming  
    print("\n")
    print(text_stem)
    
    try:
        #Get Identity of BMKG in Twitter
        user = api.get_user(text_stem)
        print ("Name:", user.name)
        print ("Name:", user.screen_name)
        print ("Number of tweets: " + str(user.statuses_count))
        print ("followers_count: " + str(user.followers_count))
        print ("Account location: ", user.location)
        print ("Account created at: ", user.created_at)
        print ("Account geo enabled: ", user.geo_enabled)

        cur.execute("UPDATE rt6 SET location=%s WHERE no=%s",
               (str(user.location), str(n)))
    except tweepy.error.TweepError:
        print("user not found")
        cur.execute("UPDATE rt6 SET location=%s WHERE no=%s",
               (str("user not found"), str(n)))
    except UnicodeEncodeError:
        print("unicode error")
        cur.execute("UPDATE rt6 SET location=%s WHERE no=%s",
               (str("unicode error"), str(n)))    

    n=n+1

conn.commit()
cur.close()
conn.close()
