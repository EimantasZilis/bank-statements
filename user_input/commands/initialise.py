import pandas as pd
import file_management as fm

def process(commands=None, config=None):
    """ Run commands for 'initialise' subparser """
    if commands.setup:
        print("Initialising user files and folders...")
        setup_path(commands.setup[0], config)
        setup_files_and_dirs()

def setup_path(common_path, config):
    """ Validate and set up common path """
    validate_path(common_path)
    show_path_changes(common_path, config)
    write_path(common_path, config)

def validate_path(path):
    if not fm.path_exists_or_is_creatable(path):
        err = "{} is not a valid path\n >> Enter a different path"
        raise ValueError(err.format(path))

def show_path_changes(new_path, config):
    prev_path = config.lookup("COMMON_PATH")
    if prev_path == new_path:
        print(" >> No path changes")
    else:
        if prev_path:
            print(" >> Old path: {}".format(prev_path))
        print(" >> New path: {}".format(new_path))

def write_path(path, config):
    """ Set common path in config.json """
    config.update("COMMON_PATH", path)
    config.write()

def setup_files_and_dirs():
    """ Initialise user files and directories in common_path """
    setup_raw_data()

def setup_raw_data_template():
    """ Initialise raw data.xlsx file template """
    cols = ["Date", "Description", "Extra", "Amount"]
    blank_df = pd.DataFrame([[""]*len(cols)], columns=cols)
    return fm.XlsxWrapper(filename="raw data.xlsx", type='I', df=blank_df)

def setup_raw_data():
    """ Write raw data.xlsx file template to file. It does
    not overwrite the file if it already exists. It raises
    IOError exception instead"""
    raw_data = setup_raw_data_template()
    try:
        raw_data.write(overwrite_check=True)
        print(" >> Created {}".format(raw_data.filename))
    except IOError as error:
        print(error)
