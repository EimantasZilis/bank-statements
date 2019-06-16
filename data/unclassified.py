from data.raw import classify
from system.file_management import Jdict
from system.file_management import Statements
from data.summary import get_transactions_summary

categories = Jdict("u_cmappings")
classified = Statements("classified")
unclassified = Statements("unclassified")

def process():
    """ Check for any manually classified transactions in
    unclassified.xlsx and update classified.xlsx lines. """
    if unclassified.is_blank():
        print(" >> All transactions classified already")
    else:
        newly_classified = unclassified.df.dropna(axis=0, subset=['Type'])
        if newly_classified.empty:
            print(" >> No new classifications available")
        else:
            show_summary()
            update_categories_dict(newly_classified)
            update_classified_data(newly_classified)
            update_unclassified_data(newly_classified)

def show_summary():
    total_count, new_count, unclassified = get_transactions_summary("Unclassified")
    info = " >> New classifications: {c}/{t}"
    print(info.format(c=new_count, t=total_count))

def update_classified_data(newly_classified):
    """ Update classified data with newly_classified.
    Also find other similar transactions and classify
    them as well. """
    classified.update(newly_classified)
    classify(classified)
    classified.write()

def update_unclassified_data(newly_classified):
    """ Amend or remove unclassified data """
    if unclassified.equal(newly_classified):
        unclassified.delete_file()
    else:
        unclassified.drop_rows(newly_classified.index)
        unclassified.write()

def update_categories_dict(newly_classified):
    """ Update categories dictionary with new classifications """
    for id in newly_classified.index:
        line = newly_classified.loc[id]
        categories.update(line.Info, line.Type)
    categories.write()
