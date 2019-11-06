import pytest

from unit_tests.mocks import (
    MockFile,
    MockPath,
    MockUser
)

@pytest.fixture
def mock_user(monkeypatch, tmpdir):
    monkeypatch.chdir(tmpdir)
    yield MockUser(tmpdir)

@pytest.fixture
def mock_path(monkeypatch, tmpdir):
    monkeypatch.chdir(tmpdir)
    yield MockPath(tmpdir)

@pytest.fixture
def mock_file(monkeypatch, tmpdir):
    monkeypatch.chdir(tmpdir)
    yield MockFile(tmpdir)