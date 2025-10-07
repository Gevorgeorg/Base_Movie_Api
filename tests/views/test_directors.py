import pytest
from unittest.mock import patch, MagicMock
from app import app


class TestDirectorsViews:
    @pytest.fixture
    def client(self):
        return app.test_client()

    def test_get_all_directors(self, client):
        with patch('views.directors.director_service') as mock_service:
            mock_service.get_all.return_value = [
                MagicMock(id=1, name="Vovan"),
                MagicMock(id=2, name="Ivan")
            ]
            response = client.get('/directors/')
            assert response.status_code == 200
            mock_service.get_all.assert_called_once()

    def test_create_director(self, client):
        with patch('views.directors.director_service') as mock_service:
            mock_director = MagicMock()
            mock_director.id = 1
            mock_service.create.return_value = mock_director

            response = client.post('/directors/', json={
                "name": "New Director"
            })

            assert response.status_code == 201
            mock_service.create.assert_called_once_with({"name": "New Director"})

    def test_get_director_by_id(self, client):
        with patch('views.directors.director_service') as mock_service:
            mock_director = MagicMock()
            mock_director.id = 1
            mock_director.name = "Vovan"
            mock_service.get_one.return_value = mock_director

            response = client.get('/directors/1')

            assert response.status_code == 200
            mock_service.get_one.assert_called_once_with(1)

    def test_update_director(self, client):
        with patch('views.directors.director_service') as mock_service:
            response = client.put('/directors/1', json={
                "name": "Updated Director"
            })

            assert response.status_code == 204
            mock_service.update.assert_called_once_with({"name": "Updated Director"}, 1)

    def test_partial_update_director(self, client):
        with patch('views.directors.director_service') as mock_service:
            response = client.patch('/directors/1', json={
                "name": "Updated Director"
            })

            assert response.status_code == 204
            mock_service.partially_update.assert_called_once_with({"name": "Updated Director"}, 1)

    def test_delete_director(self, client):
        with patch('views.directors.director_service') as mock_service:
            response = client.delete('/directors/1')

            assert response.status_code == 204
            mock_service.delete.assert_called_once_with(1)
