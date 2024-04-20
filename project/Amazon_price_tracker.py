from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def amazon_price_tracker(product_url):
    try:
        service = Service()
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--incognito')
        amazon_driver = webdriver.Chrome(service=service, options=options)
        price_selector = "div.a-section.a-spacing-none.aok-align-center.aok-relative span.a-price-whole"
        amazon_driver.get(product_url)
        WebDriverWait(amazon_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, price_selector)))
        price_element = amazon_driver.find_element(By.CSS_SELECTOR, price_selector)
        price = price_element.text
        if price:
            return price,None
        else:
            return None, "No price found"
    except Exception as e:
        return None, str(e)
    finally:
        amazon_driver.quit()

'''product_url = input("Enter product url: ")
price, error = amazon_price_tracker(product_url)
if price is not None:
    print("The price is:", price)
else:
    print("Error:", error)'''
