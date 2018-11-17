import transaction
import datetime
import setup
import numpy as np
import pandas as pd

def initialise():
    """
    Gets transaction data from spreadsheets.
        
    Output:
        df      dataframe with transaction dates as index
                and following columns:
                  - Amount: transaction amount
                  - Type: assigned transaction type
                  - Desc: transaction description                     
    """ 

    debug = setup.debugMode()
    inputFilePath = setup.inputPath()
    print('Reading transaction data\n >>',inputFilePath,'\n')
    data = pd.read_csv(inputFilePath, encoding='ISO-8859-1')
    data = data.drop(['Country Code', 'Currency'], axis=1)
    df = transaction.process(data)
    return df


def write_csv(statement_data):
    """
    Write data to CSV to path specified in setup module.
    Input:
        statement_data            df to export as csv
    """
    outputFilePath = setup.outputPath()
    print('Updating transaction data...\n >>',outputFilePath)
    statement_data.to_csv(outputFilePath)
    return
    
