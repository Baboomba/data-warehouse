from config import DATA_DIR
from data.database import DBConnection
from data.query import QuerySet
import math
import os
import pandas as pd
from pandas import DataFrame


class DevideCloseFile:
    '''
    오라클에서 추출한 csv 파일을 정산년도에 따라 나누는 코드
    Parameter
    ---
    date >> '2024-01-01' 파일명에 들어가는 이름
    '''
    def __init__(self, date: str, promotion: bool=False):
        self.date = date.replace('-', '')
        self.data = self.read()
        self.data_dic = {}
        self.result(promotion)
    
    def read(self):
        files = os.listdir(DATA_DIR['extracted'])
        return pd.read_csv(fr'{DATA_DIR["extracted"]}\{files[0]}', delimiter=',')
    
    def select_promotion(self, promotion: bool):
        if promotion:
            self.data = self.data[self.data['유무상 구분'] == '무상']
        return self

    def devide_data(self):
        self.data_dic['2020'] = self.data[self.data['정산년도'] == 2020]
        self.data_dic['2021'] = self.data[self.data['정산년도'] == 2021]
        self.data_dic['2022_2023'] = self.data[self.data['정산년도'].isin([2022, 2023])]
        return self
    
    def to_csv(self):
        for key, data in self.data_dic.items():
            size = len(data)
            limit = size / 1000000
            limit = math.ceil(limit)
            
            for idx in range(limit):
                temp = data.iloc[idx * 1000000 : (idx + 1) * 1000000, :]
                temp.to_csv(fr'result\{self.date}_CLOSE_SCP_{key}_{idx}.csv', encoding='euc-kr', index=False)
    
    def result(self, promotion):
        self.select_promotion(promotion)\
            .devide_data()\
            .to_csv()


class Extraction:
    def __init__(self):
        pass
    
    @staticmethod
    def get_sales_performance(start: str=None) -> DataFrame:
        query = QuerySet.sales_performance(start)
        db = DBConnection()
        return db.execute_query(query)
    
    @staticmethod
    def get_techno_performance(start: str=None) -> DataFrame:
        query = QuerySet.technomart_performance(start)
        db = DBConnection()
        return db.execute_query(query)
    
    @staticmethod
    def get_member_list(end_date: str=None) -> DataFrame:
        query = QuerySet.member_list(end_date)
        db = DBConnection()
        return db.execute_query(query)
    
    @staticmethod
    def get_member_close(end_date: str=None) -> DataFrame:
        query = QuerySet.member_close(end_date)
        db = DBConnection()
        return db.execute_query(query)
    
    @staticmethod
    def get_claim(end_date: str=None) -> DataFrame:
        query = QuerySet.claim(end_date)
        db = DBConnection()
        return db.execute_query(query)