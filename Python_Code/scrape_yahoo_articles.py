from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import logging

def scrape_yahoo_article(url):
    # Set up Chrome options
    chrome_options = Options()
    
    # Define the user data directory path
    user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data")
    
    # Specify a new profile directory (this can be any name)
    profile_dir = os.path.join(user_data_dir, "SeleniumProfile")
    
    # Add the user data directory to Chrome options
    chrome_options.add_argument(f"user-data-dir={profile_dir}")

    # Specify the path to ChromeDriver if not in PATH
    # Update this path
    cwd = os.getcwd()
    service = Service(cwd+'\\chromedriver-win64\\chromedriver.exe')  # Update this path
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the URL
        driver.get(url)

        # Wait for the page to load
        time.sleep(20)  # Adjust as needed for the page to load

        # Find the article body
        article_div = driver.find_element(By.CLASS_NAME, 'body.yf-5ef8bf')

        # Extract text from all <p> tags within the article body
        paragraphs = article_div.find_elements(By.TAG_NAME, 'p')
        article_text = '\n'.join([para.text for para in paragraphs])
        
        return article_text
    except Exception as e:
        logging.critical(f"An error occurred: {e}")
        return f"An error occurred: {e}"
    finally:
        driver.quit()

if __name__ == "__main__":
    url = "https://finance.yahoo.com/news/3-stocks-could-huge-winners-084300855.html"
    article_content = scrape_yahoo_article(url)
    
    # Print the scraped article content
    print(article_content)

    # Optionally, save to a TXT file
    with open('article.txt', 'w', encoding='utf-8') as file:
        file.write(article_content)

