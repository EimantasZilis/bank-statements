# Bank-Statements

### Description
Learn more about your spending habits and find out where your money is going!

It uses transaction data from the bank statements, classifies
data based on user defined categories and summarises findings in through plots.

The plots show the findings through monthly and annual timeframes and how
expenses vary for different categories.

### Table of Contents
1. Installation
1.1 Common directory
1.2 Input files
2. Usage
2.1 Classify transactions
2.2 Generate plots

#### 1. Installation
##### 1.1 common directory
All user input and output files should be located in a COMMON directory:
C:\Users\Eimantas\Dropbox\finances
This is currently hard coded in user_io.directory().
Change the directory to specify where files will be located.

##### 1.2 Input files
Two input files are required:
 - COMMON\input data\raw data.csv
 - COMMON\input data\categories.csv

raw.data.csv contains transaction data from bank statements.
The first row contains the columns headings and it must contain
the following columns:
 - Date
 - Description
 - Optional_type
 - Amount

Optional_type column is mandatory, but the data underneath is optional.
If transactions contain any pre-categorised data by other sources
(e.g. bank), it can be put there.

The first row of categories.csv contains a list of
categories to classify data into. The rows underneath have a list of
associated keywords.

For example, if there is a transaction in raw_data.csv:
| Date      | Description   | Optional_type | Amount |
| --------- | ------------- | ------------- | ------ |
| 18/8/2005 | KFC - TOOTING |               | £3.20  |
| 20/3/2017 | TFL - LONDON  | TRAINS        | 15.20  |

and categories.csv has:
| Fast food   | Travel        | Groceries  | BLACKLIST |
| ----------  | ------------- | ---------- | --------- |
| MCDONALDS   | TFL           | SAINSBURYS | PAYING IN |
| KFC         | NATIONAL RAIL | TESCO      |           |
| BURGER KING | TRAINS        | WAITROSE   |           |

The 1st transaction will be classified as 'Fast food'.
The 2nd one will be classified as 'Travel'.

BLACKLIST is a special category than can be used in categories.csv.
If there are any transactions classified as BLACKLIST, they will be
excluded from the data set. For example, this is useful if we want to
exclude transactions for paying into a card.

#### 2. Usage
##### 2.1 Classify transactions
First, the data needs to be classified. Create categories.csv with desired
categories and run the code.

If there are any transactions that cannot be classified into any
categories in categories.csv, it will export these transactions into
COMMON\output data\unclassified.csv. Put associated keywords under a
category of your choice in categories.csv and re-run the code.
The list of un-classified transactions should be getting smaller.

##### 2.2 Generate plots
Once the data is classified, it will plot the annual and monthly summary in
COMMON\plots\Annual and COMMON\plots\Monthly.

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
