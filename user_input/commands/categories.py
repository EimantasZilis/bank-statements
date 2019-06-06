import sys
from system.file_management import Jdict
from user_input.commands.info import show_categories_summary
from user_input.commands.info import get_categories_summary
from user_input.commands.data import migrate as reprocess_raw_data

def process(command=None):
    """ Run commands for 'categories' subparser """
    if command.delete:
        Delete(command.delete)
    if command.add:
        Create(command.add)
    if command.show:
        show_categories_summary()

class AmendCategories():
    """ Base class for amending categories"""
    def __init__(self, params=None):
        self.existing_categories = None
        self.action_categories = None
        self.params = params
        self.config = None
        self.initialise()

    def initialise(self):
        """ Initialise instance parameters"""
        try:
            self.initialise_existing_categories()
            self.parse_params()
        except ValueError as error:
            print(error)
            sys.exit()

    def initialise_existing_categories(self):
        self.config = Jdict("u_categories")
        self.existing_categories = self.config.lookup("CATEGORIES")

    def parse_params(self):
        """ Validate params and parse it into action_categories.
        It does it by separating comma-delimited categories into a
        list and remove any blank strings. """
        categories = self.params.split(",")
        self.action_categories = list(filter(None, categories))
        if not self.action_categories:
            raise ValueError(" >> Invalid categories entered")

    def show_actionable_categories(self):
        for category in self.action_categories:
            print(" >>", category)

class Create(AmendCategories):
    """ Class for creating new categories """
    def __init__(self, params):
        super().__init__(params=params)
        self.do_it()

    def do_it(self):
        """ Create new categories """
        print("Adding new categories...")
        try:
            self.validate_new_categories()
            self.show_actionable_categories()
            self.update_categories_config()
            reprocess_raw_data("\nRe-processing raw statements...")
        except ValueError as error:
            print(error)

    def validate_new_categories(self):
        """ Validate new categories. It checks if there
        are no duplicates """
        if self.action_categories is not None:
            upper = [x.upper() for x in self.existing_categories]
            duplicates = [n for n in self.action_categories if n.upper() in upper]
            if duplicates:
                dups = ", ".join(duplicates)
                error = " >> Cannot create duplicate categories: {}".format(dups)
                raise ValueError(error)

    def update_categories_config(self):
        """ Create new categories and add to config.json"""
        self.config.extend("CATEGORIES", self.action_categories)
        self.config.write()

class Delete(AmendCategories):
    """ Class for deleting existing categories """
    def __init__(self, params):
        super().__init__(params=params)
        self.do_it()

    def do_it(self):
        """ Delete categories """
        print("Deleting categories...")
        try:
            self.validate_categories_to_delete()
            self.show_actionable_categories()
            self.delete_references_to_mappings()
            self.delete_categories_from_config()
            reprocess_raw_data("\nRe-processing raw statements...")
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
        self.config.update("CATEGORIES", updated)
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
