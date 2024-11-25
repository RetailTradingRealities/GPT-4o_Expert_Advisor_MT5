import requests
import pymysql
from openai import OpenAI


def analyze_stock_data(pSymbol):
    # OpenAI API Key
    api_key = 'sk-8jo3OHTwPnEtOSuW7S_OWQ7wwDG-NVhzAtmhhOlL-tT3BlbkFJWs_mpScF9FZVPxLCvuaToeUpPYGM4lSn3IE4Qr5-UA'
    client = OpenAI(organization='org-fT2PuaSBV6sMBqbyfckbzMVU',
                    project='proj_L7hhFh6dxM4wBQlo2sE0NSeN',
                    api_key = api_key,)
    # URLs for files
    image_url = f"https://momentum-trend.com/gpt-4_ea_images/{pSymbol}.png"
    txt_file_path = f"{pSymbol}_article.txt"
    income_statement_csv = f"{pSymbol}_income_statement.csv"  # or path C:Users/Philip/Documents etc...
    cash_flow_csv = f"{pSymbol}_cashflow_statement.csv"

    # Fetch the image from the URL
    image_response = requests.get(image_url)
    image_content = image_response.content

    # Prepare files for the request
    files = {
        'file1': ('chart.png', image_content, 'image/png'),
        'file2': ('news_articles.txt', open(txt_file_path, 'r', encoding='utf-8').read(), 'text/plain'),
        'file3': ('income_statement.csv', open(income_statement_csv, 'r').read(), 'text/csv'),
        'file4': ('cash_flow_statement.csv', open(cash_flow_csv, 'r').read(), 'text/csv')
    }
    

# GPT-4 request to analyze the data

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Replace with "gpt-4-turbo" or other available models
        messages=[
            {"role": "system", "content": "You are a Financial Analyst"},
            {"role": "user", "content": "Please analyze the chart png image, news, income statement, and cash flow data provided. Summarize in less than 250 words and end with one of these phrases: Bullish, Bearish, Flat, Close-All."},
            {"role": "user",
                "content": [
                    {"type": "text", "text": f"This is a screenshot chart .png image for {pSymbol}"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            }
                        },
                    ],
            },
            {"role": "user", "content": f"These are the web scraped news articles on {pSymbol} : {files['file2']} "},
            {"role": "user", "content": f"This is a csv file of the Income Statement for {pSymbol} : {files['file3']} "},
            {"role": "user", "content": f"This is a csv file of the Cash Flow Statement for {pSymbol} : {files['file4']} "},
        ],
        
    )
    # Extract the model's response
    
    temp_str = response.choices[0].message.content
    print(f'{temp_str}')
    return response.choices[0].message.content



#===============================================================================
#|def save_to_database(response, pSymbol):                                     |
#===============================================================================

# Function to save response to MySQL database
def save_to_database(response, pSymbol):
    try:
        
        connection = pymysql.connect(
        host="YOUR_WEBSITE_IPADDRESS",
        user="YOUR_DATABASE_USERNAME",
        password="YOUR_DATABASE_PASSWORD",
        database="YOUR_DATABASE_NAME"
        )
         
        cursor = connection.cursor()
        
        # Create a table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_analysis (
                id INT AUTO_INCREMENT PRIMARY KEY,
                stock_symbol VARCHAR(10),       
                summary TEXT,
                sentiment VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP       
            )
        """)
        
        cursor.execute("SHOW TABLES")

        for x in cursor:
            print(x)

        #response_edit = response.replace("\n"," ")
        # Determine sentiment from response
        sentiment = next((phrase for phrase in ["Bullish", "Bearish", "Flat", "Close-All"] if phrase in response[-150:].title()), None)

        # Insert the summary into the database
        cursor.execute("INSERT INTO stock_analysis (stock_symbol, summary, sentiment) VALUES (%s, %s, %s)", (pSymbol, response, sentiment))
        connection.commit()

    except pymysql.MySQLError as err:
        print(f"Error: {err}")
    finally:
        if 'connection' in locals() and connection.open:
            cursor.close()
            connection.close()
            print("Connection closed")

 
# Call the function to analyze the data
if __name__ == "__main__":
    gpt_analysis = analyze_stock_data("NVDA")
    if gpt_analysis:
        # Save the summary to the database
        save_to_database(gpt_analysis, "NVDA")
        print("Summary saved to the database.")




            