from summarizer import Summarizer
import os
from tqdm import tqdm

text_file_path = [n for n in os.listdir() if n.find('.txt') != -1]

for text_path in tqdm(text_file_path):
    with open(text_path,'r',encoding='UTF-8') as file:
        df = file.readlines()
    for content in df: 
        content = [content.replace('\n','')]
        content = ['TITLE'] + content
        title = 'TITLE'
        text = content[-(len(content)-1):]
    
        input = {'title':title,'text':' '.join(text)}
        input['text'] = input['text'].encode('UTF-8').decode("ascii","ignore")
        input['text'] = " ".join(input['text'].replace('\n',' ').split())
    
        summarizer = Summarizer()
        result = summarizer.summarize(input['text'], input['title'], 'Undefined', 'Undefined')
        result = summarizer.sortScore(result)
        result = summarizer.sortSentences(result[:2])
        
        with open(text_path[:-4]+'_teaser.txt','a',encoding='UTF-8') as file:
            for num,r in enumerate(result):
                file.write(r['sentence'] + '\n')
                file.write('score: ' + str(r['totalScore']) + '\n')
                file.write('order: ' + str(r['order']) + '\n')
                if num != len(result)-1:
                    file.write(40*'-' + '\n')
                    
        with open(text_path[:-4]+'_teaser.txt','a',encoding='UTF-8') as file:
            file.write(100*'='+'\n')
        
        
