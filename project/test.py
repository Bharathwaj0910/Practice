import queue
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from multiprocessing import Process, Queue

def get_amazon_price(product_name, queue):
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
        titles = amazon_driver.find_elements(By.CSS_SELECTOR, title_selector)
        prices = amazon_driver.find_elements(By.CSS_SELECTOR, price_selector)
        product_link = amazon_driver.find_elements(By.CSS_SELECTOR, product_links)
        a = product_name.split()
        pn = product_name
        title_text1 = []  # Define title_text1 before the loop
        for i in range(1, len(titles)):
            title_text1.append(titles[i])
        for title, price, link in zip(title_text1, prices, product_link):
            title_text = title.text.replace(" ", "")
            title_display = title.text
            price_text = price.text
            link_url = link.get_attribute('href')
            tt = title_text.lower()
            if "refurbished" in title_text.lower():
                continue
            else:
                for b in a:
                    if b.lower() not in title_text.lower():
                        break
                    elif b.lower() in title_text.lower():
                        if a.index(b) == len(a) - 1:
                            if "pro" in tt or "max" in tt or "+" in tt or "lite" in tt or "plus" in tt:
                                if "pro" in tt and "pro" in pn or "lite" in tt and "lite" in pn or "+" in tt and "+" in pn:
                                    if "pro" in tt and "pro" in pn or "max" in tt and "max" in pn or "+" in tt and "+" in pn or "lite" in tt and "lite" in pn or "plus" in tt and "plus" in pn:
                                        amazon_driver.quit()
                                        r=(title_display, price_text, link_url)
                                        queue.put(r)
                                    continue
                                continue
                            amazon_driver.quit()
                            r=(title_display, price_text, link_url)
                            queue.put(r)
        queue.put((None, None, None))
    except Exception as e:
        print("An error occurred while fetching Amazon price:", e)
        queue.put((None, None, None))
    finally:
        amazon_driver.quit()

def get_flipkart_price(product_name, queue):
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
        WebDriverWait(flipkart_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, title_selector)))
        WebDriverWait(flipkart_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, price_selector)))
        # WebDriverWait(flipkart_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, spec_selector)))
        WebDriverWait(flipkart_driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, product_links)))
        title = flipkart_driver.find_elements(By.CSS_SELECTOR, title_selector)
        price = flipkart_driver.find_elements(By.CSS_SELECTOR, price_selector)
        specs = flipkart_driver.find_elements(By.CSS_SELECTOR, spec_selector)
        product_link = flipkart_driver.find_elements(By.CSS_SELECTOR, product_links)
        a = product_name.split()
        pn = product_name.lower()
        for title, price, spec, link in zip(title, price, specs, product_link):
            title_text = title.text.replace(" ", "")
            title_display = title.text
            price_text = price.text
            spec_text = spec.text.replace(" ", "")
            link_url = link.get_attribute('href')
            tt = title_text.lower()
            st = spec_text.lower()
            if "refurbished" in title_text.lower():
                continue
            else:
                for b in a:
                    if b.lower() not in tt and b.lower() not in st:
                        break
                    elif b.lower() in tt or b.lower() in st:
                        if a.index(b) == len(a) - 1:
                            if "pro" in tt or "max" in tt or "+" in tt or "lite" in tt or "plus" in tt:
                                if "pro" in tt and "pro" in pn or "lite" in tt and "lite" in pn or "+" in tt and "+" in pn or "plus" in tt and "plus" in pn:
                                    if "pro" in tt and "pro" in pn or "max" in tt and "max" in pn or "+" in tt and "+" in pn or "lite" in tt and "lite" in pn or "plus" in tt and "plus" in pn:
                                        flipkart_driver.quit()
                                        r= (title_display, price_text, link_url)
                                        queue.put(r)
                                    continue
                                continue
                            flipkart_driver.quit()
                            r=(title_display, price_text, link_url)
                            queue.put(r)
        queue.put((None, None, None))
    except Exception as e:
        print("An error occurred while fetching Flipkart price", e)
        queue.put((None, None, None))
    finally:
        flipkart_driver.quit()

'''def print_product_details(product_name, price, product_url):
    print(f"Product Name: {product_name}")
    print(f"Price: ₹{price}")
    print(f"Product URL: {product_url}")

if __name__ == "__main__":
    product_name = input("Enter product name: ")
    
    # Create separate queues for Amazon and Flipkart results
    amazon_queue = Queue()
    flipkart_queue = Queue()

    # Create separate processes for scraping Amazon and Flipkart prices
    p1 = Process(target=get_amazon_price, args=(product_name, amazon_queue))
    p2 = Process(target=get_flipkart_price, args=(product_name, flipkart_queue))
    p1.start()
    p2.start()

    # Retrieve results from Amazon and Flipkart queues
    amazon_result = amazon_queue.get()
    flipkart_result = flipkart_queue.get()

    # Print Amazon product details
    if amazon_result[0] != "No matching product found":
        print("\nAmazon Product Details:")
        print_product_details(amazon_result[0], amazon_result[1], amazon_result[2])
    else:
        print("No matching product found on Amazon")

    # Print Flipkart product details
    if flipkart_result[0] != "No matching product found":
        print("\nFlipkart Product Details:")
        print_product_details(flipkart_result[0], flipkart_result[1], flipkart_result[2])
    else:
        print("No matching product found on Flipkart")'''
