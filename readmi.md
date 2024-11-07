* Hướng dẫn thiết lập thử nghiệm Selenium
1. Cài đặt WebDriver
Selenium yêu cầu trình điều khiển dành riêng cho trình duyệt để tự động hóa trình duyệt. Đối với Chrome, hãy sử dụng ChromeDriver.

Tải xuống ChromeDriver :
Truy cập Trang tải xuống ChromeDriver .
Chọn phiên bản ChromeDriver phù hợp với phiên bản trình duyệt Chrome của bạn.
Sau khi tải xuống, hãy giải nén tệp và thêm tệp thực thi ChromeDriver vào đường dẫn hệ thống của bạn (xem hướng dẫn bên dưới).
Thêm WebDriver vào Đường dẫn hệ thống:

Cửa sổ :
Sao chép đường dẫn thực thi ChromeDriver.
Mở Thuộc tính hệ thống > Nâng cao > Biến môi trường.
Trong "Biến hệ thống", tìm Pathvà nhấp vào Chỉnh sửa .
Nhấp vào Mới và dán đường dẫn ChromeDriver, sau đó nhấp vào OK .
Python
2. Để cài đặt Selenium vào dự án Python, hãy sử dụng pip:
pip install selenium
3.Xác định các tình huống thử nghiệm
Trước khi tạo các trường hợp thử nghiệm, hãy xác định các kịch bản thử nghiệm chính dựa trên phương pháp thử nghiệm hộp đen. Tập trung vào việc xác thực đầu vào, điều hướng và chức năng.
Xác thực đầu vào : Kiểm tra biểu mẫu và trường nhập liệu của người dùng với nhiều dữ liệu khác nhau, bao gồm dữ liệu đầu vào hợp lệ, không hợp lệ và trường hợp ngoại lệ. Đảm bảo hệ thống phản hồi chính xác.
Điều hướng : Xác minh rằng các liên kết, nút và các thành phần điều hướng khác dẫn đến các trang hoặc phần dự định. Ví dụ: nút "Đăng ký" sẽ mở trang đăng ký.
Kiểm tra chức năng : Kiểm tra các tính năng cốt lõi, chẳng hạn như đăng nhập, tìm kiếm, gửi biểu mẫu và các chức năng quan trọng khác, để xác nhận chúng hoạt động như mong đợi. Xác định từng chức năng chính và chia thành các kịch bản kiểm tra nhỏ hơn.
4. ví dụ cho test login
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

* dùng câu lệnh để chạy
  -pytest test_login.py
  -pytest -v test_login.py
  -pip install pytest-html
  -pytest --html=report.html