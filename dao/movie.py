from dao.model.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, id: int) -> Movie:
        """Получить один фильм по ID"""

        return self.session.query(Movie).get(id)

    def get_all(self, page: int = None, director_id: int = None, genre_id: int = None, status: str = None) -> list:
        """Получить все фильмы с возможной фильтрацией"""

        query = self.session.query(Movie)


        if director_id:
            query = query.filter(Movie.director_id == director_id)
        if genre_id:
            query = query.filter(Movie.genre_id == genre_id)

        if status == "new":
            query = query.order_by(Movie.year.desc())

        if page:
            per_page = 12
            skip = (page - 1) * per_page
            return query.offset(skip).limit(per_page).all()

        return query.all()

    def create(self, data: dict) -> Movie:
        """Создать новый фильм"""

        movie: Movie = Movie(**data)
        self.session.add(movie)
        self.session.commit()
        return movie

    def update(self, movie: Movie) -> Movie:
        """Обновить фильм"""

        self.session.add(movie)
        self.session.commit()
        return movie

    def delete(self, id: int) -> None:
        """Удалить фильм"""

        movie: Movie = self.get_one(id)
        self.session.delete(movie)
        self.session.commit()
