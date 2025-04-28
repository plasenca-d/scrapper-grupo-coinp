
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import ua_generator
from selenium.webdriver.support.ui import WebDriverWait
from data.urls import BASE_URL, pagination_definition
from data.brands import brands
from data.product import product_css_selector
import time
import random
import pandas as pd


user_agent = ua_generator.generate("desktop", browser="chrome")

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-application-cache")
options.add_argument("--disable-infobars")
options.add_argument("--no-sandbox")
options.add_argument("--hide-scrollbars")
options.add_argument("--enable-logging")
options.add_argument("--log-level=0")
options.add_argument(f"--user-agent={user_agent}") 
print("User-Agent:", user_agent)

driver: WebDriver = webdriver.Chrome(options=options)

driver.set_window_size(1920, 1080)

try:
  products_by_brand: dict[str, list[str]] = {}

  for brand in brands:
      if brand.url_name not in products_by_brand:
          products_by_brand[brand.url_name] = []

      page = 1
      while True:
        try:
            print(f"Getting page {page} - Brand: {brand.name}")
            url = BASE_URL + brand.url_name + pagination_definition(page)
            print(url)

            driver.get(url)

            sleep_time = random.uniform(1, 5)
            print(f"Sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)

            # Use a slightly shorter wait time maybe, or keep 10s. If elements aren't there, it will time out.
            anchor_elements_per_page = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card_product_v1 > div.derecha > div > div.product_name_v1 > a"))
            )

            # Check if no products were found on the page
            if len(anchor_elements_per_page) == 0:
                print(f"No more products found on page {page} for brand {brand.name}. Moving to next brand.")
                break # Exit the while loop for this brand

            # Process found products
            print(f"Found {len(anchor_elements_per_page)} products on page {page}.")
            for anchor_element in anchor_elements_per_page:
                product_url = anchor_element.get_attribute("href")
                if product_url:
                    products_by_brand[brand.url_name].append(product_url)
            
            if len(anchor_elements_per_page) < 16:
                print(f"End of pages reached for brand {brand.name}. Moving to next brand.")
                break

            # Increment page number for the next iteration
            page += 1

        except BaseException as e:
            print(f"An error occurred or end of pages reached on page {page} for brand {brand.name}: {e}")
            break

  df_columns = ["name", "description", "price", "sku", "image", "brand"]
  
  df = pd.DataFrame(columns=df_columns)
  
  for brand_name, product_urls in products_by_brand.items():
    print(f"Brand: {brand_name}")
    print(f"Number of products: {len(product_urls)}")
    print("Product URLs:")
    for product_url in product_urls:
        driver.get(product_url)
        sleep_time = random.uniform(1, 5)
        print(f"Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)

        product_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, product_css_selector("name")))
        )
        
        product_description = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, product_css_selector("description")))
        )
        
        product_price = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, product_css_selector("price")))
        )
        
        product_sku = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, product_css_selector("sku")))
        )
        
        product_image = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, product_css_selector("image")))
        )
        
        new_row = {
            "name": product_name.text,
            "description": product_description.text,
            "price": product_price.text,
            "sku": product_sku.text,
            "image": product_image.get_attribute("src"),
            "brand": brand_name
        }
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    df.to_csv("products.csv", index=False)
    print("CSV file saved.")  

finally:
    print("Closing the WebDriver...")
    driver.quit()
    print("WebDriver closed.")