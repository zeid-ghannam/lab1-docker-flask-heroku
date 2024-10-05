import pytest
from app import create_app
from app.models import db, Person
from flask import url_for

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        
        with app.app_context():
            db.drop_all()

def test_get_person(client):
    # Create a test person
    with client.application.app_context():
        person = Person(name="John Doe", age=30)
        db.session.add(person)
        db.session.commit()
        person_id = person.id

    # Test GET request
    response = client.get(f'/persons/{person_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == "John Doe"
    assert data['age'] == 30

def test_get_nonexistent_person(client):
    response = client.get('/persons/999')
    assert response.status_code == 404

def test_get_all_persons(client):
    # Create test persons
    with client.application.app_context():
        db.session.add(Person(name="John Doe", age=30))
        db.session.add(Person(name="Jane Doe", age=28))
        db.session.commit()

    # Test GET request
    response = client.get('/persons')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['name'] == "John Doe"
    assert data[1]['name'] == "Jane Doe"

def test_create_person(client):
    # Test POST request
    response = client.post('/persons', json={"name": "Alice", "age": 25})
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == "Alice"
    assert data['age'] == 25
    assert 'id' in data
    # assert response.headers['Location'].endswith(f"/persons/{data['id']}")

def test_update_person(client):
    # Create a test person
    with client.application.app_context():
        person = Person(name="Bob", age=40)
        db.session.add(person)
        db.session.commit()
        person_id = person.id

    # Test PATCH request
    response = client.patch(f'/persons/{person_id}', json={"name": "Robert", "age": 41})
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == "Robert"
    assert data['age'] == 41

def test_update_nonexistent_person(client):
    response = client.patch('/persons/999', json={"name": "Nobody", "age": 0})
    assert response.status_code == 404

def test_delete_person(client):
    # Create a test person
    with client.application.app_context():
        person = Person(name="Charlie", age=35)
        db.session.add(person)
        db.session.commit()
        person_id = person.id

    # Test DELETE request
    response = client.delete(f'/persons/{person_id}')
    assert response.status_code == 204

    # Verify person is deleted
    response = client.get(f'/persons/{person_id}')
    assert response.status_code == 404

def test_delete_nonexistent_person(client):
    response = client.delete('/persons/999')
    assert response.status_code == 404