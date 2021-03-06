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
        if filename is None:
            # These values are not set if filename is None
            filepath = None
            subfolder = ""
            type_name = ""
            type_id = ""
        else:
            filepath = os.path.join(subfolder, filename)

        file_object = File(filepath, type_id, system_file)

        if with_file and (filename is None or not filename):
            with pytest.raises(ValueError):
                file_object.file_pointer(with_file=with_file)
        else:
            base_path = mock_file.base_path(system_file)
            expected = os.path.join(base_path, type_name, subfolder)
            expected = os.path.join(expected, filename) if with_file else expected
            assert file_object.file_pointer(with_file=with_file) == expected

    @staticmethod
    @pytest.mark.parametrize("filename", SampleFile.FILENAMES)
    @pytest.mark.parametrize("subdir", SampleFile.SUBFOLDERS)
    @pytest.mark.parametrize("type_code,type_name", SampleFile.type_dict())
    def test_fx_parse_inputs(mock_file, filename, subdir, type_code, type_name):
        filepath = None if filename is None else os.path.join(subdir, filename)
        if filename is None:
            # These values are not set if filename is None
            type_name = ""
            type_code = ""
            subdir = ""

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

    @staticmethod
    @pytest.mark.parametrize("filename", SampleFile.FILENAMES)
    @pytest.mark.parametrize("type_code", SampleFile.type_codes())
    @pytest.mark.parametrize("system_file", [True, False])
    def test_class_init(monkeypatch, mock_file, filename, type_code, system_file):
        init_file_mock = Mock()
        init_file = "system.file_management.File.init_file"
        monkeypatch.setattr(init_file, init_file_mock)

        file_object = File(filename, type_code, system_file)
        init_file_mock.assert_called_once_with()

        assert file_object.expected_extension == None
        assert file_object.system_file == system_file
        assert file_object.filename == filename
        assert file_object.subfolders == ''
        assert file_object.type == type_code

    @staticmethod
    @patch("os.remove")
    @pytest.mark.parametrize("exception", [None, FileNotFoundError])
    def test_fx_delete_file(os_remove, monkeypatch, mock_file, exception):
        fp = "mock path"
        file_pointer_mock = Mock(return_value=fp)
        file_pointer = "system.file_management.File.file_pointer"
        monkeypatch.setattr(file_pointer, file_pointer_mock)

        os_remove.side_effect = exception
        file_object = File().delete_file()
        os_remove.assert_called_once_with(fp)

    @staticmethod
    @pytest.mark.parametrize("filename", [None, "hello.txt"])
    @pytest.mark.parametrize("subfolders", SampleFile.SUBFOLDERS)
    @pytest.mark.parametrize("type_code, type_name", SampleFile.type_dict())
    def test_fx_rename(mock_file, filename, subfolders, type_code, type_name):
        orig_subfolders = "subdir"
        orig_filename = "orig.txt"
        orig_type_name = ""
        orig_type = ""

        if filename is None:
            filename = orig_filename
            subfolders = orig_subfolders

        if not type_code:
            type_name = orig_type_name

        file_object = File(orig_filename, orig_type)
        fp = os.path.join(subfolders, filename)
        file_object.rename(fp, type_code)

        assert file_object.type == type_name
        assert file_object.filename == filename
        assert file_object.subfolders == subfolders

    @staticmethod
    @pytest.mark.parametrize("exists", [True, False])
    @pytest.mark.parametrize("file_pointer", [None, "mock path"])
    def test_fx_file_exists(monkeypatch, exists, file_pointer):
        if file_pointer is None:
            with pytest.raises(TypeError):
                File.file_exists(file_pointer)
        else:
            mock_isfile = Mock(return_value=exists)
            monkeypatch.setattr("system.file_management.os.path.isfile", mock_isfile)
            assert exists == File.file_exists(file_pointer)
            mock_isfile.assert_called_once_with(file_pointer)

    @staticmethod
    @pytest.mark.parametrize("exists", [True, False])
    @pytest.mark.parametrize("file_pointer", [None, "subdir/file.txt"])
    def test_fx_overwrite_check(monkeypatch, exists, file_pointer):
        if file_pointer is None:
            with pytest.raises(TypeError):
                File.overwrite_check(file_pointer)
                return

        path_str = "system.file_management"
        mock_file_exists = Mock(return_value=exists)
        monkeypatch.setattr(f"{path_str}.File.file_exists", mock_file_exists)

        if exists:
            with pytest.raises(IOError):
                File.overwrite_check("mock")
        else:
            File.overwrite_check("mock")

    @staticmethod
    @pytest.mark.parametrize("file", SampleFile.FILENAMES)
    @pytest.mark.parametrize("extension", SampleFile.EXTENSIONS)
    def test_fx_validate_file_extension(monkeypatch, file, extension):
        def run_test(filename, extension):
            file_extension = None if file is None else os.path.splitext(filename)[1]
            file_object = File(filename)
            file_object.expected_extension = extension

            do_nothing = (filename is None) or (extension is None)
            same_extension = extension == file_extension
            add_extension = file_extension is ''
            raise_error = (file_extension != extension)
            print(f'\nfilename: {filename}\n >> file_extension: {file_extension}')
            print(f' >> expected extension: {extension}')
            if do_nothing or same_extension:
                print(f' >> do nothing or same')
                file_object.validate_file_extension()
                assert file_object.filename == filename

            elif add_extension:
                print(f' >> add')
                file_object.validate_file_extension()
                assert file_object.filename == f"{filename}{extension}"

            elif raise_error:
                print(f' >> error')
                with pytest.raises(ValueError):
                    file_object.validate_file_extension()
            else:
                raise ValueError(
                        f"Unaccounted case in unit test. This test needs a fix \
                        \n >> filename: {filename}\n >> extension: {extension}"
                )

        # Test 1: use filename with extension
        run_test(file, extension)

        # # Test 2: use filename without extension
        filename = None if file is None else os.path.splitext(file)[0]
        run_test(filename, extension)

