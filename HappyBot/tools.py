# import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
import chromedriver_binary


def scrape_puns():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get("https://parade.com/1024249/marynliles/funny-puns/")  # url for puns
    puns_list = [p_tag.text for p_tag in driver.find_elements(By.XPATH, "//article//p") if
                 p_tag.text and p_tag.text[0].isnumeric()]
    driver.close()
    driver.quit()
    cleaned_list = [re.sub(r"^[0-9]{1,3}\. ", "", i) for i in puns_list]
    return cleaned_list
