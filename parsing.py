# import logg ing
from distutils.log import ERROR
import requests
from requests import Response
from bs4 import BeautifulSoup
# from mysql import connector
from bs4.element import NavigableString
import logging
import sqlite3

con = sqlite3.connect('uzmoviebotdb.db')
cur = con.cursor()
# config = {
#     'user':'mirabror',
#     'password':'devmir1998@@',
#     'host':'127.0.0.1',
#     'database':"uzmoviebotdb",
#     "raise_on_warnings":True
# } 
logging.basicConfig(level=ERROR)
logging.basicConfig(level = logging.DEBUG)

# connection = connector.connect(**config)
# cursor_genre = connection.cursor()
# cursor_category = connection.cursor()

"""tables"""
# cursor = connection.cursor()
# with open("Copy of Untitled Diagram.sql", "r") as f1:
#     tbs = (f1.read()).split("\n\n")
#     for tb in tbs:
#         cursor.execute(tb)
#         print("1")
 
class Moviebot():
    
    """class Moviebot// uzmovi.com"""
    
    main_url = "http://uzmovi.com/"
    
    
    def __init__(self, next_url):
        self.next_url = next_url
        
    
    def take_content(self, number="", url=""):
        if number == "" and url == "":
            data = requests.get(self.main_url + self.next_url, timeout=10)
            return BeautifulSoup(data.text, features='html.parser')
        elif number != "":
            data = requests.get(self.main_url + self.next_url + number,timeout=10)
            return BeautifulSoup(data.text, features='html.parser')
        else:
            if url !="":
                data = requests.get(url, timeout=10)
                return BeautifulSoup(data.text, features='html.parser')
         
    
    def get_page_urls(self, number=""):
        page_urls = []
        content = self.take_content(number)
        div = content.find("div", id="news_set_sort")
        div2_list = div.find_next_siblings(class_="shortstory-in categ")
        for div in div2_list:
            page_urls.append((div.a)['href'])
        return page_urls
        
    def take_pagination_number(self):
        content = self.take_content()
        div = content.find('div', class_="pages-numbers")
        div_content = div.contents
        return div_content[-1].string
    
    def get_all_movie_urls(self):
        urls=[]
        range1 = self.take_pagination_number()
        for i in range(int(range1)):
            content = self.get_page_urls(f"/page/{i}")
            urls += content                
        return urls
    
    def take_all_movie_data(self):
        list1 = []
        for i in self.get_all_movie_urls()[::-1]:
            data = self.take_content(url=i)
            div = data.find("div", id="fstory-film")
            
            div2 = div.find('div', class_="finfo-title", string="Nomi")
            movie_name = (div2.find_next_sibling('div', class_="finfo-text")).string
                     
            div2 = div.find('div', class_="finfo-title", string="Davlati")
            if div2 == None:
                movie_country = ""
            else:
                movie_country = (div2.find_next_sibling('div', class_="finfo-text")).string
                
            div2 = div.find('div', class_="finfo-title", string="Sanasi")
            if div2 == None:
                movie_year = 2017
            else:
                div_year = (div2.find_next_sibling('div', class_="finfo-text")).string
                if ('.' in div_year) or ("HD, TAS-IX"==div_year) or ("2017, TAS-IX"==div_year) :
                    movie_year = 2017 
                else:
                    movie_year = int(div_year)
                            
            div2 = div.find('div', class_="finfo-title", string="Tili")
            if div2 == None:
                movie_lan= ""
            else:
                movie_lan = (div2.find_next_sibling('div', class_="finfo-text")).string
            
            div2 = div.find('div', class_="finfo-title", string="Davomiyligi")
            if div2 == None:
                movie_duration = ""
            else:
                movie_duration = (div2.find_next_sibling('div', class_="finfo-text")).string
            
            movie_views_count = 4253
            
            img = div.find('img')
            movie_banner = img['data-src']
                     
            source_link = i
            
            div2 = (div.find("div", class_="finfo-title", string="Janr")) 
            if div2 == None:
                movie_genres = ""
            else:
                div_genre = div2.find_next_sibling()
                movie_genres = [a.string for a in div_genre.find_all("a")]
            
            
            
            list1.append([movie_name, movie_country, (movie_year), movie_lan, movie_duration, movie_views_count, movie_banner, source_link])
        return list1
         
         
# serial = Moviebot('serial')
# serial_data = serial.take_all_movie_data()

# multfilm = Moviebot('multfilm')
# multfilm_data = multfilm.take_all_movie_data()

# uzbek_kino = Moviebot('uzbek-kinolar')
# uzbek_data = uzbek_kino.take_all_movie_data()

# premyera = Moviebot("xfsearch/year/2022")
# premyera_data = premyera.take_all_movie_data()

# trailer = Moviebot("treyler")
# trailer_data = trailer.take_all_movie_data()

# hind = Moviebot('hind-kinolar')
# hind_data = hind.take_all_movie_data()
 
# show = Moviebot("konsert")
# show_data = show.take_all_movie_data()

# militant = Moviebot("jangari")
# militant_data = militant.take_all_movie_data()

# ujas = Moviebot("ujas")
# ujas_data = ujas.take_all_movie_data()

# history = Moviebot('tarixiy')
# history_data = history.take_all_movie_data()

# comedy = Moviebot('comediy')
# comedy_data = comedy.take_all_movie_data()

# drama = Moviebot('drama')
# drama_data = drama.take_all_movie_data()

# melodrama = Moviebot('melodrama')
# melodrama_data = melodrama.take_all_movie_data()

# adventure = Moviebot("sarguzasht")
# adventure_data = adventure.take_all_movie_data()

# klassika = Moviebot("klassika")
# klassika_data = klassika.take_all_movie_data()

# fantastika = Moviebot('fantastika')
# fantastika_data = fantastika.take_all_movie_data()


biography = Moviebot("biografy")
biography_data = biography.take_all_movie_data()

# query = (   
#         "INSERT INTO movies(title, country, released_year, language, duration, views_count, banner_link, source_link)"
#         "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
# )

query = (   
        "INSERT INTO movies(title, country, released_year, language, duration, views_count, banner_link, source_link)"
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
)
# # , 'uzbek-kinolar', 'xfsearch/year/2022', 'treyler', 'hind-kinolar', 'konsert', 'jangari', 'ujas' ,'tarixiy', 'comediy', 'drama' , 'melodrama' , 'sarguzasht' , 'klassika', 'fantastika', 'biografy'
# for type in ['serial', 'multfilm'  ]:
#     movie_data = Moviebot(type).take_all_movie_data()
#     for data in movie_data:
#         if data == None:
#             continue
#         else:
#             cur.execute(query, tuple(data))
#             # print(type(data))


for data in biography_data:
    if data == None:
        continue
    else:
        cur.execute(query, tuple(data))
        print(type(data))
print("finished...")
con.commit()
con.close()    
# connection.commit()
# connection.cursor()













































 