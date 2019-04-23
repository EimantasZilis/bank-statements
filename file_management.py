import os
import json
import pandas as pd

class File:
    """ Class for initialising and handling user files """
    common_path = r"C:\Users\Eimantas\Dropbox\finances"
    types = {'I': "Input", 'O': "Output", "P": "Plot"}

    def __init__(self, filename=None, type=''):
        self.filename = ''
        self.subfolders = ''
        self.type = ''
        self.parse_inputs(filename, type)
        self.init_dirs()

    def get_type_name(self):
        """ Return type name based on code. """
        return File.types.get(self.type, '')

    def parse_inputs(self, filename, type_code):
        """ Process filename and type_code. It parses
        the data into filename, subfolders and type """
        if self.filename is None:
            raise ValueError("Unspecified Filename")
        else:
            self.subfolders, self.filename = os.path.split(filename)
            self.type = File.types.get(type_code, "")

    def init_dirs(self):
        """ Initialise relevant directories """
        fp = self.file_pointer(with_file=False)
        os.makedirs(fp, exist_ok=True)

    def file_pointer(self, with_file=True):
        """ Return full file pointer to the file """
        fp =  os.path.join(File.common_path, self.type, self.subfolders)
        if with_file:
            fp = os.path.join(fp, self.filename)
        return fp

    def delete_file(self):
        """ Delete file """
        fp = self.file_pointer()
        os.remove(fp)

    def rename(self, new_name=None, new_type=None):
        """ Change file name and type"""
        if new_name is not None:
            self.subfolders, self.filename = os.path.split(new_name)
        if new_type is not None:
            self.type = File.types.get(new_type, "")

class JsonWrapper(File):
    """ Class for manipulating JSON files """

    def __init__(self, Filename=None, Type=''):
        super().__init__(filename=Filename, type=Type)
        self.dict = None
        self.read()

    def read(self):
        """ Read categories from .json file.
        Set up empty dictionary if file does
        not exist. """
        try:
            fp = self.file_pointer()
            with open(fp, "r") as file:
                self.dict = json.load(file)
        except FileNotFoundError:
            self.dict = {}

    def write(self, filename=None):
        """ Write categories to .json file. """
        fp = self.file_pointer()
        with open(fp, "w+") as file:
            json.dump(self.dict, file, indent=4, sort_keys=True)

    def update(self, id, value):
        """ Update value in dictionary. """
        self.dict[id] = value

    def append(self, id, value):
        """ It will append value to the list keyed on id.
        It will create a list of values if and when needed """
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

    def lookup(self, key, not_found_val=None):
        """ Look up a value in dictionary """
        return self.dict.get(key, not_found_val)

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

class XlsxFile(File):
    """ A class for manipulating Xlsx file properties and layout """
    mandatory_columns = ("Date", "Amount")

    def __init__(self, filename=None, type='', df=None):
        super().__init__(filename=filename, type=type)
        self.df = df

    def read(self, sheet="Sheet1"):
        """ Read categories from .xlsx file. Initialise
        the dataframe with mandatory_columns if the file
        does not exist. """
        try:
            fp = self.file_pointer()
            self.df = pd.read_excel(fp, sheet_name=sheet)
        except FileNotFoundError:
            cols = {col: [] for col in XlsxFile.mandatory_columns}
            self.df = pd.DataFrame(cols)

    def write(self, sheet="Sheet1", file_pointer=None):
        """ Write dataframe to .xlsx file if it isn't None """
        if file_pointer is None:
            file_pointer = self.file_pointer()
        writer = pd.ExcelWriter(file_pointer, engine="xlsxwriter",
                                datetime_format='dd mmm yyyy')
        self.df.to_excel(writer, sheet_name=sheet)
        worksheet = writer.sheets[sheet]
        worksheet.autofilter(0, 0, 0, 4)
        worksheet.freeze_panes(1, 0)
        writer.save()

    def write_as(self, new_name=None, new_type=None):
        """ Rename the file and write to it. """
        self.rename(new_name, new_type)
        self.write()

    def validate(self, mand_cols=None):
        """ Check if dataframe meets expected format.
        It must have all mandatory columns including the ones
        specified in mand_cols.
        Columns "None" in mand_cols are ignored. """

        if mand_cols is None:
            all_mand_cols = list(XlsxFile.mandatory_columns)
        else:
            all_mand_cols = [col for col in mand_cols if col is not None]
            all_mand_cols.extend(XlsxFile.mandatory_columns)

        xlsx_set = set(self.df.columns.values)
        mand_set = set(all_mand_cols)
        missing_cols = mand_set - xlsx_set
        if missing_cols:
            err_msg = "Mandatory column(s) not found in "
            err_txt = [err_msg, self.filename, ": ", ", ".join(missing_cols)]
            raise ValueError("".join(err_txt))

    def initialise(self, mand_cols=None):
        """ Initialise the dataframe
        Read the file and validate it. """
        self.read()
        self.validate(mand_cols)

