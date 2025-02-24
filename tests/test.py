import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_read_orders(self):
        response = client.get("/orders")
        self.assertEqual(response.status_code, 200)

    def test_create_order(self):
        response = client.post(
            "/orders",
            json={"symbol": "TSLA", "price": 184.0, "quantity": 4, "order_type": "sell"}
        )
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
