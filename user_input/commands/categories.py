import sys
from system.file_management import Jdict
from user_input.commands.info import show_categories_summary
from user_input.commands.info import get_categories_summary
from user_input.commands.data import migrate as reprocess_raw_data

def process(command=None):
    """ Run commands for 'categories' subparser """

    if command.delete:
        Delete(command.delete, command.bad)
    if command.add:
        Create(command.add, command.bad)
    if command.show:
        show_categories_summary()

class AmendCategories:
    """ Base class for amending categories"""
    def __init__(self, params=None, blacklist=False):
        self.existing_categories = None
        self.action_categories = None
        self.blacklist = blacklist
        self.reprocess_data = True
        self.params = params
        self.config = None
        self.initialise()

    def initialise(self):
        """ Initialise instance parameters"""
        try:
            self.initialise_existing_categories()
            self.check_existing_categories()
            self.parse_params()
        except ValueError as error:
            print(error)
            sys.exit()

    def initialise_existing_categories(self):
        self.config = Jdict("u_categories")
        ltype = self.lookup_type()
        self.existing_categories = self.config.lookup(ltype)

    def parse_params(self):
        """ Validate params and parse it into action_categories.
        It does it by separating comma-delimited categories into a
        list and remove any blank strings. """

        categories = self.params.split(",")
        self.action_categories = list(filter(None, categories))
        if not self.action_categories:
            raise ValueError(" >> Invalid categories entered")

    def check_existing_categories(self):
        """ Check if there are any existing categories. If there
        aren't any, set reprocess_data data flag to False to
        avoid raw data being imported"""
        if not self.existing_categories:
            self.reprocess_data = False

    def show_info(self, action):
        if self.blacklist:
            print("{} blacklisted categories...".format(action))
        else:
            print("{} categories...".format(action))
        for category in self.action_categories:
            print(" >>", category)

    def lookup_type(self):
        """ Get lookup type for u_categories.json depending
        if it is looking at blacklisted categories """
        if self.blacklist:
            return "BLACKLIST"
        else:
            return "CATEGORIES"

    def recalculate_data(self):
        """ Reprocess statements data if
        reprocess flag is set."""
        if self.reprocess_data:
            reprocess_raw_data("\nRe-processing raw data...")

class Create(AmendCategories):
    """ Class for creating new categories """
    def __init__(self, params, blacklist):
        super().__init__(params=params, blacklist=blacklist)
        self.do_it()

    def do_it(self):
        """ Create new categories """
        try:
            self.validate_new_categories()
            super().show_info("Adding")
            self.update_categories_config()
            super().recalculate_data()
        except ValueError as error:
            print(error)

    def validate_new_categories(self):
        """ Validate new categories. It checks if there
        are no duplicates """
        if self.existing_categories is None:
            return

        if self.action_categories is not None:
            upper = [x.upper() for x in self.existing_categories]
            duplicates = [n for n in self.action_categories if n.upper() in upper]
            if duplicates:
                dups = ", ".join(duplicates)
                error = " >> Cannot create duplicate categories: {}".format(dups)
                raise ValueError(error)

    def update_categories_config(self):
        """ Create new categories and add to config.json"""
        ltype = super().lookup_type()
        self.config.extend(ltype, self.action_categories)
        self.config.write()

class Delete(AmendCategories):
    """ Class for deleting existing categories """
    def __init__(self, params, blacklist):
        super().__init__(params=params, blacklist=blacklist)
        self.do_it()

    def do_it(self):
        """ Delete categories """
        try:
            self.validate_categories_to_delete()
            super().show_info("Deleting")
            self.delete_references_to_mappings()
            self.delete_categories_from_config()
            super().recalculate_data()
        except ValueError as error:
            print(error)

    def validate_categories_to_delete(self):
        """ Validate categories about to be deleted """
        action_upper = {a.upper():a for a in self.action_categories}
        existing_upper = {e.upper():e for e in self.existing_categories}
        bad_categories = [v for k, v in action_upper.items()
                          if k not in existing_upper.keys()]
        if bad_categories:
             err = " >> Cannot delete non-existent categories: {}"
             error = err.format(", ".join(bad_categories))
             raise ValueError(error)
        else:
            self.action_categories = [v for k, v in existing_upper.items()
                                      if k in action_upper.keys()]

    def delete_categories_from_config(self):
        """ Delete categories from config.json """
        updated = [cat for cat in self.existing_categories
                   if cat not in self.action_categories]
        ltype = super().lookup_type()
        self.config.update(ltype, updated)
        self.config.write()

    def delete_references_to_mappings(self):
        """ Delete any references to mappings
        from u_cmappings.json """
        cmappings = Jdict("u_cmappings")
        cmappings.transpose()
        for category in self.action_categories:
            cmappings.pop(category)
        cmappings.transpose()
        cmappings.write()
