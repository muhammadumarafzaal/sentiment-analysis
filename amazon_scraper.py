from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def get_amazon_data(url):
    """
    Scrapes Amazon with Smart Scrolling to trigger lazy-loaded reviews.
    """
    
    # 1. SETUP CHROME OPTIONS
    options = Options()
    # options.add_argument("--headless")  # Keep commented to see what's happening
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled") 
    
    # Robust User Agent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    data = {
        "title": "Unknown Product",
        "image": "",
        "description": "",
        "reviews": []
    }

    try:
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Initial wait for page load
        time.sleep(random.uniform(2, 4))

        # 2. SCRAPE DETAILS (Title, Image, etc.)
        try:
            # Title
            try:
                data["title"] = driver.find_element(By.ID, "productTitle").text.strip()
            except:
                data["title"] = driver.title

            # Image
            try:
                img = driver.find_element(By.CSS_SELECTOR, "#landingImage, #imgBlkFront")
                data["image"] = img.get_attribute("src")
            except:
                pass

            # Description
            try:
                desc = driver.find_element(By.ID, "feature-bullets")
                data["description"] = desc.text.strip()
            except:
                data["description"] = "Description not available."
                
        except Exception as e:
            print(f"Error getting details: {e}")

        # 3. SMART SCROLLING (Crucial for Reviews)
        print("Scrolling to trigger reviews...")
        
        # Get total page height
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        
        # Scroll down in chunks (mimic human reading) to trigger lazy loading
        # Amazon loads reviews when you hit the bottom 30% of the page
        for i in range(1, total_height, 600):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(0.2) # Small pause between scrolls
            
        # Ensure we are at the very bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2) 

        # 4. WAIT & EXTRACT REVIEWS
        print("Looking for reviews...")
        try:
            # Explicitly wait up to 10 seconds for review bodies to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-hook='review-body']"))
            )
        except:
            print("Reviews did not load in time.")

        # Grab the elements
        review_elements = driver.find_elements(By.CSS_SELECTOR, "[data-hook='review-body']")
        
        # If main page has no reviews, sometimes they are in a different container
        if not review_elements:
            review_elements = driver.find_elements(By.CSS_SELECTOR, ".review-text-content")

        for review in review_elements:
            text = review.text.strip()
            if text:
                data["reviews"].append(text)
        
        print(f"Successfully scraped {len(data['reviews'])} reviews.")

    except Exception as e:
        print(f"Scraping Error: {e}")
        
    finally:
        driver.quit()
    
    return data

if __name__ == "__main__":
    # Test with a known product
    test_url = "https://www.amazon.com/dp/B08N5KWB9H" 
    print(get_amazon_data(test_url))