import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from main import app, get_db

DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="session")
def engine():
    return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def person_id(client):
    response = client.post(
        "/persons/",
        json={"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com", "role_type": "patient"}
    )
    assert response.status_code == 200
    data = response.json()
    return data["person_id"]


def test_read_person(client, person_id):
    response = client.get(f"/persons/{person_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["person_id"] == person_id


def test_update_person(client, person_id):
    response = client.put(
        f"/persons/{person_id}",
        json={"first_name": "Jane Updated"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["person_id"] == person_id


def test_delete_person(client, person_id):
    response = client.delete(f"/persons/{person_id}")
    assert response.status_code == 200
    response = client.get(f"/persons/{person_id}")
    assert response.status_code == 404


def test_read_nonexistent_person(client):
    response = client.get("/persons/999999")
    assert response.status_code == 404
