from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def get_product_price(product_name, website):
    # Set up Chrome WebDriver
    service = Service()  # Path to chromedriver executable
    options = Options()
    #options.add_argument('--headless')  # Run Chrome in headless mode
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Target website URL based on the provided argument
        if website.lower() == "amazon":
            target_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
            title_selector = ".s-result-item .a-text-normal"
            price_selector = "div[data-cy='price-recipe'] span.a-price"
        elif website.lower() == "flipkart":
            target_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}"
            title_selector = "._4rR01T"
            price_selector = "._30jeq3"
            spec_selector = ".rgWa7D"
        elif website.lower() == "ebay":
            target_url = f"https://www.ebay.com/sch/i.html?_nkw={product_name.replace(' ', '+')}"
            title_selector = ".s-item__title"
            price_selector = ".s-item__price"
        else:
            return "Unsupported website", None

        # Load the website
        driver.get(target_url)

        # Wait for elements to load
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, title_selector)))
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, price_selector)))

        # Find all product titles and prices
        titles = driver.find_elements(By.CSS_SELECTOR, title_selector)
        prices = driver.find_elements(By.CSS_SELECTOR, price_selector)
        
        if website.lower() == "flipkart":
            specs = driver.find_elements(By.CSS_SELECTOR, spec_selector)

        print("Number of titles found:", len(titles))
        print("Number of prices found:", len(prices))

        a = product_name.split()

        # Iterate through titles and prices to find matching ones
        if website.lower() == "flipkart":
            for title, price, spec in zip(titles, prices, specs):
                title_text = title.text
                price_text = price.text
                spec_text = spec.text.replace(" ", "")
                print(title_text," - ",price_text)
                if "refurbished" in title_text.lower():
                    continue
                else:
                    for b in a:
                        if b.lower() not in title_text.lower() and b.lower() not in spec_text.lower():
                            break
                        elif b.lower() in title_text.lower() or b.lower() in spec_text.lower():
                            if a.index(b) == len(a) - 1:
                                driver.quit()  # Close the browser
                                return title_text, price_text
                print("No matching product found")
                return "No matching product found", None
        else:
            for title, price in zip(titles, prices):
                title_text = title.text.replace(" ", "")
                price_text = price.text
                print(title_text," - ",price_text)
                if "refurbished" in title_text.lower():
                    continue
                else:
                    for b in a:
                        if b.lower() not in title_text.lower():
                            break
                        elif b.lower() in title_text.lower():
                            if a.index(b) == len(a) - 1:
                                driver.quit()  # Close the browser
                                return title_text, price_text
            print("No matching product found")
            return "No matching product found", None

    except (TimeoutException, NoSuchElementException) as e:
        print("An error occurred:", e)
        return "Error", None

    finally:
        driver.quit()  # Close the browser

# Example usage
product_name = input("Enter product name: ")
website = input("Enter website (Amazon, Flipkart, or eBay): ")
title, price = get_product_price(product_name, website)
print("Title:", title)
print("Price:", price)

