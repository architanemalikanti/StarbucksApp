from selenium import webdriver
import requests
import io
from PIL import Image

#CONTINUE AT 14:51 IN THE TUTORIAL

#path of the web driver:
PATH = "/Users/architanemalikanti/Desktop/BackendProjects/starbucksProject/WebScrape/chromedriver.exe"


wd = webdriver.Chrome(PATH) #initiates the web driver. 

image_url = "https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg"


def downloadImage(download_path, url, file_name):

    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content) #converts the image into a bytes io format (we're storing this image directly in memory). just binary data
        image = Image.open(image_file) #opens the image as an actual image
        file_path = download_path + file_name


        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Image downloaded successfully")

    except Exception as e:
        print("error downloading image: ", e)

    


downloadImage("", image_url, "test.jpg")