class XlsxData(XlsxFile):
    """ A class for working with Xlsx file data """

    def __init__(self, filename=None, type='', df=None):
        super().__init__(filename=filename, type=type, df=df)

    def set_datetime(self, column=None, format=None):
        """ Converts a column to datetime with a given format.
        Column can be "index". """

        if column is None or format is None:
            err = "Cannot column to datetime: column or format not specified"
            raise ValueError(err)
        elif column == "index":
            pass
        elif column not in self.df.columns.values.tolist():
            raise ValueError("{c} is not a valid column".format(c=column))

        if column == "index":
            self.df.index = pd.to_datetime(self.df.index, format=format)
        else:
            self.df[column] = pd.to_datetime(self.df[column], format=format)

    def index_name(self):
        """ Return index name against the dataframe """
        return self.df.index.name

    def current_columns(self):
        """ Return a list of current column names"""
        return list(self.df.columns.values)

    def add_columns(self, new_columns, value):
        """ Adds columns to a data frame and
        populates it with value. """
        for new_col in new_columns:
            last_col_loc = len(self.current_columns())
            self.df.insert(last_col_loc, new_col, value)

    def rename_columns(self, rename_columns=None):
        """ Rename column labels. For changes to take
        place, existing column names must be present in
        rename_columns = {old_name1: new_name1, ...} """
        if rename_columns is not None:
            self.df.rename(columns=rename_columns, inplace=True)

    def merge_columns(self, col1=None, col2=None, col_name=None, replace=False):
        """ Merge two columns to create a new string based
        column. It will remove orignal columns if replace=True"""

        if col_name is None:
            raise ValueError("New column name must be specified")
        elif col1 is None or col2 is None:
            raise ValueError("Two column names not specified")

        str_col1 = self.df[col1].apply(lambda x: str(x))
        str_col2 = self.df[col2].apply(lambda x: str(x))
        self.df[col_name] = str_col1 + "|" + str_col2

        if replace:
            self.drop_columns(drop_cols=[col1, col2])

    def drop_rows(self, drop_index):
        """ Drop rows based on drop_index. It removes
        rows from instance that share the same index """
        drop_type = type(drop_index)
        if isinstance(drop_index, list) or isinstance(drop_index, int):
            self.df.drop(drop_index, inplace=True)
        else:
            indexes_in_df = drop_index.isin(self.df.index.values).tolist()
            if all(indexes_in_df):
                self.df.drop(index=drop_index, axis=1, inplace=True)
            else:
                err_txt = "Cannot drop some the rows with these IDs:\n >> {ids} \
                          \nThey are not in {file}"
                err = err_txt.format(ids=drop_index.values, file=self.filename)
                raise ValueError(err)

    def drop_columns(self, mandatory_cols=None, drop_cols=None):
        """ Drop columns. mandatory_cols and drop_cols
        are mutually exclusive. It will drop any columns
        specified in drop_cols. Alternatively, it will drop
        any columns not in mandatory_cols."""
        if drop_cols is not None:
            pass
        elif mandatory_cols is not None:
            current_cols = set(self.current_columns())
            mand_cols = set(mandatory_cols)
            drop_cols = current_cols - mand_cols
        self.df.drop(columns=drop_cols, axis=1, inplace=True)

    def show(self, n=5):
        """ Show dataframe contents. """
        print(self.df.head(n))

    def blank(self):
        """ Returns True if dataframe is empty.
        False otherwise """
        return self.df.empty

    def filter(self, values, inplace=False):
        """ Returns a copy of dataframe
        containing filtered values """
        if inplace:
            self.df = self.df[values]
        else:
            return self.df[values].copy()

    def filter_by_index(self, id):
        """ Return datarame when
        filtering by index """
        return self.df.loc[id]

    def set_index_name(self, name):
        """ Set index name"""
        self.df.index.name = name

    def apply(self, condition):
        """ Apply a condition to a dataframe"""
        return self.df.apply(condition, axis=1)

    def get_attr(self, attribute):
        """ Get attribute values from a dataframe"""
        return getattr(self.df, attribute)

    def set(self, attribute, values):
        """ Set values to an attribute
        within a dataframe """
        self.df[attribute] = values

    def update(self, new_df):
        """ Update dataframe with data from
        a new dataframe """
        if self.blank():
            self.df = new_df
        else:
            self.df.update(new_df)

    def equal(self, new_df):
        """ Return True if new_df is the same
        dataframe as the class instance """
        return self.df.equals(new_df)

    def index_values(self):
        for val in self.df.index:
            yield val

    def count_rows(self):
        return len(self.df.index)

class XlsxWrapper(XlsxData):
    """ A class for working with .xlsx files.
    It stores data in pandas dataframe for data
    manipulation and combines xlsxwriter for file I/O """

    def __init__(self, filename=None, type='', df=None):
        super().__init__(filename=filename, type=type, df=df)

class Statements(XlsxWrapper):
    """ A class for working with bank statements """
    mandatory_columns = ("ID", "Type")

    def __init__(self, filename=None, type='', df=None):
        super().__init__(filename=filename, type=type, df=df)
        self.read()
        self.validate()

    def read(self, Sheet="Sheet1"):
        """ Read the .xlsx file. If the dataframe is not
        initialised, it will read the dataframe from file
        and add mandatory columns. """
        if self.df is None:
            super().read(sheet=Sheet)
            current_columns = self.df.columns.values.tolist()
            for col in Statements.mandatory_columns:
                if col not in current_columns:
                    self.df[col] = None

    def validate(self, mand_cols=None):
        """ Check if statements xlsx file meets the expected format.
        Check mandatory columns and set ID as an index column. """
        if mand_cols is None:
            mand_cols = Statements.mandatory_columns
        super().validate(mand_cols)
        self.df.set_index("ID", inplace=True)
