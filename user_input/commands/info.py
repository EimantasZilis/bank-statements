import pandas as pd
from data.summary import get_categories_summary
from data.summary import get_transactions_summary
from system.file_management import Jdict
from system.file_management import Statements

def process(commands=None):
    """ Run commands for 'info' subparser """
    if commands.all:
        commands.tranasctions = True
        commands.categories = True
        commands.path = True

    if commands.path:
        show_common_path()
    if commands.transactions:
        show_transactions_summary()
    if commands.categories:
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

def show_transactions_summary():
    """ Show transactions summary"""
    total, classified, unclassified = get_transactions_summary()
    txt = "\nTransactions\n >> Total: {}\n >> Classified: {}\n >> Unclassified: {}"
    print(txt.format(total, classified, unclassified))
