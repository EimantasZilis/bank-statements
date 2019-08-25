import os
import json
import pandas as pd

class File:
    """ Class for initialising and handling user files """
    types = {'D': "Data", "P": "Plot"}

    def __init__(self, filename=None, type='', system_file=False):
        self.expected_extension = None
        self.system_file = system_file
        self.filename = filename
        self.subfolders = ''
        self.type = type
        self.init_file()

    def init_file(self):
        """ Initialise file if filename is specified
        and parse it into filename, subfolders and type.
        It also creates relevant directories if required. """
        if self.filename is not None:
            self.parse_inputs(self.filename, self.type)
            self.init_dirs()

    def get_type_name(self):
        """ Return type name based on code. """
        return File.types.get(self.type, '')

    def parse_inputs(self, filename, type_code):
        """ Process filename and type_code. It parses
        the data into filename, subfolders and type """
        self.subfolders, self.filename = os.path.split(filename)
        self.type = File.types.get(type_code, "")

    def init_dirs(self):
        """ Initialise relevant directories """
        fp = self.file_pointer(with_file=False)
        os.makedirs(fp, exist_ok=True)

    def base_path(self):
        """ Return base path for the output depending on
        whether this is a file used by the source code or
        a file amendable/viewable by the user. """
        if self.system_file:
            return os.path.join(os.getcwd(), "system", "configuration")
        else:
            config = Jdict("u_paths")
            return config.lookup("COMMON")

    def file_pointer(self, with_file=True):
        """ Return full file pointer to the file """
        base = self.base_path()
        fp =  os.path.join(base, self.type, self.subfolders)
        if with_file:
            fp = os.path.join(fp, self.filename)
        return fp

    def delete_file(self):
        """ Delete file """
        fp = self.file_pointer()
        try:
            os.remove(fp)
        except FileNotFoundError:
            pass

    def rename(self, new_name=None, new_type=None):
        """ Change file name and type"""
        if new_name is not None:
            self.subfolders, self.filename = os.path.split(new_name)
        if new_type is not None:
            self.type = File.types.get(new_type, "")

    def file_exists(self, fp=None):
        """ Check if file exists. Returns True/False."""
        if fp is None:
            fp = self.file_pointer()
        return os.path.isfile(fp)

    def overwrite_check(self, fp):
        """ Raise IOError exception if the file already
        exists. It can be used as a check before the file
        is created."""
        if self.file_exists(fp):
            filename = os.path.basename(fp)
            error = " >> {} already exists. File was not overwritten."
            raise IOError(error.format(filename))

    def validate_file_extension(self):
        """ Check if file extension is set and compare
        against expected file extension if is isn't None.
        It adds expected extension to filename if extension
        isn't set. It raises an error if extension is already
        different to expected extension. It does nothing if
        extension is the same as expected extension. """
        if self.filename is None or self.expected_extension is None:
            return

        extension = os.path.splitext(self.filename)[1]
        if extension == self.expected_extension:
            pass
        elif extension == '':
            self.filename += self.expected_extension
        else:
            err = "File {f} must have {e} extension"
            error = err.format(f=self.filename, e=self.expected_extension)
            raise ValueError(error)

