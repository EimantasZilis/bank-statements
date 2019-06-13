import argparse
from system.file_management import Jdict

def init_parser():
    """ Initialise and definte user input commands
    available in command prompt for the app """
    parser = argparse.ArgumentParser(description='Finances app')
    subparsers = parser.add_subparsers(dest="parser")

    # Parser for initialising the app
    parser_init = subparsers.add_parser("initialise", help="Initialise the app")
    parser_init.add_argument("-s", "--setup", nargs="+", dest="setup",
                             help="Set up user files in specified directory")

    # Parser for defining categories
    parser_types = subparsers.add_parser("categories", help="Amend categories")
    parser_types.add_argument("-s", action="store_true", default=False,
                              dest="show", help="Show current categories")
    parser_types.add_argument("-a", type=str, dest="add",
                              help="Add new (comma-delimited) categories. \
                              Must have quotes around the list")
    parser_types.add_argument("-d", type=str, dest="delete",
                              help="Delete (comma-delimited) categories. \
                              Must have quotes around the list.")

    # Parser for data operations
    parser_data = subparsers.add_parser("data", help="Process data")
    parser_data.add_argument("-i", action="store_true", default=False,
                             help='Import raw data', dest="migrate")
    parser_data.add_argument("-c", action="store_true", default=False,
                             help="Classify data", dest="classify")

    # Parser for plotting
    parser_plot = subparsers.add_parser("plot", help="Generate plots")
    parser_plot.add_argument("-a", action="store_true", default=False,
                             dest="all", help='All')

    parser_info = subparsers.add_parser("info", help="Summary about the app")
    parser_info.add_argument("-a", action="store_true", default=False,
                             dest="all", help="All info")
    parser_info.add_argument("-c", action="store_true", default=False,
                             dest="categories", help="Categories info")
    parser_info.add_argument("-p", action="store_true", default=False,
                             dest="path", help="Common path info")

    return parser.parse_args()

def process_commands(commands=None):
    """ Process input command and execute a given option """
    try:
        pre_process_validation(commands)
    except ValueError as err:
        print(err)
        return

    if commands.parser == "info":
        # Process commands for showing info
        import user_input.commands.info as info_cmd
        info_cmd.process(commands)

    if commands.parser == "initialise":
        # Process commands for initialising the app
        import user_input.commands.initialise as init_cmd
        init_cmd.process(commands)

    if commands.parser == "categories":
        # Process commands related to categories
        import user_input.commands.categories as cat_cmd
        cat_cmd.process(commands)

    if commands.parser == "data":
        # Process commands related to data processing
        import user_input.commands.data as data_cmd
        data_cmd.process(commands)

    if commands.parser == "plot":
        # Process commands responsible for generating plots
        import user_input.commands.plots as plots_cmd
        plots_cmd.process(commands)

def pre_process_validation(commands):
    """ Carry out any validation commands before
    any commands get processed. """
    if commands is None or commands.parser == "":
        raise ValueError("No input command specified")
    validate_common_path(commands)

def validate_common_path(commands):
    """ Validate if common path exists and if commands
    can be run even if it doesn't """
    if common_path_exists():
        return

    ok_commands = {"initialise" : "setup"}
    ok_command = ok_commands.get(commands.parser)
    if ok_command is None:
        err = "Common path is not defined\n" \
               " >> Set it up before running other commands"
        raise ValueError(err)

def common_path_exists():
    """ Check if common path exists. Returns True/False"""
    cpath = Jdict("u_paths")
    return cpath.is_blank()
