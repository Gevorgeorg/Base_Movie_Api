import pytest
from unittest.mock import patch, MagicMock
from app import app


class TestGenresViews:
    @pytest.fixture
    def client(self):
        return app.test_client()

    def test_get_all_genres(self, client):
        with patch('views.genres.genre_service') as mock_service:
            mock_service.get_all.return_value = [
                MagicMock(id=1, name="Comedy"),
                MagicMock(id=2, name="drama")
            ]
            response = client.get('/genres/')
            assert response.status_code == 200
            mock_service.get_all.assert_called_once()

    def test_create_genre(self, client):
        with patch('views.genres.genre_service') as mock_service:
            mock_genre = MagicMock()
            mock_genre.id = 1
            mock_service.create.return_value = mock_genre

            response = client.post('/genres/', json={
                "name": "New Genre"
            })

            assert response.status_code == 201
            mock_service.create.assert_called_once_with({"name": "New Genre"})

    def test_get_genre_by_id(self, client):
        with patch('views.genres.genre_service') as mock_service:
            mock_genre = MagicMock()
            mock_genre.id = 1
            mock_genre.name = "Comedy"
            mock_service.get_one.return_value = mock_genre

            response = client.get('/genres/1')

            assert response.status_code == 200
            mock_service.get_one.assert_called_once_with(1)

    def test_update_genre(self, client):
        with patch('views.genres.genre_service') as mock_service:
            response = client.put('/genres/1', json={
                "name": "Updated Genre"
            })

            assert response.status_code == 204
            mock_service.update.assert_called_once_with({"name": "Updated Genre"}, 1)

    def test_partial_update_genre(self, client):
        with patch('views.genres.genre_service') as mock_service:
            response = client.patch('/genres/1', json={
                "name": "Updated Genre"
            })

            assert response.status_code == 204
            mock_service.partially_update.assert_called_once_with({"name": "Updated Genre"}, 1)

    def test_delete_genre(self, client):
        with patch('views.genres.genre_service') as mock_service:
            response = client.delete('/genres/1')

            assert response.status_code == 204
            mock_service.delete.assert_called_once_with(1)
