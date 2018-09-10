import data

"""
Run this module to get transcation data from .txt file (data copied
from PDFs by hand) and output a CSV file with assigned category to
each transaction.

It will read and write data to directories specified in setup module.
"""

statementData = data.get()        # Get data from statements
data.writeCSV(statementData)      # Write data to CSV
