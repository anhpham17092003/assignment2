import pytest
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedAlertPresentException,  ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.common.alert import Alert
import time
import random



@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
#thêm sản phẩm vào giỏ hàng    
def test_add_item_to_cart(driver: webdriver.Chrome):
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
        "//a[@href='/item-detail?product-id=3']",
        "//a[@href='/item-detail?product-id=4']",
        "//a[@href='/item-detail?product-id=5']",
        "//a[@href='/item-detail?product-id=6']"
    ]

# Chọn ngẫu nhiên một sản phẩm
    selected_product_xpath = random.choice(products_xpath)
    time.sleep(5)
    driver.find_element(By.XPATH, selected_product_xpath).click()
    time.sleep(5)
    add_to_cart_button = driver.find_element(By.XPATH, "//a[contains(@class, 'btn btn-primary add2cart') and contains(@onclick, 'addToCart(')]")
    add_to_cart_button.click()
    time.sleep(1)
    
  
    # Kiểm tra giỏ hàng đã được cập nhật
    cart_badge = driver.find_element(By.ID, "cartCounter").text
    assert cart_badge == "1"
    time.sleep(2)

    # Mở giỏ hàng và kiểm tra sản phẩm
    cart_icon = driver.find_element(By.CSS_SELECTOR, ".fa.fa-shopping-cart")
    cart_icon.click()
    time.sleep(2)
    cart_items = driver.find_elements(By.CLASS_NAME, "table-wrapper-responsive")

    # Kiểm tra nếu sản phẩm được thêm thành công
    product_found = False
    product_names = ["Dell Gaming G3 3500", "Dell XPS 8570","Dell Latitude E7410","Dell Latitude 7420","Dell Precision 3541","Dell XPS 9710","Lenovo ThinkPad"]
    
    for item in cart_items:
        if any(name in item.text for name in product_names):
            product_found = True
            break
    assert product_found, "Sản phẩm được chọn không nằm trong giỏ hàng!"
# Test  thanh toán
def test_checkout(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-login']").click()
    driver.find_element(By.ID, "usrname").send_keys("Anh")
    driver.find_element(By.ID, "password").send_keys("Anhpham1@.")
    driver.find_element(By.ID, "login btn").click()
    time.sleep(5)
    driver.find_element(By.XPATH, "//a[@href='/product-list']").click()
    time.sleep(3)
    # Danh sách các XPATH của các sản phẩm
    products_xpath = [
        "//a[@href='/item-detail?product-id=1']",
        "//a[@href='/item-detail?product-id=2']",
        "//a[@href='/item-detail?product-id=3']",
        "//a[@href='/item-detail?product-id=4']",
        "//a[@href='/item-detail?product-id=5']",
        "//a[@href='/item-detail?product-id=6']"
    ]

# Chọn ngẫu nhiên một sản phẩm
    selected_product_xpath = random.choice(products_xpath)
    time.sleep(5)
    driver.find_element(By.XPATH, selected_product_xpath).click()
    time.sleep(5)
    add_to_cart_button = driver.find_element(By.XPATH, "//a[contains(@class, 'btn btn-primary add2cart') and contains(@onclick, 'addToCart(')]")
    add_to_cart_button.click()
    time.sleep(1)
    # Thêm sản phẩm vào giỏ hàng
    driver.find_element(By.XPATH, selected_product_xpath).click()
    time.sleep(5)

    # Mở giỏ hàng
    cart_icon = driver.find_element(By.CSS_SELECTOR, ".fa.fa-shopping-cart")
    cart_icon.click()
    time.sleep(5)
    # Nhấn nút CHECKOUT
  # Sau khi thêm sản phẩm vào giỏ hàng, thực hiện thanh toán
    driver.find_element(By.ID, "checkout btn").click()  # Sử dụng class để tìm nút

    # Bước 1: CHOOSE YOUR CITY
    step1_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '#shipping-address-content')]"))
    )
    step1_link.click()

   # Chọn dropdown thành phố
    city_dropdown = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "mySelect"))  # Sử dụng ID đúng cho dropdown thành phố
)

# Sử dụng Select để lấy tất cả các tùy chọn từ dropdown
    select = Select(city_dropdown)
    all_options = select.options

# Lọc các tùy chọn (bỏ "--Please Select--" ra ngoài)
    valid_options = [option for option in all_options if option.text != '--Please Select--']
# Chọn một thành phố ngẫu nhiên từ danh sách các tùy chọn hợp lệ
    random_city = random.choice(valid_options)
