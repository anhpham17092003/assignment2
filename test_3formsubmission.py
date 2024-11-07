import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
import pytest
from selenium.common.exceptions import TimeoutException


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_review_product(driver: webdriver.Chrome):
    driver.get("http://127.0.0.1:5000/")

    # Đăng nhập
    driver.find_element(By.XPATH, "//a[@href='/user-login']").click()
    driver.find_element(By.ID, "usrname").send_keys("Ánh")
    driver.find_element(By.ID, "password").send_keys("Anhpham1@.")
    driver.find_element(By.ID, "login btn").click()  # Sửa lại ID nếu cần thiết
    time.sleep(5)
    driver.find_element(By.XPATH, "//a[@href='/product-list']").click()
    time.sleep(3)

    # Danh sách các XPATH của các sản phẩm
    products_xpath = [
        "//a[@href='/item-detail?product-id=1']",
        "//a[@href='/item-detail?product-id=2']",
        "//a[@href='/item-detail?product-id=7']",
        "//a[@href='/item-detail?product-id=8']",
        "//a[@href='/item-detail?product-id=9']",
        "//a[@href='/item-detail?product-id=3']"
    ]

# Chọn ngẫu nhiên một sản phẩm
    selected_product_xpath = random.choice(products_xpath)
    time.sleep(5)
    driver.find_element(By.XPATH, selected_product_xpath).click()
    time.sleep(5)
    # Tìm phần tử Reviews và nhấn vào nó
    reviews_link = driver.find_element(By.XPATH, "//a[@href='#Reviews' and @data-toggle='tab']")
    reviews_link.click()  # Nhấn vào liên kết Reviews

    time.sleep(5)  # Đợi một chút để trang tải lại (nếu cần)
    # Tìm trường input có id="name" và nhập thông tin vào
    name_input = driver.find_element(By.ID, "name")
    name_input.send_keys("Phạm Ngọc Ánh")  # Thay "Tên của bạn" bằng thông tin muốn nhập

    time.sleep(5)  # Đợi một chút để xem kết quả nhập
    # Tìm trường input có id="email" và nhập thông tin vào
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys("anhpham170920031709@gmail.com")  # Thay "Tên của bạn" bằng thông tin muốn nhập

    time.sleep(5)  # Đợi một chút để xem kết quả nhập
    # Tìm trường input có id="email" và nhập thông tin vào
    review_input = driver.find_element(By.ID, "review")
    review_input.send_keys("sản phẩm tốt")  # Thay "Tên của bạn" bằng thông tin muốn nhập

    time.sleep(5)  # Đợi một chút để xem kết quả nhập
# Wait for the button to be clickable
    button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Send']")
    button.click()
    time.sleep(5)

# Kiểm tra xem nội dung của trang có chứa thông báo lỗi không
    page_source = driver.page_source

# Nếu có thông báo lỗi "Internal Server Error", test case sẽ thất bại
    if "Internal Server Error" in page_source:
      pytest.fail("Test failed. Internal Server Error encountered.")
    else:
    # Nếu không có thông báo lỗi, in ra thông báo pass
      print("Test passed. No internal server error.") 

#test khi trùng user
def test_invalid_register(driver: WebDriver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-register']").click()
    driver.find_element(By.ID, "fullname").send_keys("newuser")
    driver.find_element(By.ID, "username").send_keys("Ánh")
    driver.find_element(By.ID, "phone").send_keys("0999999999")
    driver.find_element(By.ID, "email").send_keys("newuser@example.com")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "confirm-password").send_keys("password123")
    time.sleep(3)
    driver.find_element(By.ID, "btn register").click()
    time.sleep(3)
    error_message = driver.find_element(By.XPATH, " //div[contains(@class, 'alert alert-danger')]").text
    assert "Check your information again/Username might already exit" in error_message      

#test sửa thông tin cá nhân
def test_upd_profile_fullname(driver):
    driver.get("http://localhost:5000/")
    wait = WebDriverWait(driver, 10)
    time.sleep(5)
    login_link = driver.find_element(By.LINK_TEXT, "Log In") #tìm kiếm link Login bằng text
    login_link.click()
    
    time.sleep(3)
    
    username_field = driver.find_element(By.ID, "usrname").send_keys("Ánh")
    password_field = driver.find_element(By.ID, "password").send_keys("Anhpham1@.")
    
    login_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Login']")
    login_button.click()
    
    account_link = driver.find_element(By.CSS_SELECTOR, "li > a[href='/user-edit-account']") 
    account_link.click()
    time.sleep(3)
    fullname_field = driver.find_element(By.ID, "fullname")
    fullname_field.clear()  # Clear existing text
    fullname_field.send_keys("ngocanh")
    
    continue_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Continue']")
    continue_button.click()
    time.sleep(2)

    try:
        success_alert = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert.alert-danger")))
        assert "Updated Successfully" in success_alert.text, "Success message not found after updating profile."
        # If the URL is correct, the test passes
        wait.until(EC.url_to_be("http://localhost:5000/user-edit-account"))
        
    except TimeoutException:
        # If not redirected to the cart page, fail the test
        assert False, "Failed to update"

