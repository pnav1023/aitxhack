from selenium import webdriver
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyperclip
from typing import List, Tuple, Optional
import time 
from mock_data import mock_data
from dataclasses import dataclass

@dataclass
class Condition:
    name: str
    description: str

@dataclass
class ConditionData:
    gene: Optional[str] = None
    conditions: Optional[Condition] = None
    condition_references: Optional[List[str]] = None
    suppliments: Optional[List[Condition]] = None
    suppliment_references: Optional[List[str]] = None

def parse_ellipses_result(data: str) -> Tuple[List[Condition], List[str]]:
    # Split the data into conditions and references
    parts = data.split('\n[')
    conditions_text = parts[0]
    references_text = '[' + parts[1] if len(parts) > 1 else ""

    # Parse conditions
    condition_pattern = r'\*\*(.*?)\*\*: (.*?)(?=\n-|\Z)'
    conditions = []
    for match in re.finditer(condition_pattern, conditions_text, re.DOTALL):
        name = match.group(1)
        description = match.group(2).strip()
        conditions.append(Condition(name=name, description=description))

    # Parse references
    reference_pattern = r'\[(\d+(?:\.\d+)?)\](.*?)(?=\n\[|\Z)'
    references = []
    for match in re.finditer(reference_pattern, references_text, re.DOTALL):
        references.append(match.group(2).strip())

    return (conditions, references)

def test_parse_hla_b27_data():
    return parse_ellipses_result(mock_data[0])

def scrapeEpsilon() -> List[ConditionData]:
    genes = ["HLA-B27",  "ADRB3"] # "DAX1 (NR0B1)", "WNT10A", "TCF7L2", "BRCA1", "BRCA2", "SHANK3", "HLA-C", "CHRM2", "TSEN54",]
    # gene_talents = ["CHRM2", "TSEN54", "ADRB3", ]
    drivers = []
    data: List[ConditionData] = []
    for gene in genes:
        drivers.append(webdriver.Chrome())

    for driver in drivers:
        driver.get('https://www.epsilon-ai.com/search')

    time.sleep(3)

    # ====

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

    for i, driver in enumerate(drivers):
        condition  = ConditionData()
        copy_button_w_references = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div[1]/div[2]/div/div/button[2]")
        copy_button_w_references.click()
        time.sleep(1)
        copied_text = pyperclip.paste()
        condition.gene = genes[i]
        parsed = parse_ellipses_result(copied_text)
        condition.conditions = parsed[0]
        condition.condition_references = parsed
        data.append(condition)

    for driver in drivers:
        driver.quit()
    # ====

    drivers = []
    for gene in genes:
        drivers.append(webdriver.Chrome())

    for driver in drivers:
        driver.get('https://www.epsilon-ai.com/search')

    time.sleep(3)

    for i in range(0, len(genes)):
        search_bar = drivers[i].find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/textarea")
        search_bar.clear()
        search_text = f'What supplements can increase the methylation of {genes[i]}'
        search_bar.send_keys(search_text)
        search_bar.send_keys(Keys.RETURN)

    time.sleep(30)

    for driver in drivers:
        copy_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div[1]/div[2]/button[1]")
        copy_button.click()

    time.sleep(1)

    for i, driver in enumerate(drivers):
        copy_button_w_references = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[3]/div[1]/div/div/div/div[1]/div[2]/div/div/button[2]")
        copy_button_w_references.click()
        time.sleep(1)
        copied_text = pyperclip.paste()
        condition = data[i]
        parsed = parse_ellipses_result(copied_text)
        condition.suppliments = parsed[0]
        condition.suppliment_references = parsed[1]

    return data
    # ===


if __name__ == "__main__":
    print(test_parse_hla_b27_data())
