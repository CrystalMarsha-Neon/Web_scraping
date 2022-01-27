from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
#mendapatkan link berita
class link_news:
    def __init__(self,page):
        self.page = page

    def get_single_link(self):
        all_link = []
        single_link = []
        for i in range(1,self.page+1):
            base_url = "https://www.detik.com"
            second_url = "/search/searchall?query=finance&siteid=29&sortby=time&page=%s" % i
            headers = {"Accept-Language" : "en-US, en;q=0.5"}
            url = base_url + second_url
            results = requests.get(url, headers=headers)
            soup = BeautifulSoup(results.text, "html.parser")
            li =[]
            for link in soup.find_all('a'):
                li.append(link.get('href'))

            word = 'finance.detik'
            exclusion = 'https://finance.detik.com'
            link_detik = [x for x in li if word in x and x != exclusion] 
            all_link.append(link_detik)
            for i in all_link:
                for j in i:
                    single_link.append(j)   
        unique_link = list(set(single_link))
        return unique_link

class news_scraping:
    def __init__(self,link):
            self.link = link
    
    def get_news(self):
        title = []
        author = []
        date = []
        link_picture = []
        content = []
        output = dict()
        results = requests.get(self.link)
        soup = BeautifulSoup(results.text, "html.parser")

        news = soup.find_all('article', class_='detail')
        for container in news:
            #title     
            title_name = container.find('h1',class_='detail__title').text.strip() if container.find('h1',class_='detail__title') else '-'

            #author
            author_name = container.find('div',class_='detail__author').text.strip() if container.find('div',class_='detail__author') else '-'

            #date
            date_of_post = container.find('div',class_='detail__date').text.strip() if container.find('div',class_='detail__date') else '-'

            #content
            news_content = container.find('div',class_ = 'detail__body-text itp_bodycontent').text.strip() if container.find('div',class_ = 'detail__body-text itp_bodycontent') else '-'

            #link picture
            try:
                image_tags = container.find_all('img', class_='p_img_zoomin img-zoomin')[0].attrs['src'] if container.find_all('img', class_='p_img_zoomin img-zoomin') else '-'  
            except:
                #mengantisipasi error karena link berbentuk video
                image_tags.append('error')


        #mengubah menjadi data frame
        output['title'] = title_name
        output['author'] = author_name
        output['date'] = date_of_post
        output['content'] =news_content.replace("\r\n","").replace('\n','')
        output['link_picture'] = image_tags
        output['url'] = self.link
        return output