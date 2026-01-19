from datetime import datetime

from fastapi import HTTPException
import pytest

from user.domain.user import User
from user.infra.db_models.user import User as UserModel
from user.infra.repository.user_repo import UserRepository
from utils.db_utils import row_to_dict


@pytest.fixture
def mock_session_local(mocker):
    return mocker.patch(
        "user.infra.repository.user_repo.SessionLocal", autospec=True
    )


def test_find_by_email_user_exists(mock_session_local, mocker):
    now = datetime.now()
    mock_user = UserModel(
        id=1,
        email="test@example.com",
        name="Test User",
        password="secret",
        created_at=now,
        updated_at=now,
        memo=None,
    )
    mock_db = mocker.MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    mock_session_local.return_value = mock_db
    mock_db.__enter__.return_value = mock_db
    user_repository = UserRepository()

    result = user_repository.find_by_email("test@example.com")
    assert result == User(**row_to_dict(mock_user))


def test_find_by_email_user_does_not_exist(mock_session_local, mocker):
    mock_db = mocker.MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_session_local.return_value = mock_db
    mock_db.__enter__.return_value = mock_db
    user_repository = UserRepository()

    with pytest.raises(HTTPException) as exception:
        user_repository.find_by_email("nonexistent@example.com")

    assert exception.value.status_code == 422