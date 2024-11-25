import yfinance as yf
import logging


def scrape_key_financials(pSymbol):
    ticker = yf.Ticker(pSymbol)

    df=ticker.income_stmt
    if df.empty:
        print(f'{pSymbol} Income Statement DataFrame is empty!')
        logging.critical(f'{pSymbol} Income Statement DataFrame is empty!') 
    else:   
        print(df)
        # Save the dataframe to a CSV file
        df.to_csv(f'{pSymbol}_income_statement.csv', index=True)
        print(f"{pSymbol} key financials saved to {pSymbol}_income_statement.csv")
        logging.info(f"{pSymbol} key financials saved to {pSymbol}_income_statement.csv")

    df_2=ticker.cashflow
    if df_2.empty:
        print(f'{pSymbol} Cash Flow Statement  DataFrame is empty!')
        logging.critical(f'{pSymbol} Cash Flow Statement  DataFrame is empty!')
    else:   
        print(df_2)
        # Save the dataframe to a CSV file
        df_2.to_csv(f'{pSymbol}_cashflow_statement.csv', index=True)
        print(f"{pSymbol} key financials saved to {pSymbol}_cashflow_statement.csv")
        logging.info(f"{pSymbol} key financials saved to {pSymbol}_cashflow_statement.csv")

if __name__ == "__main__":
    scrape_key_financials("MSFT")
    