# Chọn thành phố ngẫu nhiên trong dropdown
    random_city.click()
    # Bước 2: PAYMENT METHOD
    step2_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '#payment-method-content')]"))
    )
    step2_link.click()

   # Chọn phương thức thanh toán
    payment_method = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@type='radio' and @name='paymentmethod']"))  # Phương thức thanh toán
    )
    payment_method.click()

    # Bước 3: CONFIRM ORDER
    step3_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '#confirm-content')]"))
    )
    step3_link.click()

# Nhấn vào nút xác nhận đơn hàng
    confirm_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "button-confirm"))
)
    confirm_button.click()
    time.sleep(5)

    confirm_box = driver.switch_to.alert

    # Lấy nội dung văn bản của hộp thoại confirm
    confirm_text = confirm_box.text
    print(f"Nội dung của hộp thoại confirm: {confirm_text}")

# Chọn "OK" để chấp nhận hộp thoại
    confirm_box.accept()  # Nhấn "OK"
    time.sleep(5)

    confirm_box1 = driver.switch_to.alert

    # Lấy nội dung văn bản của hộp thoại confirm
    confirm_text = confirm_box1.text
    print(f"Nội dung của hộp thoại confirm: {confirm_text}")

# Chọn "OK" để chấp nhận hộp thoại
    confirm_box1.accept()  # Nhấn "OK"
    time.sleep(5)
    cart_icon = driver.find_element(By.CSS_SELECTOR, ".fa.fa-shopping-cart")
    cart_icon.click()
    time.sleep(2)
    cart_items = driver.find_elements(By.CLASS_NAME, "table-wrapper-responsive")
    product_found = False
    for item in cart_items:
        if "Please add some products into Cart!!!" in item.text:
            product_found = True
            break 
    assert product_found, "Thanh toán thành công"
#test đặt lại order    
def test_reorder(driver):
    driver.get("http://127.0.0.1:5000/")
    wait = WebDriverWait(driver, 10)
    time.sleep(5)
    login_link = driver.find_element(By.LINK_TEXT, "Log In") #tìm kiếm link Login bằng text
    login_link.click()
    
    time.sleep(3)
    
    username_field = driver.find_element(By.ID, "usrname").send_keys("Ánh")
    password_field = driver.find_element(By.ID, "password").send_keys("Anhpham1@.")
    
    driver.find_element(By.ID, "login btn").click()
    
    account_link = driver.find_element(By.CSS_SELECTOR, "li > a[href='/user-edit-account']") 
    account_link.click()
    time.sleep(3)
    
    order_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li > a[href='/orders']")))
    order_link.click()

    # Wait for the cancel button to be clickable
    reorder_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[onclick="cancelOrder(1, 2);"]')))
    reorder_button.click()
    time.sleep(1)

    confirm_box = driver.switch_to.alert

    # Lấy nội dung văn bản của hộp thoại confirm
    confirm_text = confirm_box.text
    print(f"Nội dung của hộp thoại confirm: {confirm_text}")

    confirm_box.accept()  # Nhấn "OK"
    time.sleep(5)


    try:
        wait.until(EC.url_to_be("http://127.0.0.1:5000/cart"))
        # If the URL is correct, the test passes
    except TimeoutException:
        # If not redirected to the cart page, fail the test
        assert False, "Failed to redirect to the cart page after reorder."

#test hủy order
def test_cancel_order(driver):
    driver.get("http://127.0.0.1:5000/")
    wait = WebDriverWait(driver, 10)
    time.sleep(2)
    login_link = driver.find_element(By.LINK_TEXT, "Log In") #tìm kiếm link Login bằng text
    login_link.click()
    
    time.sleep(2)
    
    driver.find_element(By.ID, "usrname").send_keys("Ánh")
    driver.find_element(By.ID, "password").send_keys("Anhpham1@.")
    
    driver.find_element(By.ID, "login btn").click()
    
    account_link = driver.find_element(By.CSS_SELECTOR, "li > a[href='/user-edit-account']") 
    account_link.click()
    time.sleep(2)
    
    order_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li > a[href='/orders']")))
    order_link.click()
    time.sleep(1)

    # Wait for the cancel button to be clickable
    cancel_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Cancel']")))
    cancel_button.click()
    time.sleep(4)

    confirm_box = driver.switch_to.alert

    # Lấy nội dung văn bản của hộp thoại confirm
    confirm_text = confirm_box.text
    print(f"Nội dung của hộp thoại confirm: {confirm_text}")

    confirm_box.accept()  # Nhấn "OK"
    time.sleep(2)
    
    confirm_box2 = driver.switch_to.alert

    # Lấy nội dung văn bản của hộp thoại confirm
    confirm_text = confirm_box2.text
    print(f"Nội dung của hộp thoại confirm: {confirm_text}")

    confirm_box2.accept()  # Nhấn "OK"
    time.sleep(2)
    try:
        wait.until(EC.url_to_be("http://127.0.0.1:5000/orders"))
        # If the URL is correct, the test passes
    except TimeoutException:
        # If not redirected to the cart page, fail the test
        assert False, "Failed to redirect to the cart page after reorder."
