import statements
import plot.monthly
import plot.summary

def main():
    statements.process_unclassified_data()
    statements.import_raw_data()
    classified = statements.get_classified_data()
    plot.monthly.do_it(classified.df)
    plot.summary.do_it(classified.df)

if __name__ == "__main__":
    main()
