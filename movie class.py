from datetime import datetime


class Movie:
    def __init__(self,movie_code,movie_name,cinema_number,cinema_start_time,cinema_end_time,date,original_price,discount):
        self._date = None
        self._discount = None
        self._original_price = None
        self.movie_code = movie_code
        self.movie_name = movie_name
        self.cinema_number = cinema_number
        self.cinema_start_time = cinema_start_time
        self.cinema_end_time = cinema_end_time
        self.date = date
        self.original_price = original_price
        self.discount = discount


    def __str__(self):
        information = []
        all_attributes = dir(self)
        for attribute in all_attributes:
            if attribute.startswith("_"):
                continue
            try:
                value = getattr(self, attribute)
                if callable(value):
                    continue
                information.append(f"{attribute}: {value}")
            except AttributeError:
                pass
        return '\n'.join(information)

    @property
    def original_price(self):
        return self._original_price

    @original_price.setter
    def original_price(self, value):
        try:
            int(value)
        except ValueError:
            raise ValueError("Error From class Movie: Please enter numeric value")
        self._original_price = int(value)

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        try:
            int(value)
        except ValueError:
            raise ValueError("Error From class Movie: Please enter numeric value")
        if int(value) > 100 or int(value) < 0:
            raise ValueError("Error From class Movie: discount must be between 0 and 100")
        self._discount = int(value)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        try:
            datetime.strptime(value, "%Y/%m/%d")
        except ValueError:
            raise ValueError("Error From class Movie: Invalid date (format YY/MM/DD)")
        except Exception as e:
            raise Exception(f"Unknown Error From class Movie: {e}")
        self._date = str(value)

    @property
    def _start_time(self):
        if self.cinema_start_time is None: return None
        return datetime.strptime(self.cinema_start_time, "%H:%M")

    @property
    def _end_time(self):
        if self.cinema_end_time is None: return None
        return datetime.strptime(self.cinema_end_time, "%H:%M")

    @property
    def final_price(self):
        if self.original_price is None: return None
        return self.original_price * (100 - self.discount)/100

    @property
    def movie_time(self):
        if self._start_time is None and self._end_time is None: return None
        duration = self._end_time - self._start_time
        minutes = int(duration.total_seconds() / 60)
        if minutes < 0:
            minutes += 24 * 60
        return minutes


class MovieManager:
    def __init__(self):
        self.movies = []

    def __str__(self):
        information = []
        for movie in self.movies:
            information.append(str(movie))
        return '\n'.join(information)

    def find_movie(self, movie_code):
        for movie in self.movies:
            if movie.movie_code == movie_code:
                return movie
        raise ValueError ("Error From MovieManager: Movie not found (find_movie)")

    def add_movie(self,movie_code,movie_name,cinema_number,cinema_start_time,cinema_end_time,date,original_price,discount):
        if self.repeat_code_check(movie_code): raise ValueError("Error From class MovieManager: Movie Code Already Exists")
        self.movies.append(
            Movie(movie_code,movie_name,cinema_number,cinema_start_time,cinema_end_time,date,original_price,discount)
        )

    def remove_movie(self,movie_code):
        for movie in self.movies:
            if movie.movie_code == movie_code:
                self.movies.remove(movie)
                return True
        raise ValueError(f"Error From class MovieManager: Movie Code Not Found (remove_movie)")

    def update_movie(
            self,movie_code,movie_name=None,cinema_number=None,cinema_start_time=None,
            cinema_end_time=None,date=None,original_price=None,discount=None
    ):
            for index,movie in enumerate(self.movies):
                if movie.movie_code == movie_code:
                    if movie_name is not None: movie.movie_name = movie_name
                    if cinema_number is not None: movie.cinema_number = cinema_number
                    if cinema_start_time is not None: movie.cinema_start_time = cinema_start_time
                    if cinema_end_time is not None: movie.cinema_end_time = cinema_end_time
                    if date is not None: movie.date = date
                    if original_price is not None: movie.original_price = original_price
                    if discount is not None: movie.discount = discount

    def repeat_code_check(self,movie_code):
        for movie in self.movies:
            if movie.movie_code == movie_code:
                return True
        return False

# if __name__ == "__main__":
#     movie = Movie(
#         'M001','Joker','0001','18:00','20:00',
#                   '2025/01/12','30','25'
#     )
#     print(movie)


