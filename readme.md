# Bank-Statements

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
2. Usage
   - Classify transactions
   - Generate plots

#### 1. Installation
##### Common directory
All user input and output files should be located in a COMMON directory:
C:\Users\Eimantas\Dropbox\finances
This is currently hard coded in file_management.py File class.
Change the directory to specify where files will be located.

##### Input files
One input file is required:
 - COMMON\Input\raw data.xlsx

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

#### 2. Usage
##### Classify transactions

By running the code, it will do two things:
1. It will classify all transaction it already knows about.
These will be saved in COMMON\Output\classified.xlsx.
2. Any transactions it cannot classify will be moved to
COMMON\Output\unclassified.xlsx. The "Type" column will be blank.
By classifying the lines and putting categories in Type column,
these transactions will be moved to classified.xlsx next time the code is run.
If there are no more unclassified lines left, unclassified.xlsx will be deleted.

BLACKLIST is a special category than can be used when classifying transactions.
If there are any transactions classified as BLACKLIST, they will be
excluded from the data set. For example, this is useful if we want to
exclude transactions for paying into a card.

##### Generate plots
*** Plot cannot be generated at the moment ****

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
