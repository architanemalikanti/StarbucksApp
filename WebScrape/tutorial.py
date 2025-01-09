from selenium import webdriver
import requests
import io
from PIL import Image
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service


#CONTINUE AT 14:51 IN THE TUTORIAL

#path of the web driver:

PATH = "/Users/architanemalikanti/Desktop/BackendProjects/starbucksBackend/WebScrape/chromedriver.exe"
service = Service(PATH)
wd = webdriver.Chrome(service=service)


#wd = webdriver.Chrome(PATH) #initiates the web driver. 

def getImagesFromGoogle(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = "https://www.google.com/search?tbm=isch&q=chocolate+croissant"
    wd.get(url)
    image_urls = set()
    skips=0
    while len(image_urls)+skips < max_images:
        scroll_down(wd)
        thumbnails = wd.find_elements(By.CSS_SELECTOR, "img.sFlh5c.FyHeAf.iPVvYb")
        print(f"Found {len(thumbnails)} thumbnails.")  # Debugging
        for img in thumbnails[len(image_urls)+skips: max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images=wd.find_elements(By.CSS_SELECTOR, "img.n3VNCb")
            for img in images:
                if img.get_attribute('src') in image_urls:
                    max_images+=1
                    skips+=1

                    break
                if img.get_attribute('src') and 'http' in img.get_attribute('src'):
                    image_urls.add(img.get_attribute('src'))
                    print(f"Found {len(image_urls)}")
    return image_urls






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

urls= getImagesFromGoogle(wd, 1, 6)
for i, url in enumerate(urls):
    downloadImage("imgs/", url, str(i)+".jpg")
wd.quit() #closes the web driver.


    




