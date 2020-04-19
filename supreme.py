from selenium import webdriver
import time
from config import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    
    return driver, success


# main function
def main():
    url = URL
    print(url)
    driver = openChrome(url)
    driver, success = addToCart(driver)
    if success:
        print("Checked out success, ready for payment")
        driver, success = checkout(driver)
    else:
        print("Error: Checkout failed")
    time.sleep(3)
    closeChrome(driver)


# Run python3 ./main.py
if __name__ == "__main__":
    main()