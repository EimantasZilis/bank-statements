from file_management import JsonWrapper as jdict
from file_management import Statements

def process(commands=None, config=None):
    """ Run commands for 'info' subparser """
    if commands.all:
        show_all(config)
    else:
        if commands.categories:
            show_categories_summary(config)
        if commands.path:
            show_common_path(config)

def show_all(config=None):
    """ Show information about the whole app"""
    print("\n")
    show_common_path(config)
    show_categories_summary(config)

def show_common_path(config=None):
    print("Common path")
    print(" >>", config.lookup("COMMON_PATH"), "\n")

def show_categories_summary(config):
    """ Show categories summary"""
    print("Classified transactions")
    categories_info = get_categories_summary(config)
    categories_info.show(" >> ")
    show_unclassified_summary()

def get_unclassified_count():
    """ Get a number of unclassified transactions"""
    classified = Statements("unclassified.xlsx", "O")
    return classified.count_rows()

def show_unclassified_summary():
    """ Show information about unclassified transactions"""
    count = get_unclassified_count()
    print("\nUnclassified transactions\n >> {}".format(count))

def get_categories_summary(config):
    """ Gets information about defined categories.
    Shows their names and a number of transactions
    used with each one """
    classified = Statements("classified.xlsx", "O")
    categories = config.lookup("CATEGORIES")
    cat_count = {k:0 for k in categories}
    cat_info = jdict(dict=cat_count)
    for category in categories:
        filtered = classified.select_by("Type", category)
        cat_info.update(category, filtered.count_rows())
    return cat_info
