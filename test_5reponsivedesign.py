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



#test cập nhật số lượng sản phẩm
def test_quantity_item(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-login']").click()
    driver.find_element(By.ID, "usrname").send_keys("Ánh")
    driver.find_element(By.ID, "password").send_keys("Anhpham1@.")
    driver.find_element(By.ID, "login btn").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//a[contains(@onclick, \"addToCart(18, 'Macbook Air Pro 2018'\")]").click()
    time.sleep(2)
    cart_icon = driver.find_element(By.CSS_SELECTOR, ".fa.fa-shopping-cart")
    cart_icon.click()
    time.sleep(2)
    quantity_input = driver.find_element(By.ID, "product-quantity")
    random_quantity = random.randint(1, 10)
    quantity_input.clear()  # Xóa giá trị cũ
    quantity_input.send_keys(str(random_quantity))
    time.sleep(3)
    driver.find_element(By.XPATH, "//a[@href='/']").click()
    cart_quantity = driver.find_element(By.ID, "cartCounter").text  # Lấy số lượng từ cart_quantity
    assert int(cart_quantity) == random_quantity  
    time.sleep(3)


#test xem chi tiết sản phẩm
def test_item_detail(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-login']").click()
    driver.find_element(By.ID, "usrname").send_keys("Ánh")
    driver.find_element(By.ID, "password").send_keys("Anhpham1@.")
    driver.find_element(By.ID, "login btn").click()  # Sửa lại ID nếu cần thiết
    time.sleep(2)
    driver.find_element(By.XPATH, "//a[@href='/product-list']").click()
    time.sleep(2)

    products_xpath = [
        "//a[@href='/item-detail?product-id=1']",
        "//a[@href='/item-detail?product-id=2']",
        "//a[@href='/item-detail?product-id=3']",
        "//a[@href='/item-detail?product-id=4']",
        "//a[@href='/item-detail?product-id=5']",
        "//a[@href='/item-detail?product-id=6']"
    ]
    
    selected_product_xpath = random.choice(products_xpath)
    time.sleep(5)
    driver.find_element(By.XPATH, selected_product_xpath).click()
    time.sleep(5)
    detail_item = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "h1"))
)
    product_names = ["Dell Gaming G3 3500", "Dell XPS 8570","Dell Latitude E7410","Dell Latitude 7420","Dell Precision 3541","Dell XPS 9710","Lenovo ThinkPad"]
    product_found = False
    product_found = False
    for product in product_names:
      if product in detail_item.text:
        product_found = True
        break

# In ra kết quả
    if product_found:
      print("Sản phẩm đã tìm thấy")
    else:
      print("Không tìm thấy sản phẩm")
    