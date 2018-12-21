import bs4 
from bs4 import BeautifulSoup as soup
import re
from urllib.request import urlopen as req # kullanırken urrlib.request yazmak yerine req diye kısaltıldı
from FlaskWebProject1.functions import *

class basic_site(object):
    keywords_counts = {}
        
    def __init__(self,name):
        self.name = name
        self.page_soup = get_page(self.name)
    def set_keyword_counts(self, keywords):
        self.page_soup = turkish_character_control(str(self.page_soup))
        for word in keywords:
            word = turkish_character_control(word)
            self.keywords_counts[word] = find_keyword_count(self.page_soup,word)
        return self.keywords_counts

class site(object):
    keywords = []
    keywords_counts = {}
    keywords_counts_in_all_urls = {}
    first_depth = []
    second_depth = {}
    def __init__(self,url,keywords): #constructor fonksiyon sitenin urlsi geliyor 
        self.name = url
        self.keywords = keywords
        self.page_soup = get_page(self.name)
        self.page_soup = turkish_character_control(str(self.page_soup))        
        for word in self.keywords_counts:
            word = turkish_character_control(word)
            self.keywords_counts[word] = find_keyword_count(self.page_soup,word)
            self.keywords_counts_in_all_urls[word] = self.keywords_counts[word]

    def init_first_depth(self):
        page = get_page(self.name)
        if page is not "":
            for link in page.find_all('a'):
                sub_url = link.get('href')
                if (sub_url.startswith("http") is False and sub_url is not '#') or sub_url.startswith(self.name):
                    if(sub_url.startswith(self.name)):
                        self.first_depth.append(basic_site(sub_url))
                    else:
                        self.first_depth.append(basic_site(self.name+sub_url))
        self.first_depth = list(set(self.first_depth))
        return
    def init_second_depth(self):
        for pages in self.first_depth:
            if pages.page_soup is not "":
                self.second_depth[pages] = []
                for link in pages.page_soup.find_all('a'):
                    sub_url = ""
                    sub_url = link.get('href')
                    if (sub_url.startswith("http") is False and sub_url is not '#' and sub_url is not "") or sub_url.startswith(self.name):
                        if sub_url.startswith(self.name):
                            self.second_depth[pages].append(basic_site(sub_url))                            
                        else:
                            self.second_depth[pages].append(basic_site(self.name+sub_url))
                self.second_depth[pages] = list(set(self.second_depth[pages]))
        return
    def init_keyword_counts(self):
        for page in self.first_depth:
            result = page.set_keyword_counts(self.keywords)
            for it in result:
                self.keywords_counts_in_all_urls[it] += result[it]           
        for key in self.second_depth:
            key.set_keyword_counts(self.keywords)
            for page in self.second_depth[key]:
                result = page.set_keyword_counts(self.keywords)
                for it in result:
                    self.keywords_counts_in_all_urls[it] += result[it] 
        return
    def get_tree(self):
        return self.second_depth
    def get_keywords_counts(self):
        self.init_first_depth();
        self.init_second_depth();
        self.init_keyword_counts();
        return self.keywords_counts_in_all_urls