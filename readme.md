# Bank-Statements
Learn more about your spending habits and find out where your money is going!
Use the data from the bank statements to classify into pre-defined categories
and create insights into your budget.

## Table of Contents
1. Installation
   - Minimum requirements
2. Configuration
   - Set up common path
   - Define categories
3. Usage
   - Set up raw data
   - Migrate raw data
   - Classify data
   - Reclassify data
   - Analysis

## 1. Installation
### 1.1 Minimum requirements
   - Excel (2013)
   - Argparse (1.1)
   - Json (2.0.9)
   - Matplotlib
   - Numpy (1.15.1)
   - Pandas (0.24.1)
   - Python (3.6.0)
   - XlsxWriter (1.1.5)

## 2. Configuration
The app is dependant on data from bank statements. So in order to use the app
and analyse the data, a few things need to happen first. Firstly, you need to
specify where the data will be located. Then you need to define which
categories you would like to put your transactions against.

### 2.1 Set up common path
Common path is a location where user files will be located and will be used by
the app. It will contain files for raw data, transactions to classify and other
types of data processed by the app.

To specify common path, execute
```
python main.py initialise -s C:\Users\Eimantas\Dropbox\finances
```
where the argument after `-s` specifies the directory.
By running the initialisation command, few things happen.
 - It tells the app the common path is located.
 - It creates relevant directories.
 - It creates raw.xlsx Excel file template in common_path\Data directory.

At any point, you can run
```
python main.py info -p
```
to check the common path of the app.

### 2.2 Define categories
Transactions will be put classified based on pre-defined categories. For now,
create a preliminary list of categories of your choice such as "Groceries",
"Transport" and "Rent" by running
```
python main.py categories -a "Groceries,Transport,Rent"
```
More categories can be added at any time using the same `categories -a` command.
Similarly, to delete unwanted categories such as "Rent" and "Groceries", run
```
python main.py categories -d "Rent,Groceries"
```
You can check current categories by running
```
python main.py categories -s
```
It will also display the number of transactions against each category.

"BLACKLIST" is a special type of category which should be created among others.
Any transactions put against it will be ignored by the app. This can be useful
if you insist to ignore certain types of transactions without deleting them from
 file. These could be transactions for paying off the credit card, where it is
not classified as expense.

## 3. Usage
With categories set up and raw.xlsx file template available, the data from bank
statements can be migrated into the app, transactions can be classified and
analysis can be done.

### 3.1 Set up raw data
raw.xlsx file template was created as part of the first step and it will be
used for storing raw data from bank statements. While it is currently empty, the
data from bank statements should copied into and maintained as new data becomes
available.

There are four mandatory columns in the file: Date, Description, Extra and
Amount. (Transaction) date and amount are self explanatory columns. Description
column should be used for transaction description as specified on the bank
statements. "Extra" column does not need to be filled and can be used for user
reference as a way of distinguishing similar transactions.

For example, raw.xlsx might contain
| Date | Description | Extra | Amount |
| -------- | ------------- | --- | --- |
| 01/01/01 | Petrol station | | 24.10 |
| 01/01/01 | Petrol station | | 30.10 |

Later on, you may have specified that anything with "Petrol station" keywords
should be classified as "Transport" and it would classify both transactions
under "Transport". If you actually bought groceries and fuel at the petrol
station on the same day, you might insist of keeping the transactions separate
and classify them into different types. This can be accomplished by leaving
descriptions as is and using "Extra" column, by specifying additional keywords
to distinguish between categories via

| Date | Description | Extra | Amount |
| -------- | ------------- | --- | --- |
| 01/01/01 | Petrol station | Food | 24.10 |
| 01/01/01 | Petrol station |  | 30.10 |

it would put these transactions under separate categories, provided that you
classify them as separate later on.

Raw.xlsx spreadsheet can contain extra columns for user reference, however the
app will only use Date, Description, Extra and Amount columns. The app does not
modify or overwrite this file, even if `python main.py initialise -s` is
executed with the same common path again.

### 3.2 Migrate raw data
When the data is copied into raw.xlsx, it can be migrated into the app by using
```
python main.py data -i
```
This will import data, validate and process it. By doing so, it will
create new Excel files in common_path\Data.
 - classified.xlsx contains all classified and unclassified transactions. It
   is similar to raw.xlsx with an extra "Type" column representing category.
 - unclassified.xlsx will contain any unclassified transactions.
 - Excluded returns.xlsx contains transaction pairs with the same descriptions
   and equal, but opposite (positive and negative) amounts. These are excluded
   transactions from classified.xlsx

### 3.3 Classify data
Transactions are classified via unclassified.xlsx file. Use "Type" column to
classify transactions. The column cells have built in dropdown with the list of
categories to choose from. To process the transactions, run  
```
python main.py data -c
```
It will go through the file and move classifications into classified.xlsx.
By doing so, it will also remove transactions from unclassified.xlsx. If there
are not transactions left in unclassified.xlsx, the file will be removed.

### 3.4 Reclassify data
Categories can removed at any point, even if there are already any classified
transactions against those categories. If that happens, it will remove those
classifications from already classified transactions and put them into
unclassified.xlsx. The transactions can be classified again using the normal
process.

### 3.5 Analysis
You can run the analysis and generate plots summarising expenses. This will only
use classified data from classified.xlsx. The plots are generated by running
```
python main.py plots -a
```

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
