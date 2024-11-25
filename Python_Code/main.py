from scrape_yahoo_articles import scrape_yahoo_article
from scrape_financials import scrape_key_financials
from scrape_news_urls_sel import scrape_yahoo_urls

from gpt_4o_mini_reqeusts import analyze_stock_data, save_to_database
from pathlib import Path
import logging
from datetime import datetime
import os

#This will iterate through a list of Symbols 
# retrieve Top 10 news urls, save to a txt file
# scrape the content of those articles, save to a txt file
# then send a query via webrequest to chat GPT4-o-mini API
# the response will be saved in a txt file and then sent out to MySQL database .

def main():
    # Define the logs directory
    logs_directory = "gpt4_logs"
    cwd = os.getcwd()
    output_path =os.path.join(cwd, logs_directory)

    # Create the logs directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Define the log filename with timestamp
    log_filename = os.path.join(output_path, "{:%d-%m-%Y %H%M%S}.log".format(datetime.now()))

    # Set up logging configuration    filename="logs\{:%d-%m-%Y %H%M%S}.log"

    logging.basicConfig(level=logging.INFO, filename=log_filename,
                        filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info(f"PROGRAM START")
    symbol_list = [ "NVDA", "COST", "META", "MSFT", "TSLA" ]
       
    for y in symbol_list :
        my_file = Path(f"{y}_article.txt")
        if my_file.is_file():
            #lets clear all txt and csv files
            file = open(f"{y}_article.txt","r+",newline="")
            file.truncate(0) # Clears file   
                
        my_file = Path(f"{y}_income_statement.csv")
        if my_file.is_file():
            file = open(f"{y}_income_statement.csv","r+",newline="")
            file.truncate(0) # Clears file
        my_file = Path(f"{y}_cashflow_statement.csv")
        if my_file.is_file():    
            file = open(f"{y}_cashflow_statement.csv","r+",newline="")
            file.truncate(0) # Clears file         
        
        #scrape_news_urls_copy.scrape_yahoo_urls(y)
            #GET TOP 10 NEWS URLS FOR SYMBOL
            #PUT IT IN A FILE NAMED [y]_NEWS_URLS.TXT
        if __name__ == "__main__":
            filename = scrape_yahoo_urls(y)
            print(f"{y} URLS saved to {filename}")


        #SPILT TXT FILE INTO A LIST OF URLS []
        #read txt file create list[]
        with open("news_urls.txt") as f:
            urls_list = [line.rstrip('\n') for line in f]	
        #urls_list = [http://finance... , http://finance..., http://...]

        for x in urls_list :
            #scrape_articles_copy.scrape_yahoo_article(x)
            #create txt file and append
            # file name will be [y]_articles.txt i.e META_articles.txt
                
            if __name__ == "__main__":
                article_content = scrape_yahoo_article(x)
                if len(article_content)==0:
                    logging.warning(f"{y} yahoo finance article string is EMPTY!!!")
                    logging.warning(f"Skipping saving {y} empty article!!!")
                    continue;
                else:
                    # Print the scraped article content
                    print(article_content)

                    # Optionally, save to a TXT file
                    with open(f'{y}_article.txt', 'a', encoding='utf-8') as file:
                        file.write(article_content)
        if len(urls_list)==0:
            print(f"{y} news_urls.txt is EMPTY!!!")
            logging.warning(f"{y} news_urls.txt is EMPTY!!!")
            logging.warning(f"Skipping {y} !!!")
            continue
       
        scrape_key_financials(y)

        # Call the function to analyze the data
        if __name__ == "__main__":
            
            gpt_analysis = analyze_stock_data(y)
            if gpt_analysis:
                # Save the summary to the database
                save_to_database(gpt_analysis, y)
                print(f"Summary of {y} saved to the database.")
            

    logging.info(f"PROGRAM FINISH")

if __name__ == "__main__":
    main()           