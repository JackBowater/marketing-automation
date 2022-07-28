import os
from dotenv import load_dotenv
import requests
import webbrowser
import csv
from html_extractor import html_extractor, email_formatter
import author_script

#pulls data from .env file
load_dotenv('.env') 

cookies = {'CONSENT': str(os.getenv("GOOGLE_CONSENT_COOKIE"))}
keyword = os.getenv("KEYWORD")
time_frame = os.getenv("TIME_FRAME")
num_searches = int(os.getenv("NUM_SEARCHES"))
tabs = os.getenv("TABS")
file_name = os.getenv("FILE_NAME")
search_type = os.getenv("SEARCH_TYPE")
country_code = os.getenv("COUNTRY_CODE").upper()

#creates list of keywords
keywords = keyword.split('\\')

#if output file doesn't exist, create it
if not os.path.exists(file_name+'.csv'):
    f = open(file_name+'.csv', 'w')

#writes data to file_name. Also checks if input is unique.
def data_exporter(duplicate, email, first, last, company, country, snippet, website, time):
    with open(file_name+'.csv', 'r+', encoding='utf-16', errors='ignore', newline='\n') as data:
        unique = True
        for row in csv.reader(data, delimiter=','):
            if (first, last, website) == (row[2], row[3], row[7]):
                unique = False
                break
            if (first, last) == (row[2], row[3]):
                duplicate = 'duplicate author'
        if unique:   
                writer = csv.writer(data, delimiter=',')
                writer.writerow([duplicate, email, first, last, company, country, snippet, website, time])

def captcha_check(url):
    captcha_test = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">'
    if captcha_test in url.text:
        errors = open('errors.txt', 'a')
        errors.write('Captcha needs refreshing.')
        quit()
    else:
        print('Captcha good.')

if '__main__' == __name__:
    #start up message to confirm some details
    if input('You are about to perform ' + str(num_searches*10) + ' searches of the keyword(s): ' + keyword.replace('\\', ', ').replace('+', ' ') +'. Are you sure? (y/n)') != "y":
        quit()
    #try to write title to file_name.csv. Also checks to see if file_name is open.
    try:
        data_exporter('duplicate author', 'email address', 'first name', 'last name', 'company', 'country', 'snippet', 'website', 'date published')
    except:
        input(file_name + '.csv is already open. Please close and press enter.')
    print('The script has begun. This can take a few minutes.')

    url = 'https://www.google.com/search?q={keyword}{search_type}{time}&start={num_searches}{country}'
    
    #sets correct url inputs
    #search type
    if search_type:
        search_url = '&tbm=nws'
    else:
        search_url = search_type
    #time frame
    if time_frame == '':
        time_url = ''
    elif time_frame in ['h', 'd', 'w', 'm', 'y']:
        time_url = '&tbs=qdr:{time}'.format(time = time_frame)
    else:
        time_url = '&tbs=ar:1'
    #country
    if country_code:
        country_url = '&cr=country{country_code}'.format(country_code = country_code)
    else:
        country_url = country_code
    #for loop using entries in keywords
    for y in keywords:
        #counter reset for print message
        counter = 0
        for x in range(num_searches):
            num_searches_url = x*10
        #performs google news search
            r=requests.get(url.format(keyword=y, search_type=search_url, time=time_url, num_searches=num_searches_url, country=country_url), cookies=cookies)
            captcha_check(r)
        #pulls links from google in groups of 10.
            position = r.text.find('<a href="/url?q=')
            for x in range(10):
                counter += 1
                print('Accessing page ' + str(counter) +' out of a maximum of ' + str(num_searches*10)+' for keyword "'+y+'".')
                (news_link, position) = html_extractor('<a href="/url?q=', position, '&', r)
                #filters all none url news links (errors)
                if news_link.startswith('https://'):
                    #filters all google links
                    if not news_link.startswith(('https://accounts.google.com', 'https://support.google.com', 'https://www.google.com')):
                        (first, last, email, country, title, time) = author_script.db_checker(news_link, country_code)
                        company = news_link.replace(('https://' or 'https://www.' or 'www.' or 'http://'), '')
                        #tries to break up authors to save them as individual fields
                        if first != None and first.find(',') != -1:
                            authors = first.split(',')
                            for x in authors:
                                try:
                                    (first, last) = x.split(' ')
                                except:
                                    first = x
                                new_email = email_formatter(first, last, email)    
                                data_exporter(None, new_email, first, last, company[:company.find('/')], country, title, news_link, time)
                        else:
                            data_exporter(None, email, first, last, company[:company.find('/')], country, title, news_link, time)
                        if tabs == '1':
                            webbrowser.open_new_tab(news_link)