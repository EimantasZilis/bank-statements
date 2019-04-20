from pandas.api.types import is_numeric_dtype
import file_management as fm

raw_data = fm.XlsxWrapper("raw data.xlsx", "I")
raw_data.initialise()
categories = fm.JsonWrapper("categories.json", "I")
classified = fm.Statements("classified.xlsx", "O")
unclassified = fm.Statements("unclassified.xlsx", "O")

def validate():
    """ Validate and clean input data, remove expense-return
    transaction pairs and classify each transaction. """

    raw_data.set_index_name('ID')
    raw_data.set_datetime("Date", "%d/%m/%Y")
    add_info_column(raw_data)

    if not is_numeric_dtype(raw_data.get_attr("Amount")):
        raise ValueError('"Amount" column contains non-numeric values.')

    remove_returns(raw_data)
    classify(raw_data)
    drop_blacklisted_transactions(raw_data)

    if not raw_data.blank():
        raw_data.write_as(new_name="classified.xlsx", new_type="O")

    blank_types = raw_data.get_attr("Type") == ""
    if blank_types.any():
        classified_index = raw_data.filter(~blank_types).index.values.tolist()
        raw_data.drop_rows(classified_index)
        raw_data.write_as(new_name="unclassified.xlsx", new_type="O")

def add_info_column(raw_data):
    raw_data.get_attr("Description").fillna("", inplace=True)
    raw_data.get_attr("Extra").fillna("", inplace=True)
    raw_data.merge_columns("Description", "Extra", "Info", True)

def classify(raw_data):
    """ Classify transactions and assign their
    type to a new "Type" column. """
    types = raw_data.get_attr("Info").apply(lambda x: categories.lookup(x, ""))
    raw_data.set("Type", types)

def drop_blacklisted_transactions(df):
    """ Remove transactions that have type 'BLACKLIST' """
    black = raw_data.get_attr("Type") == "BLACKLIST"
    black_index = raw_data.filter(black).index
    raw_data.drop_rows(black_index)

def remove_returns(raw_data):
    """ Find pairs of transactions with the same, but
    negative amounts. This indicates an item being returned:
    net spending of 0. Remove these transaction pairs. """

    negative_amounts = raw_data.get_attr("Amount") < 0
    returns_df = raw_data.filter(negative_amounts)
    if returns_df.empty:
        return

    returns = fm.XlsxWrapper("Excluded returns.xlsx", "O", returns_df)

    for return_id in returns.index_values():
        return_line = returns.filter_by_index(return_id)
        orig_amount = raw_data.get_attr("Amount") == -1*return_line.Amount
        orig_desc = raw_data.get_attr("Info") == return_line.Info
        expenses = raw_data.filter(orig_amount & orig_desc)

        if expenses.empty:
            returns.df.drop(return_id,inplace=True)
        else:
            # Find closest expense date compared to return date
            expenses["Delta"] = (return_line["Date"] - expenses.Date)
            past_expenses = expenses.Delta.dt.days >= 0
            if not(past_expenses.any()):
                continue

            expenses = expenses[past_expenses]
            buy_id = expenses.Delta.idxmin(axis=0)
            raw_data.drop_rows([buy_id, return_id])

    if not returns.blank():
        returns.write()

def add_date_cols(raw_data):
    """ Add extra columns to the dataframe:
    Week (of the year), YearMonth (Month and year), Year and delta
    (difference between days compared to the earliest one) """

    date_col = raw_data.get_attr("Date")
    min_date = date_col.min()
    raw_data.set("delta", date_col.map(lambda dt: (dt-min_date).days))
    raw_data.set("Week", date_col.map(lambda dt: dt.isocalendar()[1]))
    raw_data.set("YearMonth", date_col.map(lambda dt: dt.replace(day=1)))
    raw_data.set("Year", date_col.map(lambda dt: dt.replace(month=1,day=1)))

def update_classified_data(newly_classified):
    """ Update classified data with newly_classified """
    print(" >> Updating classified data")
    classified.update(newly_classified)
    classified.write()

def update_unclassified_data(newly_classified):
    """ Amend or remove unclassified data """
    print(" >> Updating unclassified data")
    if unclassified.equal(newly_classified):
        unclassified.delete_file()
    else:
        unclassified.drop_rows(newly_classified.index)
        unclassified.write()

def update_categories_dict(newly_classified):
    """ Update categories dictionary with new classifications """
    print(" >> Updating classifications")
    for id in newly_classified.index:
        line = newly_classified.loc[id]
        categories.update(line.Info, line.Type)
    categories.write()

def get_classified_data():
    """ Get classified data """
    return classified

def import_raw_data():
    """ Import data f   rom raw_data.xlsx, tidy it up
    and classify transactions based on the known,
    classified transactions """
    mand_columns = ['Date', 'Description', 'Extra', 'Amount']
    raw_data.drop_columns(mand_columns)
    validate()

def process_unclassified_data():
    """ Check for any manually classified transactions in
    unclassified.xlsx and update classified.xlsx lines. """
    if not unclassified.blank():
        newly_classified = unclassified.df.dropna(axis=0, subset=['Type'])

        new_count = len(newly_classified.index)
        total_count = unclassified.count_rows()
        info = "{c} / {t} classified in unclassified.xlsx"
        print(info.format(c=new_count, t=total_count))

        if not newly_classified.empty:
            print("Processing unclassified data...")
            update_classified_data(newly_classified)
            update_unclassified_data(newly_classified)
            update_categories_dict(newly_classified)
