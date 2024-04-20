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
        service = Service()  
        options = Options()
        options.add_argument('--headless')  
        options.add_argument('--incognito')
        amazon_driver = webdriver.Chrome(service=service, options=options)
        amazon_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
        title_selector = ".s-result-item .a-text-normal"
        price_selector = "span.a-price-whole"
        product_links = "a.a-link-normal.a-text-normal"

        amazon_driver.get(amazon_url)
        WebDriverWait(amazon_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, title_selector)))
        WebDriverWait(amazon_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, price_selector)))
        WebDriverWait(amazon_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, product_links)))
        titles= amazon_driver.find_elements(By.CSS_SELECTOR,title_selector)
        prices = amazon_driver.find_elements(By.CSS_SELECTOR, price_selector)
        product_link = amazon_driver.find_elements(By.CSS_SELECTOR, product_links)
        a=product_name.split()
        title_text1=[]
        for i in range(1,len(titles)):
            title_text1.append(titles[i])
        for title, price, link in zip(title_text1, prices,product_link):
            title_text = title.text.replace(" ", "")
            title_display = title.text
            price_text = price.text
            link_url = link.get_attribute('href')
            print(title_text," - ",price_text)
            if "refurbished" in title_text.lower():
                continue
            else:
                for b in a:
                    if b.lower() not in title_text.lower():
                        break
                    elif b.lower() in title_text.lower():
                        if a.index(b) == len(a) - 1:
                            amazon_driver.quit() 
                            return title_display, price_text, link_url
        print("No matching product found")
        return "No matching product found", None, None
    except Exception as e:
        print("An error occurred while fetching Amazon price:", e)
        return None, None,None
    finally:
        amazon_driver.quit()  

def get_flipkart_price(product_name):
    try:
        service = Service()  
        options = Options()
        options.add_argument('--headless') 
        options.add_argument('--incognito')
        flipkart_driver = webdriver.Chrome(service=service, options=options)
        flipkart_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}"
        title_selector = ".KzDlHZ"
        price_selector = "._4b5DiR"
        spec_selector = "._6NESgJ"
        product_links = "a.CGtC98"
        flipkart_driver.get(flipkart_url)
        WebDriverWait(flipkart_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,title_selector)))
        WebDriverWait(flipkart_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, price_selector)))
        #WebDriverWait(flipkart_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, spec_selector)))
        WebDriverWait(flipkart_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, product_links)))
        title = flipkart_driver.find_elements(By.CSS_SELECTOR,title_selector)

        price = flipkart_driver.find_elements(By.CSS_SELECTOR, price_selector)
        specs = flipkart_driver.find_elements(By.CSS_SELECTOR, spec_selector)
        product_link = flipkart_driver.find_elements(By.CSS_SELECTOR, product_links)
        a=product_name.split()
        for title, price, spec, link in zip(title, price, specs, product_link):
            title_text = title.text.replace(" ", "")
            title_display = title.text
            price_text = price.text
            spec_text = spec.text.replace(" ", "")
            link_url = link.get_attribute('href')
            print(title_text," - ",price_text," - ",spec_text)
            if "refurbished" in title_text.lower():
                continue
            else:
                for b in a:
                    if b.lower() not in title_text.lower() and b.lower() not in spec_text.lower():
                        break
                    elif b.lower() in title_text.lower() or b.lower() in spec_text.lower():
                        if a.index(b) == len(a) - 1:
                            flipkart_driver.quit()  # Close the browser
                            return title_display, price_text,link_url
                print("No matching product found")
                return "No matching product found", None , None
    except Exception as e:
        print("An error occurred while fetching Flipkart price",e)
        return None, None, None
    finally:
        flipkart_driver.quit() 


'''product_name = input("Enter product name: ")
amazon_title, amazon_price, amazon_link = get_amazon_price(product_name)
flipkart_title, flipkart_price,flipkart_link = get_flipkart_price(product_name)
print("Amazon Title:", amazon_title)
print("Amazon Price:", amazon_price)
print("Amazon Product link:", amazon_link)
print("Flipkart Title:", flipkart_title)
print("Flipkart Price:", flipkart_price)
print("Flipkart Product link:", flipkart_link)'''
