import os
import pathlib

class SampleUser:
    CATEGORIES = ["Services", "Groceries", "Transport"]


class SamplePath:
    HOME = str(pathlib.Path.home())
    INVALID = [os.path.join("em", "x"), None, 1, 0, ""]

    @staticmethod
    def user_home():
        return [SamplePath.HOME]

    @staticmethod
    def subfolders():
        return SamplePath.SUBFOLDERS

    @staticmethod
    def invalid_paths():
        return SamplePath.INVALID_PATHS

    @staticmethod
    def get_all():
        return SamplePath.INVALID + [SamplePath.HOME]

    @staticmethod
    def creatable():
        invalid = [(p, False) for p in SamplePath.INVALID]
        creatable = os.path.join(SamplePath.HOME, "subfolder")
        return invalid + [(SamplePath.HOME, True), (creatable, True)]


class SampleFile(SamplePath):
    SUBFOLDERS = ["", "sub1", os.path.join("sub1", "sub2")]
    FILENAMES = ["", "text.txt", "config.json", "excel.xlsx"]
    TYPE_MAPPINGS = {"": "", "D": "Data", "P": "Plot", "X": ""}
    
    @classmethod
    def type_codes(cls):
        return [code for code in cls.type_mappings().keys()]

    @classmethod
    def type_names(cls):
        return [name for name in cls.type_mappings().values()]

    @classmethod
    def type_dict(cls):
        return cls.TYPE_MAPPINGS.items()