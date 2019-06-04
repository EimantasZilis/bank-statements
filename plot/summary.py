import matplotlib.pylab as plt
import matplotlib.cm as cm
import pandas as pd
import numpy as np

import plot.stats as stats
import plot.generate as generate
import system.file_management as fm

TIMEFRAME = 'Year'

def do_it(main_df):
    """
    Generate a plot capturing yearly changes for each expense
    category. Each plot contains four subplots:
        1. Total annual spendings for each category
        2. (Expense category / total expenses) ratio for each category
        3. Total spendings per year
        4. Total distribution of spendings per year: amount vs date
    """
    ptable = stats.pivotTable(main_df, TIMEFRAME, 'Amount')
    f, axs = plt.subplots(2, 2, figsize=(20, 10))

    # Subplot 1: Annual expenses for each category
    axs[0][0] = subplot1(axs[0][0], ptable)
    # Subplot 2: Expense category / totals each year
    axs[0][1] = subplot2(axs[0][1], stats.ratios(ptable))
    # Subplot 3: Total annual expenses
    axs[1][0] = subplot3(axs[1][0], stats.totals(ptable))
    # Subplot 4: Frequencies - amount vs date scatter
    axs[1][1] = subplot4(axs[1][1], main_df)

    # Write data
    f.tight_layout()
    image = fm.File(filename='summary.png', type="P")
    filepath = image.file_pointer()
    plt.savefig(filepath, bbox_inches='tight')
    print(' >>',filepath)
    del image

def subplot1(axis, data):
    """
    Generate the first yearly subplot, showing total
    spendings on each category across the years.
    """
    data.plot(
        kind='bar',
        cmap=plt.cm.Blues,
        ylim=generate.min_max_lims(data,250),
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


def subplot2(axis, data):
    """
    Generate the 2nd yearly subplot, showing ratio
    of (expense category / total expenses) for all
    expenses categories across the years.
    """
    data.plot(
        kind='bar',
        cmap=plt.cm.Blues,
        ylim=generate.min_max_lims(data, 10),
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


def subplot3(axis, data):
    """
    Generate the 3rd yearly subplot, showing total
    spendings across the years.
    """
    data.index = data.index.strftime("%Y").values
    data.plot(
        kind='bar',
        edgecolor = "k",
        cmap=plt.cm.Blues_r,
        ylim=generate.min_max_lims(data,1000),
        ax=axis,
        rot=0
    )
    axis.set_title('Total annual expenses')
    axis.set_ylabel('Amount')
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    axis.set_xlabel("")
    return axis


def subplot4(axis, data):
    """
    Generate the 4th yearly subplot, showing spending
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
    new_xlim = generate.min_max_lims(data.delta, minval=0)
    axis.set_ylim(new_xlim)
    axis.set_yscale('log')
    axis.set_ylim(new_ylim)
    axis.set_ylabel('Amount')
    axis.grid(linestyle=':')
    axis.xaxis.grid(False)
    axis.set_xlabel("")
    axis.set_title('Complete purchase history')
    xlabels = generate.date_labels(data, 'YearMonth')
    axis.set_xticks(xlabels.delta)
    axis.set_xticklabels(xlabels.label)
    return axis
