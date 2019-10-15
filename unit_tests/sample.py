import os
import pathlib

class User:
    HOME_PATH = str(pathlib.Path.home())
    CATEGORIES = ["Services", "Groceries", "Transport"]


class Path:
    @staticmethod
    def user_home():
        return User.HOME_PATH

    @staticmethod
    def subfolders():
        return ["", "sub1", os.path.join("sub1", "sub2")]

    @staticmethod
    def creatable_paths():
        return {
            User.home_path(): True,
            os.path.join(User.home_path(), "subfolder"): True,
            os.path.join("em", "x"): False, 
            None: False, 
            1: False,
            0: False, 
            "": False
        }


class File(Path):
    TYPE_MAPPINGS = {"": "", "D": "Data", "P": "Plot", "X": ""}
    FILENAMES = ["text.txt", "config.json", "excel.xlsx"]
    SYSTEM_FILES = [True, False]

    @classmethod
    def filenames(cls):
        return cls.FILENAMES
    
    @classmethod
    def type_codes(cls):
        return [code for code in cls.type_mappings().keys()]

    @classmethod
    def type_names(cls):
        return [name for name in cls.type_mappings().values()]

    @classmethod
    def system_files(cls):
        return cls.SYSTEM_FILES