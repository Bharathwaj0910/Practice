from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def flipkart_price_tracker(product_url):
    try:
        service = Service()
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--incognito')
        flipkart_driver = webdriver.Chrome(service=service, options=options)
        price_selector = ".CxhGGd"
        flipkart_driver.get(product_url)
        WebDriverWait(flipkart_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, price_selector)))
        price_element = flipkart_driver.find_element(By.CSS_SELECTOR, price_selector)
        price = price_element.text
        if price:
            return price
        else:
            return None, "No price found"
    except Exception as e:
        return None, str(e)
    finally:
        flipkart_driver.quit()

'''product_url = input("Enter product url: ")
price, error = flipkart_price_tracker(product_url)
if price is not None:
    print("The price is:", price)
else:
    print("Error:", error)'''