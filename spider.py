import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os
import argparse


####                 Spider Program
### The spider program allow you to extract all the images from a website, recursively, byproviding a url as a parameter
###          Option -r : recursively downloads the images in a URL received as a parameter.
###          Option -r -l [N] : indicates the maximum depth level of the recursive download. If not indicated, it will be 5.
###          Option -p [PATH] : indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.
### The program will download the following extensions by default : [jpg, jpeg, png, gif, bmp].
####

extensions = ["jpg", "jpeg", "png", "gif", "bmp"]

def extract_urls(soup, base_url, max_depth):
    print("ectracting urls")

def extract_images(url):
    extracted_urls = []
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    images_tags = soup.find_all("img")
    for image_tag in images_tags:
        image_src = image_tag.get('src') if image_tag.get('src') != None else image_tag.get('data-src')
        extension = image_src.split("/")[-1].split(".")[-1] if image_tag.get('src') != None else image_src.split("/")[-1].split(".")[-1].split("?")[0]
        if extension in extensions:
            extracted_urls.append(image_src)
    return extracted_urls

def download_images(extracted_images_url, save_path):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    for image_url in extracted_images_url:
        res = requests.get(image_url)
        if image_data.status_code == 200:
            print("you have a nice body")
        else:
            print("not a valid url")
        image_data = requests.get(image_url).content
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
        extracted_images_urls = extract_images(current)
        download_images(extracted_images_urls, save_path)
        if depth < max_depth:
            new_urls = extract_urls(current, depth + 1, max_depth)
            urls.extend([(url, depth + 1) for url in new_urls])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spider Program to download images recursively from a website.")
    parser.add_argument("url", help="The URL of the website to scrape")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively download images")
    parser.add_argument("-l", "--depth", type=int, default=5, help="Maximum depth level for recursive download")
    parser.add_argument("-p", "--path", default="./data/", help="Path to save downloaded files")
    args = parser.parse_args()

    base_url = args.url
    max_depth = args.depth
    save_path = args.path

    extracted_urls = extract_images(base_url)
    download_images(extracted_urls, save_path)
    # if args.recursive:
    #     spidey_scrap(base_url, max_depth, save_path)
    # else:
    #     print("Recursive option not specified. Use '-r' to enable recursive scraping.")