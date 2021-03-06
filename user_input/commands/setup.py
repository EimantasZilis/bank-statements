import pandas as pd
from system.file_management import Excel
from system.file_management import Jdict
from system.file_management import Path

def process(commands=None):
    """ Run commands for 'setup' subparser """
    if commands.path:
        print("Setting up common path...")
        setup_path(commands.path[0])
        setup_files_and_dirs()

def setup_path(common_path):
    """ Validate and set up common path """
    validate_path(common_path)
    upaths = get_upaths()
    show_path_changes(common_path, upaths)
    write_path(common_path, upaths)

def get_upaths():
    return Jdict("u_paths")

def validate_path(path):
    user_path = Path(path)
    if not user_path.exists_or_is_creatable():
        err = "{} is not a valid path\n >> Enter a different path"
        raise ValueError(err.format(path))

def show_path_changes(new_path, upaths):
    prev_path = upaths.lookup("COMMON")
    if prev_path == new_path:
        print(" >> No path changes")
    else:
        if prev_path:
            print(" >> Old path: {}".format(prev_path))
        print(" >> New path: {}".format(new_path))

def write_path(path, upaths):
    """ Set common path in config.json """
    upaths.update("COMMON", path)
    upaths.write()

def setup_files_and_dirs():
    """ Initialise user files and directories in common_path """
    setup_raw_data()

def setup_raw_data_template():
    """ Initialise raw data.xlsx file template """
    cols = ["Date", "Description", "Extra", "Amount"]
    blank_df = pd.DataFrame([[""]*len(cols)], columns=cols)
    return Excel(filename="raw", type="D", df=blank_df)

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
