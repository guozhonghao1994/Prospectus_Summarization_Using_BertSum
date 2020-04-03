## Prospectus Summarization Using BertSum

![License](https://img.shields.io/badge/license-apache2_2-blue.svg)

**This code is for NLP final report** [Prospectus Summarization Using BertSum](https://github.com/guozhonghao1994/Prospectus_Summarization_Using_BertSum/blob/master/Final%20Report.pdf)

### [Goal](#readme)
We aim to use a deep-learning model called BertSum to summarize IPO prospectus. IPO prospectus is an important source of information. It provides information on business model, competition, risks and opportunities, and financial situations. However, it is usually a very long legal document. It could be very time-consuming to go through the whole legal document. Therefore, in order to help generate a big picture of the company, we tried to use BertSum to further condense summary part. This would be helpful especially when you are not familiar with the company and the industry that it operates in.

### [Web Scraping and Data Cleaning](#readme)
See `.\get_prospectus\get_prospectus.py`. You need the **Company Name** as well as **CIK** to get the 424B prospectus from *U.S. SECURITIES AND EXCHANGE COMMISSION* website. Commonly, it will create 6 text files:
- raw prospectus
- raw summary
- cleaned prospectus
- cleaned summary
- cleaned prospectus with [CLS][SEP] tokens
- cleaned summary with [CLS][SEP] tokens

**Warning**: 
- *You should manually adjust the format of cleaned text file. For example, you should delete the last [CLS][SEP] for each paragraph, you should delete [CLS][SEP] in decimals, names, etc.*
- *You should delete the space in file name when running BertSum.*

### [TextRank & TextTeaser](#readme)
We compare the performance of BertSum with TextRank & TextTeaser. In `./textrank` and `./textteaser` folder, you will see code, raw text and summarized text. Notice that this two models are just for reference. We would like to show how powerful BertSum is when comparing with obsolete algos.

### [Preparation](#readme)
We borrowed the idea from [Fine-tune BERT for Extractive Summarization](https://arxiv.org/pdf/1903.10318.pdf) and [Text Summarization with Pretrained Encoders](https://www.aclweb.org/anthology/D19-1387.pdf). The [author](https://github.com/nlpyang/PreSumm/tree/dev) has given us well-trained models and preprocessed data already. We can directly download from her Google Drive.
#### Download the processed data
[Pre-processed data](https://drive.google.com/file/d/1DN7ClZCCXsk2KegmC6t4ClBwtAf5galI/view), unzip the zipfile and put all .pt files into `./bert_data`
#### Trained models
[CNN/DM Extractive](https://drive.google.com/file/d/1kKWoV0QCbeIuFt85beQgJ4v0lujaXobJ/view), unzip the zipfile and put .pt file into `./models/ext`

[CNN/DM Abstractive](https://drive.google.com/file/d/1-IKVCtc4Q-BdZpjXc4s70_fRsWnjtYLr/view), unzip the zipfile and put .pt file into `./models/abs`

#### Package Requirements
Python 3.6

`torch==1.1.0` `pytorch_transformers` `tensorboardX` `multiprocess pyrouge`

### [Usage](#readme)
#### Extractive
```
python train.py -task ext -mode test_text -test_from MODEL_PATH -text_src RAW_TEXT_PATH -result_path OUTPUT_PATH -log_file LOG_PATH -visible_gpus -1
```

#### Absractive
```
python train.py -task abs -mode test_text -test_from MODEL_PATH -text_src RAW_TEXT_PATH -result_path OUTPUT_PATH -log_file LOG_PATH -visible_gpus -1
```
