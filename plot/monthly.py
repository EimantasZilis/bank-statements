import matplotlib.pylab as plt
import matplotlib.cm as cm
import numpy as np

import stats
import user_io
import plot.generate as generate

TIMEFRAME = 'YearMonth'

def do_it(main_df):
    """
    Generate a plot capturing monthly changes for each expense
    category. Each plot contains four subplots:
        1. Total expenses against expense category spendings per month
        2. (Expense category / total expenses) ratio per month
        3. Expense category distribution of amount vs date
        4. Two rolling averages for expense category per month

    """
    xlabels = generate.date_labels(main_df, TIMEFRAME)
    ptable = stats.pivotTable(main_df, TIMEFRAME, 'Amount')
    monthly_totals = tidy(stats.totals(ptable))
    monthly_fraction = stats.ratios(ptable)

    # Generate a set of plots for each expense category
    for category in ptable.index:
        f, axs = plt.subplots(2, 2, figsize=(20,10))

        # Subplot 1: expense category vs totals each month
        category_summary = tidy(ptable.loc[category])
        data = [monthly_totals, category_summary]
        axs[0][0] = subplot1(axs[0][0], data, category, xlabels)

        # Subplot 2: expense category / totals each month
        category_fraction = tidy(monthly_fraction.T[category])
        axs[0][1] = subplot2(axs[0][1], category_fraction, category, xlabels)

        # Subplot 3: Spending distribution if amount vs date
        data = main_df[main_df.Type==category]
        axs[1][0] = subplot3(axs[1][0], data, category, xlabels)

        # Subplot 4: rolling averages of expense category each month
        axs[1][1] = subplot4(axs[1][1], data, category, xlabels)

        # Write data
        f.tight_layout()
        filename = category + '.png'
        filepath = user_io.directory(filename,'Pm')
        plt.savefig(filepath, bbox_inches='tight')
        print(' >>',filepath)
    return


def subplot1(axis, data, category, xlabels):
    """
    Generate the first monthly subplot, showing spending
    for each category and total expenses for each month
    in comparison.
    """
    category_expenses = data[1]
    overall_monthly_expenses = data[0]
    set_ylim = generate.min_max_lims(overall_monthly_expenses['Amount'],100)
    overall_monthly_expenses.plot(
        kind='bar',
        y='Amount',
        x=TIMEFRAME,
        cmap=plt.cm.Blues,
        ylim=set_ylim,
        edgecolor = "k",
        ax=axis,
    )

    category_expenses.plot(
        kind='bar',
        y='Amount',
        x=TIMEFRAME,
        cmap=plt.cm.Blues_r,
        ax=axis,
        rot=0
    )

    axis.set_xlabel("")
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    axis.set_ylabel('Amount')
    axis.set_xticklabels(xlabels.label)
    axis.set_title('Monthly expenses for '+ str(category))
    axis.legend(['Total', category])
    return axis


def subplot2(axis, data, category, xlabels):
    """
    Generate the 2nd monthly subplot. It plots the ratio
    of (expense category / total expenses) for each month.
    """
    set_ylim = generate.min_max_lims(data['Amount'],5)
    data.plot(
        kind='bar',
        x=TIMEFRAME,
        y='Amount',
        ylim=set_ylim,
        cmap=plt.cm.Blues_r,
        edgecolor = "k",
        ax=axis,
        rot=0
    )

    axis.set_xlabel("")
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    axis.set_ylabel("%")
    axis.set_xticklabels(xlabels.label)
    axis.set_title(str(category) + ' / total monthly expenses')
    axis.legend([category])
    return axis


def subplot3(axis, data, category, xlabels):
    """
    Generate the 3rd monthly subplot showing spending
    distribution of amount vs date.
    """

    axis.scatter(
        data.delta,
        data.Amount,
        color=cm.Blues(1.),
        marker='o',
        alpha=0.3,
        s=40
    )

    new_ylim = generate.min_max_lims(data.Amount, roundup=50, minval=0.1)
    new_xlim = generate.min_max_lims(data.delta)

    axis.set_ylim(new_ylim)
    axis.set_xlim(new_xlim)
    axis.set_yscale('log')
    axis.set_xlabel("")
    axis.grid(linestyle=':')
    axis.set_ylabel('Amount')
    axis.set_xticks(xlabels.delta)
    axis.set_xticklabels(xlabels.label)
    axis.set_title('Purchase history for '+str(category))
    return axis


def subplot4(axis, data, category, xlabels):
    """
    Generate the 4th monthly subplot showing two
    rolling averages for expense category.
    """
    rolling_size = [3, 6]
    rolling_averages = generate.rolling_mean(
        data, 'Amount', TIMEFRAME, rolling_size
    )
    set_ylim = generate.min_max_lims(rolling_averages,20)
    set_xlim = generate.min_max_lims(rolling_averages.index,0)
    colours = cm.Blues(np.linspace(0.35,1,3))

    rolling_averages.plot(
        ylim=set_ylim,
        xlim=set_xlim,
        color=colours,
        linewidth=4,
        kind='line',
        style='-',
        alpha=0.8,
        ax=axis,
        rot=0
    )

    mra = '-monthly rolling average'
    apply_legends = [str(x) + mra for x in rolling_size]
    axis.set_xlabel("")
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    axis.set_ylabel('Amount')
    axis.set_xticks(xlabels.delta)
    axis.set_xticklabels(xlabels.label)
    axis.set_title('Rolling average values for ' + category)
    axis.legend(apply_legends)
    return axis


def tidy(df):
    """
    Tidy up data frame that is cut from a pivot table.
    Resets index, add columns: timeframe, 'Amount'
    """

    df = df.reset_index()
    df.columns = [TIMEFRAME, 'Amount']
    dindex = df.loc[:,TIMEFRAME].idxmin(axis=1)
    date_min = df.loc[dindex,TIMEFRAME]

    df.loc[:,TIMEFRAME] = df.loc[:,TIMEFRAME].map(
        lambda dt: (dt - date_min).days
    )
    return df
