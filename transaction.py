import re
import datetime
import calendar
import setup
import pandas as pd


def getTypes(txt):
    """
    Given transaction description txt, it finds matching transaction
    types based on typesDict.

    1) It will return 'Bad' if a bad transaction is found such as paying in.
    2) If more than one type is found, it will return those types.
    3) If no matching type is found, it will return None

    Input:
        txt        Transaction description
    Output:
        types      Transaction types
    """
    if isinstance(txt, list):
        txt = ' '.join(txt)
        
    types = []  
    typesDict = setup.getTransactionTypeDict()
    for transType in typesDict:
        keywords = typesDict[transType]
        for keyword in keywords:
            found = re.search(keyword, txt, re.IGNORECASE)
            if found and transType == 'Bad':
                return transType
            elif found and transType not in types:
                types.append(transType)
                
    if not(types):
        types = None
    else:
        types = ','.join(types)
        return types


def process(df):
    """
    Process input data
    
    Input:
        df          Input dataframe with raw data
    Output:
        df          New data frame that contains:
                        'Date'   - Transaction datetime as index 
                        'Amount' - Transaction amount
                        'Desc'   - transaction description
                        'Type'   - Transaction type                            
    """

    print('Cleaning data...')
    df['Description1'] = df['Description1'].map(lambda x: x + ' ')
    df['Desc'] = df['Description1'] + df['Description2']
    df['Type'] = df['Desc'].map(lambda x: getTypes(str(x)))
    df['Amount'] = df.loc[:,'Amount'].map(
        lambda x: float(re.sub('[£|,]', '', x))
    )

    ok = (df['Amount'] >= 0) & (df['Type']!= 'Bad')
    df = df[ok]

    df = df.set_index('Date')
    df.index = pd.to_datetime(df.index)
    df['Amount'] = df['Amount'].astype(float)

    # Add extra columns
    df['Week'] = df.index.map(lambda dt: dt.isocalendar()[1])
    df['YearMonth'] = df.index.map(lambda dt: dt.replace(day=1))
    df['Year'] = df.index.map(lambda dt: dt.replace(month=1,day=1))
    
    df.drop(columns=['Description1', 'Description2'],axis=1, inplace=True)
    df.sort_index(axis=1, inplace=True)
    return df

