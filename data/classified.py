import file_management as fm

""" a module for working with classified data.
It uses data from classified.xlsx and removes
any transactions with blank type for consitency """

classified = fm.Statements("classified.xlsx", "O")
unclassified = classified.get_attr("Type").isna()
classified.filter(~unclassified, inplace=True)

def get_classified():
    """ Return classified data"""
    return classified

def add_date_cols(df):
    """ Add extra columns to the dataframe:
    Week (of the year), YearMonth (Month and year), Year and delta
    (difference between days compared to the earliest one) """
    date_col = df.get_attr("Date")
    min_date = date_col.min()
    df.set("delta", date_col.map(lambda dt: (dt-min_date).days))
    df.set("Week", date_col.map(lambda dt: dt.isocalendar()[1]))
    df.set("YearMonth", date_col.map(lambda dt: dt.replace(day=1)))
    df.set("Year", date_col.map(lambda dt: dt.replace(month=1,day=1)))
