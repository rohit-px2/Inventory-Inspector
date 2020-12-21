import json
from time import sleep
import requests
from playsound import playsound
from bs4 import BeautifulSoup
import tldextract
import os 
from fake_useragent import UserAgent

os.chdir("..")
soundpath = os.getcwd() + "\\assets\\instock.mp3"
jsonfp = os.getcwd() + "\websites\\"


# Fake Browser Agent
user_agent = UserAgent()
browser_header = {'User-Agent': user_agent.chrome}


# Take in an array of strings, find which retailer they are from, check based on the corresponding JSON.
def check_stock(links : list, sleep_time : float) -> None:
    """ A looping function that checks whether the items in "links" are in stock (online only for now) or not.

    Arguments:
    
    links: list[str]. The list of links to be checked. Each link is a str.
    
    sleep_time: float. The number of miliseconds to wait before checking again.

    Returns: None
    """
    global canadacomp, bestbuy, memex, newegg
    # Each string contains "\n" at the back which needs to be removed to get the website link.
    links = remove_newlines(links)
    storemap : dict[str, str] = {}
    for link in links:
        storemap[link] = get_domain_name(link)
    print("Stock checking will now begin. To stop, close this window.\n")
    # Stock Check Loop!
    while(True):
        for link in links:
            if is_in_stock(link, getDict(storemap[link])):
                playsound(soundpath)
                print(link + " Is in stock!!!")
        sleep(sleep_time)


def remove_newlines(links : list) -> list:
    """ Removes the newlines of the links that are given.

    Arguments:
        links: list[str]: The list of links, where each link is a string.
    
    Returns:
        list[str]: The links with the newline characters removed.
    """
    for i in range(len(links)):
        if links[i].endswith("\n"):
            links[i] = links[i][:-1]
    return links

def get_domain_name(link : str) -> str:
    """ Gets the domain name of a website."""
    return tldextract.extract(link).domain

def getDict(domain : str) -> dict:
    """ Gets the dictionary corresponding to the domain name. """
    return json.load(open(jsonfp + domain + ".json"))

def is_in_stock(link : str, data : dict) -> bool:
    """ Returns whether the item in link is in stock or not.

    Arguments:
    - link: The URL of the item.

    - data: The dictionary containing information regarding
    
        - Which HTML element to filter to get the corresponding stock information
    
        - Which messages occur when the item is not in stock
    
    Returns: bool
    """
    global browser_header
    page = requests.get(link, headers=browser_header)
    html = BeautifulSoup(page.content, 'html.parser')
    target_class : str = data["classCode"]
    data.pop("classCode")
    instock : bool = True
    target_html = str(html.find(class_=target_class))
    for message in data:
        if data[message] not in target_html and instock:
            instock = True
        else:
            instock = False
    return instock