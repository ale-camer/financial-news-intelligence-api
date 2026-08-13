from unittest.mock import MagicMock, patch

import pytest

from src.storage.db import get_session, init_db


@patch("src.storage.db.Base.metadata.create_all")
def test_init_db(mock_create_all: MagicMock) -> None:
    # Act
    init_db()

    # Assert
    mock_create_all.assert_called_once()


@patch("src.storage.db.SessionLocal")
def test_get_session(mock_session_local: MagicMock) -> None:
    # Arrange
    mock_session = MagicMock()
    mock_session_local.return_value = mock_session

    # Act
    generator = get_session()
    session = next(generator)

    # Assert yield returns the mocked session
    assert session is mock_session

    # Assert session is closed when generator is exhausted
    with pytest.raises(StopIteration):
        next(generator)

    mock_session.close.assert_called_once()
