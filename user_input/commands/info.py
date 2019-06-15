import pandas as pd
from system.file_management import Jdict
from system.file_management import Statements

def process(commands=None):
    """ Run commands for 'info' subparser """
    if commands.all:
        show_all()
    else:
        if commands.categories:
            show_categories_summary()
        if commands.path:
            show_common_path()

def show_all():
    """ Show information about the whole app"""
    print("\n")
    show_common_path()
    show_categories_summary()
    show_transactions_summary()

def show_common_path():
    print("Common path")
    upaths = Jdict("u_paths")
    print(" >>", upaths.lookup("COMMON"), "\n")

def show_categories_summary():
    """ Show categories summary"""
    categories_info = get_categories_summary()
    print("Categories")
    if categories_info is None:
        print(" >> Categories not defined")
    else:
        categories_info.show(" >> ")

def get_categories_summary():
    """ Gets information about defined categories.
    Shows their names and a number of transactions
    used with each one """
    classified = Statements("classified")
    ucategories = Jdict("u_categories")
    categories = ucategories.lookup("CATEGORIES")
    if categories is None:
        return None

    cat_count = {k:0 for k in categories}
    cat_info = Jdict(dict=cat_count)
    if classified.is_blank():
        return cat_info

    for category in categories:
        filtered = classified.select_by("Type", category)
        cat_info.update(category, filtered.count_rows())
    return cat_info

def show_transactions_summary():
    """ Show transactions summary"""
    summary = get_transactions_summary()
    df = pd.DataFrame(summary, index=["Total", "Unique"])
    print("\nTransactions:")
    print(df.head())

def get_transactions_summary(file="classified"):
    """ Generate a summary showing a number of classified,
    unclassified and total transactions. Also shows the same
    summary for unique transactions, where transactions are
    grouped by info column. """

    all_data = Statements(file)
    total, classified, unclassified = get_count(all_data)
    all_data.drop_duplicates(subset="Info")
    total_unique, classified_unique, unclassified_unique = get_count(all_data)

    summary = {}
    summary["Total"] = [total, total_unique]
    summary["Classified"] = [classified, classified_unique]
    summary["Unclassified"] = [unclassified, unclassified_unique]
    return summary

def get_count(data):
    """ Return the number of transactions: all,
    classified and unclassified."""
    total_count = data.count_rows()
    classified_data = data.dropna(subset=["Type"], inplace=False)
    classified_count = len(classified_data.index)
    unclassified_count = total_count - classified_count
    return total_count, classified_count, unclassified_count
