import stats
import user_io
import matplotlib.pylab as plt
import pandas as pd

def all(dataframe):
    """
    Generate plots to capture an overview of expenses.
    It creates a plot for annual expenses and one for each
    expense category, capturing monthly changes.

    It saves plots to a directory specified in setup module.

    Input:
        dataframe         Input data
    """
    datatype = 'Amount'
    print('Generating plots...')
    monthly(dataframe, 'YearMonth', datatype)
    annual(dataframe, 'Year', datatype)
    return


def monthly(main_dataframe, timeframe, datatype):
    """
    Generate a plot capturing monthly changes for each expense
    category. Each plot contains four subplots:
        1. Total expenses against expense category spendings per month
        2. (Expense category / total expenses) ratio per month
        3. Expense category distribution of amount vs date
        4. Two rolling averages for expense category per month

    """
    general_properties = {
        'xlabels': date_labels(main_dataframe,timeframe),
        'rolling_window_sizes': [3, 6],
        'period': timeframe,
        'dtype': datatype,
        'category': None
    }

    # Get data to plot
    monthly_fraction = stats.ratios(main_dataframe, timeframe, datatype)
    expenses_summary = stats.pivotTable(main_dataframe, timeframe, datatype)
    monthly_totals = tidy(
        stats.totals(main_dataframe, timeframe, datatype), timeframe, datatype
    )

    summary = {}
    for category in expenses_summary.index:
        category_expenses = expenses_summary.loc[category]
        summary[category] = tidy(category_expenses, timeframe, datatype)

    # Generate a set of plots for each expense category
    for category in expenses_summary.index:
        general_properties['category'] = category
        f, axs = plt.subplots(2, 2, figsize=(20,10))

        # Subplot 1: expense category vs totals each month
        data = [monthly_totals, summary[category]]
        axs[0][0] = do_monthly_subplot1(axs[0][0], data, general_properties)

        # Subplot 2: expense category / totals each month
        data = monthly_fraction.T[category]
        axs[0][1] = do_monthly_subplot2(axs[0][1], data, general_properties)

        # Subplot 3: Spending distribution if amount vs date
        data = main_dataframe[main_dataframe.Type==category]
        axs[1][0] = do_monthly_subplot3(axs[1][0], data, general_properties)

        # Subplot 4: rolling averages of expense category each month
        data = summary[category]
        axs[1][1] = do_monthly_subplot4(axs[1][1], data, general_properties)

        # Write data
        f.tight_layout()
        filename = category + '.png'
        filepath = user_io.directory(filename,'Pm')
        plt.savefig(filepath, bbox_inches='tight')
        print(' >>',filepath)
    return


def annual(main_dataframe, timeframe, datatype):
    """
    Generate a plot capturing yearly changes for each expense
    category. Each plot contains four subplots:
        1. Total annual spendings for each category
        2. (Expense category / total expenses) ratio for each category
        3. Total spendings per year
        4. Total distribution of spendings per year: amount vs date
    """
    f, axs = plt.subplots(2, 2, figsize=(20, 10))

    general_properties = {
        'xlabels': date_labels(main_dataframe, 'YearMonth'),
        'period': timeframe,
        'dtype': datatype,
        'category': None
    }

    # Subplot 1: Annual expenses for each category
    data = stats.pivotTable(main_dataframe, timeframe, datatype)
    axs[0][0] = do_yearly_subplot1(axs[0][0], data, general_properties)

    # Subplot 2: Expense category / totals each year
    data = stats.ratios(main_dataframe, timeframe, datatype)
    axs[0][1] = do_yearly_subplot2(axs[0][1], data, general_properties)

    # Subplot 3: Total annual expenses
    data = stats.totals(main_dataframe, timeframe, datatype)
    axs[1][0] = do_yearly_subplot3(axs[1][0], data, general_properties)

    # Subplot 4: Frequencies - amount vs date scatter
    data = stats.add_dateid(main_dataframe)
    axs[1][1] = do_yearly_subplot4(axs[1][1], data, general_properties)

    # Write data
    f.tight_layout()
    filepath = user_io.directory('summary.png','Pa')
    plt.savefig(filepath, bbox_inches='tight')
    print(' >>',filepath)
    return


