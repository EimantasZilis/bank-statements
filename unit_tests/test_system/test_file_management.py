import os
import pathlib
import pytest
import shutil
import tempfile
import datetime

from system.file_management import Path, File, Jdict


USERPATH = str(pathlib.Path.home())

@pytest.fixture
def temp_new_dir():
    """ Setup a new temporary directory during setup.
    Remove temporary directory during teardown. """
    dirpath = tempfile.mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath)

@pytest.fixture(scope='function')
def upath(temp_new_dir):
    """ Setup a new temporary directory and set it as the
    user path. Re-instate the previous user path
    during teardown. """
    config = Jdict("u_paths")
    common_path = config.lookup("COMMON")
    config.update("COMMON", temp_new_dir)
    config.write()
    yield temp_new_dir
    config.update("COMMON", common_path)
    config.write()

class TestPath:
    creatable = [False, False, False, False, False, True, True]
    paths = ["em:\\x", None, 1, 0, "", USERPATH]

    @pytest.fixture
    def object(self, path):
        """ Create Path object with a given path"""
        return Path(path)

    @pytest.mark.parametrize("path", paths)
    def test_var_path(self, upath, object, path):
        assert object.path == path

    @pytest.mark.parametrize("path,tcreatable", list(zip(paths, creatable)))
    def test_fx_exists_or_is_creatable(self, upath, object, tcreatable):
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


class TestFile:
    type_mappings = [("", ""), ("D", "Data"), ("P", "Plot"), ("X", "")]
    types = ["", "D", "P", "X"]
    fnames = ["sysfile.txt", "datafile.txt", "plotfile.txt", "xfile.txt"]
    sfiles = [True, False, False, True]

    @pytest.fixture
    def bpath(self, upath, sysfile):
        system_path = os.path.join(os.getcwd(), "system", "configuration")
        mapping = {True: system_path, False: upath}
        return mapping[sysfile]

    def test_var_expected_extension(self):
        file_object = File()
        assert file_object.expected_extension == None

    @pytest.mark.parametrize("sfile", sfiles)
    def test_var_system_file(self, sfile):
        file_object = File(system_file=sfile)
        assert file_object.system_file == sfile

    @pytest.mark.parametrize("sysfile", sfiles)
    def test_fx_base_path(self, upath, sysfile, bpath):
        file_object = File(system_file=sysfile)
        assert file_object.base_path() == bpath

    @pytest.mark.parametrize("sysfile", [True, False])
    @pytest.mark.parametrize("subdirs", ["", "sub1", "sub1\\sub2"])
    @pytest.mark.parametrize("tid,ftype", type_mappings)
    def test_fx_file_pointer_with_file(self, bpath, sysfile, ftype, tid, subdirs):
        filename = "somefile.txt"
        filepath = os.path.join(subdirs, filename)
        file_object = File(filepath, tid, sysfile)
        expected = os.path.join(bpath, ftype, subdirs, filename)
        assert file_object.file_pointer() == expected

    @pytest.mark.parametrize("sysfile", [True, False])
    @pytest.mark.parametrize("subdirs", ["", "sub1", "sub1\\sub2"])
    @pytest.mark.parametrize("tid,ftype", type_mappings)
    def test_fx_file_pointer_without_file(self, bpath, sysfile, ftype, tid, subdirs):
        filename = "somefile.txt"
        filepath = os.path.join(subdirs, filename)
        file_object = File(filepath, tid, sysfile)
        expected = os.path.join(bpath, ftype, subdirs)
        assert file_object.file_pointer(False) == expected

    @pytest.mark.parametrize("filename", ["", "somefile.txt"])
    @pytest.mark.parametrize("subdirs", ["", "sub1", "sub1\\sub2"])
    @pytest.mark.parametrize("tid,ftype", type_mappings)
    def test_fx_parse_inputs(self, upath, filename, subdirs, ftype, tid):
        filepath = os.path.join(subdirs, filename)
        file_object = File(filepath, tid)
        file_check = file_object.filename == filename
        subfolders_check = file_object.subfolders == subdirs
        type_check = file_object.type == ftype
        assert file_check and subfolders_check and type_check

    @pytest.mark.parametrize("type_id,filetype", type_mappings)
    def test_fx_get_type_name(self, upath, filetype, type_id):
        file_object = File(type=type_id)
        assert file_object.get_type_name() == filetype
