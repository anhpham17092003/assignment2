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
#Test navigation 
def test_navigation_product(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-login']").click()
    driver.find_element(By.ID, "usrname").send_keys("Anh")
    driver.find_element(By.ID, "password").send_keys("Anhpham1@.")
    driver.find_element(By.ID, "login btn").click()
    driver.find_element(By.XPATH, "//a[@href='/product-list']").click()
    time.sleep(3)
    assert "product-list" in driver.current_url
    driver.find_element(By.XPATH, "//a[@href='/careers']").click()
    time.sleep(3)
    assert "careers" in driver.current_url
    cart_icon = driver.find_element(By.CSS_SELECTOR, ".fa.fa-shopping-cart")
    cart_icon.click()
    time.sleep(3)
    assert "cart" in driver.current_url
# Kiểm tra nếu URL là lỗi (404 hoặc Not Found)
def is_url_invalid(driver):
    current_url = driver.current_url
    page_source = driver.page_source

    # Kiểm tra xem URL có phải là trang lỗi không (404 hoặc Not Found)
    if "404" in current_url or "Not Found" in page_source or "The requested URL was not found on the server" in page_source:
        return True
    return False

# Kiểm tra điều hướng vào các trang
def test_navigation(driver):
    driver.get("http://127.0.0.1:5000/")  # Thay đổi URL nếu cần

    # Các liên kết cần điều hướng
    links = [
        ("Delivery Information", "/delivery-info"),
        ("Customer Service", "/customer-service"),
        ("Order Tracking", "/order-tracking"),
        ("Shipping & Returns", "/shipping-returns"),
        ("Contact Us", "/contact-us"),
        ("Careers", "/careers"),
        ("Payment Methods", "/payment-methods")
    ]
    
    previous_url = ""  # Để lưu URL trước đó và so sánh
    errors = []  # Danh sách lưu các lỗi gặp phải trong test case

    # Kiểm tra điều hướng đến các trang mong muốn
    for link_text, expected_url in links:
        try:
            # Tìm liên kết và nhấp vào
            link = driver.find_element(By.LINK_TEXT, link_text)
            link.click()

            # Đợi một chút để trang mới tải
            WebDriverWait(driver, 10).until(EC.url_changes(previous_url))
            time.sleep(2)  # Thời gian chờ để trang tải

            # Kiểm tra URL và trạng thái trang
            if is_url_invalid(driver) or driver.current_url == previous_url:
                error_message = f"Test case failed: {link_text} - URL is invalid or page not found!"
                errors.append(error_message)
                print(error_message)

            # Kiểm tra xem URL có phải là trang mong muốn không
            expected_full_url = f"http://127.0.0.1:5000{expected_url}"
            if driver.current_url != expected_full_url:
                error_message = f"Test case failed: {link_text} - Expected URL: {expected_full_url}, but got {driver.current_url}"
                errors.append(error_message)
                print(error_message)

            # In ra URL của trang hiện tại sau khi nhấn
            print(f"Đã điều hướng đến trang: {driver.current_url}")
            
            # Cập nhật previous_url để so sánh với lần sau
            previous_url = driver.current_url

            # Quay lại trang chủ để thử tiếp liên kết khác
            driver.back()
            time.sleep(2)  # Thời gian chờ để trang trở lại

        except Exception as e:
            error_message = f"Lỗi khi nhấp vào liên kết {link_text}: {e}"
            errors.append(error_message)
            print(error_message)

    # Sau khi kiểm tra tất cả các liên kết, kiểm tra xem có lỗi không
    if errors:
        print("Các lỗi phát hiện trong quá trình kiểm thử:")
        for error in errors:
            print(error)
        assert False, "Có lỗi trong các chức năng điều hướng!"

    else:
        print("Tất cả các chức năng điều hướng đều hoạt động bình thường.")
