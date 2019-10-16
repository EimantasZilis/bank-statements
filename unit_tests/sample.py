import os
import pathlib

class User:
    CATEGORIES = ["Services", "Groceries", "Transport"]


class Path:
    @staticmethod
    def user_home():
        return User.HOME_PATH

    @staticmethod
    def subfolders():
        return ["", "sub1", os.path.join("sub1", "sub2")]

    @staticmethod
    def invalid_paths():
        return [os.path.join("em", "x"), None, 1, 0, ""]


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