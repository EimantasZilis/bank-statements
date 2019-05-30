from pandas.api.types import is_numeric_dtype
import file_management as fm

""" Process and validate data from raw data.xlsx.
Convert it into useable format by merging description
and extra columns into info, removing blacklisted
transactions and classifying data where possible. """

def migrate():
    """ Import data from raw_data.xlsx, tidy it up
    and classify transactions based on the known,
    classified transactions """
    raw_data = fm.XlsxWrapper("raw data.xlsx", "I")
    raw_data.initialise()
    mand_columns = ['Date', 'Description', 'Extra', 'Amount']
    raw_data.drop_columns(mand_columns)
    validate(raw_data)

def validate(raw_data):
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

    if not raw_data.is_blank():
        raw_data.write_as(new_name="classified.xlsx", new_type="O")

    blank_types = raw_data.get_attr("Type") == ""
    show_summary(raw_data, blank_types)
    if blank_types.any():
        classified_index = raw_data.filter(~blank_types).index.values.tolist()
        raw_data.drop_rows(classified_index)
        raw_data.write_as(new_name="unclassified.xlsx", new_type="O")

def show_summary(raw_data, blank_types):
    """ Print the number of unclassified and
    classified transactions found """
    total_count = raw_data.count_rows()
    classified_count = len(raw_data.filter(~blank_types).index)
    unclassified_count = total_count - classified_count
    info = " >> Classified: {c}/{t}\n >> Unclassified: {u}/{t}"
    print(info.format(c=classified_count, t=total_count, u=unclassified_count))

def add_info_column(raw_data):
    raw_data.get_attr("Description").fillna("", inplace=True)
    raw_data.get_attr("Extra").fillna("", inplace=True)
    raw_data.merge_columns("Description", "Extra", "Info", True)

def classify(raw_data):
    """ Classify transactions and assign their
    type to a new "Type" column. """
    categories = fm.JsonWrapper("categories.json", "I")
    types = raw_data.get_attr("Info").apply(
        lambda x: categories.lookup(x, default=""))
    raw_data.set("Type", types)

def drop_blacklisted_transactions(raw_data):
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

    if not returns.is_blank():
        returns.write()
