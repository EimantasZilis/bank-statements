import file_management as fm

categories = fm.JsonWrapper("categories.json", "I")
classified = fm.Statements("classified.xlsx", "O")
unclassified = fm.Statements("unclassified.xlsx", "O")

def process():
    """ Check for any manually classified transactions in
    unclassified.xlsx and update classified.xlsx lines. """
    if unclassified.is_blank():
        print(" >> All transactions classified already")
    else:
        newly_classified = unclassified.df.dropna(axis=0, subset=['Type'])
        show_summary(unclassified, newly_classified)
        if not newly_classified.empty:
            update_classified_data(newly_classified)
            update_unclassified_data(newly_classified)
            update_categories_dict(newly_classified)

def show_summary(unclassified, newly_classified):
    new_count = len(newly_classified.index)
    total_count = unclassified.count_rows()
    info = " >> New classifications: {c}/{t}"
    print(info.format(c=new_count, t=total_count))

def update_classified_data(newly_classified):
    """ Update classified data with newly_classified """
    classified.update(newly_classified)
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
