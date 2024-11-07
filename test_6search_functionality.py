import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException 
from selenium.webdriver.common.action_chains import ActionChains

 
products = [
    "Dell Inpriration 10",
    "Macbook Pro 16 inch",
    "Lenovo ThinkPad",
    "Macbook Air Pro 2019",
    "Macbook Air 2017",
    "Laptop Inspiration 5821"
]

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit() 

#Test_search theo tên sản phẩm
def search_nameproduct(driver, product_name):
    search_icon = driver.find_element(By.CSS_SELECTOR, "i.fa.fa-search.search-btn")
    search_icon.click()
    time.sleep(2)
    
    # Nhập tên sản phẩm vào thanh tìm kiếm
    search_box = driver.find_element(By.CSS_SELECTOR, "input.form-control[name='kw']")
    search_box.clear()
    search_box.send_keys(product_name)
    
    # Nhấn nút tìm kiếm
    search_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary[type='submit']")
    search_button.click()

    # Đợi kết quả tìm kiếm tải
    time.sleep(3)  # Có thể điều chỉnh thời gian chờ tùy thuộc vào tốc độ của trang

     # Kiểm tra kết quả tìm kiếm
    search_results = driver.find_elements(By.CSS_SELECTOR, ".search-results .product-name")
    
    try: 
        results = driver.find_elements(By.CSS_SELECTOR,"div.row.product-list") 
        if len(results) > 0: 
            print("Có sản phẩm") 
        else: print("Không thấy sản phẩm cần tìm") 
    except NoSuchElementException:  
        print("Không thấy sản phẩm cần tìm")

def test_search_product(driver):
    driver.get("http://127.0.0.1:5000/")
    
    # Chọn ngẫu nhiên một sản phẩm từ danh sách
    product = random.choice(products)
    search_nameproduct(driver, product)
    print(f"Đã tìm kiếm sản phẩm: {product}")


#search theo tên hãng
def test_brand(driver):
    driver.get("http://127.0.0.1:5000/")
    time.sleep(1)
    
    brands_menu = driver.find_element(By.LINK_TEXT, "BRANDS")
    ActionChains(driver).move_to_element(brands_menu).perform()
    time.sleep(2)

    # Tìm và nhấp vào liên kết "Lenovo" trong danh sách dropdown
    lenovo_link = driver.find_element(By.CSS_SELECTOR, "a[href='/product-list?brand-id=2']")
    lenovo_link.click()
    time.sleep(3)

    assert "brand-id=2" in driver.current_url, "Test Failed: Không chuyển đến trang Lenovo"
    print("Test Passed: Đã chuyển đến trang Lenovo thành công")
    
    # Lấy danh sách các sản phẩm trong trang của hãng Lenovo
    product_items = driver.find_elements(By.CSS_SELECTOR, "div.product-item h3 a")

    # Kiểm tra từng sản phẩm xem có chứa từ "Lenovo" hay không
    all_contain_lenovo = True
    for product in product_items:
        product_name = product.text.strip()
        if not product_name:  # Nếu tên sản phẩm rỗng
            print("Test Warning: Có sản phẩm không có tên.")
            continue  # Bỏ qua sản phẩm không có tên
        if "lenovo" not in product_name.lower():  # Kiểm tra tên sản phẩm có chứa từ "Lenovo"
            print(f"Test Failed: Sản phẩm '{product_name}' không chứa từ 'Lenovo'")
            all_contain_lenovo = False
    
    assert all_contain_lenovo, "Test Failed: Có sản phẩm không chứa từ 'Lenovo' trong tên."
    print("Test Passed: Tất cả các sản phẩm đều chứa từ 'Lenovo' trong tên.")
     
    brands_menu = driver.find_element(By.LINK_TEXT, "BRANDS")
    ActionChains(driver).move_to_element(brands_menu).perform()
    time.sleep(2)
    apple_link = driver.find_element(By.CSS_SELECTOR, "a[href='/product-list?brand-id=6']")
    apple_link.click()
    time.sleep(3)

    assert "brand-id=6" in driver.current_url, "Test Failed: Không chuyển đến trang Apple"
    print("Test Passed: Đã chuyển đến trang Apple thành công")

# Lấy danh sách các sản phẩm trong trang của hãng Apple
    product_items = driver.find_elements(By.CSS_SELECTOR, "div.product-item h3 a")

# Kiểm tra từng sản phẩm xem có chứa từ "MACBOOK" hay không
    all_contain_macbook = True
    for product in product_items:
        product_name = product.text.strip()
        if not product_name:  # Nếu tên sản phẩm rỗng
            print("Test Warning: Có sản phẩm không có tên.")
            continue  # Bỏ qua sản phẩm không có tên
        if "macbook" not in product_name.lower():  # Kiểm tra tên sản phẩm có chứa từ "Macbook"
            print(f"Test Failed: Sản phẩm '{product_name}' không chứa từ 'MACBOOK'")
            all_contain_macbook = False

    assert all_contain_macbook, "Test Failed: Có sản phẩm không chứa từ 'MACBOOK' trong tên."
    print("Test Passed: Tất cả các sản phẩm đều chứa từ 'MACBOOK' trong tên.")