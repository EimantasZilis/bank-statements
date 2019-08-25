import data.classified
import plot.monthly
import plot.summary

def process(cmd):
    if cmd.all:
        plot_data()

def plot_data():
    print("Generating plots...")
    classified = data.classified.get_classified()
    data.classified.remove_blacklist(classified)
    data.classified.add_date_cols(classified)
    plot.monthly.do_it(classified.df)
    plot.summary.do_it(classified.df)
