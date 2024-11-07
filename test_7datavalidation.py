import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit() 

def test_change_pw(driver):
    driver.get("http://localhost:5000/")
    wait = WebDriverWait(driver, 10)
    time.sleep(5)
    login_link = driver.find_element(By.LINK_TEXT, "Log In") #tìm kiếm link Login bằng text
    login_link.click()
    
    time.sleep(3)
    
    re_username_field = driver.find_element(By.ID, "usrname").send_keys("Ánh")
    re_password_field = driver.find_element(By.ID, "password").send_keys("Anhpham1@.")
    
    driver.find_element(By.ID, "login btn").click()
    
    account_link = driver.find_element(By.CSS_SELECTOR, "li > a[href='/user-edit-account']") 
    account_link.click()
    time.sleep(3)   
    
    change_pw_link = driver.find_element(By.CSS_SELECTOR, "li > a[href='/user-change-password']")
    change_pw_link.click()
    time.sleep(3)  
    
    old_password = driver.find_element(By.ID, "old-password").send_keys("Anhpham1@")
    new_password = driver.find_element(By.ID, "new-password").send_keys("12345")
    confirm_password = driver.find_element(By.ID, "confirm-password").send_keys("12345")
    change_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Change']")
    change_button.click()
    time.sleep(2)
    
    username_field = driver.find_element(By.ID, "usrname").send_keys("Ánh")
    password_field = driver.find_element(By.ID, "password").send_keys("12345")
    driver.find_element(By.ID, "login btn").click()
    
    try:
        wait.until(EC.url_to_be("http://localhost:5000/"))
        # If the URL is correct, the test passes
    except TimeoutException:
        # If not redirected to the cart page, fail the test
        assert False, "Failed to change password"

