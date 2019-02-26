import sys
import user_io
import pandas as pd
import re

def import_data():
    """
    Import transaction categories and their keywords from
    csv and their keywords. Put it in dictionary
    """

    print(' >> Importing transaction categories')
    filepath = user_io.directory('categories.csv')

    try:
        categories_df = pd.read_csv(filepath)

    except FileNotFoundError:
        example_data = file_template()
        err_details = errtxt(filepath)
        print(err_details)
        print('For example...')
        print(example_data)
        sys.exit()
        
    return categories_df


def classify_data(df):

    print('\n')
    print('Assigning categories to transactions...')

    cats = {}
    categories_csv = import_data()
    for category in categories_csv.columns:
        keywords = categories_csv[category].dropna().values
        cats[category] = list(keywords)

    df['Type'] = None
    for id in df.index:
        description = df.loc[id,'Description']
        opt_type = df.loc[id,'Optional_type']
        id_type = classify(cats, description, opt_type)
        df.loc[id,'Type'] = id_type
    return df


def classify(cdict, desc, opt_type):
    """
    Given transaction description txt, it finds matching transaction
    types based on typesDict.

    1) It will return 'BLACKLIST' if a bad transaction is found.
    2) If more than one type is found, it will return comma-delimited
       types.
    3) If no matching type is found, it will return None

    Input:
        categories       Dictionary for transaction categories and keywords
                         associated with them.
        txt              Transaction description
    Output:
        types            Transaction types
    """

    if not(desc) and not(opt_type):
        return None

    categories = []
    txts = [desc, opt_type]
    for txt in txts:
        if not(txt):
            continue

        for category in cdict:
            keywords = cdict[category]
            for keyword in keywords:
                found = re.search(keyword, txt, re.IGNORECASE)
                if found and category == 'BLACKLIST':
                    return category
                elif found and category not in categories:
                    categories.append(category)

        if categories:
            break

    if not(categories):
        return None

    categories = ','.join(categories)
    return categories


def remove_blacklisted_transactions(df):
    """ Remove transactions that have type 'BLACKLIST' """
    blacklist = df.Type == 'BLACKLIST'
    df = df[~blacklist]
    return df


def errtxt(filepath):
    """ Generate missing 'categories.csv' file error txt with guidance """

    errtxt = (
        'ERROR: File with category definitions not found.\n'
        ' >> ' + str(filepath) + '\n'
        ' >> To clasify transactions, specify categories and\n'
        '    associated keyword with each category.\n\n'
        '    "BLACKLIST" is an optional reserved category name.\n'
        '    Any transactions with matching keywords will be\n'
        '    ignored.\n'
    )
    return errtxt


def file_template():
    """
    Generate a sample template for categories.csv
    """

    example_data = {
        'Category1':
            ['keywords1', 'keywords2', '...'],
        'Category2':
            ['keywords3', 'keywords4', '...'],
        'BLACKLIST':
            ['Paying in', 'Bad data', '...'],
        '...':
            ['...', '...', '...']
    }

    template = pd.DataFrame.from_dict(data=example_data, orient='columns')
    template = template.to_string(index=False)
    return template
