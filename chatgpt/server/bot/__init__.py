# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup

def get_html(url):
    """
    Get HTML content from the given URL.
    """
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def parse_html(html):
    """
    Parse HTML content to extract all URLs.
    """
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            links.append(href)
    return links

def filter_links(links, base_url):
    """
    Filter and standardize the URLs.
    """
    valid_links = []
    for link in links:
        # Remove anchor links
        if '#' in link:
            link = link.split('#')[0]
        
        # Handle relative URLs
        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = base_url + '/' + link

        # Basic URL validation using regex
        if re.match(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', link):
            valid_links.append(link)
    return valid_links

def crawl_web(url, max_pages=50):
    """
    Crawl a website and extract URLs.
    """
    visited = set()
    queue = [url]
    all_links = []
    
    while queue and len(visited) < max_pages:
        current_url = queue.pop(0)
        
        if current_url in visited:
            continue
            
        print(f"Crawling: {current_url}")
        visited.add(current_url)
        
        html = get_html(current_url)
        if html:
            links = parse_html(html)
            valid_links = filter_links(links, current_url)
            all_links.extend(valid_links)
            
            for link in valid_links:
                if link not in visited:
                    queue.append(link)
                    
    return list(set(all_links))

if __name__ == '__main__':
    start_url = "http://www.example.com"  # Replace with the URL you want to crawl.
    all_urls = crawl_web(start_url)
    
    print("\nAll URLs found:")
    for url in all_urls:
        print(url)
