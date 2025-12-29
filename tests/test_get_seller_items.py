import pytest
import random


class TestGetSellerItems:
    """
    Тесты для получения всех объявлений продавца: GET /api/1/:sellerID/item
    """

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_seller_items_success(self, api_client, new_seller_id):
        """TC-020: Успешное получение объявлений существующего продавца"""
        created_items = []
        for i in range(3):
            data = {
                "sellerID": new_seller_id,
                "name": f"Объявление продавца {i}",
                "price": 1000 * (i + 1),
                "statistics": {
                    "likes": 0,
                    "viewCount": 0,
                    "contacts": 0
                }
            }
            response = api_client.create_item(data)
            if response.status_code == 200:
                created_items.append(response.json())

        get_response = api_client.get_seller_items(new_seller_id)

        assert get_response.status_code == 200, \
            f"Expected 200, got {get_response.status_code}: {get_response.text}"

        items = get_response.json()

        assert isinstance(items, list), "Response should be a list"

        created_ids = {item["id"] for item in created_items}
        response_ids = {item["id"] for item in items}

        assert created_ids.issubset(response_ids), \
            "All created items should be in response"

    @pytest.mark.positive
    def test_get_seller_items_empty_list(self, api_client):
        """TC-021: Получение объявлений продавца без объявлений"""
        unique_seller_id = random.randint(111111, 999999)

        response = api_client.get_seller_items(unique_seller_id)

        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}: {response.text}"

        items = response.json()
        assert isinstance(items, list), "Response should be a list"

    @pytest.mark.negative
    def test_get_seller_items_invalid_seller_id_string(self, api_client):
        """TC-022: Получение объявлений с невалидным sellerID (строка)"""
        response = api_client.get_seller_items("abc")

        assert response.status_code == 400, \
            f"Expected 400, got {response.status_code}: {response.text}"

    @pytest.mark.negative
    def test_get_seller_items_negative_seller_id(self, api_client):
        """TC-023: Получение объявлений с отрицательным sellerID"""
        response = api_client.get_seller_items(-1)

        assert response.status_code == 400, \
            f"Expected 400, got {response.status_code}"

    @pytest.mark.negative
    def test_get_seller_items_zero_seller_id(self, api_client):
        """TC-024: Получение объявлений с sellerID = 0"""
        response = api_client.get_seller_items(0)

        assert response.status_code == 400, \
            f"Expected 400, got {response.status_code}"

    @pytest.mark.integration
    def test_get_only_specific_seller_items(self, api_client):
        """TC-025: Проверка что возвращаются только объявления указанного продавца"""
        seller_id_1 = random.randint(111111, 555555)
        seller_id_2 = random.randint(555556, 999999)

        for i in range(2):
            data = {
                "sellerID": seller_id_1,
                "name": f"Seller 1 Item {i}",
                "price": 1000,
                "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
            }
            api_client.create_item(data)

        for i in range(2):
            data = {
                "sellerID": seller_id_2,
                "name": f"Seller 2 Item {i}",
                "price": 2000,
                "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
            }
            api_client.create_item(data)

        response = api_client.get_seller_items(seller_id_1)

        assert response.status_code == 200
        items = response.json()

        for item in items:
            assert item["sellerId"] == seller_id_1, \
                f"Item {item['id']} has wrong sellerId: {item['sellerId']}, expected {seller_id_1}"

    @pytest.mark.positive
    def test_get_seller_items_response_structure(self, api_client, new_seller_id):
        """Проверка структуры ответа согласно swagger"""
        data = {
            "sellerID": new_seller_id,
            "name": "Проверка структуры",
            "price": 1000,
            "statistics": {"likes": 5, "viewCount": 50, "contacts": 2}
        }
        create_resp = api_client.create_item(data)
        assert create_resp.status_code == 200

        response = api_client.get_seller_items(new_seller_id)
        assert response.status_code == 200

        items = response.json()
        assert isinstance(items, list)
        assert len(items) > 0

        item = items[0]

        required_fields = ["id", "sellerId", "name", "price", "statistics", "createdAt"]
        for field in required_fields:
            assert field in item, f"Item should contain '{field}'"
