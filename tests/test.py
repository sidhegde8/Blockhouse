import unittest
from fastapi.testclient import TestClient
from app.main import app, get_db, Order, engine, Base

client = TestClient(app)

def setup_test_db():
    Base.metadata.drop_all(bind=engine)  # Clear existing tables
    Base.metadata.create_all(bind=engine)  # Create fresh tables

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        setup_test_db()  # Ensure database is set up before tests

    def test_read_orders(self):
        response = client.get("/orders")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"orders": []})  # Expect empty orders list initially

    def test_create_order(self):
        payload = {
            "symbol": "AAPL",
            "price": 150.0,
            "quantity": 10,
            "order_type": "buy"
        }
        response = client.post("/orders", json=payload)
        print(response.json())  # Debugging output
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
