import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()  


#Test log in
def test_valid_login(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-login']").click()
    driver.find_element(By.ID, "usrname").send_keys("Anh")
    driver.find_element(By.ID, "password").send_keys("Anhpham1@.")
    driver.find_element(By.ID, "login btn").click()
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:5000/"))
    assert driver.current_url == "http://127.0.0.1:5000/"

def test_invalid_login(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-login']").click()
    driver.find_element(By.ID, "usrname").send_keys("user")
    driver.find_element(By.ID, "password").send_keys("123")
    driver.find_element(By.ID, "login btn").click()
    error_message = driver.find_element(By.XPATH, " //div[contains(@class, 'alert alert-danger')]").text
    assert "Incorrect Username or Password" in error_message
def test_valid_logout(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-login']").click()
    driver.find_element(By.ID, "usrname").send_keys("Anh")
    driver.find_element(By.ID, "password").send_keys("Anhpham1@.")
    driver.find_element(By.ID, "login btn").click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/user-logout']"))
    ).click()
    
    WebDriverWait(driver, 10).until(
        EC.url_contains("http://127.0.0.1:5000/user-login")
    )
#test lấy lại mật khẩu    
def test_forget_password(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-login']").click()
     # Nhấn vào "Forget Password?" để điều hướng đến trang quên mật khẩu
    driver.find_element(By.XPATH, "//a[@href='/user-forget-password']").click()
      # Điền thông tin email vào trường email trên trang quên mật khẩu
    driver.find_element(By.ID, "email").send_keys("anhpham170920031709@gmail.com")
    time.sleep(5)
# Chờ nút "Send" có thể nhấp được
    button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Send']")
    button.click()
    time.sleep(5)
    try:
        # Chờ thông báo thành công xuất hiện trong khoảng thời gian 10 giây
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'OTP has been sent!')]"))
        )
        print("Test passed: OTP has been sent successfully.")
    except:
        # Nếu không thấy thông báo trong 10 giây, test case failed
        print("Test failed: OTP was not sent. Unable to reset password.")
        assert False, "Test failed: OTP was not sent."