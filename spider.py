import requests
import urllib.request
from bs4 import BeautifulSoup

####                 Spider Program
### The spider program allow you to extract all the images from a website, recursively, byproviding a url as a parameter
###          Option -r : recursively downloads the images in a URL received as a parameter.
###          Option -r -l [N] : indicates the maximum depth level of the recursive download. If not indicated, it will be 5.
###          Option -p [PATH] : indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.
### The program will download the following extensions by default : [jpg, jpeg, png, gif, bmp].
####

recursivity_level = 5
default_folder_path = "data"


def extract_urls():
    print("extracting urls")
   


def extract_images():
    print("extracting images")
    # parse tags that contains images url's and construct a list to pass to download func()


def download_images(images_urls):
    print("downloading images")
    # check if allowed extention



def spidey_scrap():
    print("this is the main function")
    # extract the html of a page using beatifulSoup


extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
