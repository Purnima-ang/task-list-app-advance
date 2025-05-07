import pytest
from tests import create_app  # Adjust this import based on your app's structure

@pytest.fixture
def client():
    app = create_app()  # Initialize your Flask app here (adjust if needed)
    with app.test_client() as client:
        yield client
