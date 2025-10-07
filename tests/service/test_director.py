from dao.director import DirectorDAO
from service.director import DirectorService
from dao.model.director import Director
from unittest.mock import MagicMock
import pytest


@pytest.fixture()
def director_dao()->DirectorDAO:
    director_dao: DirectorDAO = DirectorDAO(None)

    director_one: Director = Director(id=1, name='Biba')
    director_two: Director = Director(id=2, name='Boba')
    new_director: Director = Director(id=3, name='newcomer')
    updated_director: Director = Director(id=1, name='Bobr')

    director_dao.get_one = MagicMock(return_value=director_one)
    director_dao.get_all = MagicMock(return_value=[director_one, director_two])
    director_dao.create = MagicMock(return_value=new_director)
    director_dao.update = MagicMock(return_value=updated_director)
    director_dao.delete = MagicMock(return_value=None)

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao: DirectorDAO) -> None:
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self) -> None:
        director: Director = self.director_service.get_one(1)
        assert director is not None
        assert director.name == 'Biba'
        assert director.id == 1

    def test_get_all(self) -> None:
        directors: list = self.director_service.get_all()
        assert directors is not None
        assert len(directors) == 2

    def test_create(self) -> None:
        new_director: dict = {"name": "newcomer"}
        director: Director = self.director_service.create(new_director)
        assert director.id == 3
        assert director.name == "newcomer"

    def test_update(self) -> None:
        updated_director: dict = {"id": 1, "name": "Bobr"}
        director: Director = self.director_service.update(updated_director,1)
        assert director.id == 1
        assert director.name == "Bobr"

    def test_delete(self) -> None:
        self.director_service.delete(1)
