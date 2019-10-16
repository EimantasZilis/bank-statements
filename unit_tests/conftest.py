import pytest

from unittest.mock import patch, Mock

from unit_tests.mocks import MockUser


@pytest.fixture
def mock_user(monkeypatch, tmpdir):
    monkeypatch.chdir(tmpdir)
    yield MockUser(tmpdir)