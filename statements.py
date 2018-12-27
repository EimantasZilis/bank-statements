import datetime
import sys
import re

import pandas as pd

import user_io
import categories




def validate(df):
    """
    Validate and clean input data, remove expense-return
    transaction pairs and classify each transaction.

    It also adds new columns to the dataframe:
        - Type: Predicted transaction classification
        - Week: transaction week of the Year
        - YearMonth: transaction month and year
        - Year: transaction year
    """

    print('Validating data...')

    df.index.name = 'ID'
    df.Description = df.Description.fillna('')
    df.Optional_type = df.Optional_type.fillna('')
    df.Amount = df.Amount.map(lambda x: re.sub('[£|,]', '', x))
    df.Amount = df.Amount.astype(float)
    df.Date = pd.to_datetime(df.Date)
    df = remove_returns(df)
    df = categories.classify_data(df)

    if not(df.empty):
        export_classified_data(df)

    unclassified = df.Type.isnull()
    if unclassified.any():
        export_unclassified_data(df)
        sys.exit()

    df = categories.remove_blacklisted_transactions(df)
    df = add_date_cols(df)

    df.drop(
        columns=['Description', 'Optional_type'],
        inplace=True,
        axis=1
    )
    return df


def remove_returns(df):
    """
    Find pairs of transactions with the same, but negative amounts.
    This indicates an item being returned: net spending of 0.
    Remove these transaction pairs.

    Export the transaction pairs into csv. These represent removed
    data from the df.
    """

    removed = {
        'Amount': [],
        'Buy ID': [],
        'Return ID': [],
        'Buy date': [],
        'Return date': [],
        'Description': [],
        'Optional_type': []
    }

    returns = df[df['Amount'] < 0]
    for return_index in returns.index:
        return_transaction = returns.loc[return_index]

        orig_expenses = df[
            (df.Amount == -1*return_transaction.Amount) \
            & (df.Description == return_transaction.Description)
        ].copy()

        if not(orig_expenses.empty):
            # Find smallest (return-purchase) date difference
            orig_expenses['Diff'] = orig_expenses.loc[:,'Date'].map(
                lambda x: (return_transaction['Date'] - x).days
            )

            past_expenses = orig_expenses['Diff'] >= 0
            if not(past_expenses.any()):
                continue

            expenses = orig_expenses[past_expenses]
            matching_index = expenses.loc[:,'Diff'].idxmin(axis=0)
            df = df.drop(df.index[[matching_index, return_index]])
            expense = expenses.loc[matching_index]

            # Add dropped transactions to 'removed' dict
            removed['Description'].append(return_transaction['Description'])
            removed['Return date'].append(return_transaction['Date'])
            removed['Amount'].append(-1*return_transaction['Amount'])
            removed['Optional_type'].append(expense['Optional_type'])
            removed['Buy date'].append(expense['Date'])
            removed['Return ID'].append(return_index)
            removed['Buy ID'].append(matching_index)

    # Export to csv
    for column in removed:
        if column != []:
            filepath = user_io.directory('excluded returns.csv')
            pd.DataFrame(removed).to_csv(filepath, index=False)
            print(' >> Excluded return transaction pairs')
            print(' >>',filepath)
            break
    return df

def add_date_cols(df):
    """
    Add extra columns to the dataframe:
        Week:       Week of the year.
        YearMonth:  Month and year.
        Year:       Year
        delta:      Difference of every date compared to the earliest one.

    """
    min_date = df.Date.min()
    df['delta'] = df.Date.map(lambda dt: (dt-min_date).days)
    df['Week']  = df.Date.map(lambda dt: dt.isocalendar()[1])
    df['YearMonth'] = df.Date.map(lambda dt: dt.replace(day=1))
    df['Year'] = df.Date.map(lambda dt: dt.replace(month=1,day=1))
    return df

def export_classified_data(df):
    """ Export classified data to csv. """
    classified_path = user_io.directory('classified.csv')
    df.to_csv(classified_path)
    print('\n','Exporting classified transactions...')
    print(' >>',classified_path,'\n')
    return


def export_unclassified_data(df):
    """
    Generate a warning about unclassified Transactions
    and export unclassified to a csv.
    """

    incomplete = df[unclassified].sort_values(by='Description')
    incomplete_path = user_io.directory('unclassified.csv')
    incomplete.to_csv(incomplete_path)
    print('Exporting unclassified transactions...')
    print(' >>',incomplete_path)
    print(' >> Make sure all transactions are classified to continue')
    return


def errtxt(filepath):
    """ Generate missing 'raw data.csv' file error txt with guidance """

    errtxt = (
        'ERROR: File with input transaction data not found.\n'
        ' >> ' + str(filepath) + '\n'
        ' >> It must have mandatory columns:\n'
        '    "Date" - transaction date.\n'
        '    "Description" - text describing transaction.\n'
        '    "Optional_type" - Category specified by data source (optional)\n'
        '    "Amount" - transaction amount. It assumes it is in pounds and\n'
        '               removes any "£" symbols.\n'
        '               Transactions with any other non-numeric characters\n'
        '               will be ignored.\n'
    )
    return errtxt


def file_template():
    """
    Generate a sample template for categories.csv
    """
    example_data = {
        'Date    ':
            ['01/02/03', '22/11/16', '...'],
        'Description' :
            ['Sainsbury\'s', 'Tesco', '...'],
        'Optional_type':
            ['Online', 'food shopping', '...'],
        ' Amount':
            ['£15.03', '0.2', '...'],
        '...':
            ['...', '...', '...']
        }

    template = pd.DataFrame.from_dict(data=example_data, orient='columns')
    template = template.to_string(index=False)
    return template


# Import data from statements
filepath = user_io.directory('raw data.csv')
print('\nReading transaction data\n >>',filepath,'\n')

try:
    raw_data = pd.read_csv(filepath, encoding='ISO-8859-1')
    mand_columns = ['Date', 'Description', 'Optional_type', 'Amount']
    data = raw_data[mand_columns].copy()
    data = validate(data)

except FileNotFoundError:
    template = file_template()
    err_details = errtxt(filepath)
    print(err_details)
    print('For example...')
    print(template)
    sys.exit()
