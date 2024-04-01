from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def get_amazon_price(product_name):
    try:
        # Set up Chrome WebDriver for Amazon
        service = Service()  # Path to chromedriver executable
        options = Options()
        options.add_argument('--headless')  # Run Chrome in headless mode
        amazon_driver = webdriver.Chrome(service=service, options=options)
        
        # Target Amazon URL
        amazon_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"

        # Load Amazon website
        amazon_driver.get(amazon_url)

        # Wait for elements to load
        WebDriverWait(amazon_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".s-result-item .a-text-normal")))
        WebDriverWait(amazon_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-cy='price-recipe'] span.a-price")))

        # Find first product and its price
        product = amazon_driver.find_element(By.CSS_SELECTOR, ".s-result-item .a-text-normal")
        title = product.text.strip()
        price = amazon_driver.find_element(By.CSS_SELECTOR, "div[data-cy='price-recipe'] span.a-price").text.strip()

        return title, price
    except Exception as e:
        print("An error occurred while fetching Amazon price:", e)
        return None, None
    finally:
        amazon_driver.quit()  # Close the Amazon browser session

def get_flipkart_price(product_name):
    try:
        # Set up Chrome WebDriver for Flipkart
        service = Service()  # Path to chromedriver executable
        options = Options()
        options.add_argument('--headless')  # Run Chrome in headless mode
        flipkart_driver = webdriver.Chrome(service=service, options=options)

        # Target Flipkart URL
        flipkart_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}"

        # Load Flipkart website
        flipkart_driver.get(flipkart_url)

        # Wait for elements to load
        WebDriverWait(flipkart_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "._4rR01T")))
        WebDriverWait(flipkart_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "._30jeq3")))

        # Find first product and its price
        product = flipkart_driver.find_element(By.CSS_SELECTOR, "._4rR01T")
        title = product.text.strip()
        price = flipkart_driver.find_element(By.CSS_SELECTOR, "._30jeq3").text.strip()

        return title, price
    except Exception as e:
        print("An error occurred while fetching Flipkart price:", e)
        return None, None
    finally:
        flipkart_driver.quit()  # Close the Flipkart browser session

# Example usage
product_name = input("Enter product name: ")
amazon_title, amazon_price = get_amazon_price(product_name)
flipkart_title, flipkart_price = get_flipkart_price(product_name)
print("Amazon Title:", amazon_title)
print("Amazon Price:", amazon_price)
print("Flipkart Title:", flipkart_title)
print("Flipkart Price:", flipkart_price)
