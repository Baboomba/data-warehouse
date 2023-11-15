import numpy as np
import pandas as pd



class Update:
    
    def __init__(self, foreign_key: str, data_path: str):
        self.__foreign_key = foreign_key
        self.data_path = data_path
        self.data = pd.read_parquet(self.data_path)
        pass
    
    def get_foreign_key(self):
        pass
    
    def set_foreign_key(self):
        pass
    
    def update_one(self):
        pass
    
    def update_many(self):
        pass
    
    def update_all(self):
        pass


def update_table(function):
    
    def wrapper(*args, **kwargs):
        
        function(*args, **kwargs)
        
        