import webbrowser
import json
from time import sleep
import requests
from bs4 import BeautifulSoup

sleep_time_ms = 5000


# Take in an array of strings, find which retailer they are from, check based on the corresponding JSON.
def check_stock(links):
    return