def do_monthly_subplot1(axis, data, general_properties):
    """
    Generate the first monthly subplot, showing
    spending for each category and total expenses
    for each month in comparison.

    Input:
        axis                    Plot axis
        data                    Data to plot
        general_properties      Extra properties
    Output:
        axis                    Modified plot axis
    """
    expense_category = general_properties['category']
    new_xlabels = general_properties['xlabels']
    timeframe = general_properties['period']
    datatype = general_properties['dtype']
    overall_monthly_expenses = data[0]
    category_expenses = data[1]

    overall_monthly_expenses.plot(
        kind='bar',
        y=datatype,
        x=timeframe,
        cmap=plt.cm.Blues,
        ylim=new_limits(overall_monthly_expenses[datatype],100),
        edgecolor = "k",
        ax=axis,
    )

    category_expenses.plot(
        kind='bar',
        y=datatype,
        x=timeframe,
        cmap=plt.cm.Blues_r,
        ax=axis,
        rot=0
    )

    axis.set_xlabel("")
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    axis.set_ylabel(datatype)
    axis.set_xticklabels(new_xlabels.label)
    axis.set_title('Monthly expenses for '+ str(expense_category))
    axis.legend(['Total', expense_category])
    return axis


def do_monthly_subplot2(axis, data, general_properties):
    """
    Generate the 2nd monthly subplot.
    It plots the ratio of (expense category / total expenses)
    for each month.

    Input:
        axis                    Plot axis
        data                    Data to plot
        general_properties      Extra properties
    Output:
        axis                    Modified plot axis
    """

    expense_category = general_properties['category']
    new_xlabels = general_properties['xlabels']
    timeframe = general_properties['period']
    datatype = general_properties['dtype']

    category_fraction = tidy(data, timeframe, datatype)
    category_fraction.plot(
        kind='bar',
        x=timeframe,
        y=datatype,
        ylim=new_limits(category_fraction[datatype],5),
        cmap=plt.cm.Blues,
        edgecolor = "k",
        ax=axis,
        rot=0
    )

    axis.set_xlabel("")
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    axis.set_ylabel("%")
    axis.set_xticklabels(new_xlabels.label)
    axis.set_title(str(expense_category) + ' / total monthly expenses')
    axis.legend([expense_category])
    return axis


def do_monthly_subplot3(axis, data, general_properties):
    """
    Generate the 3rd monthly subplot showing spending
    distribution of amount vs date.

    Input:
        axis                    Plot axis
        data                    Data to plot
        general_properties      Extra properties
    Output:
        axis                    Modified plot axis
    """
    expense_category = general_properties['category']
    new_xlabels = general_properties['xlabels']
    timeframe = general_properties['period']
    datatype = general_properties['dtype']

    data.plot(
        x='delta',
        y=datatype,
        kind='scatter',
        ylim=new_limits(data[datatype],50),
        xlim=new_limits(data.delta),
        alpha=0.3,
        ax=axis,
        s=40,
        c='k'
    )

    axis.set_xlabel("")
    axis.grid(linestyle=':')
    axis.set_ylabel(datatype)
    axis.set_xticks(new_xlabels.delta)
    axis.set_xticklabels(new_xlabels.label)
    axis.set_title('Purchase history for '+str(expense_category))
    return axis


def do_monthly_subplot4(axis, data, general_properties):
    """
    Generate the 4th monthly subplot showing two
    rolling averages for expense category.

    Input:
        axis                    Plot axis
        data                    Data to plot
        general_properties      Extra properties
    Output:
        axis                    Modified plot axis
    """
    rolling_windows = general_properties['rolling_window_sizes']
    expense_category = general_properties['category']
    new_xlabels = general_properties['xlabels']
    timeframe = general_properties['period']
    datatype = general_properties['dtype']

    rolling_averages = rolling_mean(data, datatype, rolling_windows)
    data_columns = rolling_averages.columns.values[1:]
    rolling_averages.plot(
        x=timeframe,
        ylim=new_limits(rolling_averages[data_columns],20),
        xlim=new_limits(rolling_averages[timeframe],0),
        cmap=plt.cm.tab10,
        linewidth=4,
        kind='line',
        style='-',
        alpha=0.8,
        ax=axis,
        rot=0
    )

    mra = '-monthly rolling average'
    apply_legends = [str(x) + mra for x in rolling_windows]

    axis.set_xlabel("")
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    axis.set_ylabel(datatype)
    axis.set_xticks(new_xlabels.delta)
    axis.set_xticklabels(new_xlabels.label)
    axis.set_title('Rolling average values for ' + expense_category)
    axis.legend(apply_legends)
    return axis