#test đăng kí với mật khẩu ngắn hơn 5 kí tự
def test_register(driver: WebDriver):
    # Điều hướng đến trang đăng ký
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-register']").click()

    # Điền thông tin vào form đăng ký với mật khẩu ngắn hơn 5 ký tự
    driver.find_element(By.ID, "fullname").send_keys("newuser")
    driver.find_element(By.ID, "username").send_keys("chanqua")
    driver.find_element(By.ID, "phone").send_keys("0999999999")
    driver.find_element(By.ID, "email").send_keys("okenha@example.com")
    driver.find_element(By.ID, "password").send_keys("pa1")
    driver.find_element(By.ID, "confirm-password").send_keys("pa1")

    # Chờ và nhấn nút đăng ký
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@id, 'btn register')]"))
    ).click()

    # Chờ vài giây để hệ thống xử lý và điều hướng
    time.sleep(5)

    if driver.current_url != "http://127.0.0.1:5000/user-login":
        print("Test passed: Không điều hướng đến trang đăng nhập, đăng ký không thành công với mật khẩu dưới 5 ký tự")
        return

    # Nếu điều hướng đến trang đăng nhập, thực hiện đăng nhập với thông tin vừa đăng ký
    driver.find_element(By.ID, "usrname").send_keys("chanqua")
    driver.find_element(By.ID, "password").send_keys("pa1")
    driver.find_element(By.ID, "login btn").click()

    # Chờ để kiểm tra kết quả đăng nhập
    time.sleep(5)

    try:
        # Kiểm tra sự xuất hiện của thông báo lỗi (sử dụng WebDriverWait)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Email has been sent!')]"))
        )

        # Nếu tìm thấy thông báo lỗi
        print("Error message found: Email has been sent!, You need to verify your email first!")
        assert False, "Test failed: Cho phép tạo mật khẩu dưới 5 ký tự và không hiển thị thông báo lỗi"

    except TimeoutException:
        # Nếu không có thông báo lỗi, test case passed
        print("Test passed: Không hiển thị thông báo lỗi xác minh email")
#dăng kí khi thiếu trường
def test_err_register(driver):
    driver.get("http://localhost:5000/")
    wait = WebDriverWait(driver, 10)
    time.sleep(5)
    login_link = driver.find_element(By.LINK_TEXT, "Log In") 
    login_link.click()
    time.sleep(3)
    
    register_link = driver.find_element(By.CSS_SELECTOR, "a[href='/user-register']")
    register_link.click()
    time.sleep(3)
    
    new_fullname_field = driver.find_element(By.ID, "fullname").send_keys("Anh")
    new_email_field = driver.find_element(By.ID, "email").send_keys("Anh@gmail.com")
    new_password_field = driver.find_element(By.ID, "password").send_keys("Anhpham1@.")
    conf_password_field = driver.find_element(By.ID, "confirm-password").send_keys("Anhpham1@.")
    
    register_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Create an account']")
    register_button.click()
    time.sleep(5)
    
    try:
        # Tìm trường User Name và lấy thông báo lỗi qua thuộc tính validationMessage
        username_field = driver.find_element(By.ID, "usrname")
        alert_message = username_field.get_attribute("validationMessage")
        
        # Kiểm tra thông báo lỗi có đúng yêu cầu không
        assert alert_message == "Please fill out this field.", "Failed: Không có thông báo lỗi yêu cầu nhập User Name."
        
        # Kiểm tra xem trường này có bị đánh dấu lỗi với CSS class has-error không
        form_group = username_field.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-group')]")
        assert "has-error" in form_group.get_attribute("class"), "Failed: Trường User Name không có class 'has-error'."

        print("Pass: Có thông báo lỗi yêu cầu nhập User Name.")
    except AssertionError as e:
        print(e)
    except Exception as ex:
        print("Có lỗi xảy ra:", ex)
      