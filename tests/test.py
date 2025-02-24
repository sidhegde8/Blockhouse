import unittest
from fastapi.testclient import TestClient
from app.main import app, get_db, Order, engine, Base
from sqlalchemy.orm import sessionmaker

client = TestClient(app)

# ✅ Reset the database before running tests
def reset_test_db():
    with engine.begin() as conn:
        Base.metadata.drop_all(bind=conn)  # Clears existing tables
        Base.metadata.create_all(bind=conn)  # Recreates tables

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reset_test_db()  # ✅ Ensure database is empty before tests run

    def test_read_orders(self):
        response = client.get("/orders")
        print("Initial /orders response:", response.json())  # ✅ Debugging
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])  # ✅ Expect an empty list

    def test_create_order(self):
        payload = {
            "symbol": "AAPL",
            "price": 150.0,
            "quantity": 10,
            "order_type": "buy"
        }
        response = client.post("/orders", json=payload)
        print("Create Order Response:", response.json())  # ✅ Debugging
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