def do_yearly_subplot1(axis, data, general_properties):
    """
    Generate the first yearly subplot, showing total
    spendings on each category across the years.

    Input:
        axis                    Plot axis
        data                    Data to plot
        general_properties      Extra properties
    Output:
        axis                    Modified plot axis
    """
    data.plot(
        kind='bar',
        cmap=plt.cm.Blues,
        ylim=new_limits(data,250),
        edgecolor = "k",
        ax=axis,
        rot=0
    )

    axis.set_title('Total annual expenses')
    axis.legend(data.columns.strftime("%Y").values)
    axis.set_ylabel(general_properties['dtype'])
    axis.set_xlabel("")
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    return axis


def do_yearly_subplot2(axis, data, general_properties):
    """
    Generate the 2nd yearly subplot, showing ratio
    of (expense category / total expenses) for all
    expenses categories across the years.

    Input:
        axis                    Plot axis
        data                    Data to plot
        general_properties      Extra properties
    Output:
        axis                    Modified plot axis
    """
    data.plot(
        kind='bar',
        cmap=plt.cm.Blues,
        ylim=new_limits(data, 10),
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


def do_yearly_subplot3(axis, data, general_properties):
    """
    Generate the 3rd yearly subplot, showing total
    spendings across the years.

    Input:
        axis                    Plot axis
        data                    Data to plot
        general_properties      Extra properties
    Output:
        axis                    Modified plot axis
    """
    data.index = data.index.strftime("%Y").values
    data.plot(
        kind='bar',
        edgecolor = "k",
        cmap=plt.cm.Blues_r,
        ylim=new_limits(data,1000),
        ax=axis,
        rot=0
    )
    axis.set_title('Total annual expenses')
    axis.set_ylabel(general_properties['dtype'])
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    axis.set_xlabel("")
    return axis


def do_yearly_subplot4(axis, data, general_properties):
    """
    Generate the 4th yearly subplot, showing spending
    distribution of amount vs date.

    Input:
        axis                    Plot axis
        data                    Data to plot
        general_properties      Extra properties
    Output:
        axis                    Modified plot axis
    """
    new_xlabels = general_properties['xlabels']
    datatype = general_properties['dtype']

    data.plot(
        kind='scatter',
        x='delta',
        y=datatype,
        ylim=new_limits(data[datatype],50),
        alpha=0.3,
        ax=axis,
        s=40,
        c='k'
    )

    axis.set_ylabel(datatype)
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    axis.set_xlabel("")
    axis.set_title('Complete purchase history')
    axis.set_xticks(new_xlabels['delta'].values)
    axis.set_xticklabels(new_xlabels['label'].values)
    return axis


def date_labels(df,timeframe='YearMonth'):
    """
    For a range of dates in df.index, it generates custom xlabels
    to be used in the plot that look like:

    minDate,..., Jan\n2018, Feb, ..., Dec, Jan\n2018, Feb, ..., maxDate

    Input:
        df          dataframe, that has dates in df.index
        timeframe   timeframe used for the plot
    Output:
        xlabels
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


def tidy(df, timeframe, datatype):
    """
    Tidy up and prepare a dataframe that
    is cut from a pivot table.

    Input:
        df
        timeframe
        datatype
    Output:
        df
    """

    df = df.reset_index()
    df.columns = [timeframe, datatype]

    dindex = df.loc[:,timeframe].idxmin(axis=1)
    date_min = df.loc[dindex,timeframe]

    df.loc[:,timeframe] = df.loc[:,timeframe].map(
        lambda dt: (dt - date_min).days
    )
    return df


def new_limits(df,roundup=10):
    """
    Calculates new limits [0, xmax] to be used for plotting.
    xmax is a rounded up maximum value that is also divisable
    by roundup.

    E.g.
    temp = pd.DataFrame({'A':[1,2,3,4,8],'B':[6,7,8,11,17]})
    print(new_limits(temp,5))       # returns [0, 20]

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
    Calculate mean rollong values for df[datatype]
    for a given window size window_sizes.
    """
    centre = False
    smoothing = None
    for wsize in window_sizes:
        col_name = str(wsize) + '-month rolling average'
        df[col_name] = df[datatype].fillna(0).rolling(
            wsize,
            win_type=smoothing,
            center=centre,
            min_periods=1
        ).mean()

    df.drop(columns=[datatype], inplace=True, axis=1)
    return df
