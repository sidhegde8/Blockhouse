import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_read_orders(self):
        response = client.get("/orders")
        self.assertEqual(response.status_code, 200)

    def test_create_order(self):
        payload = {
            "symbol": "AAPL",
            "price": 150.0,
            "quantity": 10,
            "order_type": "buy"
        }
        response = client.post("/orders", json=payload)
        print(response.json())  # Debugging: Check API response
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
