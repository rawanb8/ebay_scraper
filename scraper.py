from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import pandas as pd
import os

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
wait = WebDriverWait(driver, 15)

url="https://www.ebay.com/globaldeals/tech"
driver.get(url)
time.sleep(5)

last_height = driver.execute_script("return document.body.scrollHeight")
while True: 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    
data=[]
try:
    container = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='sections-container']")))

    products = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@itemscope='itemscope']")))


    for product in products:
        try:
            title=product.find_element(By.XPATH,".//h3[contains(@class, 'dne-itemtile-title')]").get_attribute("title")
        except:
            title = "N/A"
        
        try:
            price=product.find_element(By.XPATH,".//span[@itemprop='price']").text
        except:
            price="N/A"
            
        try:
            original_price=product.find_element(By.XPATH,".//span[contains(@class, 'itemtile-price-strikethrough')]").text
        except:
            original_price="N/A"
            
        try:
            shipping = product.find_element(By.XPATH, ".//span[@class='dne-itemtile-delivery']").text
        except:
            shipping = "N/A"
            
        try:
            item_url = product.find_element(By.XPATH, ".//a[@itemprop='url']").get_attribute("href")
        except:
            item_url = "N/A"
            
        item_data={
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "title":title,
            "price":price,
            "original_price":original_price,
            "shipping":shipping,
            "item_url":item_url
        }
        
        data.append(item_data)
except Exception as e:
    print(f"Where is the ciontainerrr: {e}, did the page load??")
driver.quit()

df=pd.DataFrame(data)
file_name="ebay_tech_deals.csv"
if not os.path.exists(file_name):
    df.to_csv(file_name, index=False)
else:
    df.to_csv(file_name, mode='a', header=False, index=False)
    