class Jdict(File):
    """ Class for manipulating JSON files and dictionaries """

    def __init__(self, Filename=None, Type='', dict=None, system_file=True):
        super().__init__(filename=Filename, type=Type, system_file=system_file)
        self.dict = dict
        self.initialise()

    def initialise(self):
        """ Initialise file """
        self.pre_read_validation()
        self.read()

    def pre_read_validation(self):
        """ Do validation before file is read. """
        self.expected_extension = ".json"
        self.validate_file_extension()

    def read(self):
        """ Read categories from .json file. Set up empty
        dictionary if file does not exist. Don't read if
        dict attribute is not None or if the filename is
        not specified. """
        if self.dict is not None or self.filename is None:
            return
        try:
            fp = self.file_pointer()
            with open(fp, "r") as file:
                self.dict = json.load(file)
        except FileNotFoundError:
            self.dict = {}

    def write(self):
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

    def extend(self, id, value):
        """ Extends the list and add a value keyed on id. """
        current_values = self.dict.get(id, None)
        if current_values is None:
            self.dict[id] = value
        elif isinstance(current_values, list):
            self.dict[id].extend(value)
        else:
            self.dict[id] = [current_values, value]

    def is_blank(self):
        """ Returns True if dict attribute is None"""
        return self.dict == None

    def show(self, pad='', level=None):
        """ Print the contents of categories dictionary.
        It will show each category and its keywords in
        pad XXXXX | ['YYYYY', 'ZZZZZ', ...] format. It
        adds padding at the end to each XXXXX in order
        to make the bars align for all categories. It
        prints None if dict attribute is None """

        if level is None:
            use_dict = self.dict
        else:
            use_dict = self.lookup(level)

        if use_dict is None:
            print(pad, None, " | ",  None)
            return

        max_length = 0
        for id in use_dict.keys():
            if max_length < len(id):
                max_length = len(id)
        for id, val in use_dict.items():
            padded_id = pad + id + (max_length - len(id))*' '
            print(padded_id, ' | ', val)

    def lookup(self, *keys, default=None):
        """ Look up a value in dictionary based on key.
        By providing multiple keys, it will get the values
        from nested dictionaries. If there are no nested
        dictionaries or the value against the key is not
        present, it will return the value specified in
        default.
        If a tuple is passed in via keys[0], it will
        iterate through it rather than keys as a whole."""
        if isinstance(keys[0], tuple) or isinstance(keys[0], list):
            if len(keys) == 1 and len(keys[0]) > 1 :
                # Iterable variable was passed in.
                # Iterate through it instead rather than keys
                keys = keys[0]

        new_level = self.dict
        for key in keys:
            if not isinstance(new_level, dict):
                return default
            new_level = new_level.get(key, default)
        return new_level

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

    def pop(self, key, default=None):
        """ Delete key from dictionary """
        self.dict.pop(key, default)

    def keys(self):
        return self.dict.keys()

    def items(self):
        return self.dict.items()

    def values(self):
        return self.dict.values()

