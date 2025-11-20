import csv
from datetime import datetime
from abc import ABC, abstractmethod

class BaseManager(ABC):
    def __init__(self):
        self.datas = []

    def add(self,entity):
        if self.get(entity.primary_key): raise ValueError ("Error From class BaseManager: got same primary key in the Manager")
        self.datas.append(entity)

    def remove(self, data_code):
        for data in self.datas:
            if data.primary_key == data_code:
                self.datas.remove(data)
                return True
        return False

    def update(self, data_code, **kwargs):
        for data in self.datas:
            if data.primary_key != data_code: continue
            for key, value in kwargs.items():
                try:
                    if kwargs[key] is not None: setattr(data, key, value)
                except KeyError:
                    raise KeyError("Error From class BaseManager: kwargs got parameter that isn't exist in your Entity")
            return True
        return False

    def get(self, data_code):
        for data in self.datas:
            if data.primary_key == data_code:
                return data
        return None

class BaseEntity(ABC):
    @property
    @abstractmethod
    def primary_key(self):
        """
        这里需要继承的子类返回自己的主键
        """
        pass

    @abstractmethod
    def convert_to_list(self):
        """
        这里需要继承的子类把自己的数据转换为列表
        """
        pass


class Movie(BaseEntity):
    def __init__(self,movie_code,movie_name,cinema_number,cinema_start_time,cinema_end_time,date,original_price,discount):
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
    def primary_key(self):
        return self.movie_code

    @property
    def original_price(self):
        return self._original_price

    @property
    def discount(self):
        return self._discount

    @property
    def date(self):
        return self._date

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

    @original_price.setter
    def original_price(self, value):
        try:
            int(value)
        except ValueError:
            raise ValueError("Error From class Movie: Please enter numeric value")
        self._original_price = int(value)

    @discount.setter
    def discount(self, value):
        try:
            int(value)
        except ValueError:
            raise ValueError("Error From class Movie: Please enter numeric value")
        if int(value) > 100 or int(value) < 0:
            raise ValueError("Error From class Movie: discount must be between 0 and 100")
        self._discount = int(value)

    @date.setter
    def date(self, value):
        try:
            datetime.strptime(value, "%Y/%m/%d")
        except ValueError:
            raise ValueError("Error From class Movie: Invalid date (format YY/MM/DD)")
        except Exception as e:
            raise Exception(f"Unknown Error From class Movie: {e}")
        self._date = str(value)

    def convert_to_list(self):
        return [
            self.movie_code,self.movie_name,self.cinema_number,self.cinema_start_time,
            self.cinema_end_time,self.date,self.original_price,self.discount
        ]


class MovieManager(BaseManager):
    def __init__(self):
        super().__init__()

    def __str__(self):
        information = []
        for movie in self.datas:
            information.append(str(movie))
        return '\n\n'.join(information)

    def add_for_non_entity(self,movie_code, movie_name, cinema_number, cinema_start_time, cinema_end_time, date, original_price,
                   discount):
        movie = Movie(movie_code, movie_name, cinema_number, cinema_start_time, cinema_end_time, date, original_price,
                     discount)
        super().add(movie)

    def remove(self, movie_code):
        if super().remove(movie_code): return True
        raise ValueError(f"Error From class MovieManager: Movie Code Not Found (remove_movie)")

    def update(
            self,movie_code,movie_name=None,cinema_number=None,cinema_start_time=None,
            cinema_end_time=None,date=None,original_price=None,discount=None
    ):
        super().update(
            data_code=movie_code, movie_name=movie_name, cinema_number=cinema_number,
            cinema_start_time=cinema_start_time, cinema_end_time=cinema_end_time, original_price=original_price,
            discount=discount
        )

class FileManager:
    def __init__(self,file_path):
        self.file_path = file_path

    def write_to_csv(self,movies):
        with open(self.file_path,"w",newline="") as csv_file:
            writer = csv.writer(csv_file)
            for movie in movies:
                writer.writerow(movie.get_data_for_file())

if __name__ == "__main__":
     movie_all = MovieManager()
     movie_all.add_for_non_entity('M001', 'Joker', '0001', '18:00', '20:00',
                   '2025/01/12','30','25')
     movie_all.add_for_non_entity('M002', 'Joker', '0001', '18:00', '20:00',
                   '2025/01/12','30','25')
     print(movie_all)


