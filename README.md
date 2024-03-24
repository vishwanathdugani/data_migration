# Data Migration Project

## Introduction
This project aims to migrate an existing Customer Relationship Management (CRM) system to a more efficient and scalable database design. This README outlines the project setup, including the initial models and their limitations, the improvements made, and a comprehensive guide on how to migrate using modern tools.

## Getting Started

### Cloning the Repository
To clone the project repository, use the following command:
```
git clone git@github.com:vishwanathdugani/data_migration.git
```

### Prerequisites
- **Docker**: Ensure you have Docker installed on your system.
- **Python Environment (without Docker)**: Python 3.11+, virtual environment, and pip.

### Running the Project with Docker
```
docker-compose up --build
```

### Running the Project without Docker
1. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run tests:
   ```
   pytest test_api.py
   ```

## Project Structure
- `original_models.py`: Contains the original database models.
- `models.py`: Contains the improved and optimized models.
- `test_api.py`: Includes tests for creating a `Person`. To run tests and generate a report, use the command: 
   ```
   docker exec -it <container-name> pytest --html=report.html
   ```

## Limitations and Issues with the Old Models

The original models suffered from several limitations, including data duplication between Contact and Patient records, inconsistent representation of medical conditions, complex management of multiple user types, and inefficient tracking of patient journeys and appointments. These issues complicated data synchronization, introduced inconsistency, and made the system harder to maintain and scale.

## Improved Models

The redesigned data model addresses the aforementioned issues by unifying similar entities, introducing clear structures for user roles, patient journeys, and referrals, and simplifying entity relationships. This holistic approach enhances data integrity, streamlines system maintenance, and supports scalability, ultimately leading to more effective patient and contact management.

## Migration Steps

### Using Django's Migration System or Alembic in FastAPI

For Django projects, the built-in migration system automatically generates migration files based on model changes, which can be applied to update the database schema.

For FastAPI projects, Alembic can be used for database migrations. Alembic requires manual creation of migration scripts but provides a powerful and flexible way to manage database schema changes.

### Migration Process

1. **Data Mapping and Cleanup**: Review the current data, map each field to the new structure, and clean up any inconsistencies.

2. **Schema Creation for New Model**: Develop the new database schema based on the improved model.

3. **Data Migration Scripts**: Write scripts to migrate data from the old structure to the new one, accommodating for complex data transformations.

4. **Pilot Testing**: Perform a pilot migration to identify and address potential issues.

5. **Full Data Migration**: Execute the migration scripts to transfer all data to the new model.

6. **Validation and Verification**: Test the new system thoroughly to ensure data integrity and functionality.

7. **Phased Rollout**: Gradually roll out the new system to users, providing necessary training and support.

8. **Decommission Old System**: Once the new system is stable and widely adopted, decommission the old system according to data retention protocols.

This guide should provide a comprehensive overview of the migration process, from understanding the limitations of the old models to executing a successful migration to the improved models.