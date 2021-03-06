import pandas as pd
import numpy as np
import matplotlib.pylab as plt

def pivotTable(dataFrame, timeframe, values):

        """
        Create a pivot table out of dataFrame

        Input:
            values         String specifying values for pivot table
        Output:
            ptable         Pivot table:
                             - index: Transaction types
                             - columns: Timeframe ('Years' or 'YearMonth')
                             - values: Amount
        """
        dfCols = dataFrame.columns.tolist()
        ptable = dataFrame.pivot_table(
            index = ['Type'],
            columns = [timeframe],
            values = [values],
            aggfunc=np.sum
        )

        ptable = ptable.fillna(0)
        ptable.columns = ptable.columns.droplevel(0)
        return ptable

def totals(ptable):
    """
    Calculate a sum of values in datatype column,
    for each timeframe.

    Input:
        ptable       Pivot table

    Ouptput:
        total        New dataframe with index = df[timeframe] and
                     datatype column with total values
    """
    total = ptable.sum(axis=0)
    if not(isinstance(total,pd.DataFrame)):
        total.to_frame()
    return total

def ratios(ptable):
    """
    Calculate the ratio of (category expenses/total expenses)
    Input:
        ptable       Pivot table

    Ouptput:
        total        New dataframe with ratios for each category
    """
    percentages = (ptable/ptable.sum())*100
    return percentages

def add_dateid(dataframe, expense_category=None):
    """
    Add a new 'date_id' column to the dataframe. It
    represents a date difference between earliest date
    and each date in the index.
    It has optional filtering by expense category.

    Input:
        dataframe           Dataframe with dates in dataframe.index
        expense_category    Optional expense category to filter by
    Output:

    """
    min_date = dataframe.Date.min()
    dataframe['delta'] = dataframe.Date.map(lambda dt: (dt - min_date).days)

    if expense_category:
        dataframe = dataframe[dataframe['Type']==expense_category]
    return dataframe
