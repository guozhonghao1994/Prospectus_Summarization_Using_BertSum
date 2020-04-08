#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import re
import requests
import bs4
from edgar.company import Company #web scraping package for edgar system
import os

os.chdir('C:/Users/Administrator/Desktop/amber/NLP/project')


# # EDGAR web scraping

# name = 'Baidu, Inc.'
# CIK = '0001329099'
# 
# name = 'Alibaba Group Holding Ltd'
# CIK = '0001577552'
# 
# name = 'Bilibili Inc.'
# CIK = '0001723690'
# 
# name = 'Tesla, Inc.'
# CIK = '0001318605'
# 
# name = 'Pinduoduo Inc.'
# CIK = '0001737806'
# 
# name = 'Futu Holdings Ltd'
# CIK = '0001754581'
# 
# name = 'GSX Techedu Inc.'
# CIK = '0001768259'
# 
# name = 'Uber Technologies, Inc'
# CIK = '0001543151'
# 
# name = 'DouYu International Holdings Ltd'
# CIK = '0001762417'

# In[520]:


#%%time
name = 'Alibaba Group Holding Ltd'#input1 for the edgar package
CIK = '0001577552'#input2 for the edgar package
company = Company(name, CIK)
link = company.get_filings_url(filing_type = '424B4') #get the url for 424B4 (i.e. IPO prospectus) filing catalogue page
filename = name.replace(' ','_')

# In[541]:


#link


# In[522]:


#get the filing link in the filing catalogue page
#%%time
r = requests.get(link)
data = r.text
link_list =re.findall(r'href=\"(.+\-index.htm)', data)
link1 = 'https://www.sec.gov' + link_list[0]


# In[523]:


#get the full file link in htm format
#%%time
r = requests.get(link1)
data = r.text
link_list =re.findall(r'href=\"(\/Archives.+\.htm)\"', data)
link2 = 'https://www.sec.gov' + link_list[0]


# In[542]:


#link2


# In[525]:


#use beautiful soup to do web scraping
#%%time
resp = requests.get(link2)
soup = bs4.BeautifulSoup(resp.text, "html.parser")

#since the BertSum package only focuses on the text in the prospectus, we need to find out all the tables that contains numbers and delete them
tables = soup.findAll('table')
num = []
a = len(tables)
#some companies include the dot points using table format, so we need to separate all the tables with numbers
for i in range(a-1):
    if tables[i].find('tr',{'bgcolor': '#cceeff'}) != None:
        num.append(i)
#print(num)


# In[526]:


#decompose the tables from the web page
if num == []:
    for table in tables:
        table.decompose()
else:
    for i in num:
        tables[i].decompose()


# # Extract summary from the full text and pre-processing

# In[527]:

with open('soup.txt','w',encoding = 'utf-8') as f:
    f.write(soup.text)
    
#find prospectus summary and save it into list
summary_lst = re.findall('PROSPECTUS SUMMARY([\s\S]+)RISK FACTORS\s+',soup.text)
summary = str(summary_lst[0])

#deal with punctuation marks
summary = summary.replace('\xa0', ' ')
summary = summary.replace('. \n', '.\n')
#save it into a file
sum_name = filename + CIK + '_summary.txt'
with open(sum_name,'w',encoding= 'utf-8') as f2:
    f2.write(summary)


# In[528]:


summary = open(sum_name, 'r', encoding = 'utf-8')
lines = summary.readlines()
txt = []
#delete all of the blank lines and 'table of contents'
for line in lines:
    if '.\n' in line:
        txt.append(line)
    else:
        if (line != '\n') & ('Table of Contents' not in line) & ('Table of Contents'.upper() not in line):
            line = line.replace('\n', ' ')
            txt.append(line)
clean = ''.join(txt)
#delect numbers which as pages
clean = re.sub(r'(\d+){1,2}(\s+){2,}','',clean)


# In[529]:


clean_name = filename + CIK +'_clean_summary.txt'
f2 = open(clean_name,'w',encoding='utf-8')
f2.write(clean)
f2.close()


# In[530]:


