//+------------------------------------------------------------------+
//|                                            Screenshot2Server.mq5 |
//|                                               Philip Sang-Nelson |
//|                            https://www.mql5.com/en/users/rtr_ltd |
//+------------------------------------------------------------------+
#property copyright "Retail Trading Realities Ltd"
#property link      "https://www.mql5.com/en/users/rtr_ltd"
#property version   "1.00"

//GLOBAL VARIABLES
datetime gBarTime;

string name;
string in,out;
string symbol_list[] = {"NVDA", "COST", "META", "TSLA","MSFT" } ;
int symbol_list_len;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//---
   symbol_list_len = ArraySize(symbol_list);
    
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//---
   
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
   datetime rightBarTime = iTime(_Symbol, PERIOD_H2,0);
// check if furthest right bar has the same open time as our global variable
   if(rightBarTime != gBarTime)
     {
         // set the global variable to be the time of the next bar
         gBarTime = rightBarTime;
         //OnBar();    
         for(int SymbolLoop = 0; SymbolLoop < symbol_list_len; SymbolLoop++)
         {
            //call our OnBar() function
            OnBar(symbol_list[SymbolLoop]);
         }
     }
   
  }

//+-------------------------------------------------------------------+
//+-------------------------------------------------------------------+
//| void OnBar(string pSymbol)                                        |
//+-------------------------------------------------------------------+
//+-------------------------------------------------------------------+

//When called code will execute
void OnBar(string pSymbol)
{
     
    //Screenshot file name. Cannot exceed 63 characters. Screenshot files are placed in the \Files directory.
    name= pSymbol + ".png"; 
   //Changes the symbol and period of the specified chart.The function is asynchronous, 
   //i.e. it sends the command and does not wait for its execution completion   
   ChartSetSymbolPeriod(0,pSymbol,PERIOD_D1);

   Sleep(5000); // 5 Second delay 5000 milliseconds
    // Step 1: Capture the chart screenshot
    if (ChartScreenShot(0, name, 800, 600, ALIGN_RIGHT))
    {
        Print("Screenshot saved successfully ");        
        SendFileToServer(name);
    }
    else
    {
        Print("Failed to capture screenshot.");
    } 
    

}//end of OnBar()

//+----------------------------------------------------------------+
//| F U N C T I O N S
//+----------------------------------------------------------------+

//+----------------------------------------------------------------+
//| SendFiletoServer()
//+----------------------------------------------------------------+

void SendFileToServer(string pfilePath)
{
    // Prepare to send the file
    char postData[];
    string headers;
    string url;
    int res;
    char result[];

    // Load the file into the buffer READ AND WRITE PNG FILE AS BINARY
    int fileHandle = FileOpen(pfilePath, FILE_READ | FILE_BIN );
    Print(fileHandle) ;
    if (fileHandle != INVALID_HANDLE)
    {
        
        int fileSize = (int)FileSize(fileHandle);
        ArrayResize(postData, fileSize);
        FileReadArray(fileHandle, postData, 0, fileSize);
        FileClose(fileHandle);
        
         if(ArraySize(postData) == 0){Print("Binary png file is EMPTY");}
         else{Print("Array size of binary png is  : ", ArraySize(postData) ); }
        
        // Set the headers for the HTTP request
        // Prepare the HTTP headers
        headers = "Content-Type: application/octet-stream\r\n";
        headers += "Content-Disposition: form-data; name=\"file\"; filename=\""+name+"\"\r\n";
        Print("headers = ", headers);
        url = "https://YOUR-WEBSITE.COM/YOUR_DIRECTORY/upload_screenshot.php"; // our PHP database
        
        // Send the HTTP request
        
        string resultHeaders;
        res = WebRequest("POST", url, headers, 5000, postData, result, resultHeaders);
        
        if (res == 200)
        {
            Print("File uploaded successfully.");
            Print(__FUNCTION__, " > Server response is ", res);
            string resultText = CharArrayToString(result) ;
            Print(__FUNCTION__, " > ", resultText) ;
        }
        else
        {
            Print("File upload failed. Error code: ", GetLastError());
        }
    }
    else
    {
        Print("Failed to open file for reading.");
        Print(__FUNCTION__, " > Server response is ", res, " and the error is ", GetLastError() );
        string resultText = CharArrayToString(result) ;
        Print(__FUNCTION__, " > ", resultText) ;
    }
}

//+----------------------------------------------------------------+
//| 
//+----------------------------------------------------------------+
