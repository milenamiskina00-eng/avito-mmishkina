import pytest
import uuid


class TestGetItem:
    """
    Тесты для получения объявления по ID: GET /api/1/item/:id
    """

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_existing_item(self, api_client, created_item):
        """TEST-015: Успешное получение существующего объявления"""
        item_id = created_item["id"]

        response = api_client.get_item(item_id)

        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}: {response.text}"

        response_data = response.json()

        # Согласно swagger ответ - это МАССИВ
        assert isinstance(response_data, list), \
            f"Response should be array, got {type(response_data)}"

        assert len(response_data) > 0, "Response array should not be empty"

        item = response_data[0]

        # Проверяем обязательные поля согласно swagger
        required_fields = ["id", "sellerId", "name", "price", "statistics", "createdAt"]
        for field in required_fields:
            assert field in item, f"Item should contain '{field}'"

        # Проверяем соответствие данных
        assert item["id"] == created_item["id"]
        assert item["name"] == created_item["name"]
        assert item["price"] == created_item["price"]

    @pytest.mark.negative
    def test_get_nonexistent_item(self, api_client):
        """TEST-016: Получение несуществующего объявления"""
        fake_uuid = str(uuid.uuid4())

        response = api_client.get_item(fake_uuid)

        assert response.status_code == 404, \
            f"Expected 404, got {response.status_code}: {response.text}"

    @pytest.mark.negative
    def test_get_item_with_invalid_id_format(self, api_client):
        """TEST-017: Получение объявления с невалидным форматом ID"""
        response = api_client.get_item("invalid-id-format")

        # Согласно swagger может быть 400 или 404
        assert response.status_code in [400, 404], \
            f"Expected 400 or 404, got {response.status_code}: {response.text}"

    @pytest.mark.negative
    def test_get_item_with_special_characters(self, api_client):
        """TEST-019: Получение объявления с ID содержащим спецсимволы"""
        response = api_client.get_item("!@#$%^&*()")

        assert response.status_code in [400, 404], \
            f"Expected 400 or 404, got {response.status_code}"

    @pytest.mark.integration
    def test_get_item_matches_created_data(self, api_client, new_seller_id):
        """TEST-031: Создание и последующее получение объявления"""
        create_data = {
            "sellerID": new_seller_id,
            "name": "Проверка соответствия данных",
            "price": 9999,
            "statistics": {
                "likes": 10,
                "viewCount": 100,
                "contacts": 5
            }
        }

        create_response = api_client.create_item(create_data)
        assert create_response.status_code == 200, \
            f"Failed to create: {create_response.text}"

        created_item = create_response.json()
        item_id = created_item["id"]

        get_response = api_client.get_item(item_id)
        assert get_response.status_code == 200

        response_data = get_response.json()

        assert isinstance(response_data, list)
        item = response_data[0]

        assert item["name"] == create_data["name"]
        assert item["price"] == create_data["price"]
        assert item["sellerId"] == create_data["sellerID"]

    @pytest.mark.positive
    def test_get_item_response_structure(self, api_client, created_item):
        """Проверка структуры ответа GET согласно swagger"""
        item_id = created_item["id"]

        response = api_client.get_item(item_id)
        assert response.status_code == 200

        response_data = response.json()

        assert isinstance(response_data, list)
        assert len(response_data) > 0

        item = response_data[0]

        assert isinstance(item["id"], str)
        assert isinstance(item["sellerId"], int)
        assert isinstance(item["name"], str)
        assert isinstance(item["price"], int)
        assert isinstance(item["createdAt"], str)

    @pytest.mark.negative
    def test_get_item_empty_id(self, base_url):
        """TEST-018: Получение объявления с пустым ID"""
        import requests

        response = requests.get(
            f"{base_url}/api/1/item/",
            headers={"Accept": "application/json"}
        )

        assert response.status_code == 400, \
            f"Expected error status, got {response.status_code}"
