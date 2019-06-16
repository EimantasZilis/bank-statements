from system.file_management import Jdict
from system.file_management import Statements

""" A module for getting information about
transactions and their summaries"""

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

def get_transactions_summary(file="Classified", filter="Total"):
    """ Return a number of total, classified and
    unclassified transactions in a file.
    file can be "classified" or "unclassified"
    Can filter by total and unique transactions """

    ok_filters = ["Total", "Unique"]
    ok_files = ["Classified", "Unclassified"]

    if file not in ok_files:
        err = "{} invalid valid file.\n >> Must be one of {}"
        raise ValueError(err.format(file, ", ".join(ok_files)))

    elif filter not in ok_filters:
        err = "{} invalid filter.\n >> Must be one of {}"
        raise ValueError(err.format(file, ", ".join(ok_files)))

    all_data = Statements(file)
    if filter == "Unique":
        all_data.drop_duplicates(subset="Info")

    total_count, classified_count, unclassified_count = get_count(all_data)
    return total_count, classified_count, unclassified_count

def get_count(data):
    """ Return the number of transactions: all,
    classified and unclassified."""
    total_count = data.count_rows()
    classified_data = data.dropna(subset=["Type"], inplace=False)
    classified_count = len(classified_data.index)
    unclassified_count = total_count - classified_count
    return total_count, classified_count, unclassified_count
