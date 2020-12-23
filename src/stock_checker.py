import json
from time import sleep
import requests
from playsound import playsound
from bs4 import BeautifulSoup
import tldextract
import os 
from fake_useragent import UserAgent
import concurrent.futures
import multiprocessing

os.chdir("..")
soundpath = os.getcwd() + "\\assets\\instock.mp3"
jsonfp = os.getcwd() + "\websites\\"


# Fake Browser Agent
user_agent = UserAgent()
browser_header = {'User-Agent': user_agent.chrome}

# TODO:
    # Add amazon to supported list
    # Either improve CLI or create a GUI

# Take in an array of strings, find which retailer they are from, check based on the corresponding JSON.
def check_stock(links : list, sleep_time : float) -> None:
    """ A looping function that checks whether the items in "links" are in stock (online only for now) or not.

    Arguments:
    
    links: list[str]. The list of links to be checked. Each link is a str.
    
    sleep_time: float. The number of miliseconds to wait before checking again.

    Returns: None
    """
    # Each string contains "\n" at the back which needs to be removed to get the website link.
    links = remove_newlines(links)
    storemap : dict[str, str] = {}
    for link in links:
        storemap[link] = get_domain_name(link)
    print("Stock checking will now begin. To stop, close this window.\n")
    executor = concurrent.futures.ThreadPoolExecutor(max_workers = multiprocessing.cpu_count())
    # Stock Check Loop!
    while(True):
        pages = list(executor.map(fetch_content, links))
        for i in range(len(pages)):
            if is_in_stock(pages[i], get_relevant_dict(storemap[links[i]])):
                print(links[i] + " Is in stock!!!")
                playsound(soundpath)
        sleep(sleep_time)


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