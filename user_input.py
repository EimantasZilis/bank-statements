import argparse

def init():
    """ Initialise and definte user input commands
    available in command prompt for the app """
    parser = argparse.ArgumentParser(description='Finances app')
    parser.add_argument("-i","--import", action="store_true", default=False,
                        help='Import raw data into the app', dest="migrate")
    parser.add_argument("-c", "--classify", action="store_true", default=False,
                        help="Classify data from unclassified.xlsx",
                        dest="classify")
    parser.add_argument("-p", "--plot",  action="store_true", default=False,
                        dest="plot", help='Generate plots')
    return parser.parse_args()

def classify_data():
    print("Classifying data from unclassified.xlsx...")
    import data.unclassified
    data.unclassified.process()
    print(" >> Done")

def import_data():
    print("Importing data from raw.xlsx...")
    import data.raw
    data.raw.migrate()
    print(" >> Done")

def plot_data():
    print("Generating plots...")
    import data.classified
    import plot.monthly
    import plot.summary
    classified = data.classified.get_classified()
    data.classified.add_date_cols(classified)
    plot.monthly.do_it(classified.df)
    plot.summary.do_it(classified.df)
    print(" >> Done")
