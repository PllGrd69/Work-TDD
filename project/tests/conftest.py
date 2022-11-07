import os
 
import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise
from app.main import create_application
from app.config import get_settings, Settings
 
 
def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))
 
 
@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
 
        # testing
        yield test_client
 
    # tear down
 
 
# new
@pytest.fixture(scope="module")
def test_app_with_db():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
 
        # testing
        yield test_client
 
    # tear down
def test_read_summary_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"