from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyperclip
import time 

genes = ["HLA-B27",  "ADRB3"] # "DAX1 (NR0B1)", "WNT10A", "TCF7L2", "BRCA1", "BRCA2", "SHANK3", "HLA-C", "CHRM2", "TSEN54",]
# gene_talents = ["CHRM2", "TSEN54", "ADRB3", ]
drivers = []
for gene in genes:
    drivers.append(webdriver.Chrome())

for driver in drivers:
    driver.get('https://www.epsilon-ai.com/search')

time.sleep(3)

for i in range(0, len(genes)):
    search_bar = drivers[i].find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/textarea")
    search_text = f'what conditions are associated with {genes[i]}'
    search_bar.send_keys(search_text)
    search_bar.send_keys(Keys.RETURN)

time.sleep(30)

for driver in drivers:
    copy_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div[1]/div[2]/button[1]")
    copy_button.click()

time.sleep(1)

for driver in drivers:
    copy_button_w_references = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div[1]/div[2]/div/div/button[2]")
    copy_button_w_references.click()
    time.sleep(1)
    copied_text = pyperclip.paste()
    print("Copied text:", copied_text)

for driver in drivers:
    driver.quit()
