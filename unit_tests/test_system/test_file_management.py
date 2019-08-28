import os
from pathlib import Path as userpath
import pytest
from system.file_management import Path

class TestPath:
    creatable = [False, False, False, False, False, True, True]
    paths = ["what:\\x", None, 1, 0, "", str(userpath.home()),
            os.path.splitdrive((userpath.home()))[0]]

    @pytest.mark.parametrize("temp_path", paths)
    def test_var_path_1(self, temp_path):
        p_object = Path(temp_path)
        assert p_object.path == temp_path

    def path_exists_or_is_creatable(self, temp_path, temp_creatable):
        p_object = Path(temp_path)
        assert p_object.exists_or_is_creatable() == temp_creatable

    @pytest.mark.parametrize("tpath,tcreatable", zip(paths, creatable))
    def test_path_exists_or_is_creatable_1(self, tpath, tcreatable):
        self.path_exists_or_is_creatable(tpath, tcreatable)

    def test_path_exists_or_is_creatable_2(self, tmpdir):
        self.path_exists_or_is_creatable(str(tmpdir), True)
