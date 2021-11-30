import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.settings.settings import settings_factory
from src.user_repository.sql_user_repository import sql_user_repository_factory
from tests.fakes.fake_settings import fake_settings_factory
from tests.fakes.fake_user_repository import fake_user_repository_factory


@pytest.fixture()
def client():
    app.dependency_overrides[sql_user_repository_factory] = fake_user_repository_factory
    app.dependency_overrides[settings_factory] = fake_settings_factory
    return TestClient(app)
