from system.file_management import Jdict
from system.file_management import Statements

""" A module for getting information about
transactions and their summaries"""

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

    summary = get_transactions_breakdown(file)
    total_count = summary.lookup("All", filter, default=0)
    classified_count = summary.lookup("Classified", filter, default=0)
    unclassified_count = summary.lookup("Unclassified", filter, default=0)
    return total_count, classified_count, unclassified_count

def get_transactions_breakdown(file="classified"):
    """ Generate a summary showing a number of classified,
    unclassified and total transactions. Also shows the same
    summary for unique transactions, where transactions are
    grouped by info column. """

    # Get info for all data
    all_data = Statements(file)
    total, classified, unclassified = get_count(all_data)

    # Get info for unique data
    all_data.drop_duplicates(subset="Info")
    total_unique, classified_unique, unclassified_unique = get_count(all_data)

    summary = {
        "All": {
            "Total": total,
            "Unique": total_unique
        },
        "Classified": {
            "Total": classified,
            "Unique": classified_unique
        },
        "Unclassified": {
            "total": unclassified,
            "Unique": unclassified_unique
        }
    }
    return Jdict(dict=summary)

def get_count(data):
    """ Return the number of transactions: all,
    classified and unclassified."""
    total_count = data.count_rows()
    classified_data = data.dropna(subset=["Type"], inplace=False)
    classified_count = len(classified_data.index)
    unclassified_count = total_count - classified_count
    return total_count, classified_count, unclassified_count
