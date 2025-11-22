from Entity import Movie, BaseEntity

import csv
from datetime import datetime
from abc import ABC, abstractmethod

class BaseManager:
    def __init__(self,entity_type : type[BaseEntity],entity_list : list[BaseEntity]):
        self.entity_type = entity_type
        self.datas = entity_list

    @property
    def datas(self):
        return self._datas

    @datas.setter
    def datas(self, value):
        if type(value) != list: raise TypeError("Error From class BaseManager: The value must be a list")
        self._datas = value
        for item in value:
            if type(item) != self.entity_type:
                raise TypeError("Error From class BaseManager: The item in the value must be of type object")
        self._datas = value

    def add(self):
        if self.exists(self.entity_type.primary_key): raise ValueError ("Error From class BaseManager: got same primary key in the Manager, function: add")
        self.datas.append(self.entity_type)

    def remove(self, data_code):
        for data_object in self.datas:
            if data_object.primary_key == data_code:
                self.datas.remove(data_object)
                return True
        return False

    def update(self, data_code, **kwargs):
        for data_object in self.datas:
            if data_object.primary_key != data_code: continue
            for key, value in kwargs.items():
                if value is None: continue
                if hasattr(data_object, key): setattr(data_object, key, value)
                else: raise KeyError("Error From class BaseManager: There is no key to match,check your parameter, function: update")
            return True
        return False

    def get(self, data_code):
        for data_object in self.datas:
            if data_object.primary_key == data_code:
                return data_object
        return None

    def exists(self,data_code):
        if self.get(data_code): return True
        return False



class MovieManager(BaseManager):
    def __init__(self,entity_list : list[BaseEntity]):
        super().__init__(entity_type= Movie,entity_list=  entity_list)

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
        raise ValueError(f"Error From class MovieManager: Movie Code Not Found, function: remove")

    def update(
            self,movie_code,movie_name=None,cinema_number=None,cinema_start_time=None,
            cinema_end_time=None,date=None,original_price=None,discount=None
    ):
        super().update(
            data_code=movie_code, movie_name=movie_name, cinema_number=cinema_number,
            cinema_start_time=cinema_start_time, cinema_end_time=cinema_end_time, original_price=original_price,
            discount=discount
        )

