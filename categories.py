import os
import sys
import json
import user_io
import pandas as pd
import re
import datetime

class UserIO:
    """ Handles file structure for user files """
    common_path = r"C:\Users\Eimantas\Dropbox\finances"
    types = {'I': "Input", 'O': "Output", "P": "Plot"}

    def __init__(self, filename=None, type=''):
        self.file_pointer = None
        self.filename = filename
        self.type = type
        self.path = None
        self.init_path()

    def get_type_name(self):
        return self.types.get(self.type, '')

    def init_path(self):
        if self.filename is None:
            raise ValueError("Unspecified Filename")
        else:
            type_name = self.get_type_name()
            self.path = os.path.join(self.common_path, type_name)
            self.file_pointer = os.path.join(self.path, self.filename)
            os.makedirs(self.path, exist_ok=True)

    def delete_file(self):
        os.remove(self.file_pointer)

class JsonWrapper(UserIO):
    """ Class for reading, writing
    and manipulating JSON files """

    def __init__(self, Filename=None, Type=''):
        super().__init__(filename=Filename, type=Type)
        self.dict = None
        self.read()

    def read(self):
        """ Read categories from .json file.
        Set dict attribute to empty dictionary
        if file does not exist. """
        try:
            with open(self.file_pointer, "r") as file:
                self.dict = json.load(file)
        except FileNotFoundError:
            self.dict = {}

    def write(self, filename=None):
        """ Write categories to .json file. """
        with open(self.file_pointer, "w+") as file:
            json.dump(self.dict, file, indent=4, sort_keys=True)

    def update(self, id, value):
        """ Update value in dict attribute. """
        self.dict[id] = value

    def append(self, id, value):
        """ It will append value to the list against id. It
        will create a list of values if and when needed """

        current_values = self.dict.get(id, None)
        if current_values is None:
            self.dict[id] = value
        elif isinstance(current_values, list):
            self.dict[id].append(value)
        else:
            self.dict[id] = [current_values, value]

    def show(self):
        """ Print the contents of categories dictionary.
        It will show each category and its keywords in
        XXXXX | ['YYYYY', 'ZZZZZ', ...] format.
        It adds padding at the end to each XXXXX in
        order to make the bars align for all categories. """
        max_length = 0
        for id in self.dict.keys():
            if max_length < len(id):
                max_length = len(id)
        for id, val in self.dict.items():
            padded_id = id + (max_length - len(id))*' '
            print(padded_id, ' | ', val)
        print('\n')

    def lookup(self, key):
        """ Look up a value in dictionary """
        return self.dict.get(key)

    def transpose(self):
        """ Swap key-value pairs in self.dict.
        E.g. convert {A:[a1, a2, ...], B:[b1, b2, ...]}
        dictionary to {a1:A, a2:A, ..., b1:B, b2:B, ...}
        and vice versa.

        It does not work with nested lists. It will raise
        and exception if it comes across a dictionary
        like {A:[[...], [...], ...], B:b1, ...} """

        old_dict = self.dict
        old_keys = old_dict.keys()
        self.dict = {}
        frequencies = {}

        for id in old_keys:
            values = old_dict[id]
            if not isinstance(values, list):
                values = [values]

            for value in values:
                if isinstance(value, list):
                    err_txt = "Nested lists not supported:" + str(values)
                    raise TypeError(err_txt)

                val_frequency = frequencies.get(value, 0)
                if val_frequency == 0:
                    self.dict[value] = id
                    frequencies[value] = 1

                elif val_frequency == 1:
                    self.dict[value] = [self.dict[value], id]
                    frequencies[value] += 1

                elif val_frequency > 1:
                    self.dict[value].append(id)
                    frequencies[value] += 1

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
