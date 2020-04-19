from selenium import webdriver
import time
from config import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

URL = "https://www.supremenewyork.com/shop/all/" + product_type

# opens chrome and returns the instance
def openChrome(url):
    print("Opening Chrome...")
    chrome_options = webdriver.ChromeOptions()                                              # initialize Crhome options
    chrome_options.add_argument("--incognito")                                              # incognito
    chrome_options.add_argument("start-maximized")                                          # windows maximized
    chrome_options.add_argument("disable-infobars")                                         # disable info
    chrome_options.add_argument("--disable-extensions")                                     # disable extensions
    chrome_options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) \
            AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17")       # set up user agent
    driver = webdriver.Chrome(executable_path = "./chromedriver_79",
                                options = chrome_options)                                   # find location of driver
    driver.get(url)                                                                         # load argument url
    return driver

# pass a driver reference to close the instance
def closeChrome(driver):
    print("Closing Chrome...")
    driver.quit()

def addToCart(driver):
    success = False                                                                         # initialize success to false
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((\
        By.CLASS_NAME, "name-link")))                                                       # wait for products to display
    all_products = driver.find_elements_by_xpath(\
        "//div[@class=\"product-name\"]//a[@class=\"name-link\"]")                          # get all products
    current_product = None                                                                  # initialize product to None
    for product in all_products:
        if product_name.lower() in product.text.lower()\
            or product.text.lower() == product_name.lower():
                current_product = product
                break
    
    if current_product:
        print("Clicking into: ", current_product.text)
        current_product.click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,\
            "//img[@alt=\"" + product_colour + "\"]" ))).click()                            # click on product colour
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,\
            "//input[@class=\"button\"]" ))).click()                                        # click on add to cart
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,\
            "//a[@class=\"button checkout\"]" ))).click()                                   # click on check out now
        success = True
    else:
        print("ERROR: Didn't find product")
    
    return driver, success
    

def checkout(driver):
    success = False
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,\
            "#order_billing_name" ))).send_keys(name)                                       # enter name
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,\
            "#order_email" ))).send_keys(email)                                             # enter email
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,\
            "#order_tel" ))).send_keys(tel)                                                 # enter telephone
    
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,\
            "#order_billing_country" )))                                                    # wait for country
    
    country_select = Select(driver.find_element_by_xpath("//select[@id=\"order_billing_country\"]"))
    country_select.select_by_visible_text(country)
    
    state_select = Select(driver.find_element_by_xpath("//select[@id=\"order_billing_state\"]"))
    state_select.select_by_visible_text(province)
            
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,\
            "#bo" ))).send_keys(address)                                                    # enter address
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,\
            "#oba3" ))).send_keys(apt_unit)                                                 # enter apt / unit
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,\
            "#order_billing_zip" ))).send_keys(postal_zip)                                  # enter zip
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,\
            "#order_billing_city" ))).send_keys(city)                                       # enter city
    
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,\
            "#rnsnckrn" ))).send_keys(card_no)                                              # enter card no
           
    card_month_select = Select(driver.find_element_by_xpath("//select[@id=\"credit_card_month\"]"))
    card_month_select.select_by_visible_text(card_expiry_month)
    
    card_year_select = Select(driver.find_element_by_xpath("//select[@id=\"credit_card_year\"]"))
    card_year_select.select_by_visible_text(card_expiry_year)
    
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,\
            "#orcer" ))).send_keys(card_cvv)                                                # enter card cvv
    
    time.sleep(0.5)
    agreement_xpath = "/html/body/div[2]/div[1]/form/div[2]/div[2]/fieldset/p[2]/label/div/ins"
    agreement_element = driver.find_element_by_xpath(agreement_xpath)                       # find agreement element
    driver.execute_script("arguments[0].click();", agreement_element)                       # execute script since element is hidden
    
    
    time.sleep(0.5)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((\
        By.XPATH, "//input[@value=\"process payment\"]"))).click()                          # click on process payment
    
    success = True
    
    return driver, success


# main function
def main():
    start_time = time.time()
    url = URL
    print(url)
    driver = openChrome(url)
    driver, cart_success = addToCart(driver)
    if cart_success:
        print("Checked out success, ready for payment")
        driver, payment_success = checkout(driver)
        if payment_success:
            print("CHECK PAYMENT")
            # TODO: check order and/or retry
        else:
            print("Error: Payment failed")
    else:
        print("Error: Checkout failed")
    
    print("Checkout Time: %s seconds" % (time.time() - start_time))
    time.sleep(3)
    closeChrome(driver)


# Run python3 ./main.py
if __name__ == "__main__":
    main()