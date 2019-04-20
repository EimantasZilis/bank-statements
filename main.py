import statements
import plot.monthly
import plot.summary

def main():
    statements.process_unclassified_data()
    statements.import_raw_data()
    classified = statements.get_classified_data()

    # Remove unclassified data for plotting purposes
    unclassified = classified.get_attr("Type").isna()
    classified.filter(~unclassified, inplace=True)
    statements.add_date_cols(classified)

    plot.monthly.do_it(classified.df)
    plot.summary.do_it(classified.df)

if __name__ == "__main__":
    main()
