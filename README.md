## Prospectus Summarization Using BertSum

![License](https://img.shields.io/badge/license-apache2_2-blue.svg)

### Goal
We aim to use a deep-learning model called BertSum to summarize IPO prospectus. IPO prospectus is an important source of information. It provides information on business model, competition, risks and opportunities, and financial situations. However, it is usually a very long legal document. It could be very time-consuming to go through the whole legal document. Therefore, in order to help generate a big picture of the company, we tried to use BertSum to further condense summary part. This would be helpful especially when you are not familiar with the company and the industry that it operates in.

### Web Scraping and Data Cleaning
See `.\get_prospectus\get_prospectus.py`. You need the **company name** as well as **CIK** to get the 424B prospectus from *U.S. SECURITIES AND EXCHANGE COMMISSION* website. 
