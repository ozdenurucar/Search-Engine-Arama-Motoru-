import csv
import sqlite3 as db
import re
import bs4 
from urllib.request import urlopen as req # kullanırken urrlib.request yazmak yerine req diye kısaltıldı
from bs4 import BeautifulSoup as soup # kullanırken BeatifulSoup yazmak yerine soup olarak kısaltıldı
def get_page(url): # getpage fonksiyon tanımı
	try:
		client = req(url)
		page = client.read()
		client.close()
		return soup(page,"html.parser") # sayfa beatifulsoup ile parse edildi
	except:	
		return ""
	return ""

def find_keyword_count(page,keyword):
    wordlist=re.findall(r'\S+', page)#regular expression kullanarak boşluğa göre ayırma işlemi
    wordfreq = wordlist.count(keyword)
    return wordfreq

def turkish_character_control(text):
     characters = {'ı' : 'I', 'İ' : 'I', 'ö' : 'O', 'Ö' : 'O', 'ü' : 'U', 'Ü' : 'U', 'ş' : 'S', 'Ş' : 'S', 'ğ' : 'G', 'Ğ' : 'Ğ', ',' : ' ', "'" : ' ', ';' : ' ', '.' : ' '}
     for char in characters:
        for ch in text:
            if(char in ch):
                text=text.replace(ch,characters[ch])
     text = text.upper()
     return text

def get_keyword_count(input_url,keyword):
    page_soup = get_page(input_url)
    page_soup = turkish_character_control(str(page_soup))
    keyword = turkish_character_control(keyword)
    return find_keyword_count(str(page_soup),keyword)

def url_sorting(keywords,urls):
    keywords_counts = {}
    for word in keywords:
        keywords_counts[word] = []
        for url in urls:
            keywords_counts[word].append((get_keyword_count(url,word),url))
    score = {}
    for url in urls:
        score[url] = 0

    for iter in keywords_counts:
        keywords_counts[iter].sort(key=lambda tup: tup[0])
        point = 0
        for it in keywords_counts[iter]:
            if it[0] is not 0:
                score[it[1]] = score[it[1]] + 5*point
            point += 1
        point = 0
    url_score = []
    for it in score:
        url_score.append((score[it],it))
    url_score.sort()
    return (url_score,keywords_counts)

def web_site_sorting(sites,keywords):
    main_page = {}
    first_depth = {}
    for it in sites:
        main_page[it] = get_keyword_count(it)
        first_depth[it] = list(get_all_links(it))
    return ""

#3. Algoritma
def get_Tree(input_url,keyword):
    for it in input_url:
        site=class_site.site(it)
        page=get_page(it)
        for word in keyword:
            if page is not "":
                site.keyword_count=get_keyword_count(it,word)
                for link in page.find_all('a'):
                    sub_url = link.get('href')
                    if (sub_url.startswith("http") is False and sub_url is not '#') or sub_url.startswith(it):
                            site.first_depth[sub_url]=[]
                            if(sub_url.startswith(it)):
                                site.first_depth[sub_url].append((get_keyword_count(sub_url,word),keyword))
                                sec_page = get_page(sub_url)
                            else:
                                sub_url=it+sub_url
                                site.first_depth[sub_url]=[]
                                site.first_depth[sub_url].append((get_keyword_count(sub_url,word),keyword))
                                sec_page = get_page(it+sub_url)
                            if sec_page is not "":
                                 for urls in sec_page.find_all('a'):
                                    sub = str(urls.get('href'))
                                    if (sub.startswith("http") is False and sub is not '#') or sub.startswith(sub_url):
                                        if(sub.startswith(sub_url)):
                                            site.second_depth[sub]=(sub_url,(get_keyword_count(sub,word)))
                                        else:
                                            site.second_depth[sub]=(sub_url,get_keyword_count(sub_url+sub,word))



#4. Algoritma:Semantik Analiz
def get_synonyms(keyword):
    new_keywords = []
    with open('Esanlamli.csv',encoding='utf8') as csvfile:
       reader = csv.DictReader(csvfile)
       for row in reader:
            row['Kelime'] = turkish_character_control(row['Kelime'])
            row['Es'] = turkish_character_control(row['Es'])
            for word in keyword:
                word = turkish_character_control(word)
                if(row['Kelime'] == word):
                    new_keywords.append(row['Es'])
                    new_keywords.append(word)
                if(row['Es'] == word):
                    new_keywords.append(word)
                    new_keywords.append(row['Kelime'])
                new_keywords.append(word)
    return set(new_keywords)
