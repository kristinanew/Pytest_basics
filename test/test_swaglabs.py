from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import pytest
from time import sleep

def launch_swaglabs():
    global driver
    driver = webdriver.Firefox(executable_path=r'C:\WebDriver\geckodriver.exe')
    driver.get('https://saucedemo.com/')


def login_swaglabs():
    driver.find_element(By.ID,'user-name').send_keys('standard_user')
    driver.find_element(By.NAME,'password').send_keys('secret_sauce')
    driver.find_element(By.CLASS_NAME,'submit-button').click()


def capture_evidence():
    image_name=(rf"C:\Users\AccuAdmin\Desktop\projects\Pytest_basics\test\evidence\image-{datetime.today().strftime('%m%d%y-%H%M%S')}.png")
    driver.save_screenshot(image_name)

def text_is_displayed(text):
    return text.lower() in driver.page_source.lower()

                                ### TEST CASES ###
def test_launch_login_page():
    launch_swaglabs()
    assert driver.title == 'Swag Labs'
    capture_evidence()
    driver.quit()

login_form_parameters = [
    ('locked_out_user','secret_sauce',  'Sorry, this user has been locked out'),
    ('test',            'test',         'Username and password do not match any user in this service')
]

@pytest.mark.parametrize("username, password, checkpoint", login_form_parameters)
def test_invalid_login_credentials(username, password, checkpoint):
    launch_swaglabs()
    driver.find_element(By.ID,'user-name').send_keys(username)
    driver.find_element(By.NAME,'password').send_keys(password)
    driver.find_element(By.CLASS_NAME,'submit-button').click()
    sleep(5)
    assert text_is_displayed(checkpoint)
    capture_evidence()
    driver.quit()

    
                            ###### SETUP AND TEARDOWN ######
@pytest.fixture()
def setup(request):
    # the following code runs before each test
    launch_swaglabs()
    login_swaglabs()

    #the following code runs after each test
    def teardown():
        capture_evidence()
        driver.quit()
    request.addfinalizer(teardown)

def test_valid_login_credentials(setup):
    assert text_is_displayed('products')


def test_view_product_details(setup):
    product_names=driver.find_elements(By.CLASS_NAME,'inventory_item_name')
    product_names[0].click()
    assert text_is_displayed('back to products')

def test_add_item_to_cart(setup):
    add_buttons=driver.find_elements(By.CSS_SELECTOR,".btn_primary")
    add_buttons[0].click()
    