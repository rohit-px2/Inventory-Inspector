import json
from time import sleep
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import requests
from playsound import playsound
from bs4 import BeautifulSoup
import tldextract
import os 
from fake_useragent import UserAgent
from PyQt5.QtWidgets import QTextBrowser

os.chdir("..")
SOUNDPATH = os.getcwd() + "\\assets\\instock.mp3"
jsonfp = os.getcwd() + "\websites\\"

user_agent = UserAgent()
browser_header = {'User-Agent': user_agent.chrome}

# Take in an array of strings, find which retailer they are from, check based on the corresponding JSON.
def check_stock(links : list, sleep_time : float, textarea : QTextBrowser, executor, storemap) -> None:
    """ A function that checks whether the items in "links" are in stock (online only for now) or not.\n
    Arguments:\n
    - links: list[str]. The list of links to be checked. Each link is a str.\n
    - sleep_time: float. The number of miliseconds to wait before checking again.\n
    Returns: None
    """
    # Strings may contain "\n" at the end which we need to remove (if it's there) to get the URL.
    pages = list(executor.map(fetch_content, links))
    for i in range(len(pages)):
        if is_in_stock(pages[i], get_relevant_dict(storemap[links[i]])):
            # In stock message is green
            textarea.append(links[i] + " Is in stock!!!")
            playsound(SOUNDPATH)
        else:
            # Out of stock message is red
            textarea.append(links[i] + " Out of stock")



def remove_newlines(links : list) -> list:
    for i in range(len(links)):
        if links[i].endswith("\n"):
            links[i] = links[i][:-1]
    return links


def get_domain_name(link : str) -> str:
    return tldextract.extract(link).domain


def get_relevant_dict(domain : str) -> dict:
    """ Gets the dictionary corresponding to the domain name.  \n
    Requires: domain is one of \n
    - "canadacomputers"
    - "bestbuy"
    - "newegg"
    - "memoryexpress"
    """
    return json.load(open(jsonfp + domain + ".json"))


def fetch_content(link : str):
    ''' Fetches the content of the URL corresponding to link. '''
    global browser_header
    page = requests.get(link, headers=browser_header)
    print("Got a page: " + link)
    return page


def is_in_stock(page : requests.Response, data : dict) -> bool:
    """ Returns whether the item in link is in stock or not.

    Arguments:
    - link: The URL of the item.

    - data: The dictionary containing information regarding
    
        - Which HTML element to filter to get the corresponding stock information
    
        - Which messages occur when the item is not in stock
    
    Returns: bool
    """
    html = BeautifulSoup(page.content, 'html.parser')
    target_class : str = data["classCode"]
    messages : list = data["messages"] # list[str]
    instock : bool = True
    target_html = str(html.find(class_=target_class))
    for message in messages:
        if message not in target_html and instock:
            instock = True
        else:
            instock = False
    return instock