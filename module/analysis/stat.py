from config import DATA_PATH
import numpy as np
import pandas as pd
from datetime import datetime




class HoldingPeriod:
    '''
    제품별 유지기간 집계
    '''
    def __init__(self, path_list: list, fill_nan: bool=False, file_num: int=0):
        self.files = self.load_files(path_list)
        self.fill_nan_date(fill_nan, file_num)
    
    def load_files(self, path_list: list):
        '''
        읽을 파일 리스트를 인풋
        
        데이터프레임 리스트를 반환
        '''
        empty = []
        for path in path_list:
            df = pd.read_parquet(path, engine='pyarrow')
            empty.append(df)
        return empty
    
    def fill_nan_date(self, fill_nan: bool, file_num):
        '''
        해지일이 없는 값을 현재 시점으로 채움
        
        날짜 타입을 datetime 객체로 변환
        
        fill_nan
        ---
        빈 값을 채우는 옵션(불리언)
        
        file_num
        ---
        생성자로 로드된 데이터프레임 리스트의 인덱스
        '''
        if fill_nan:
            today = datetime.today()
            self.files[file_num]['보험해지일'][self.files[file_num]['보험해지일'].isna()] = today
            self.files[file_num]['보험가입일'] = pd.to_datetime(self.files[file_num]['보험가입일'])
            self.files[file_num]['보험해지일'] = pd.to_datetime(self.files[file_num]['보험해지일'])
        else:
            pass
    
    def add_holding_period(self, file_num: int, day: bool, month: bool):
        if day:
            self.files[file_num]['유지 기간'] = (self.files[file_num]['보험해지일'] - self.files[file_num]['보험가입일']).dt.days
        if month:
            self.files[file_num]['유지 개월'] = (self.files[file_num]['보험해지일'].dt.year - self.files[file_num]['보험가입일'].dt.year) * 12 + (self.files[file_num]['보험해지일'].dt.month - self.files[file_num]['보험가입일'].dt.month)
            

class JoinCloseRate:
    member_columns = ['상품정보', '보험가입일', '보험해지일']
    cate_columns = ['상품정보', '제품군', '유무상']
    member_table_path = DATA_PATH['member_list']
    cate_table_path = DATA_PATH['program_category']
    
    def __init__(self, save: bool):
        self.data = pd.read_parquet(self.member_table_path)[self.member_columns]
        self.result = self.collect_results()
        self.save = self.save_result(save)
    
    def reduce_columns(self):
        self.data = self.data[self.member_columns]
        return self
    
    def type_transform(self):
        self.data['보험가입일'] = pd.to_datetime(self.data['보험가입일']).dt.to_period('M')
        self.data['보험해지일'] = pd.to_datetime(self.data['보험해지일']).dt.to_period('M')
        return self
    
    def processing_category_table(self):
        cate = pd.read_parquet(self.cate_table_path)
        cate = cate[self.cate_columns]
        condition = (cate['제품군'] == '스마트폰')
        cate['제품군'] = np.where(condition, '스마트폰', '기타')
        return cate
    
    def merge_category(self):
        cate = self.processing_category_table()
        self.data = pd.merge(self.data, cate, on='상품정보', how='left')
        return self
    
    def filter_paid_product(self):
        self.data = self.data[self.data['유무상'] == '유상']
        return self
    
    def extract_join(self):
        join = self.data.groupby(['보험가입일', '제품군'])['상품정보'].count().reset_index()
        join.rename(columns={'상품정보': '가입'}, inplace=True)
        join['가입 연도'] = join['보험가입일'].dt.year
        join['가입 월'] = join['보험가입일'].dt.month
        return join
    
    def extract_close(self):
        close = self.data.groupby(['보험가입일', '보험해지일', '제품군'])['상품정보'].count().reset_index()
        close.rename(columns={'상품정보': '해지'}, inplace=True)
        close['가입 연도'] = close['보험가입일'].dt.year
        close['가입 월'] = close['보험가입일'].dt.month
        close['해지 연도'] = close['보험해지일'].dt.year
        close['해지 월'] = close['보험해지일'].dt.month
        return close
    
    def collect_results(self) -> dict:
        dic = {}
        self.reduce_columns().type_transform().merge_category().filter_paid_product()
        dic['가입'] = self.extract_join()
        dic['해지'] = self.extract_close()
        return dic
    
    def save_result(self, save: bool):
        if save:
            now = datetime.now().strftime('%Y%m%d')
            path = fr'result\가입해지율_{now}.xlsx'
            
            with pd.ExcelWriter(path) as writer:
                self.result['가입'].to_excel(writer, sheet_name='가입건', index=False)
                self.result['해지'].to_excel(writer, sheet_name='해지건', index=False)