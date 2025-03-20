# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup

def get_html(url):
    """
    Get the HTML content of a given URL.
    :param url: The URL to fetch.
    :return: The HTML content as a string, or None if an error occurred.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  #