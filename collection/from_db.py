from config import DATA_DIR
import math
import os
import pandas as pd


class DevideCloseFile:
    def __init__(self, date: str):
        self.date = date
        self.data = self.read()
        self.data_dic = {}
        self.result()
    
    def read(self):
        files = os.listdir(DATA_DIR['extracted'])
        return pd.read_csv(fr'{DATA_DIR["extracted"]}\{files[0]}', delimiter=',')

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
                temp.to_csv(fr'result\{self.date}_SCP_{key}_{idx}.csv', encoding='euc-kr', index=False)
    
    def result(self):
        self.devide_data().to_csv()