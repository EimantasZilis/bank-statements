import matplotlib.pylab as plt
import pandas as pd

import user_io
import statements
import stats


def monthly(main_df):
    """
    Generate a plot capturing monthly changes for each expense
    category. Each plot contains four subplots:
        1. Total expenses against expense category spendings per month
        2. (Expense category / total expenses) ratio per month
        3. Expense category distribution of amount vs date
        4. Two rolling averages for expense category per month

    """

    ptable = stats.pivotTable(main_df, common_timeframe, 'Amount')
    expenses_summary = stats.ratios(ptable)
    monthly_totals = tidy(stats.totals(ptable))

    # Generate a set of plots for each expense category
    for category in expenses_summary.index:
        f, axs = plt.subplots(2, 2, figsize=(20,10))

        # Subplot 1: expense category vs totals each month
        summary = tidy(expenses_summary.loc[category])
        data = [monthly_totals, summary]
        axs[0][0] = do_monthly_subplot1(axs[0][0], data, category)

        # Subplot 2: expense category / totals each month
        data = expenses_summary.T[category]
        axs[0][1] = do_monthly_subplot2(axs[0][1], data, category)
        # Subplot 3: Spending distribution if amount vs date
        data = main_df[main_df.Type==category]
        axs[1][0] = do_monthly_subplot3(axs[1][0], data, category)

        # Subplot 4: rolling averages of expense category each month
        axs[1][1] = do_monthly_subplot4(axs[1][1], data, category)

        # Write data
        f.tight_layout()
        filename = category + '.png'
        filepath = user_io.directory(filename,'Pm')
        plt.savefig(filepath, bbox_inches='tight')
        print(' >>',filepath)
    return


def annual(main_df):
    """
    Generate a plot capturing yearly changes for each expense
    category. Each plot contains four subplots:
        1. Total annual spendings for each category
        2. (Expense category / total expenses) ratio for each category
        3. Total spendings per year
        4. Total distribution of spendings per year: amount vs date
    """
    ptable = stats.pivotTable(main_df, common_timeframe, 'Amount')
    f, axs = plt.subplots(2, 2, figsize=(20, 10))

    # Subplot 1: Annual expenses for each category
    axs[0][0] = do_yearly_subplot1(axs[0][0], ptable)

    # Subplot 2: Expense category / totals each year
    data = stats.ratios(ptable)
    axs[0][1] = do_yearly_subplot2(axs[0][1], data)

    # Subplot 3: Total annual expenses
    data = stats.totals(ptable)
    axs[1][0] = do_yearly_subplot3(axs[1][0], data)

    # Subplot 4: Frequencies - amount vs date scatter
    data = stats.add_dateid(main_df)
    axs[1][1] = do_yearly_subplot4(axs[1][1], data)

    # Write data
    f.tight_layout()
    filepath = user_io.directory('summary.png','Pa')
    plt.savefig(filepath, bbox_inches='tight')
    print(' >>',filepath)
    return


def do_monthly_subplot1(axis, data, category):
    """
    Generate the first monthly subplot, showing spending
    for each category and total expenses for each month
    in comparison.
    """
    category_expenses = data[1]
    overall_monthly_expenses = data[0]
    set_ylim = min_max_lims(overall_monthly_expenses['Amount'],100)

    overall_monthly_expenses.plot(
        kind='bar',
        y='Amount',
        x=common_timeframe,
        cmap=plt.cm.Blues,
        ylim=set_ylim,
        edgecolor = "k",
        ax=axis,
    )

    category_expenses.plot(
        kind='bar',
        y='Amount',
        x=common_timeframe,
        cmap=plt.cm.Blues_r,
        ax=axis,
        rot=0
    )

    axis.set_xlabel("")
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    axis.set_ylabel('Amount')
    axis.set_xticklabels(common_xlabels.label)
    axis.set_title('Monthly expenses for '+ str(category))
    axis.legend(['Total', category])
    return axis


