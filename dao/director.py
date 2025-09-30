from dao.model.director import Director


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, id: int) -> Director:
        """Получить одного режиссера по ид"""

        return self.session.query(Director).get(id)

    def get_all(self) -> list:
        """Получить всех"""

        return self.session.query(Director).all()

    def create(self, data: dict) -> Director:
        """Добавить нового режиссера"""

        new: Director = Director(**data)
        self.session.add(new)
        self.session.commit()
        return new

    def update(self, director: Director) -> Director:
        """Обновить информацию о режиссере"""

        self.session.add(director)
        self.session.commit()
        return director

    def delete(self, id: int) -> None:
        """Удалить режиссера"""

        director: Director = self.get_one(id)
        self.session.delete(director)
        self.session.commit()
