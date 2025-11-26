import csv
import pathlib
import inspect
from Entity import *
from Manager import *

class BaseFileHandler:
    def __init__(self,file_path):
        self.file_path = file_path
        if type(self) is BaseFileHandler: raise TypeError("BaseFileHandler cannot be instantiated")

    @property
    def file_path(self):
        return self._get_actual_path(self._file_path)

    @file_path.setter
    def file_path(self,value):
        with open(value,'a') as f:
            pass
        self._file_path = value

    @staticmethod
    def _get_actual_path(file_path):
        if pathlib.Path(file_path).is_file():
            return pathlib.Path(file_path).resolve()
        else: raise FileNotFoundError(f"Error From class BaseFileHandler: File({file_path} Not Found,function: get_actual_path")


    def write_to_csv(self,datas):
        with open(self.file_path,"w",newline="") as csv_file:
            writer = csv.writer(csv_file)
            for data in datas:
                writer.writerow(data)

    def append_to_csv(self, datas):
        with open(self.file_path,"a",newline="") as csv_file:
            writer = csv.writer(csv_file)
            for data in datas:
                writer.writerow(data)

    def get_from_csv(self):
        with open(self.file_path,"r",newline="") as csv_file:
            file_content = []
            reader = csv.reader(csv_file)
            for row in reader:
                file_content.append(row)
        return file_content

    def __delete_row_from_csv(self,row):
        original_data = self.get_from_csv()
        try:
            original_data.pop(row - 1)
        except IndexError:
            raise IndexError(f"Error From class FileHandler: Row({row}) is out of range, function: delete_row_from_csv")
        self.write_to_csv(original_data)

    def __update_row_from_csv(self,row,new_data):
        original_data = self.get_from_csv()
        try:
            original_data[row - 1] = new_data
        except IndexError:
            raise IndexError(f"Error From class FileHandler: Row({row}) is out of range, function: update_row_from_csv ")
        self.write_to_csv(original_data)

    def __clear_csv(self):
        with open(self.file_path,"w",newline="") as csv_file:
            pass



class ObjectFileHandler(BaseFileHandler):
    def __init__(self, file_path, entity_type : type[AbstractEntity]):
        super().__init__(file_path)
        self.entity_type = entity_type

    def __str__(self):
        return f"file_path: {self.file_path}\nentity_type: {self.entity_type}"

    def write_to_csv(self,object_list : list):
        data_to_write = []
        entity_sig = list(inspect.signature(self.entity_type.__init__).parameters.keys())
        entity_sig.remove('self')
        data_to_write.append(entity_sig)
        for row  in object_list:
            data_to_write.append(row.convert_to_list())
        super().write_to_csv(data_to_write)

    def get_from_csv(self):
        csv_data = super().get_from_csv()
        if not csv_data: return False
        header = csv_data.pop(0)
        entity_sig = list(inspect.signature(self.entity_type.__init__).parameters.keys())
        entity_sig.remove('self')
        if header != entity_sig: raise ValueError("Error From class ObjectFileHandler: Wrong header")
        return [self.entity_type.convert_to_object(csv_list) for csv_list in csv_data if csv_list]

