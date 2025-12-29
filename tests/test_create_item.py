import pytest
import requests
import uuid


class TestCreateItem:
    """
    Тесты для создания объявлений POST /api/1/item
    """

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_create_item_success(self, api_client, new_seller_id):
        """TEST-001: Успешное создание объявления с валидными данными"""
        data = {
            "sellerID": new_seller_id,
            "name": "Тестовое объявление",
            "price": 1000,
            "statistics": {
                "likes": 0,
                "viewCount": 0,
                "contacts": 0
            }
        }

        response = api_client.create_item(data)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        response_data = response.json()

        required_fields = ["id", "sellerId", "name", "price", "statistics", "createdAt"]
        for field in required_fields:
            assert field in response_data, f"Response should contain '{field}'"

        assert response_data["name"] == data["name"]
        assert response_data["price"] == data["price"]
        assert response_data["sellerId"] == data["sellerID"]

    @pytest.mark.negative
    def test_create_item_without_statistics(self, api_client, new_seller_id):
        """
        TEST-002: Создание объявления без поля statistics
        """
        data = {
            "sellerID": new_seller_id,
            "name": "Объявление без статистики",
            "price": 500
        }

        response = api_client.create_item(data)

        assert response.status_code == 400, \
            f"Expected 400 (statistics is required), got {response.status_code}: {response.text}"

    @pytest.mark.positive
    def test_create_item_with_zero_price(self, api_client, new_seller_id):
        """TEST-003: Создание объявления с минимальной ценой (0)"""
        data = {
            "sellerID": new_seller_id,
            "name": "Бесплатное объявление",
            "price": 0,
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }

        response = api_client.create_item(data)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        response_data = response.json()
        assert response_data["price"] == 0

    @pytest.mark.negative
    def test_create_item_with_negative_price(self, api_client, new_seller_id):
        """TEST-004: Создание объявления с отрицательной ценой"""
        data = {
            "sellerID": new_seller_id,
            "name": "Объявление с отрицательной ценой",
            "price": -100,
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }

        response = api_client.create_item(data)

        assert response.status_code == 400, \
            f"Expected 400 for negative price, got {response.status_code}: {response.text}"

    @pytest.mark.negative
    def test_create_item_without_seller_id(self, api_client):
        """TEST-005: Создание объявления без обязательного поля sellerID"""
        data = {
            "name": "Объявление без sellerID",
            "price": 1000,
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }

        response = api_client.create_item(data)

        assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.text}"

    @pytest.mark.negative
    def test_create_item_without_name(self, api_client, new_seller_id):
        """TEST-006: Создание объявления без обязательного поля name"""
        data = {
            "sellerID": new_seller_id,
            "price": 1000,
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }

        response = api_client.create_item(data)

        assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.text}"

    @pytest.mark.negative
    def test_create_item_without_price(self, api_client, new_seller_id):
        """TEST-007: Создание объявления без обязательного поля price"""
        data = {
            "sellerID": new_seller_id,
            "name": "Объявление без цены",
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }

        response = api_client.create_item(data)

        assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.text}"

    @pytest.mark.negative
    def test_create_item_with_empty_body(self, api_client):
        """TEST-008: Создание объявления с пустым телом запроса"""
        response = api_client.create_item({})

        assert response.status_code == 400, \
            f"Expected 400 for empty body, got {response.status_code}: {response.text}"

    @pytest.mark.negative
    def test_create_item_with_invalid_json(self, base_url):
        """TEST-009: Создание объявления с невалидным JSON"""
        response = requests.post(
            f"{base_url}/api/1/item",
            data="invalid json {",
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        assert response.status_code == 400, \
            f"Expected 400 for invalid JSON, got {response.status_code}: {response.text}"

    @pytest.mark.negative
    def test_create_item_with_empty_name(self, api_client, new_seller_id):
        """TEST-012: Создание объявления с пустым именем"""
        data = {
            "sellerID": new_seller_id,
            "name": "",
            "price": 1000,
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }

        response = api_client.create_item(data)

        assert response.status_code == 400, \
            f"Expected 400 for empty name, got {response.status_code}: {response.text}"

    @pytest.mark.negative
    def test_create_item_with_string_seller_id(self, api_client):
        """TEST-013: Создание объявления с sellerID строкового типа"""
        data = {
            "sellerID": "abc",
            "name": "Тестовое объявление",
            "price": 1000,
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }

        response = api_client.create_item(data)

        assert response.status_code == 400, \
            f"Expected 400 for string sellerID, got {response.status_code}: {response.text}"

    @pytest.mark.negative
    def test_create_item_with_string_price(self, api_client, new_seller_id):
        """TEST-014: Создание объявления с price строкового типа"""
        data = {
            "sellerID": new_seller_id,
            "name": "Тестовое объявление",
            "price": "123",
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }

        response = api_client.create_item(data)

        assert response.status_code == 400, \
            f"Expected 400 for string price, got {response.status_code}: {response.text}"

    @pytest.mark.positive
    def test_create_item_with_long_name(self, api_client, new_seller_id):
        """TEST-011: Создание объявления с очень длинным именем"""
        data = {
            "sellerID": new_seller_id,
            "name": "A" * 1000,
            "price": 1000,
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }

        response = api_client.create_item(data)

        assert response.status_code == 200, \
            f"Unexpected status code: {response.status_code}"

    @pytest.mark.positive
    def test_create_item_with_special_characters_in_name(self, api_client, new_seller_id):
        """TEST-038: SQL-инъекция в поле name (проверка безопасности)"""
        data = {
            "sellerID": new_seller_id,
            "name": "'; DROP TABLE items;--",
            "price": 1000,
            "statistics": {
                "likes": 1,
                "viewCount": 1,
                "contacts": 1
            }
        }

        response = api_client.create_item(data)

        assert response.status_code == 400, \
            f"Unexpected status code: {response.status_code}"

    @pytest.mark.integration
    def test_create_multiple_items_unique_ids(self, api_client, new_seller_id):
        """TEST-033: Проверка уникальности ID объявлений"""
        ids = set()

        for i in range(3):
            data = {
                "sellerID": new_seller_id,
                "name": f"Test Item {i}",
                "price": 1000 + i,
                "statistics": {
                    "likes": 1,
                    "viewCount": 1,
                    "contacts": 1
                }
            }
            response = api_client.create_item(data)

            if response.status_code == 200:
                item_id = response.json().get("id")
                assert item_id not in ids, f"Duplicate ID found: {item_id}"
                ids.add(item_id)

        assert len(ids) == 3, "Should have 3 unique IDs"

    @pytest.mark.negative
    def test_create_item_with_incomplete_statistics(self, api_client, new_seller_id):
        """TEST-034: Создание объявления с неполной статистикой"""
        data = {
            "sellerID": new_seller_id,
            "name": "Объявление с неполной статистикой",
            "price": 1000,
            "statistics": {
                "likes": 10
            }
        }

        response = api_client.create_item(data)

        assert response.status_code == 400, \
            f"Unexpected status code: {response.status_code}"

    @pytest.mark.positive
    def test_create_item_response_structure(self, api_client, new_seller_id):
        """Проверка структуры ответа согласно swagger"""
        data = {
            "sellerID": new_seller_id,
            "name": "Проверка структуры ответа",
            "price": 5000,
            "statistics": {
                "likes": 10,
                "viewCount": 100,
                "contacts": 5
            }
        }

        response = api_client.create_item(data)
        assert response.status_code == 200

        response_data = response.json()

        assert isinstance(response_data["id"], str), "id should be string"
        assert isinstance(response_data["sellerId"], int), "sellerId should be integer"
        assert isinstance(response_data["name"], str), "name should be string"
        assert isinstance(response_data["price"], int), "price should be integer"
        assert isinstance(response_data["createdAt"], str), "createdAt should be string"

        if response_data["statistics"] is not None:
            stats = response_data["statistics"]
            assert isinstance(stats.get("likes"), int), "likes should be integer"
            assert isinstance(stats.get("viewCount"), int), "viewCount should be integer"
            assert isinstance(stats.get("contacts"), int), "contacts should be integer"
