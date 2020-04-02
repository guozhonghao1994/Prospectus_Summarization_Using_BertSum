import time
import re
import requests
import bs4
from edgar.company import Company


# name = 'Baidu, Inc.'
# CIK = '0001329099'
# 
name = 'Alibaba Group Holding Ltd'
CIK = '0001577552'
# 
# name = 'Bilibili Inc.'
# CIK = '0001723690'

# name = 'Tesla, Inc.'
# CIK = '0001318605'

company = Company(name, CIK)
link = company.get_filings_url(filing_type = '424B4')


r = requests.get(link)
data = r.text
link_list =re.findall(r'href=\"(.+\-index.htm)', data)
link1 = 'https://www.sec.gov' + link_list[0]


r = requests.get(link1)
data = r.text
link_list =re.findall(r'href=\"(\/Archives.+\.htm)\"', data)
link2 = 'https://www.sec.gov' + link_list[0]


resp = requests.get(link2)
soup = bs4.BeautifulSoup(resp.text, "html.parser")
tables = soup.findAll('table')
num = []
a = len(tables)
for i in range(a-1):
    if tables[i].find('tr',{'bgcolor': '#cceeff'}) != None:
        num.append(i)


if num == []:
    for table in tables:
        table.decompose()
else:
    for i in num:
        tables[i].decompose()


# # Extract summary from the full text and pre-processing


summary_lst = re.findall('PROSPECTUS SUMMARY([\s\S]+)RISK FACTORS\s+',soup.text)

summary = str(summary_lst[0])
summary = summary.replace('\xa0', ' ')
summary = summary.replace('. \n', '.\n')
sum_name = name + CIK + '_summary.txt'
with open(sum_name,'w',encoding= 'utf-8') as f2:
    f2.write(summary)


summary = open(sum_name, 'r', encoding = 'utf-8')
lines = summary.readlines()
txt = []
for line in lines:
    if '.\n' in line:
        txt.append(line)
    else:
        if (line != '\n') & ('Table of Contents' not in line) & ('Table of Contents'.upper() not in line):
            line = line.replace('\n', ' ')
            txt.append(line)
clean = ''.join(txt)
clean = re.sub(r'(\d+){1,2}(\s+){2,}','',clean)
#clean = re.sub(r'Table of Contents', '',clean,re.I)



clean_name = CIK +'_clean_summary.txt'
# clean_name = name + CIK +'_clean_summary.txt'
f2 = open(clean_name,'w',encoding='utf-8')
f2.write(clean)
f2.close()



summary = open(clean_name, 'r', encoding = 'utf-8')
lines = summary.readlines()
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
clean = ''.join(txt)


f2 = open(clean_name,'w',encoding='utf-8')
f2.write(clean)
f2.close() 


test = open(clean_name, 'r', encoding = 'utf-8')
lines = test.readlines()
for line in lines:
    if len(str(line).split()) > 512:
        #print(2)
        print(len(str(line).split()))


clean = clean.replace('.','. [CLS] [SEP]')
with_CLS = CIK +'_clean_summary_with_CLS_and_SEP.txt'
# with_CLS = name + CIK +'_clean_summary_with_CLS_and_SEP.txt'
f3 = open(with_CLS,'w',encoding='utf-8')
f3.write(clean)
f3.close()


# # Extract the body and pre-processing


body_lst = re.findall('RISK FACTORS([\s\S]+)',soup.text)
body = str(body_lst[0])
body = body.replace('\xa0', ' ')
body = body.replace('. \n', '.\n')
body_name = name + CIK + '_body.txt'
with open(body_name,'w',encoding= 'utf-8') as f2:
    f2.write(body)


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


body_clean_name = name + CIK +'_body_clean.txt'
f2 = open(body_clean_name,'w',encoding='utf-8')
f2.write(body_clean)
f2.close()



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


f2 = open(body_clean_name,'w',encoding='utf-8')
f2.write(body_clean)
f2.close() 


test = open(body_clean_name, 'r', encoding = 'utf-8')
lines = test.readlines()
for line in lines:
    if len(str(line).split()) > 512:
        #print(2)
        print(len(str(line).split()))


body_clean = body_clean.replace('.','. [CLS] [SEP]')
body_with_CLS = name + CIK +'_body_clean_with_CLS_and_SEP.txt'
f3 = open(body_with_CLS,'w',encoding='utf-8')
f3.write(clean)
f3.close()