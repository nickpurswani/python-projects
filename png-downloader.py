import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

folder_name = "fold"
#make folder
if not os.path.exists(folder_name):
    os.mkdir(folder_name)
else:
    pass  
os.chdir(folder_name)
url = 'https://icons8.com/icon/set/logos/color'
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all img tags 
    images = soup.find_all('img')
    
    def download_image(i):
        img_src = i.get('src')
        if img_src and img_src.endswith('.png'):
            img_url = urljoin(url, img_src)
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                img_name = os.path.basename(img_url)
                if not os.path.exists(img_name):
                            with open(img_name, 'wb') as img_file:#write image in folder
                                img_file.write(img_response.content)
                                print(f"Downloaded: {img_name}")
                else:
                     print(f"File Exists: {img_name}")
            else:
                print(f"Failed to download {img_name}")

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_image, images)
        
else:
    print(f"Failed to fetch the website. Status code: {response.status_code}")
#change name for simplicity
for i,file_name in enumerate(os.listdir()):
    if file_name.endswith('.png'):
            os.rename(file_name,f"{i}.png")