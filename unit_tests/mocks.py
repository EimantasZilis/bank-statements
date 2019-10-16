import json
import os
import pathlib

from unittest.mock import Mock, patch

from system.file_management import Jdict, os
from unit_tests.sample import User


class MockUser:
    def __init__(self, tmpdir):
        self.common_path = tmpdir
        self._init_user()
    
    def _init_user(self):
        def setup_u_paths(cwd):
            """ Setup user's COMMON path by creating
            u_paths.json in a temporary directory"""
            fp = os.path.join(cwd, "system", "configuration", "u_paths.json")
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            with open(fp, "w+") as file:
                u_paths = {"COMMON": str(cwd)}
                json.dump(u_paths, file, indent=4, sort_keys=True)
        
        setup_u_paths(self.common_path)


class MockPath(MockUser):
    def __init__(self, tmpdir):
        super().__init__(tmpdir)

    @staticmethod
    def user_home():
        return str(pathlib.Path.home())