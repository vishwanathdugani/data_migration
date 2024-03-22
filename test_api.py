from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, engine
from main import app, get_db

# Configure test database
DATABASE_URL = "sqlite:///./test_test.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency override for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app = app
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_read_person():
    # Create a new person
    response = client.post(
        "/people/",
        json={"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "role_type": "patient"}
    )
    assert response.status_code == 201
    person_id = response.json()["person_id"]

    # Read the created person
    response = client.get(f"/people/{person_id}")
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"

    # Cleanup
    client.delete(f"/people/{person_id}")

# Add similar tests for MedicalCondition, Appointment, PatientJourney, Referral, PhysicianDetails, and Hospital

def test_medical_condition_lifecycle():
    # Create a new medical condition
    response = client.post(
        "/medical_conditions/",
        json={"name": "TestCondition", "abbreviation": "TC"}
    )
    assert response.status_code == 201
    condition_id = response.json()["medical_condition_id"]

    # Read the created medical condition
    response = client.get(f"/medical_conditions/{condition_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "TestCondition"

def test_appointment_lifecycle():
    # Assuming a person exists; replace '1' with a dynamic retrieval if necessary
    person_id = 1
    # Create a new appointment
    response = client.post(
        "/appointments/",
        json={"person_id": person_id, "appointment_time": "2023-01-01T10:00:00", "notes": "Initial Consultation"}
    )
    assert response.status_code == 201
    appointment_id = response.json()["appointment_id"]

    # Read the created appointment for the person
    response = client.get(f"/appointments/person/{person_id}")
    assert response.status_code == 200
    assert any(appointment["appointment_id"] == appointment_id for appointment in response.json())

def test_patient_journey_lifecycle():
    # Assuming a person and a medical condition exist; replace '1' with dynamic retrieval if necessary
    person_id, medical_condition_id = 1, 1
    # Create a new patient journey
    response = client.post(
        "/patient_journeys/",
        json={"person_id": person_id, "medical_condition_id": medical_condition_id, "stage": "lead"}
    )
    assert response.status_code == 201
    journey_id = response.json()["journey_id"]

    # Read the created patient journey
    response = client.get(f"/patient_journeys/{journey_id}")
    assert response.status_code == 200
    assert response.json()["stage"] == "lead"

def test_referral_lifecycle():
    # Create a new referral
    response = client.post(
        "/referrals/",
        json={"type": "EAP", "details": "Details about the referral", "start_date": "2023-01-01", "end_date": "2023-12-31"}
    )
    assert response.status_code == 201
    referral_id = response.json()["referral_id"]

    # Read the created referral
    response = client.get(f"/referrals/{referral_id}")
    assert response.status_code == 200
    assert response.json()["type"] == "EAP"

def test_physician_details_hospital_lifecycle():
    # Create a new hospital
    hospital_response = client.post(
        "/hospitals/",
        json={"name": "Test Hospital", "city": "Test City"}
    )
    assert hospital_response.status_code == 201
    hospital_id = hospital_response.json()["hospital_id"]

    # Assuming a person (physician) exists; replace '1' with dynamic retrieval if necessary
    person_id = 1
    # Create new physician details
    details_response = client.post(
        "/physician_details/",
        json={"person_id": person_id, "medical_license_number": "123456", "hospital_id": hospital_id}
    )
    assert details_response.status_code == 201
    details_id = details_response.json()["physician_details_id"]

    # Read the created physician details
    details_read_response = client.get(f"/physician_details/{details_id}")
    assert details_read_response.status_code == 200
    assert details_read_response.json()["medical_license_number"] == "123456"

    # Read the created hospital
    hospital_read_response = client.get(f"/hospitals/{hospital_id}")
    assert hospital_read_response.status_code == 200
    assert hospital_read_response.json()["name"] == "Test Hospital"