def do_monthly_subplot2(axis, data, category):
    """
    Generate the 2nd monthly subplot. It plots the ratio
    of (expense category / total expenses) for each month.
    """

    category_fraction = tidy(data)
    set_ylim = min_max_lims(category_fraction['Amount'],5)
    category_fraction.plot(
        kind='bar',
        x=common_timeframe,
        y='Amount',
        ylim=set_ylim,
        cmap=plt.cm.Blues,
        edgecolor = "k",
        ax=axis,
        rot=0
    )

    axis.set_xlabel("")
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    axis.set_ylabel("%")
    axis.set_xticklabels(common_xlabels.label)
    axis.set_title(str(category) + ' / total monthly expenses')
    axis.legend([category])
    return axis


def do_monthly_subplot3(axis, data, category):
    """
    Generate the 3rd monthly subplot showing spending
    distribution of amount vs date.
    """
    set_ylim = min_max_lims(data['Amount'],50)
    set_xlim = min_max_lims(data.delta)
    data.plot(
        x='delta',
        y='Amount',
        kind='scatter',
        ylim=set_ylim,
        xlim=set_xlim,
        alpha=0.3,
        ax=axis,
        s=40,
        c='k'
    )

    axis.set_xlabel("")
    axis.grid(linestyle=':')
    axis.set_ylabel('Amount')
    axis.set_xticks(common_xlabels.delta)
    axis.set_xticklabels(common_xlabels.label)
    axis.set_title('Purchase history for '+str(category))
    return axis


def do_monthly_subplot4(axis, data, category):
    """
    Generate the 4th monthly subplot showing two
    rolling averages for expense category.
    """
    rolling_averages = rolling_mean(
        data, 'Amount', common_rolling_size
    )
    set_ylim = min_max_lims(rolling_averages,20)
    set_xlim = min_max_lims(rolling_averages.index,0)
    rolling_averages.plot(
        ylim=set_ylim,
        xlim=set_xlim,
        cmap=plt.cm.tab10,
        linewidth=4,
        kind='line',
        style='-',
        alpha=0.8,
        ax=axis,
        rot=0
    )

    mra = '-monthly rolling average'
    apply_legends = [str(x) + mra for x in common_rolling_size]
    axis.set_xlabel("")
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    axis.set_ylabel('Amount')
    axis.set_xticks(common_xlabels.delta)
    axis.set_xticklabels(common_xlabels.label)
    axis.set_title('Rolling average values for ' + category)
    axis.legend(apply_legends)
    return axis


def do_yearly_subplot1(axis, data):
    """
    Generate the first yearly subplot, showing total
    spendings on each category across the years.
    """
    data.plot(
        kind='bar',
        cmap=plt.cm.Blues,
        ylim=min_max_lims(data,250),
        edgecolor = "k",
        ax=axis,
        rot=0
    )

    axis.set_title('Total annual expenses')
    axis.legend(data.columns.strftime("%Y").values)
    axis.set_ylabel('Amount')
    axis.set_xlabel("")
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    return axis


def do_yearly_subplot2(axis, data):
    """
    Generate the 2nd yearly subplot, showing ratio
    of (expense category / total expenses) for all
    expenses categories across the years.
    """
    data.plot(
        kind='bar',
        cmap=plt.cm.Blues,
        ylim=min_max_lims(data, 10),
        edgecolor = "k",
        ax=axis,
        rot=0
    )

    axis.set_title('Expense category / total annual expenses')
    axis.legend(data.columns.strftime("%Y").values)
    axis.set_xlabel("")
    axis.set_ylabel("%")
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    return axis


def do_yearly_subplot3(axis, data):
    """
    Generate the 3rd yearly subplot, showing total
    spendings across the years.
    """
    data.index = data.index.strftime("%Y").values
    data.plot(
        kind='bar',
        edgecolor = "k",
        cmap=plt.cm.Blues_r,
        ylim=min_max_lims(data,1000),
        ax=axis,
        rot=0
    )
    axis.set_title('Total annual expenses')
    axis.set_ylabel('Amount')
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    axis.set_xlabel("")
    return axis