class Excel(File):
    """ A class for working with .xlsx files.
    It stores data in pandas dataframe for data
    manipulation and combines xlsxwriter for file I/O """

    mandatory_columns = ("Date", "Amount")

    def __init__(self, filename=None, type='D', df=None):
        super().__init__(filename=filename, type=type)
        self.df = df
        self.pre_read_validation()

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

    def write_validation(self, file_pointer=None, overwrite_check=False):
        """ Do validation prior to writing the file. Throw
        exceptions if it fails any validations """
        if overwrite_check:
            # Throw exception if file already exists.
            self.overwrite_check(file_pointer)

    def write(self, sheet="Sheet1", file_pointer=None, overwrite_check=False):
        """ Write dataframe to .xlsx file if it isn't None """
        if file_pointer is None:
            # Get default file pointer if it isn't specified
            file_pointer = self.file_pointer()

        self.write_validation(file_pointer, overwrite_check)
        writer = pd.ExcelWriter(file_pointer, engine="xlsxwriter",
                                datetime_format='dd mmm yyyy')
        temp_df = self.reset_index(self.df)
        temp_df.to_excel(writer, sheet_name=sheet,header=False,
                         index=False, startrow=1)

        worksheet = writer.sheets[sheet]
        workbook = writer.book
        self.apply_styles(temp_df, worksheet, workbook)
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
            all_mand_cols = list(Excel.mandatory_columns)
        else:
            all_mand_cols = [col for col in mand_cols if col is not None]
            all_mand_cols.extend(Excel.mandatory_columns)

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

    def apply_styles(self, df, wsheet, wbook):
        """ Apply styles to xlsx spreadsheet. """
        wsheet.autofilter(0, 0, 0, len(df.columns)-1)
        wsheet.freeze_panes(1, 0)
        excel_config = Jdict("o_xlsx")
        self.apply_header_styles(df, excel_config, wsheet, wbook)
        self.apply_column_styles(df, excel_config, wsheet, wbook)
        self.apply_data_validation(df, excel_config, wsheet)

    def apply_data_validation(self, df, config, wsheet):
        """ Applies data validation to cell based on config.json.
        It checks "source" tag for "CATEGORIES" string. It will
        replace it with the list of categories if it finds one """
        categories_config = Jdict("u_categories")
        categories = [cat for cats in categories_config.values() for cat in cats]
        categories.sort()
        lookup_dropdown = ["STYLING", "COLUMN"]

        for col_num, name in enumerate(df.columns.values):
            do_lookup = list(lookup_dropdown)
            do_lookup.extend([name, "data_validation"])
            data_val = Jdict(dict=config.lookup(do_lookup))
            if data_val.is_blank():
                continue
            elif data_val.lookup("source") == "CATEGORIES":
                data_val.update("source", categories)

            wsheet.data_validation(first_row=1, first_col=col_num,
                                   last_row=1000000, last_col=col_num,
                                   options=data_val.dict)

    def apply_column_styles(self, df, excel_config, wsheet, wbook):
        """ Apply column styles based on config.json. """
        col_styles = excel_config.lookup("STYLING", "COLUMN", default={})
        for col_num, name in enumerate(df.columns.values):
            col_opts = col_styles.get(name)
            if col_opts is None:
                # Skip column if configuration not implemented
                continue
            width = float(col_opts.get("width", 20))
            cell_format = col_opts.get("cell_format", {})
            col_format = wbook.add_format(cell_format)
            wsheet.set_column(first_col=col_num, last_col=col_num,
                              width=width, cell_format=col_format)

    def apply_header_styles(self, df, excel_config, wsheet, wbook):
        """ Apply header style based on config.json. It will apply
        default configuration if it is not specified. """
        dheader = {"bold": True, "text_wrap": True, "valign": "top", "border": 1}
        header_style = excel_config.lookup("STYLING", "HEADER", default=dheader)
        header_format = wbook.add_format(header_style)
        for col_num, name in enumerate(df.columns.values):
            wsheet.write(0, col_num, name, header_format)

    def reset_index(self, df=None):
        """ Reset index for an input dataframe. It is
        only does it if index.name is specified """
        if df is None:
            return None
        elif df.index.name is not None:
            return df.reset_index()
        else:
            return df

    def pre_read_validation(self):
        """ Do validation before file is read. """
        self.expected_extension = ".xlsx"
        self.validate_file_extension()

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

    def is_blank(self):
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

    def set_values(self, attribute, values):
        """ Set values to an attribute
        within a dataframe """
        self.df[attribute] = values

    def update(self, new_df):
        """ Update dataframe with data from
        a new dataframe """
        if self.is_blank():
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

    def index(self):
        return self.df.index

    def count_rows(self):
        return len(self.df.index)

    def sort_values(self, by, axis=0, ascending=True):
        self.df.sort_values(by, axis=axis, ascending=ascending, inplace=True)

    def drop_duplicates(self, subset=None, keep="first"):
        self.df.drop_duplicates(subset=subset, keep=keep, inplace=True)

    def dropna(self, axis=0, subset=None, how='all', inplace=True):
        return self.df.dropna(axis=axis, how=how, subset=subset, inplace=inplace)


class Statements(Excel):
    """ A class for working with bank statements """
    mandatory_columns = ("ID", "Type")

    def __init__(self, filename=None, type='D', df=None):
        super().__init__(filename=filename, type=type, df=df)
        self.read()
        self.validate()

    def read(self, Sheet="Sheet1"):
        """ Read the .xlsx file. If the dataframe is not
        initialised, it will read the dataframe from file
        and add mandatory columns. """
        if self.df is None and self.filename is not None:
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

    def select_by(self, column, value=None, statement=True):
        """ Select transactions by a given column and value.
        It raises ValueError exception if a column is not in
        a statement. It will return a Statements object if
        statement is set to True and Pandas dataframe object
        otherwise"""
        if column not in self.df.columns.values:
            error = "{c} column not in {f}".format(c=column, f=self.filename)
            raise ValueError(error)

        get_results = self.get_attr(column) == value
        selection = self.filter(get_results)
        if statement:
            return Statements(df=selection.reset_index())
        else:
            return selection

def path_exists_or_is_creatable(path):
    """ Check if path exists of is creatable"""
    if not isinstance(path, str) or not path:
        return False
    try:
        return os.path.exists(path) or os.access(os.path.dirname(path), os.W_OK)
    except OSError:
        return False
