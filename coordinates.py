from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
import time
#IMPORTANT 
#1. You must pip install selenium
#2. You must download chromedriver from this link https://sites.google.com/a/chromium.org/chromedriver/downloads according to your chrome version
#3. You must download the chromedriver folder into the same folder as this python file, extract the contents of folder, and move chromedriver.exe into the same folder as this python file
def getLocation():
    options = Options()
    options.add_argument("--use--fake-ui-for-media-stream")
    driver = webdriver.Chrome(executable_path = r'C:\Users\jeffr\SI206_FinalProject\chromedriver.exe',options=options) #Edit path of chromedriver accordingly

    timeout = 20
    driver.get("https://mycurrentlocation.net/")
    wait = WebDriverWait(driver, timeout)
    time.sleep(3)

    longitude = driver.find_elements_by_xpath('//*[@id="longitude"]') #Replace with any XPath    
    longitude = [x.text for x in longitude]    
    longitude = str(longitude[0])    
    latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')    
    latitude = [x.text for x in latitude]    
    latitude = str(latitude[0])    
    driver.quit()    
    return (latitude,longitude)

