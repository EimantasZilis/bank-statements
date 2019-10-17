import pytest

from unittest.mock import patch, Mock

from unit_tests.mocks import MockPath, MockUser


@pytest.fixture
def mock_user(monkeypatch, tmpdir):
    monkeypatch.chdir(tmpdir)
    yield MockUser(tmpdir)

@pytest.fixture
def mock_path(monkeypatch, tmpdir):
    monkeypatch.chdir(tmpdir)
    yield MockPath(tmpdir)