import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def test_search():
    """
    Test case HHFD-1
    """
    work = 'QA Engineer'
    chrome_options = Options()
    chrome_options.add_argument("start-maximized") 
    chrome_options.add_argument("--disable-infobars") 
    chrome_options.add_argument("--disable-extensions") 
    
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    url = 'https://hh.ru/'
    driver.get(url=url)
    
    WebDriverWait(driver, timeout=5, poll_frequency=2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-qa="index__work-in-company-header"]')))
    
    element = driver.find_element(by=By.CSS_SELECTOR, value="[data-qa='search-input']")
    expected_placeholder = "Профессия, должность или компания"
    actual_placeholder = element.get_attribute("placeholder")

    assert actual_placeholder == expected_placeholder, "Плейсхолдер не соответствует ожидаемому значению"
    
    """
    Test case HHFD-2
    """
    
    element.click()
    element.send_keys(work)
    element = driver.find_element(by=By.CSS_SELECTOR, value='[data-qa="search-button"]')
    element.click()
    
    element = driver.find_element(by=By.CSS_SELECTOR, value="[data-qa='vacancies-catalog-header']")
    
    expected_catalog_header = 'Работа QA engineer'
    actual_catalog_header = element.text
    
    assert expected_catalog_header in actual_catalog_header, "Элемент не содержит ожидаемый текст"
    
    element = driver.find_element(by=By.CSS_SELECTOR, value='[data-qa="bloko-custom-select-select"]')
    expected_custom_select = 'По соответствию'
    actual_custom_select = element.text 
    
    assert expected_custom_select in actual_custom_select, "Элемент не содержит ожидаемый текст"

    """
    Test case HHFD-3
    """

    WebDriverWait(driver, timeout=5, poll_frequency=2).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[3]/div[1]/div/div[2]/div[2]/div[2]/main/div[1]/div[2]/div/div[1]/div/div[3]/h3/span/a')))
    
    element = driver.find_element(by=By.XPATH, value='/html/body/div[5]/div/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[1]/div/div/aside/div[7]/fieldset/div[2]/div/li/label/span/span[1]')
    element.click()
    time.sleep(3)
    WebDriverWait(driver, timeout=5, poll_frequency=2).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[3]/div[1]/div/div[2]/div[2]/div[2]/main/div[1]/div[2]/div/div[1]/div/div[3]/h3/span/a')))

    expected_query_param = "only_with_salary=true"
    current_url = driver.current_url

    assert expected_query_param in current_url, "Квери-параметр не найден в URL"
    time.sleep(3)    
    vacancies = driver.find_elements(by=By.CSS_SELECTOR, value='[class="serp-item"]')
    salary = driver.find_elements(by=By.CSS_SELECTOR, value='[data-qa="vacancy-serp__vacancy-compensation"]')
    
    salary_real = len(salary)-1
    
    assert len(vacancies) == salary_real or len(vacancies) == len(salary), "Не все вакансии с зарплатами"