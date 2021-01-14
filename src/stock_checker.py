''' A library of functions to check the stock of items at certain electronics retailers. '''
import json
import requests
from bs4 import BeautifulSoup
import tldextract
import os 
from fake_useragent import UserAgent

os.chdir("..")
SOUNDPATH = os.getcwd() + "\\assets\\instock.mp3"
jsonfp = os.getcwd() + "\websites\\"

user_agent = UserAgent()
browser_header = {'User-Agent': user_agent.chrome}


def remove_newlines(links: list) -> list:
    for i in range(len(links)):
        if links[i].endswith("\n"):
            links[i] = links[i][:-1]
    return links


def get_domain_name(link: str) -> str:
    return tldextract.extract(link).domain


def get_relevant_dict(domain: str) -> dict:
    """ Gets the dictionary corresponding to the domain name.  \n
    Requires: domain is one of \n
    - "canadacomputers"
    - "bestbuy"
    - "newegg"
    - "memoryexpress"
    """
    return json.load(open(jsonfp + domain + ".json"))


def fetch_content(link: str):
    ''' Fetches the content of the URL corresponding to link. '''
    global browser_header
    page = requests.get(link, headers=browser_header)
    return page


def is_in_stock(page: requests.Response, data: dict) -> bool:
    """ Returns whether the item in link is in stock or not.

    Arguments:
    - link: The URL of the item.

    - data: The dictionary containing information regarding
    
        - Which HTML element to filter to get the corresponding stock information
    
        - Which messages occur when the item is not in stock
    
    Returns: bool
    """
    html = BeautifulSoup(page.content, 'html.parser')
    target_class: str = data["classCode"]
    messages: list = data["messages"]  # list[str]
    instock: bool = True
    target_html = str(html.find(class_=target_class))
    for message in messages:
        if message not in target_html and instock:
            instock = True
        else:
            instock = False
    return instock