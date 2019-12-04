#import library
import pymysql
import nltk
from unidecode import unidecode
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import time

#define stopword
factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()

#define stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

#define pattern
rel  = ('gempa')
rel1 = ('mag', 'wib', 'lok', 'kedlmn')
rel2 = ('timur', 'tenggara', 'selatan', 'barat daya', 'barat', 'barat laut', 'utara', 'timur laut')

R1 = 'Relevan'
R2 = 'Tidak Relevan'
Relevan = ""

L1 = 'Lengkap'
L2 = 'Tidak Lengkap'
Lengkap = ""

#Declare Connection
conn = pymysql.connect(host='localhost', port='', user='root', passwd='', db='tes_coba', use_unicode=True, charset="utf8mb4")
cur = conn.cursor()

#Get Current Date Time
curdatetime = time.strftime("%Y-%m-%d %H:%M:%S")

#get data from database
cur.execute("SELECT text FROM `tweet2`")
row = cur.fetchall()

n = 1
for text in row:
    L = 0
    R = 0
    textfix = unidecode(str(text)).lower()          #lower text
    text_token = (nltk.word_tokenize(str(textfix))) #tokenize
    text_stop = stopword.remove(str(text_token))    #stopword
    text_stem = stemmer.stem(str(text_stop))        #stemming  
    print("\n")
    print(text_stem)

    for i in rel:
        if i in text_stem.lower():
            R=R+100

    print(R)
    if R >= 100 :
        Relevan = R1
    elif R < 100 :
        Relevan = R2
    print(Relevan)
    cur.execute("UPDATE tweet2 SET relevance=%s WHERE no=%s",
               (str(Relevan), str(n)))
    
    for ii in rel1:
        if ii in str(text_stem):
                L=L+20
    for iii in rel2:
        if iii in str(text_stem):
                L=L+20

    print(L)
    if L > 50 :
        Lengkap = L1
    else :
        Lengkap = L2
    print(Lengkap)
    cur.execute("UPDATE tweet2 SET complete=%s WHERE no=%s",
               (str(Lengkap), str(n)))
    n = n + 1
    
    
conn.commit()
cur.close()
conn.close()
