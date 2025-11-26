import inspect
from abc import ABC, abstractmethod
from datetime import datetime
from functools import cached_property


class AbstractEntity(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @property
    @abstractmethod
    def primary_key(self):
        """
        这里需要继承的子类返回自己的主键
        """
        pass

    @property
    @abstractmethod
    def header(self):
        """
        这里继承的子类需要在这个函数返回header （通常为子类创建时的参数）
        :return:
        """
        pass

    @property
    @abstractmethod
    def convert_to_list(self):
        """
        这里需要继承的子类能够返回一个列表（可以表达子类的）
        :return:
        """
        pass

    @classmethod
    @abstractmethod
    def convert_to_object(cls,list_to_convert):
        """
        这里需要继承的子类完成将list变回对象
        """
        pass

class AbstractEntity(AbstractEntity, ABC):

    @abstractmethod
    def __init__(self,*args,**kwargs):
        pass

    @property
    def header(self):
        entity_sig = list(inspect.signature(self.__init__).parameters.keys())
        entity_sig.remove('self')
        return entity_sig

    def convert_to_list(self):
        list_to_return = []
        for item in self.header:
            if not hasattr(self, item):
                raise AttributeError(f"The parameter {item} is not defined")
            try:
                list_to_return.append(getattr(self, str(item)))
            except AttributeError:
                raise AttributeError(f"The parameter {item} is defined in class {type(self).__name__},but no value")
        return list_to_return

    @classmethod
    def convert_to_object(cls, list_to_convert):
        return cls(*list_to_convert)



class MovieEntity(AbstractEntity):
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
        information.append(f"{"movie code" : <{20}}:{self.movie_code}")
        information.append(f"{"movie name" : <{20}}:{self.movie_name}")
        information.append(f"{"cinema number" : <{20}}:{self.cinema_number}")
        information.append(f"{"cinema start time" : <{20}}:{self.cinema_start_time}")
        information.append(f"{"cinema end time" : <{20}}:{self.cinema_end_time}")
        information.append(f"{"date" : <{20}}:{self.date}")
        information.append(f"{"original price" : <{20}}:{self.original_price}")
        information.append(f"{"discount" : <{20}}:{self.discount}")
        information.append(f"{"final price" : <{20}}:{self.final_price}")
        return "\n".join(information)

    def __repr__(self):
        information = []
        all_attributes = dir(self)
        for attribute in all_attributes:
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
            raise ValueError("Error From class Movie: Please enter numeric value, function: original_price setter")
        self._original_price = int(value)

    @discount.setter
    def discount(self, value):
        try:
            int(value)
        except ValueError:
            raise ValueError("Error From class Movie: Please enter numeric value, function: discount setter")
        if int(value) > 100 or int(value) < 0:
            raise ValueError("Error From class Movie: discount must be between 0 and 100, function: discount setter")
        self._discount = int(value)

    @date.setter
    def date(self, value):
        try:
            datetime.strptime(value, "%Y/%m/%d")
        except ValueError:
            raise ValueError("Error From class Movie: Invalid date (format YY/MM/DD), function: date setter")
        except Exception as e:
            raise Exception(f"Unknown Error From class Movie: {e}, function: date setter")
        self._date = str(value)

class UserEntity(AbstractEntity):


    def __init__(self,role,user_id,user_name,password):
        self.role = role
        self.user_id = user_id
        self.user_name = user_name
        self.password = password

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self,value):
        if value not in ['Technician','Manager','Clerk']: raise ValueError("Error From class UserEntity: Invalid role, function: role setter")
        self._role = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,value):
        capital_letters = 0
        small_letters = 0
        digits = 0
        special_characters = 0
        illegal_characters = 0
        for i in value:
            if i.isupper(): capital_letters += 1
            elif i.islower(): small_letters += 1
            elif i.isdecimal(): digits += 1
            elif i in ['!','@','#','$','%','^','&','*','(',')',';',':','"',"'",',','.','?','<','>','/','-','_','+','=']:
                special_characters += 1
            else: illegal_characters += 1
        if illegal_characters:     raise ValueError("Error From class UserEntity: illegal characters detected, function: password setter")
        if not capital_letters:    raise ValueError("Error From UserEntity: need capital letter, function: password setter")
        if not small_letters:      raise ValueError("Error From UserEntity: need small letter, function: password setter")
        if not digits:             raise ValueError("Error From UserEntity: need digit, function: password setter")
        if not special_characters: raise ValueError("Error From UserEntity: need special character, function: password setter")
        self._password = value

    @property
    def primary_key(self):
        return self.user_id

class CustomerEntity(UserEntity):

    def __init__(self,role,user_id,user_name,password,balance):
        super().__init__(role,user_id,user_name,password)
        self.balance = balance

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self,value):
        if value != 'Customer': raise ValueError("Error From CustomerEntity: Invalid role (It should be Customer Only), function: role setter")

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self,value):
        try:
            int(value)
        except ValueError:
            raise ValueError("Error From class CustomEntity: Balance must be interger")

        if int(value) < 0: raise ValueError("Error From class CustomEntity: Balance cannot be negative")
        self._balance = int(value)


