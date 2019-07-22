import argparse
from system.file_management import Jdict

def init_parser():
    """ Initialise and definte user input commands
    available in command prompt for the app """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="parser")
    setup_parser(subparsers)
    types_parser(subparsers)
    info_parser(subparsers)
    data_parser(subparsers)
    plotting_parser(subparsers)
    return parser.parse_args()

def setup_parser(subparsers=None):
    """ 'setup' subparser definition """
    if subparsers is None:
        return

    parser_init = subparsers.add_parser("setup", help="Setup the app")
    parser_init.add_argument("-p", nargs="+", dest="path",
                             help="Set up common path")

def types_parser(subparsers=None):
    """ 'types' subparser definition """
    if subparsers is None:
        return

    parser_types = subparsers.add_parser("categories", help="Amend categories")
    parser_types.add_argument("-s", action="store_true", default=False,
                              dest="show", help="Show current categories")
    parser_types.add_argument("-a", type=str, dest="add",
                              help="Add new (comma-delimited) categories")
    parser_types.add_argument("-d", type=str, dest="delete",
                              help="Delete (comma-delimited) categories")
    parser_types.add_argument("--bad", action="store_true", default=False,
                              help="Amend blacklisted categories")

def data_parser(subparsers=None):
    """ 'data' subparser definition """
    if subparsers is None:
        return

    parser_data = subparsers.add_parser("data", help="Process data")
    parser_data.add_argument("-i", action="store_true", default=False,
                             help='Import raw data', dest="migrate")
    parser_data.add_argument("-c", action="store_true", default=False,
                             help="Classify data", dest="classify")

def plotting_parser(subparsers=None):
    """ 'plot' subparser definition """
    if subparsers is None:
        return

    parser_plot = subparsers.add_parser("plot", help="Generate plots")
    parser_plot.add_argument("-a", action="store_true", default=False,
                             dest="all", help='All')

def info_parser(subparsers=None):
    """ 'info' subparser definition """
    if subparsers is None:
        return

    parser_info = subparsers.add_parser("info", help="Summary about the app")
    parser_info.add_argument("-a", action="store_true", default=False,
                             dest="all", help="All info")
    parser_info.add_argument("-c", action="store_true", default=False,
                             dest="categories", help="Categories info")
    parser_info.add_argument("-p", action="store_true", default=False,
                             dest="path", help="Common path info")
    parser_info.add_argument("-t", action="store_true", default=False,
                             dest="transactions", help="Transactions info")

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

    if commands.parser == "setup":
        # Process commands for initialising the app
        import user_input.commands.setup as setup_cmd
        setup_cmd.process(commands)

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
    return cpath.lookup("COMMON") is not None