#test xóa sản phẩm trong giỏ hàng
def test_delete_product_cart(driver):
    driver.get("http://localhost:5000/")
    wait = WebDriverWait(driver, 10)
    time.sleep(5)
    login_link = driver.find_element(By.LINK_TEXT, "Log In") 
    login_link.click()
    
    time.sleep(3)
    
    username_field = driver.find_element(By.ID, "usrname").send_keys("Ánh")
    password_field = driver.find_element(By.ID, "password").send_keys("Anhpham1@.")
    
    login_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Login']")
    login_button.click()
    
    productlist_link = driver.find_element(By.CSS_SELECTOR, "li > a[href='/product-list']") 
    productlist_link.click()
    time.sleep(3)
    
    product_list = driver.find_elements(By.CSS_SELECTOR, ".row.product-list .product-item")
    for i in range(3):
        add_to_cart_button = product_list[i].find_element(By.CSS_SELECTOR, ".btn.btn-default.add2cart")
        add_to_cart_button.click()
        time.sleep(1)
    
    
    cart_icon = driver.find_element(By.CSS_SELECTOR, "i.fa.fa-shopping-cart")
    cart_icon.click()
    
    try:
        # Đợi đến khi số lượng sản phẩm trong giỏ hàng được cập nhật
        initial_quantity_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cart_quantity"))
        )
        initial_quantity = int(initial_quantity_element.text)
        assert initial_quantity == 3, "Số lượng sản phẩm ban đầu phải là 3 sau khi thêm 3 sản phẩm."
    
        # Cuộn lên đầu trang sau khi kiểm tra số lượng sản phẩm
        driver.execute_script("window.scrollTo(0, 0);")  # Cuộn lên đầu trang
        time.sleep(1)

        # Tìm bảng giỏ hàng
        cart_table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table[summary='Shopping cart'] tbody"))
        )
        
        # Tìm hàng đầu tiên chứa thông tin sản phẩm
        first_product_row = cart_table.find_elements(By.TAG_NAME, "tr")[1]  # Bỏ qua hàng tiêu đề

        # Tìm nút xóa trong hàng sản phẩm đầu tiên và cuộn đến nó
        delete_button = first_product_row.find_element(By.CSS_SELECTOR, ".del-goods")
        
        driver.execute_script("arguments[0].scrollIntoView(true);", delete_button)
        time.sleep(1)

        # Đợi nút xóa có thể nhấn được
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".del-goods")))

        # Nhấn nút xóa bằng JavaScript nếu không thể nhấn bằng cách thông thường
        try:
            driver.execute_script("arguments[0].click();", delete_button)
        except ElementClickInterceptedException:
            assert False, "Không thể nhấn nút xóa do bị chặn."

        # Xử lý hộp thoại xác nhận xóa sản phẩm (confirm dialog)
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())  # Chờ alert xuất hiện
        alert.accept()  # Nhấn 'OK' trên alert
        time.sleep(1)  

        # Kiểm tra lại số lượng sản phẩm trong giỏ hàng sau khi xóa
        cart_icon = driver.find_element(By.CSS_SELECTOR, "i.fa.fa-shopping-cart")
        cart_icon.click()
        time.sleep(2)

        # Lấy số lượng sản phẩm mới trong giỏ hàng
        updated_quantity_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cart_quantity"))
        )
        updated_quantity = int(updated_quantity_element.text)

        # Kiểm tra số lượng sản phẩm đã giảm đi 1
        assert updated_quantity == initial_quantity - 1, f"Số lượng sản phẩm mong đợi là {initial_quantity - 1} nhưng lại là {updated_quantity}."
        
    except TimeoutException:
        assert False, "Không tìm thấy sản phẩm trong giỏ hàng hoặc giỏ hàng chưa được cập nhật."
    except ElementNotInteractableException:
        assert False, "Không thể tương tác với nút xóa sản phẩm."
    except NoSuchElementException:
        assert False, "Không tìm thấy phần tử giỏ hàng hoặc số lượng sản phẩm."
    except UnexpectedAlertPresentException:
        # Nếu gặp UnexpectedAlertPresentException, xử lý lại alert
        alert = Alert(driver)
        alert.accept()  # Đóng alert và tiếp tục
        assert False, "Một hộp thoại không mong đợi đã xuất hiện."        

