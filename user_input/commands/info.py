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
        show_unclassified_summary()

def get_unclassified_count():
    """ Get a number of unclassified transactions"""
    classified = Statements("unclassified")
    return classified.count_rows()

def show_unclassified_summary():
    """ Show information about unclassified transactions"""
    count = get_unclassified_count()
    print("\nUnclassified transactions\n >> {}".format(count))

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
