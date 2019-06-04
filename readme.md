# Bank-Statements

## This is currently out of date.

### Description
Learn more about your spending habits and find out where your money is going!

It uses transaction data from the bank statements, classifies
data based on user defined categories and summarises findings in through plots.

The plots show the findings through monthly and annual timeframes and how
expenses vary for different categories.

### Table of Contents
1. Installation
   - Common directory
   - Input files
2. Configuration
3. Usage
   - Import data
   - Classify data
   - Generate plots

#### 1. Installation
##### 1.1 Common directory
All user input and output files should be located in a COMMON directory:
C:\Users\Eimantas\Dropbox\finances
This is currently hard coded in file_management.py File class.
Change the directory to specify where files will be located.

##### 1.2 Input files
Two input files are required:
 - COMMON\Input\raw data.xlsx
 - COMMON\Input\config.json

raw.data.xlsx contains transaction data from bank statements.
The first row contains the columns headings and it must contain
the following columns:
 - Date
 - Description
 - Extra
 - Amount

Extra column is mandatory but the data underneath is optional.
It can be used for any other reference associated with the transaction:
e.g. pre-categorised bank data.

The dates in the spreadsheet must follow dd/mm/yyyy format.
Amount column should only contain numeric values.

config.json contains user configuration. At moment, it should
only contain the list of categories.

#### 2. Configuration
config.json in working directory is used for configuration.
Options under "XLSX" > "STYLING" > "COLUMN" specify styles
for columns in the spreadsheet.

Each column has three options:
 - width
 - cell_format
 - data_validation

cell_format is used for defining visual appearance of columns.
Cell methods and formats based on
https://xlsxwriter.readthedocs.io/format.html can be applied
against column ID in config.json.

data_validation is used for constraining data formats for columns.
The options for https://xlsxwriter.readthedocs.io/worksheet.html#data_validation
can be defined against data_validation attribute against the
column ID in config.json.

"data_validation": {"validate": "list", source": "CATEGORIES"}
is a special feature, where a dropdown will be a applied to each
cell in a column. The available values to choose from will be
taken from the list of defined categories against
COMMON\Input\config.json.      

#### 3. Usage
##### 3.1 Import data
Any new data from "raw data.xslx" must be imported into the app before any
further actions can be taken.  To do this, execute: `main.py -import` in the
command line. It will parse, validate and export data. It will also attempt to
classify data based on the known transactions.

It does not know about any transactions the first time it is run, hence the
classifications (or in other word types) will be blank. All of unclassified
transactions are exported to COMMON\Output\unclassified.xlsx.

Any transactions it already knows about will be classified and go to
COMMON\Output\classified.xlsx when running `main.py -import`

Note that Any further changes or updates to "raw data.xlsx" will not be picked
up unless the data is imported. Make sure to run `main.py -import` after each
update to the file.

##### 3.2 classify data
Any unclassified data is located in COMMON\Output\unclassified.xlsx file. To
classify the transactions, pick a classification for each from the dropdown list
against the "Type" column and save the file.

In the command line, run `main.py -classify` and it will read the file, classify
data and move all classified transactions into COMMON\Output\classified.xlsx.

If all transactions are classified within unclassified.xlsx, the file will be
deleted.

BLACKLIST is a special category than can be used when classifying transactions.
If there are any transactions classified as BLACKLIST, they will be
excluded from the data set. For example, this is useful if we want to
exclude transactions for paying into a card.

##### 3.3 Generate plots
At any given time, analysis can be done and the results summarised via plots.
They can be generated by running `main.py -plot`. This will only use classified
data from classified.xlsx.

These are the following plots generated.

Annual plot contains summary.png showing how each category changes
year-to-year. Each plot contains four subplots showing:
 - Annual expenses for each category spent per year
 - Fraction of money spend on each category per year
 - Total expenses per year
 - Purchase history of all transactions: amount vs months

There is a monthly plot for each category type showing:
 - Monthly expenses for each category spent per month
 - Fraction of money spend on each category per month
 - Purchase history for a category: amount vs months
 - Rolling average for amount spent on category each month.
   Two rolling average window sizes are used: 3 and 6 months.
