
# coding: utf-8

# First set up new environment by installing phantomjs along with Selenium binding for Python
# 

# ## 网上信息爬虫：
#     目的：爬出正面导向和负面导向的新闻，以此为训练文本数据
#     难题：研报是java借口，靠普通爬虫捕捉不到，需要一个虚拟web了视线完整爬虫
# # 
# $ mkdir scraper && cd scraper
# $ brew install phantomjs
# $ virtualenv venv
# $ source venv/bin/activate
# $ pip install selenium
# # In[1]:


from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pickle


# ### 正面研报链接

# In[2]:


pos_yan_bao = ['http://data.eastmoney.com/report/#dHA9MSZjZz0wJmR0PTImcGFnZT0x',
               'http://data.eastmoney.com/report/#dHA9MSZjZz0wJmR0PTImcGFnZT0y',
               'http://data.eastmoney.com/report/#dHA9MSZjZz0wJmR0PTImcGFnZT0z',
               'http://data.eastmoney.com/report/#dHA9MSZjZz0wJmR0PTImcGFnZT00',
               'http://data.eastmoney.com/report/#dHA9MSZjZz0wJmR0PTImcGFnZT01',
               'http://data.eastmoney.com/report/#dHA9MSZjZz0wJmR0PTImcGFnZT02',
               'http://data.eastmoney.com/report/#dHA9MSZjZz0wJmR0PTImcGFnZT03',
               'http://data.eastmoney.com/report/#dHA9MSZjZz0wJmR0PTImcGFnZT04',
               'http://data.eastmoney.com/report/#dHA9MSZjZz0wJmR0PTImcGFnZT05',
               'http://data.eastmoney.com/report/#dHA9MSZjZz0wJmR0PTImcGFnZT0xMA==',
               'http://data.eastmoney.com/report/#dHA9MSZjZz0wJmR0PTImcGFnZT0xMQ==',
               'http://data.eastmoney.com/report/#dHA9MSZjZz0wJmR0PTImcGFnZT0xMg==',
               
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0x',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0y',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0z',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT00',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT01',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT02',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT03',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT04',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT05',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0xMA==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0xMQ==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0xMg==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0xMw==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0xNA==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0xNQ==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0xNg==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0xNw==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0xOA==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0xOQ==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0yMA==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0yMQ==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0yMg==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0yMw==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0yNA==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0yNQ==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0yNg==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0yNw==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0yOA==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0yOQ==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0zMA==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0zMQ==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0zMg==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0zMw==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0zNA==',
               'http://data.eastmoney.com/report/#dHA9MiZjZz0wJmR0PTImcGFnZT0zNQ=='
               
              ]


# ### 负面研报链接

# In[3]:


neg_yan_bao = ['http://data.eastmoney.com/report/#dHA9MyZjZz0wJmR0PTQmcGFnZT0x',
               'http://data.eastmoney.com/report/#dHA9MyZjZz0wJmR0PTQmcGFnZT0y',
               'http://data.eastmoney.com/report/#dHA9MyZjZz0wJmR0PTQmcGFnZT0z',
               'http://data.eastmoney.com/report/#dHA9MyZjZz0wJmR0PTQmcGFnZT00',
               'http://data.eastmoney.com/report/#dHA9MyZjZz0wJmR0PTQmcGFnZT01',
               'http://data.eastmoney.com/report/#dHA9MyZjZz0wJmR0PTQmcGFnZT02',
               'http://data.eastmoney.com/report/#dHA9MyZjZz0wJmR0PTQmcGFnZT03',
               'http://data.eastmoney.com/report/#dHA9MyZjZz0wJmR0PTQmcGFnZT04'
              ]


    
    


# 用PhantomJS来爬去Javascript的运行tag

# In[4]:


def web_scrape(url, link_l):
    driver = webdriver.PhantomJS()
    driver.get(url)
    s = BeautifulSoup(driver.page_source,'lxml')
    temp = []
    for link in s.findAll('a', attrs={'href': re.compile("^/report/[0-9]+/")}):
        temp.append(link.get('href'))
    link_l = link_l+["http://data.eastmoney.com"+s for s in temp]
    print(len(link_l))
    return link_l


# In[5]:


pos_url = []
for url in pos_yan_bao:
#     print(url)
    try:
        pos_url = web_scrape(url, pos_url)
    except:
        pass
neg_url = []
for url in neg_yan_bao:
#     print(url)
    try:
        neg_url = web_scrape(url, neg_url)
    except:
        pass


# In[ ]:



def extract_article(url,art = {}):
    #url
    #art: dictionary 集 Key：新闻标题， Value：新闻本体
    driver = webdriver.PhantomJS()
    driver.get(url)
    s = BeautifulSoup(driver.page_source,'lxml')
    s.find_all("div", attrs={'class': re.compile("^report-content")})
    pattern = re.compile(r"\>[*+]\<")
    cleanr = re.compile(r"<[^>]*>")
    
    title = re.sub(cleanr, '', str(s.find_all("div", attrs={'class': re.compile("^report-title")})[0].find_all("h1")[0]))
    content= re.sub(cleanr, '', str(s.find_all("div",attrs={'class': re.compile("^newsContent")})))
    print(title) 
    if(len(art)<=3):
         print(content)
    art[title] = content
    return art


# ### 正面新闻集收集：

# In[ ]:


#pos_path = "/Users/Jesica/Documents/igolden/sensitivity analysis/Scrapping/pos"
#neg_path = "/Users/Jesica/Documents/igolden/sensitivity analysis/Scrapping/neg"
#os.chdir(pos_path)
import json
import numpy as np
pos_art = {}
c = 0
print("end----")
for url in pos_url:
    try:
        print(url,c)
        pos_art = extract_article(url,pos_art)
        c = c+1
#         print(c)
    except:
        pass

print("end----")
with open("data/pos0307.JSON", 'w') as fp:
    json.dump(pos_art, fp)



# ### 负面新闻收集：

# In[ ]:


neg_art = {}
for url in neg_url:
    try:
        neg_art = extract_article(url, neg_art)
    except:
        pass

with open("data/neg0307.JSON", 'w') as fp:
    json.dump(neg_art, fp)

