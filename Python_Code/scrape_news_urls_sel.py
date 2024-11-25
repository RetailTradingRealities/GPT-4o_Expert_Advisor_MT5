from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import logging
# Function to scrape news article URLs
def scrape_yahoo_urls(pSymbol):
    # Set up Chrome options
    chrome_options = Options()
    
    # Define the user data directory path
    user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data")
    
    # Specify a new profile directory (this can be any name)
    profile_dir = os.path.join(user_data_dir, "SeleniumProfile")
    
    # Add the user data directory to Chrome options
    chrome_options.add_argument(f"user-data-dir={profile_dir}")
    cwd = os.getcwd()
  
    # Specify the path to ChromeDriver if not in PATH
    # Update this path
    service = Service(cwd+'\\chromedriver-win64\\chromedriver.exe')  # Update this path
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the specified URL
        url = f"https://finance.yahoo.com/quote/{pSymbol}/news/"
        driver.get(url)

        # Wait for the page to load
        time.sleep(20)  # Adjust this if necessary for the page to fully load

        # Find all relevant <a> tags
        links = driver.find_elements(By.CSS_SELECTOR, 'a.subtle-link.fin-size-small.titles.noUnderline.yf-1e4diqp')

        # Extract URLs from the first 10 links
        urls = [link.get_attribute('href') for link in links[:10]] #no of urls
        
        # Save stock news urls to a TXT file
        with open('news_urls.txt', 'w') as file:
            for url in urls:
                file.write(url + '\n')  # Write each URL on a new line
        return 'news_urls.txt'

    except Exception as e:
        logging.critical(f"An error occurred: {e}")
        logging.error()
        print(f"An error occurred: {e}")
        return []
    
    finally:
        driver.quit()



if __name__ == "__main__":
    # Run the scraper
    news_urls = scrape_yahoo_urls("NVDA")
    
    