summary = open(clean_name, 'r', encoding = 'utf-8')
lines = summary.readlines()
txt = []
for line in lines:
    #delete sub-titles
    line = re.sub(r'\A[\s]*[A-Z]{1}(\w+)[\s\w]*(\s+){2}','',line)
    #delete titles in case some companys may exclude some content of prospectus summary into another part
    line = re.sub(r'\A([A-Z\s]+)(\s+){3}','',line)    
    #to match BertSum find paragraph longer than 512 words, if so separate it into 2 paragraphs
    if len(str(line).split()) > 512:
        #print(1)
        #print(len(str(line).split()))
        sent_lst = line.split('.')
        i = 0
        for sent in sent_lst:
            i += len(str(sent).split())
            if i > 512:
                index = sent_lst.index(sent)
                sent_lst[index-1] = sent_lst[index-1].replace('.','.\n')  
                fst = '.'.join(sent_lst[:index])
                scd = '.'.join(sent_lst[index:])  
                break
    else:
        txt.append(line)
clean = ''.join(txt)


# In[531]:


f2 = open(clean_name,'w',encoding='utf-8')
f2.write(clean)
f2.close() 


# In[532]:


test = open(clean_name, 'r', encoding = 'utf-8')
lines = test.readlines()
for line in lines:
    if len(str(line).split()) > 512:
        #print(2)
        print(len(str(line).split()))


# In[533]:

#for extraction model, need to add [CLS][SEP] at the end of each sentence
clean = clean.replace('. ','. [CLS][SEP]')
with_CLS = filename + CIK +'_clean_summary_with_CLS_and_SEP.txt'
f3 = open(with_CLS,'w',encoding='utf-8')
f3.write(clean)
f3.close()

'''
# # Extract the body and pre-processing
# basic idea is same as extracting the prospectus summary, for details, please see the comments above
# In[534]:


body_lst = re.findall('RISK FACTORS([\s\S]+)',soup.text)
body = str(body_lst[0])
body = body.replace('\xa0', ' ')
body = body.replace('. \n', '.\n')
body_name = filename + CIK + '_body.txt'
with open(body_name,'w',encoding= 'utf-8') as f2:
    f2.write(body)


# In[535]:


body = open(body_name, 'r', encoding = 'utf-8')
lines = body.readlines()
txt = []
for line in lines:
    if '.\n' in line:
        txt.append(line)
    else:
        if (line != '\n') & ('Table of Contents' not in line) & ('Table of Contents'.upper() not in line):
            line = line.replace('\n', ' ')
            txt.append(line)
body_clean = ''.join(txt)
body_clean = re.sub(r'(\d+){1,2}(\s+){2,}','',body_clean)


# In[536]:


body_clean_name = filename + CIK +'_body_clean.txt'
f2 = open(body_clean_name,'w',encoding='utf-8')
f2.write(body_clean)
f2.close()


# In[537]:


body_clean = open(body_clean_name, 'r', encoding = 'utf-8')
lines = body_clean.readlines()
txt = []
for line in lines:
    line = re.sub(r'\A[\s]*[A-Z]{1}(\w+)[\s\w]*(\s+){2}','',line)
    line = re.sub(r'\A([A-Z\s]+)(\s+){3}','',line)
    if len(str(line).split()) > 512:
        #print(1)
        #print(len(str(line).split()))
        sent_lst = line.split('.')
        i = 0
        for sent in sent_lst:
            i += len(str(sent).split())
            if i > 512:
                index = sent_lst.index(sent)
                sent_lst[index-1] = sent_lst[index-1].replace('.','.\n')  
                fst = '.'.join(sent_lst[:index])
                scd = '.'.join(sent_lst[index:])  
                break
    else:
        txt.append(line)
body_clean = ''.join(txt)


# In[538]:


f2 = open(body_clean_name,'w',encoding='utf-8')
f2.write(body_clean)
f2.close() 


# In[539]:


test = open(body_clean_name, 'r', encoding = 'utf-8')
lines = test.readlines()
for line in lines:
    if len(str(line).split()) > 512:
        #print(2)
        print(len(str(line).split()))


# In[540]:


body_clean = body_clean.replace('. ','. [CLS] [SEP]')
body_with_CLS = filename + CIK +'_body_clean_with_CLS_and_SEP.txt'
f3 = open(body_with_CLS,'w',encoding='utf-8')
f3.write(clean)
f3.close()
'''
