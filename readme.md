Project name: Bank-Statements

Description
  It analyses expenses from bank statements and classifies transactions based
  on user defined categories. It summarises expenses through plots showing how
  much money is spent on each category during monthly and annual timeframes.

Table of Contents
  1. Installation
  2. Usage

1. Installation
  All user input and output files should be located in a COMMON directory:
  C:\Users\Eimantas\Dropbox\finances
  This is currently hard coded in user_io.directory().
  Change the directory to specify where files will be located.

  Two input files are required:
   - COMMON\input data\raw data.csv
   - COMMON\input data\categories.csv

  raw.data.csv contains transaction data from bank statements.
  The first row contains the columns headings and it must contain
  the following columns:
   - Description
   - Optional_type
   - Amount

   Optional_type column is mandatory, but the data underneath is optional.
   If transactions contain any pre-categorised data by other sources
   (e.g. bank), it should be put here.

   The first row of categories.csv contains a list of
   categories to classify data into. The rows underneath have a list of
   associated keywords.

   For example, if there is a transaction in raw_data.csv:
   Date       Description     Optional_type   Amount
   18/8/2005  KFC - TOOTING                   £3.20
   20/3/2017  TFL - LONDON    TRAINS          15.50

   and categories.csv has:
   Fast food     Travel          Groceries      BLACKLIST
   MCDONALDS     TFL             SAINSBURYS     PAYING IN
   KFC           NATIONAL RAIL   TESCO
   BURGER KING   TRAINS          WAITROSE

   The 1st transaction will be classified as 'Fast food'.
   The 2nd one will be classified as 'Travel'.

   BLACKLIST is a special category than can be optionally used in
   categories.csv. If there are any transactions classified as BLACKLIST,
   they will be excluded from the data set. This is useful if we want to
   exclude some transactions such as transactions for paying into the account.

2. Usage
  First, the data needs to be classified. Create categories.csv with desired
  categories and run the code.

  If there are any transactions that cannot be classified into any categories
  specified in categories.csv, it will export these transactions into
  COMMON\output data\unclassified.csv. Classify these transactions
  in categories.csv and re-run the code.

  Once the data is classified, it will plot the annual and monthly summary in:
  COMMON\plots\Annual
    - It contains summary.png showing how each category changes year-to-year.
    - Each plot contains four subplots showing:
        a) Annual expenses for each category spent per year
        b) Fraction of money spend on each category per year
        c) Total expenses per year
        d) Purchase history of all transactions: amount vs months

  COMMON\plots\Monthly
    - It contains a plot for each category type.
    - Each plot contains four subplots showing:
        a) Monthly expenses for each category spent per month
        b) Fraction of money spend on each category per month
        c) Purchase history for a category: amount vs months
        d) Rolling average for amount spent on category each month.
           Two rolling average window sizes are used: 3 and 6 months.
