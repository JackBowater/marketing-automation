import requests
import csv
import html
from html_extractor import html_extractor, email_formatter

#checks html for all occurances of the html before author. Outputs either None, a name, or a string of names
def multiple_author_check(test_html, test_end_html, r):
    end = 0
    authors = []
    for y in range(r.text.count(test_html)):
        (name, end) = html_extractor(test_html, end, test_end_html, r)
        #if name isn't already in authors list
        if name not in authors:
            authors.append(name)
    #join list together as string
    name = ','.join(authors)
    return name

#checks if webpage uses common html before author 
def author_check(test_html, test_end_html, r, splitter):
    first = None
    last = None
    if r.text.find(test_html) != -1:
        last = None
        name = multiple_author_check(test_html, test_end_html, r)
        #checks for any unwanted /s
        name = name.replace('/', '')
        #checks if there are no digits in name
        if any(map(str.isdigit, name)):
            name = None
        try:
            if splitter: 
                (first, last) = name.split(splitter)
            else:
                (first, last) = name.split(' ')
        except:
            first = name
    return first, last

def country_check(url, prefilled, r):
    domain_end = url.find('/', 9)
    url_domain = url[domain_end-3:domain_end]
    if 'lang="' != -1:
        (lang, foo) = html_extractor('lang="', 0, '"', r)
    else:
        lang = 'en'

    if prefilled:
        return prefilled, lang
    elif url_domain.startswith('.') and url_domain != '.tv':
        return url_domain[1:3].upper(), lang
    elif lang == 'en-GB':
        return 'UK', lang
    elif lang == 'en' or 'en-US':
        return None, lang
    else:
        return lang.upper(), lang
    
title_html = [['"headline":"', '"'],['<title>', '</title>']]
time_html = [['article:modified_time" content="', '"'],['dateModified" content="', '"'],['published_time" content="', '"'],['publishDate":"', '"'],['datePublished": "', '"'],['datePublished":"', '"'],['datetime="', '"']]

def multiple_html_check(html_list, r):
    html = None
    for x in html_list:
        if r.text.find(x[0]) != -1:
            (html, foo) = html_extractor(x[0], 0, x[1], r)
            break
    return html
    
generic_author_db = [['Person","name":"', '"'],['"author":["', '"']]

def db_checker(url, country_code):
    #opens db containing website url, html before author, html after author, email format, name separator, country code.
    data = csv.reader(open('website_data.csv', 'r'), delimiter=',')
    try:
        r = requests.get(url, timeout=15)
    except:
        return None, None, None, None, None, None
    #defines variables
    first = None
    last = None
    title = None
    #initial country check
    (country, lang) = country_check(url, country_code, r)
    time = multiple_html_check(time_html, r)
    if time:
        time = time[:10]
    #checks if url can be accessed by script
    if r.status_code == 200:
        #trys to pull snippet
        title = multiple_html_check(title_html, r)
        if title:
            title = html.unescape(title.strip())
        for x in data:
            #checks if domain is listed in website_data.csv
            if url.startswith('https://'+x[0]):
                #if country is listed in website_data.csv, change it
                if x[5]:
                    country = x[5]
                #pulls author and email from website_data.csv
                (first, last) = author_check(x[1], x[2], r, x[4])
                email = email_formatter(first, last, x[3])
                #outputs first name, last name, email
                return first, last, email, country, title, time
        #trys generic test to pull author name from schema, otherwise outputs blank in all cases
        for x in generic_author_db:
            if first == None:
                (first, last) = author_check(x[0], x[1], r, None)
    return first, last, None, country, title, time