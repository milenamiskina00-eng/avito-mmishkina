import pytest
import uuid


class TestGetStatistic:
    """
    Тесты для получения статистики: GET /api/1/statistic/:id и /api/2/statistic/:id
    """

    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_statistic_success(self, api_client, created_item):
        """TC-026: Успешное получение статистики существующего объявления"""
        item_id = created_item["id"]

        response = api_client.get_statistic(item_id, version=1)

        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}: {response.text}"

        stat_data = response.json()

        assert isinstance(stat_data, list), \
            f"Response should be array, got {type(stat_data)}"

    @pytest.mark.negative
    def test_get_statistic_nonexistent_item(self, api_client):
        """TC-027: Получение статистики несуществующего объявления"""
        fake_uuid = str(uuid.uuid4())

        response = api_client.get_statistic(fake_uuid, version=1)

        assert response.status_code == 404, \
            f"Expected 404, got {response.status_code}: {response.text}"

    @pytest.mark.negative
    def test_get_statistic_invalid_id_v1(self, api_client):
        """TC-028: Получение статистики с невалидным ID (API v1)"""
        response = api_client.get_statistic("invalid-id", version=1)

        assert response.status_code == 400, \
            f"Expected 400, got {response.status_code}"

    @pytest.mark.negative
    def test_get_statistic_invalid_id_v2(self, api_client):
        """TC-028b: Получение статистики с невалидным ID (API v2)"""
        response = api_client.get_statistic("invalid-id", version=2)

        assert response.status_code == 404, \
            f"Expected 404 for API v2, got {response.status_code}"

    @pytest.mark.positive
    def test_get_statistic_initial_values(self, api_client, new_seller_id):
        """TC-029: Проверка значений статистики"""
        create_data = {
            "sellerID": new_seller_id,
            "name": "Объявление со статистикой",
            "price": 500,
            "statistics": {
                "likes": 10,
                "viewCount": 100,
                "contacts": 5
            }
        }

        create_response = api_client.create_item(create_data)
        assert create_response.status_code == 200

        created_item = create_response.json()
        item_id = created_item["id"]

        stat_response = api_client.get_statistic(item_id, version=1)
        assert stat_response.status_code == 200

        stat_data = stat_response.json()

        assert isinstance(stat_data, list)

        if len(stat_data) > 0:
            stat = stat_data[0]
            assert "likes" in stat or "viewCount" in stat or "contacts" in stat

    @pytest.mark.positive
    def test_get_statistic_api_v2(self, api_client, created_item):
        """TC-030: Получение статистики через API v2"""
        item_id = created_item["id"]

        response = api_client.get_statistic(item_id, version=2)

        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}: {response.text}"

        stat_data = response.json()
        assert isinstance(stat_data, list)

    @pytest.mark.positive
    def test_statistic_response_structure(self, api_client, created_item):
        """Проверка структуры ответа статистики согласно swagger"""
        item_id = created_item["id"]

        response = api_client.get_statistic(item_id, version=1)
        assert response.status_code == 200

        stat_data = response.json()

        assert isinstance(stat_data, list)

        if len(stat_data) > 0:
            stat = stat_data[0]

            if stat is not None:
                assert "likes" in stat
                assert "viewCount" in stat
                assert "contacts" in stat

                assert isinstance(stat["likes"], int)
                assert isinstance(stat["viewCount"], int)
                assert isinstance(stat["contacts"], int)

    @pytest.mark.positive
    def test_compare_statistic_v1_and_v2(self, api_client, created_item):
        """Сравнение ответов API v1 и v2 для статистики"""
        item_id = created_item["id"]

        response_v1 = api_client.get_statistic(item_id, version=1)
        response_v2 = api_client.get_statistic(item_id, version=2)

        assert response_v1.status_code == 200
        assert response_v2.status_code == 200

        stat_v1 = response_v1.json()
        stat_v2 = response_v2.json()

        assert stat_v1 == stat_v2, \
            f"Statistics from v1 and v2 should match: v1={stat_v1}, v2={stat_v2}"
