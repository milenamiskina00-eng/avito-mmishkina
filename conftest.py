import pytest
import requests
import random
import uuid

BASE_URL = "https://qa-internship.avito.com"


def generate_seller_id():
    """Генерация уникального sellerID в допустимом диапазоне"""
    return random.randint(111111, 999999)


@pytest.fixture(scope="session")
def base_url():
    """Базовый URL API"""
    return BASE_URL


@pytest.fixture(scope="session")
def seller_id():
    """Уникальный sellerID для тестовой сессии"""
    return generate_seller_id()


@pytest.fixture
def new_seller_id():
    """Новый уникальный sellerID для каждого теста"""
    return generate_seller_id()


@pytest.fixture
def valid_item_data(new_seller_id):
    """
    Валидные данные для создания объявления.
    ВАЖНО: согласно swagger, statistics - ОБЯЗАТЕЛЬНОЕ поле!
    """
    return {
        "sellerID": new_seller_id,
        "name": f"Test Item {uuid.uuid4().hex[:8]}",
        "price": random.randint(100, 10000),
        "statistics": {
            "likes": 0,
            "viewCount": 0,
            "contacts": 0
        }
    }


@pytest.fixture
def api_client(base_url):
    """API клиент с базовыми методами"""

    class APIClient:
        def __init__(self, base_url):
            self.base_url = base_url
            self.headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

        def create_item(self, data):
            """POST /api/1/item - Создать объявление"""
            return requests.post(
                f"{self.base_url}/api/1/item",
                json=data,
                headers=self.headers
            )

        def get_item(self, item_id):
            """GET /api/1/item/{id} - Получить объявление по ID"""
            return requests.get(
                f"{self.base_url}/api/1/item/{item_id}",
                headers={"Accept": "application/json"}
            )

        def get_seller_items(self, seller_id):
            """GET /api/1/{sellerID}/item - Получить все объявления продавца"""
            return requests.get(
                f"{self.base_url}/api/1/{seller_id}/item",
                headers={"Accept": "application/json"}
            )

        def get_statistic(self, item_id, version=1):
            """GET /api/{version}/statistic/{id} - Получить статистику"""
            return requests.get(
                f"{self.base_url}/api/{version}/statistic/{item_id}",
                headers={"Accept": "application/json"}
            )

        def delete_item(self, item_id):
            """DELETE /api/2/item/{id} - Удалить объявление"""
            return requests.delete(
                f"{self.base_url}/api/2/item/{item_id}",
                headers={"Accept": "application/json"}
            )

    return APIClient(base_url)


@pytest.fixture
def created_item(api_client, valid_item_data):
    """
    Фикстура: создаёт объявление и возвращает его данные.
    После теста удаляет объявление (cleanup).
    """
    response = api_client.create_item(valid_item_data)
    assert response.status_code == 200, f"Failed to create item: {response.text}"

    item_data = response.json()
    yield item_data

    # Cleanup: удаляем созданное объявление
    if item_data and "id" in item_data:
        api_client.delete_item(item_data["id"])
