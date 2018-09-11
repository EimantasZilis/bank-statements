import data

"""
Run this module to get transcation data from .txt file (data copied
from PDFs by hand) and output a CSV file with assigned category to
each transaction.

It will read and write data to directories specified in setup module.
"""

# Read data from statements and write to CSV
statementData = data.get()       
data.writeCSV(statementData)
