import os
import pathlib
import pytest
import datetime

from unittest.mock import Mock, patch

from system.file_management import Path, File, Jdict
from unit_tests.sample import SampleFile, SamplePath


class TestPath:

    @staticmethod
    @pytest.mark.parametrize("path", SamplePath.get_all())
    def test_var_path(mock_path, path):
        assert Path(path).path == path

    @staticmethod
    @pytest.mark.parametrize("path,creatable", SamplePath.creatable())
    def test_fx_exists_or_is_creatable(mock_path, path, creatable):
        assert Path(path).exists_or_is_creatable() == creatable

    @staticmethod
    def test_fx_init_dirs(tmpdir):
        def path_fx_init_dirs(dir, prev_expected, now_expected):
            prev_exists = os.path.exists(dir)
            path_object = Path(dir)
            path_object.init_dirs()
            now_exists = os.path.exists(dir)
            assert prev_exists == prev_expected and now_exists == now_expected

        # Test existing paths
        path_fx_init_dirs(tmpdir, True, True)
        # Test new paths

        newpath = os.path.join(tmpdir, "subfolder")
        path_fx_init_dirs(newpath, False, True)


class TestFile:

    @staticmethod
    @pytest.mark.parametrize("system_file", [True, False])
    def test_var_system_file(mock_file, system_file):
        assert File(system_file=system_file).system_file == system_file

    @staticmethod
    @pytest.mark.parametrize("system_file", [True, False])
    def test_fx_base_path(mock_file, system_file):
        file_object = File(system_file=system_file)
        assert file_object.base_path() == mock_file.base_path(system_file)

    @staticmethod
    @pytest.mark.parametrize("with_file", [True, False])
    @pytest.mark.parametrize("system_file", [True, False])
    @pytest.mark.parametrize("filename", SampleFile.FILENAMES)
    @pytest.mark.parametrize("subfolder", SampleFile.SUBFOLDERS)
    @pytest.mark.parametrize("type_id,type_name", SampleFile.type_dict())
    def test_fx_file_pointer(mock_file, with_file, system_file,
                             filename, type_id, type_name, subfolder):
        base_path = mock_file.base_path(system_file)
        filepath = os.path.join(subfolder, filename)
        file_object = File(filepath, type_id, system_file)
        expected = os.path.join(base_path, type_name, subfolder)
        expected = os.path.join(expected, filename) if with_file else expected
        assert file_object.file_pointer(with_file=with_file) == expected

    @staticmethod
    @pytest.mark.parametrize("filename", SampleFile.FILENAMES)
    @pytest.mark.parametrize("subdir", SampleFile.SUBFOLDERS)
    @pytest.mark.parametrize("type_code,type_name", SampleFile.type_dict())
    def test_fx_parse_inputs(mock_file, filename, subdir, type_code, type_name):
        filepath = os.path.join(subdir, filename)
        file_object = File(filepath, type_code)
        file_check_ok = file_object.filename == filename
        subfolder_check_ok = file_object.subfolders == subdir
        type_check_ok = file_object.type == type_name
        assert all([file_check_ok, subfolder_check_ok, type_check_ok])

    @staticmethod
    @pytest.mark.parametrize("type_code,type_name", SampleFile.type_dict())
    def test_fx_get_type_name(mock_file, type_name, type_code):
        file_object = File(type=type_code)
        assert file_object.get_type_name() == type_name

    @staticmethod
    @patch("system.file_management.Path")
    @pytest.mark.parametrize("filename", SampleFile.FILENAMES + [None])
    @pytest.mark.parametrize("type_code,type_name", SampleFile.type_dict())
    def test_fx_init_file(path_mock, monkeypatch, mock_file,
                          filename, type_code, type_name):

        parse_inputs_mock = Mock()
        parse_inputs = "system.file_management.File.parse_inputs"
        monkeypatch.setattr(parse_inputs, parse_inputs_mock)

        fp = os.path.join(mock_file.common(), type_name)
        file_pointer_mock = Mock(return_value=fp)
        file_pointer = "system.file_management.File.file_pointer"
        monkeypatch.setattr(file_pointer, file_pointer_mock)

        file_object = File(filename, type_code)
        path_object = path_mock.return_value

        if filename is None:
            parse_inputs_mock.assert_not_called()
            file_pointer_mock.assert_not_called()
            path_mock.assert_not_called()
            path_object.init_dirs.assert_not_called()
        else:
            parse_inputs_mock.assert_called_once_with(filename, type_code)
            file_pointer_mock.assert_called_once_with(with_file=False)
            path_mock.assert_called_once_with(fp)
            path_object.init_dirs.assert_called_once()
