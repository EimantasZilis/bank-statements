import pandas as pd

def date_labels(df,timeframe='YearMonth'):
    """
    For a range of dates in df.index, it generates custom xlabels
    to be used in the plot that look like:

    minDate,..., Jan\n2018, Feb, ..., Dec, Jan\n2018, Feb, ..., maxDate
    """

    dates = pd.DataFrame(df[timeframe].unique(), columns=[timeframe])
    dates.sort_values(axis=0, by=timeframe, inplace=True)

    doYears = dates[timeframe] == dates[timeframe].map(
        lambda dt: dt.replace(month=1,day=1))

    min_dindex = dates.loc[:,timeframe].idxmin(axis=1)
    doYears[min_dindex] = True

    dates.loc[doYears, 'label'] = dates.loc[doYears, timeframe].map(
        lambda dt: dt.strftime("%b\n%Y")
    )

    doMonths = doYears == False
    dates.loc[doMonths, 'label'] = dates.loc[doMonths, timeframe].map(
        lambda dt: dt.strftime("%b")
    )

    min_date = dates.loc[min_dindex,timeframe]
    dates['delta'] = dates[timeframe].map(lambda dt: (dt-min_date).days)
    return dates


def min_max_lims(df, roundup=10, minval=0):
    """
    Calculates new limits [0, xmax] to be used for plotting.
    xmax is a rounded up maximum value that is also divisable
    by roundup.

    E.g.
    temp = pd.DataFrame({'A':[1,2,3,4,8],'B':[6,7,8,11,17]})
    print(min_max_lims(temp,5))       # returns [minval, 20]

    That's because the highest number is 17 and
    the next available number divisable by 5 is 20.

    Input:
        df            Input dataframe
        roundup       Integer value used for rounding up
    Output:
        [minval, xmax]     New limits used for plotting

    """
    if isinstance(df, pd.DataFrame):
        df = df.max()

    max_val = max(df)
    if roundup != 0:
        max_val -= max_val % -roundup
    return [minval,max_val]

def rolling_mean(df, datatype, timeframe, window_sizes=[3, 6]):
    """
    Calculate mean rollong values for df['Amount']
    for a given window size window_sizes.
    """
    centre = False
    smoothing = None

    # Get total amount for each month and their deltas
    use_cols = [timeframe, 'Amount']
    df_groupby = df[use_cols].groupby(by=timeframe)
    df_rolling = df_groupby.sum().reset_index()
    delta = date_labels(df_rolling, timeframe)
    df_rolling['delta'] = delta.delta
    df_rolling.set_index('delta', inplace=True)

    for wsize in window_sizes:
        col_name = str(wsize) + '-month rolling average'
        df_rolling[col_name] = df_rolling.loc[:,'Amount'].fillna(0).rolling(
            window=wsize,
            win_type=smoothing,
            center=centre,
            min_periods=1
        ).mean()

    df_rolling.drop(
        labels=['Amount', timeframe],
        inplace=True,
        axis=1
    )
    return df_rolling