def do_yearly_subplot4(axis, data):
    """
    Generate the 4th yearly subplot, showing spending
    distribution of amount vs date.
    """

    data.plot(
        kind='scatter',
        x='delta',
        y='Amount',
        ylim=min_max_lims(data['Amount'],50),
        alpha=0.3,
        ax=axis,
        s=40,
        c='k'
    )

    axis.set_ylabel('Amount')
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    axis.set_xlabel("")
    axis.set_title('Complete purchase history')
    axis.set_xticks(common_xlabels.delta)
    axis.set_xticklabels(common_xlabels.label)
    return axis


def date_labels(df,timeframe='YearMonth'):
    """
    For a range of dates in df.index, it generates custom xlabels
    to be used in the plot that look like:

    minDate,..., Jan\n2018, Feb, ..., Dec, Jan\n2018, Feb, ..., maxDate
    """

    dates = pd.DataFrame(df[timeframe].unique(), columns=[timeframe])
    dates.sort_values(axis=0, by='YearMonth', inplace=True)

    doYears = dates[timeframe] == dates[timeframe].map(
        lambda dt: dt.replace(month=1,day=1))

    min_dindex = dates.loc[:,timeframe].idxmin(axis=1)
    doYears[min_dindex] = True

    dates.loc[doYears, 'label'] = dates.loc[doYears, timeframe].map(
        lambda dt: dt.strftime("%b\n%Y")
    )

    doMonths = doYears == False#map(lambda x: not(x))
    dates.loc[doMonths, 'label'] = dates.loc[doMonths, timeframe].map(
        lambda dt: dt.strftime("%b")
    )

    min_date = dates.loc[min_dindex,timeframe]
    dates['delta'] = dates[timeframe].map(lambda dt: (dt-min_date).days)
    return dates


def tidy(df):
    """ Tidy up and prepare a dataframe that is cut from
    a pivot table. """

    df = df.reset_index()
    df.columns = [common_timeframe, 'Amount']
    dindex = df.loc[:,common_timeframe].idxmin(axis=1)
    date_min = df.loc[dindex,common_timeframe]

    df.loc[:,common_timeframe] = df.loc[:,common_timeframe].map(
        lambda dt: (dt - date_min).days
    )
    return df


def min_max_lims(df,roundup=10):
    """
    Calculates new limits [0, xmax] to be used for plotting.
    xmax is a rounded up maximum value that is also divisable
    by roundup.

    E.g.
    temp = pd.DataFrame({'A':[1,2,3,4,8],'B':[6,7,8,11,17]})
    print(min_max_lims(temp,5))       # returns [0, 20]

    That's because the highest number is 17 and
    the next available number divisable by 5 is 20.

    Input:
        df            Input dataframe
        roundup       Integer value used for rounding up
    Output:
        [0, xmax]     New limits used for plotting

    """
    if isinstance(df, pd.DataFrame):
        df = df.max()

    max_val = max(df)
    if roundup != 0:
        max_val -= max_val % -roundup
    return [0,max_val]


def rolling_mean(df, datatype, window_sizes):
    """
    Calculate mean rollong values for df['Amount']
    for a given window size window_sizes.
    """
    centre = False
    smoothing = None

    # Get total amount for each month and their deltas
    use_cols = [common_timeframe, 'Amount']
    df_groupby = df[use_cols].groupby(by=common_timeframe)
    df_rolling = df_groupby.sum().reset_index()
    delta = date_labels(df_rolling, common_timeframe)
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
        labels=['Amount', common_timeframe],
        inplace=True,
        axis=1
    )
    return df_rolling


print('Generating plots...')
common_rolling_size = [3, 6]
common_datatype = 'Amount'
common_timeframe = 'YearMonth'
common_xlabels = date_labels(statements.data,'YearMonth')
monthly(statements.data)
common_timeframe = 'Year'
annual(statements.data)
