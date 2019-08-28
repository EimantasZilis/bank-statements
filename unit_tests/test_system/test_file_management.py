import os
import pathlib
import pytest
import shutil
import tempfile

from system.file_management import Path


USERPATH = str(pathlib.Path.home())

@pytest.fixture
def temp_new_dir():
    dirpath = tempfile.mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath)

class TestPath:
    creatable = [False, False, False, False, False, True, True]
    paths = ["em:\\x", None, 1, 0, "", USERPATH, os.path.splitdrive(USERPATH)[0]]

    @pytest.fixture
    def object(self, path):
        """ Create Path object with a given path"""
        return Path(path)

    @pytest.mark.parametrize("path", paths)
    def test_var_path(self, object, path):
        assert object.path == path

    @pytest.mark.parametrize("path,tcreatable", list(zip(paths, creatable)))
    def test_fx_exists_or_is_creatable(self, object, tcreatable):
        assert object.exists_or_is_creatable() == tcreatable

    def path_fx_init_dirs(self, dir, prev_expected, now_expected):
        prev_exists = os.path.exists(dir)
        path_object = Path(dir)
        path_object.init_dirs()
        now_exists = os.path.exists(dir)
        assert prev_exists == prev_expected and now_exists == now_expected

    def test_fx_init_dirs_1_existing(self, temp_new_dir):
        self.path_fx_init_dirs(temp_new_dir, True, True)

    def test_fx_init_dirs_2_new(self, temp_new_dir):
        newpath = os.path.join(temp_new_dir, "subfolder")
        self.path_fx_init_dirs(newpath, False, True)
