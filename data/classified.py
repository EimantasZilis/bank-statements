from system.file_management import Statements, Jdict

""" a module for working with classified data.
It uses data from classified.xlsx and removes
any transactions with blank type for consitency """

classified = Statements("classified")
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
    df.set_values("delta", date_col.map(lambda dt: (dt-min_date).days))
    df.set_values("Week", date_col.map(lambda dt: dt.isocalendar()[1]))
    df.set_values("YearMonth", date_col.map(lambda dt: dt.replace(day=1)))
    df.set_values("Year", date_col.map(lambda dt: dt.replace(month=1,day=1)))

def remove_blacklist(data):
    """ Remove blacklisted data from dataframe"""
    categories = Jdict("u_categories")
    blacklist = categories.lookup("BLACKLIST")
    bad_data = data.get_attr("Type").isin(blacklist)
    data.filter(~bad_data, inplace=True)
