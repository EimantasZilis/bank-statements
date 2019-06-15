import pandas as pd
from data.summary import get_transactions_summary
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
    show_common_path()
    show_transactions_summary()
    show_categories_summary()

def show_common_path():
    print("\nCommon path")
    upaths = Jdict("u_paths")
    print(" >>", upaths.lookup("COMMON"))

def show_categories_summary():
    """ Show categories summary"""
    categories_info = get_categories_summary()
    print("\nCategories")
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
    total, classified, unclassified = get_transactions_summary()
    txt = "\nTransactions\n >> Total: {}\n >> Classified: {}\n >> Unclassified: {}"
    print(txt.format(total, classified, unclassified))
