from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from fuzzywuzzy import fuzz

def get_amazon_price(product_name):
    try:
        # Set up Chrome WebDriver for Amazon
        service = Service()  # Path to chromedriver executable
        options = Options()
        options.add_argument('--headless')  # Run Chrome in headless mode
        amazon_driver = webdriver.Chrome(service=service, options=options)
        
        # Target Amazon URL
        amazon_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
        title_selector = ".s-result-item .a-text-normal"
        price_selector = "div[data-cy='price-recipe'] span.a-price"
        
        # Load Amazon website
        amazon_driver.get(amazon_url)

        # Wait for elements to load
        WebDriverWait(amazon_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, title_selector)))
        WebDriverWait(amazon_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, price_selector)))

        # Find first product and its price
        titles= amazon_driver.find_elements(By.CSS_SELECTOR,title_selector)
        prices = amazon_driver.find_elements(By.CSS_SELECTOR, price_selector)
        a=product_name.split()
        title_text1=[]
        for i in range(1,len(titles)):
            title_text1.append(titles[i])
        for title, price in zip(title_text1, prices):
            title_text = title.text.replace(" ", "")
            price_text = price.text
            if "refurbished" in title_text.lower():
                continue
            else:
                for b in a:
                    if fuzz.partial_ratio(b.lower(), title_text.lower()) < 80:
                        break
                    elif b.lower() in title_text.lower():
                        if a.index(b) == len(a) - 1:
                            amazon_driver.quit()  # Close the browser
                            return title_text, price_text
        print("No matching product found")
        return "No matching product found", None

       
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
        title_selector = "._4rR01T"
        price_selector = "._30jeq3"
        spec_selector = ".rgWa7D"
        
        # Load Flipkart website
        flipkart_driver.get(flipkart_url)

        # Wait for elements to load
        WebDriverWait(flipkart_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,title_selector)))
        WebDriverWait(flipkart_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, price_selector)))

        # Find first product and its price
        title = flipkart_driver.find_elements(By.CSS_SELECTOR,title_selector)
        price = flipkart_driver.find_elements(By.CSS_SELECTOR, price_selector)
        specs = flipkart_driver.find_elements(By.CSS_SELECTOR, spec_selector)
        a=product_name.split()
        for title, price, spec in zip(title, price, specs):
            title_text = title.text
            price_text = price.text
            spec_text = spec.text.replace(" ", "")
            if "refurbished" in title_text.lower():
                continue
            else:
                for b in a:
                    if fuzz.partial_ratio(b.lower(), title_text.lower()) < 80:
                        break
                    elif b.lower() in title_text.lower() or b.lower() in spec_text.lower():
                        if a.index(b) == len(a) - 1:
                            flipkart_driver.quit()  # Close the browser
                            return title_text, price_text
                print("No matching product found")
                return "No matching product found", None
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
