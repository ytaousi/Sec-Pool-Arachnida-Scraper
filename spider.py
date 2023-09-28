import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os
import argparse
import validators
import re
import time
import signal
import sys
from colorama import Fore


####                 Spider Program
### The spider program allow you to extract all the images from a website, recursively, byproviding a url as a parameter
###          Option -r : recursively downloads the images in a URL received as a parameter.
###          Option -r -l [N] : indicates the maximum depth level of the recursive download. If not indicated, it will be 5.
###          Option -p [PATH] : indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.
### The program will download the following extensions by default : [jpg, jpeg, png, gif, bmp].
####

extensions = ["jpg", "jpeg", "png", "gif", "bmp"]

def signal_handler(sig, frame):
    sys.exit(1)

def extract_urls(base_url, depth, max_depth):
    extracted_urls = []

    soup = BeautifulSoup(requests.get(base_url).text, 'html.parser')
    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        url_href = a_tag.get('href')
        if url_href != None:
            if re.search("https://", url_href):
                extracted_urls.append(url_href)
            elif re.search("http://", url_href):
                extracted_urls.append(url_href)
            else:
                extracted_urls.append(urljoin(base_url, url_href))
    print(Fore.RED + "URLS Found In [" + base_url + "]")
    if extract_urls:
        for l in extracted_urls:
            print(Fore.BLUE + "[" + str(l) + "]")
    else:
        print(Fore.GREEN + "No urls found in :[" + str(base_url) + "]")
    time.sleep(6)
    return extracted_urls

def extract_images(url):
    extracted_urls = []
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        images_tags = soup.find_all("img")
        for image_tag in images_tags:
            image_src = image_tag.get('src') if image_tag.get('src') != None else image_tag.get('data-src')
            extension = image_src.split("/")[-1].split(".")[-1] if image_tag.get('src') != None else image_src.split("/")[-1].split(".")[-1].split("?")[0]
            if extension in extensions:
                extracted_urls.append(image_src)
    print(Fore.RED + "Images Found In [" + url + "]")
    if extracted_urls:
        for l in extracted_urls:
            print(Fore.BLUE + "[" + str(l) + "]")
    else:
        print(Fore.GREEN + "No Image found in :[" + str(url) + "]")
    time.sleep(6)
    return extracted_urls

def download_images(extracted_images_url, current, save_path):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    for image_url in extracted_images_url:
        print(Fore.YELLOW + "File Getting Downloaded")
        full_path = urljoin(current, image_url)
        res = requests.get(full_path)
        if res.status_code == 200:
            image_data = requests.get(full_path).content
            filename = os.path.join(save_path, image_url.split("/")[-1])
            with open(filename, "wb") as file:
                file.write(image_data)
                print(f"Downloaded: {filename}")

def spidey_scrap(base_url, max_depth, save_path):
    res = requests.get(base_url, timeout=5)
    soup = BeautifulSoup(res.content, "html.parser")
    urls = [(base_url, 0)]
    for url in urls:
        current, depth = urls.pop(0)
        print(depth,max_depth)
        print(Fore.GREEN + "URL To Be Scrapped : [" + str(current) + "]")
        extracted_images_urls = extract_images(current)
        download_images(extracted_images_urls, current, save_path)
        if depth < max_depth:
            new_urls = extract_urls(current, depth + 1, max_depth)
            urls.extend([(url, depth + 1) for url in new_urls])
    print(Fore.WHITE + "Scrapping Finished Successfully")

def is_set(arg_name):
    if arg_name in sys.argv:
        return True 
    return False

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    parser = argparse.ArgumentParser(description="Spider Program to download images recursively from a website.")
    parser.add_argument("url", help="The URL of the website to scrape")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively download images")
    parser.add_argument("-l", "--depth", type=int, default=5, help="Maximum depth level for recursive download")
    parser.add_argument("-p", "--path", default="./data/", help="Path to save downloaded files")
    args = parser.parse_args()

    base_url = args.url
    max_depth = args.depth
    save_path = args.path

    if args.depth < 0:
        print("depth of recursevity should be a positif integer")
        exit(1)
        
    if not validators.url(args.url):
        print("Invalid Url")
        exit(1)
    
    if is_set("-l"):
        if is_set("-r") == "false":
            print("you need to enable recusivity since -l option was specified")
        else:
            spidey_scrap(base_url, max_depth, save_path)
    if is_set("-r"):
        spidey_scrap(base_url, max_depth, save_path)
    else:
        spidey_scrap(base_url, 0, save_path)

