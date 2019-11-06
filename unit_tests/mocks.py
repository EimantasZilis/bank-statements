import json
import os
import pathlib

from unittest.mock import Mock, patch


class MockUser:
    def __init__(self, tmpdir):
        self._tmpdir = tmpdir
        self._common_path = None
        self._init_user()
    
    def _init_user(self):
        def setup_paths(cwd):
            """ Setup user's paths in a temporary directory.
            Creates relevant directories and writes COMMON
            path to u_paths.json"""

            fp = os.path.join(cwd, "system", "configuration", "u_paths.json")
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            self._common_path = os.path.join(cwd, "user_data")
            os.makedirs(self._common_path)

            with open(fp, "w+") as file:
                u_paths = {"COMMON": self._common_path}
                json.dump(u_paths, file, indent=4, sort_keys=True)
        
        setup_paths(self._tmpdir)


class MockPath(MockUser):

    def __init__(self, tmpdir):
        super().__init__(tmpdir)

    def common(self):
        return self._common_path

    def base_path(self, system_file):
        system_path = os.path.join(os.getcwd(), "system", "configuration")
        mapping = {True: system_path, False: self.common()}
        return mapping[system_file]

class MockFile(MockPath):

    def __init__(self, tmpdir):
        super().__init__(tmpdir)