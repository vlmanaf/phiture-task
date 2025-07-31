from fastapi.testclient import TestClient
from app.main import app, Product

client = TestClient(app)


def test_team_builder_response_format(monkeypatch):
    # --- mock PRODUCTS to avoid depending on products.json ---
    mock_products = [
        Product(id=i, name=f"Item{i}", category=f"Cat{i}", price=10.0 + i, rating=4.0 + i * 0.1)
        for i in range(5)
    ]
    monkeypatch.setattr("app.main.PRODUCTS", mock_products)

    response = client.get("/team-builder", params={"budget": 100})
    assert response.status_code == 200

    data = response.json()

    # Response must be a list
    assert isinstance(data, list), "Response should be a list of products"

    # Each product must have correct fields and types
    for product in data:
        assert set(product.keys()) == {"id", "name", "category", "price", "rating"}
        assert isinstance(product["name"], str)
        assert isinstance(product["category"], str)
        assert isinstance(product["price"], (float, int))
        assert isinstance(product["rating"], (float, int))

    # Expect 5 products (as per optimization constraint)
    assert len(data) == 5
