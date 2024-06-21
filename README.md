Project Manual

|Overview|

This project contains three main Python scripts that facilitate different aspects of stock analysis:

1.) final_app_beta.py: Provides candlestick charts with various indicators for specified stocks.

2.) Database_Viewer.py: Allows running queries on stocks.db to retrieve information about stocks.

3.) StockNewsScraper.py: Scrapes the latest stock news articles from Yahoo Finance.

Each script can be run using its respective batch file. The project also includes a virtual environment (venv) to ensure that all required libraries are available.
____________________________________________________________________________________________________



|Project Structure|

fullstack-app/
├── venv/
├── Database_Viewer.py
├── final_app_beta.py
├── StockNewsScraper.py
├── requirements.txt
├── Manual.txt
├── final_app_beta.bat
├── Database_Viewer.bat
├── StockNewsScraper.bat
└── stocks.db
____________________________________________________________________________________________________


|Setup Instructions|

1. Copy the Project Folder:

-Copy the entire project_folder to your local machine.


2. Activate the Virtual Environment:

-Open a terminal and navigate to the project folder.
-Activate the virtual environment:

On Windows:
venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate


3. Install the Dependencies 

-Run the following command to install all the required libraries from requirements.txt:
pip install -r requirements.txt
____________________________________________________________________________________________________

|Running the Scripts|

1. final_app_beta.py:

Batch File: final_app_beta.bat

Functionality:
-Opens an input window where you can enter a stock symbol.
-Generates candlestick charts by the hour for the specified stock.
-Allows adding indicators (SMA, EMA, MACD, BB) to the chart within the output window.

Steps:

-Run final_app_beta.bat.
-Enter the stock symbol in the input field and submit.
-View the candlestick chart and apply desired indicators.



2. Database_Viewer.py:

Batch File: Database_Viewer.bat

Functionality:
-Opens a window to upload the stocks.db file.
-Allows running SQL queries on the stocks.db database to retrieve stock information.

Steps:

-Run Database_Viewer.bat.
-Upload the stocks.db file when prompted.
-Enter and run SQL queries to view stock information.



3. StockNewsScraper.py:

Batch File: StockNewsScraper.bat

Functionality:
-Scrapes the latest stock news articles from Yahoo Finance.
-Displays the titles of the articles in a scrollable window.

Steps:

-Run StockNewsScraper.bat.
-The window will automatically display the latest stock news articles.
____________________________________________________________________________________________________

|Database Schema|

stocks.db:

CREATE TABLE IF NOT EXISTS stock (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL UNIQUE,
    company TEXT NOT NULL
);

____________________________________________________________________________________________________

|Dependencies|

The requirements.txt file includes all the libraries required to run the scripts. Ensure you have installed them using the provided setup instructions.

Note: The sqlite3 and tkinter libraries are part of the standard Python library and do not need to be installed separately.

____________________________________________________________________________________________________

|Virtual Environment|

The venv folder contains the virtual environment needed to run the scripts. Ensure you activate the virtual environment before running any scripts to avoid dependency issues.

By following the instructions in this manual, you should be able to set up and run the project successfully. If you encounter any issues, ensure all steps are followed correctly and that you have a stable internet connection for installing dependencies.



