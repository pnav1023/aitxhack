from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyperclip
import time 

# Step 1: Set up the WebDriver
driver = webdriver.Chrome()  # or `webdriver.Firefox()`, etc.
driver1 = webdriver.Chrome()
driver.get('https://www.epsilon-ai.com/search')

time.sleep(3)
# Step 2: Extract data
# Wait for elements to load if necessary
search_bar = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/textarea")
search_text = "What 5 genes genetically increase your chances for obesity the most"
search_bar.send_keys(search_text)

search_bar.send_keys(Keys.RETURN)
time.sleep(30)
copy_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div[1]/div[2]/button[1]")
copy_button.click()
time.sleep(1)
copy_button_w_references = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div[1]/div[2]/div/div/button[2]")
copy_button_w_references.click()
time.sleep(1)

copied_text = pyperclip.paste()
print("Copied text:", copied_text)
# time.sleep(5)

# Step 3: Close the WebDriver
driver.quit()
driver1.quit()