#kiểm tra thanh toán = momo
def test_checkoutmomo(driver):
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.XPATH, "//a[@href='/user-login']").click()
    driver.find_element(By.ID, "usrname").send_keys("Anh")
    driver.find_element(By.ID, "password").send_keys("Anhpham1@.")
    driver.find_element(By.ID, "login btn").click()
    WebDriverWait(driver, 10).until(EC.url_to_be("http://127.0.0.1:5000/"))
    assert driver.current_url == "http://127.0.0.1:5000/"
    time.sleep(5)
    products_xpath = [
        "//a[contains(@onclick, \"addToCart(18, 'Macbook Air Pro 2018'\")]",
        "//a[contains(@onclick, \"addToCart(19, 'Macbook Air Pro 2019'\")]",
        "//a[contains(@onclick, \"addToCart(15, 'Macbook Gen1'\")]",
        "//a[contains(@onclick, \"addToCart(11, 'Laptop Inspiration 5821'\")]",
        "//a[contains(@onclick, \"addToCart(21, 'Macbook Pro MAX Gen1'\")]",
        "//a[contains(@onclick, \"addToCart(13, 'Macbook Pro M1'\")]"
    ]

    # Chọn ngẫu nhiên một sản phẩm
    selected_product_xpath = random.choice(products_xpath) 
    time.sleep(5)
    # Thêm sản phẩm vào giỏ hàng
    driver.find_element(By.XPATH, selected_product_xpath).click()
    time.sleep(5)

    # Mở giỏ hàng
    cart_icon = driver.find_element(By.CSS_SELECTOR, ".fa.fa-shopping-cart")
    cart_icon.click()
    time.sleep(5)
    # Nhấn nút CHECKOUT
  # Sau khi thêm sản phẩm vào giỏ hàng, thực hiện thanh toán
    driver.find_element(By.ID, "checkout btn").click()  # Sử dụng class để tìm nút

    # Bước 1: CHOOSE YOUR CITY
    step1_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '#shipping-address-content')]"))
    )
    step1_link.click()

   # Chọn dropdown thành phố
    city_dropdown = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "mySelect"))  # Sử dụng ID đúng cho dropdown thành phố
)

# Sử dụng Select để lấy tất cả các tùy chọn từ dropdown
    select = Select(city_dropdown)
    all_options = select.options

# Lọc các tùy chọn (bỏ "--Please Select--" ra ngoài)
    valid_options = [option for option in all_options if option.text != '--Please Select--']
# Chọn một thành phố ngẫu nhiên từ danh sách các tùy chọn hợp lệ
    random_city = random.choice(valid_options)
# Chọn thành phố ngẫu nhiên trong dropdown
    random_city.click()
    # Bước 2: PAYMENT METHOD
    step2_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '#payment-method-content')]"))
)
    step2_link.click()

# Chọn phương thức thanh toán "Pay Online"
    pay_online_option = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Pay Online')]/input[@type='radio' and @name='paymentmethod']"))
)
    pay_online_option.click()

# Chọn phương thức thanh toán qua MoMo
    momo_payment = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.XPATH, "//a[@href='/pay-with-momo']"))
)
    momo_payment.click()
    time.sleep(5)

 # Kiểm tra kết quả
    try:
        current_url = driver.current_url
        expected_url = "http://127.0.0.1:5000/pay-with-momo"
        assert current_url == expected_url, f"Failed: URL hiện tại '{current_url}' không khớp với URL mong muốn '{expected_url}'"

        if "Internal Server Error" in driver.page_source:
            pytest.fail("Failed: Trang có lỗi 'Internal Server Error'.")
        else:
            print("Passed: Điều hướng đến đúng trang 'Pay with MoMo' mà không có lỗi.")

    except AssertionError as e:
        pytest.fail(str(e))
       