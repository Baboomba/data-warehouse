from config import DATA_PATH, BACK_UP
import configparser
from data.database import DBConnection
from data.query import QuerySet
import numpy as np
import os
import pandas as pd
from pandas import DataFrame
import shutil
from typing import Dict, Any, List
# from util.config_reader import DATA_PATH, BACK_UP


class BackUp:
    '''
    Parameter
    ---
    
    file_name >>> refers the keys of DATA_PATH and BACKUP dictionary
    
    close_date >>> in the form like 20231030
    '''
    def __init__(self, file_name: str, close_date: str) -> None:
        self.file_name = file_name
        self.close_date = close_date
        self.save_name = self.destination_name()
        self.copy()
            
    def destination_name(self):
        return f'{self.file_name}_{self.close_date}.parquet'
    
    def create_destination(self):
        # return os.path.join(BACK_UP(self.file_name), self.save_name)
        return os.path.join(BACK_UP[self.file_name], self.save_name)
    
    def copy(self):
        # original_path = DATA_PATH(self.file_name)
        original_path = DATA_PATH[self.file_name]
        backup_path = self.create_destination()
        
        try:
            shutil.copy(original_path, backup_path)
        except FileNotFoundError as e:
            print(e)


# class TableControl(DBConnection):
#     '''
#     특정 테이블에 대해 업데이트를 실행하는 클래스
#     ini 파일 조작을 기초로 하기 때문에 config.py 파일 사용할 경우 활용하기 어려움
#     Parameter
#     ---
#     table_name : config 파일 DATA_PATH에 등록된 테이블
#     '''
#     _config_path = r'config.ini'
#     _path_section = 'DATA_PATH'
    
#     def __init__(self, table_name: str=None) -> None:
#         super().__init__()
#         self.data = self._read_data(table_name)
#         self._config = configparser.ConfigParser()
#         self._path_value = fr'data\table\{table_name}.parquet'
    
#     def _read_data(self, table_name: str=None) -> DataFrame:
#         if table_name in self._config.options(self._path_section):
#             raise self._logger.exception('there is no such table')
        
#         df = pd.read_parquet(DATA_PATH(table_name))
#         self._logger.write_info('table has been read')
#         return df
    
#     def create(
#             self,
#             data: DataFrame=None,
#             table_name: str=None
#         ) -> None:
#         self._add_path(table_name)
        
#         data.to_parquet(DATA_PATH(table_name))
#         self._logger.write_info(f'table named {table_name} created')
        
#     def _add_path(
#             self,
#             table_name: str=None
#         ) -> None:
#         if self._config.has_option(self._path_section, table_name):
#             raise self._logger.exception('there exists the same table name')
#         else:
#             self._config.read(self._config_path)
#             self._config[self._path_section][f'{table_name}'] = self._path_value

#             with open(self._config_path, 'w') as configfile:
#                 self._config.write(configfile)
            
#             self._logger.write_info(f'added a new section {table_name} to config file')
    
#     def update(
#             self,
#             index: Any=None,
#             column: str=None,
#             value: Any=None
#         ) -> 'TableControl':
#         try:
#             self.data.iloc[index, column] = value
#             self._logger.write_info('data updated successfully')
#         except Exception as e:
#             self._logger.exception(e)
#         return self
    
#     def insert(self):
#         pass
    
#     def delete(self):
#         pass
            

class ProgramCategoryTable(DBConnection):
    '''
    program_info 테이블에 내용이 변경될 때 program_category 테이블을 변경하기 위한 클래스
    
    Method
    ---
    insert : 신규 상품을 추가함. insert 메서드 주석 참조
    
    update : 기존 데이터를 수정함. update 메서드 주석 참조
    '''
    
    def __init__(self) -> None:
        super().__init__()
        self._query = QuerySet.program_info()
        # self.data = pd.read_parquet(DATA_PATH('program_category'))
        self.data = pd.read_parquet(DATA_PATH['program_category'])
    
    def update(
            self,
            pid: str | List[str]=None,
            column: str | List[str]=None,
            value: Any | List[Any]=None,
            save: bool=False
        ) -> 'ProgramCategoryTable':
        '''
        특정 컬럼의 값을 지정함.
        pid, column, value 파라미터의 타입과 크기는 같아야 함
        ---
        Parameter
        
        pid : 변경하고자 하는 pid(문자열 혹은 리스트)
        
        column : 값을 변경하고자 하는 컬럼명(문자열 혹은 리스트)
        
        value : 변경하고자 하는 값(문자열, 수치 등)
        
        save : 저장 여부
        '''
        if isinstance(pid, List) and isinstance(column, List):
            for __pid, __column in zip(pid, column):
                if __column not in self.data.columns:
                    raise self._logger.exception(f'there is no such columns {column}')
                
                self.data.loc[self.data['상품정보'] == __pid, __column] = value
            return self
        
        if column not in self.data.columns:
            raise self._logger.exception(f'there is no such a column {column}')
        
        self.data.loc[self.data['상품정보'] == pid, column] = value
        self._logger.write_info('data input updated')
        
        if save:
            self._save_data()
        else:
            self._logger.write_info('program info data has not been saved by the parameter option')

        return self
    
    def insert(self,
               pid: Dict[str, str]=None,
               save: bool=False
        ) -> None:
        '''
        신규 상품 추가를 위한 메서드
        
        Parameter
        ---
        pid : 신규로 유입되는 상품과 제품시리즈로 된 딕셔너리
        
        >>> pid = {'KORPRD20200710000760': 'S24'}
        '''
        self.pid = pid
        self._execute_query().\
        _select_columns().\
        _rename_columns().\
        _create_columns().\
        _select_records().\
        _read_program_category().\
        _concatenate_data().\
        _set_product_series2().\
        _change_promotion_value().\
        _set_warranty_type().\
        _drop_column().\
        _order_index()
        
        self._logger.write_info('insert ended completely')
        
        if save:
            self._save_data()
        else:
            self._logger.write_info('program info data has not been saved by the parameter option')
    
    def _execute_query(self) -> 'ProgramCategoryTable':
        self.data = self.execute_query(self._query)
        return self
    
    def _select_columns(self) -> 'ProgramCategoryTable':
        cols = [
           'PROGRAM_CODE',
           'PROGRAM_NAME',
           'CATE_SECOND',
           'BATTERY_COUNT',
           'PROMOTION_YN'
        ]
        self.data = self.data[cols]
        self._logger.write_info('the columns of the original data changed : ["PROGRAM_CODE", "PROGRAM_NAME", "CATE_SECOND", "BATTERY_COUNT", "PROMOTION_YN"]')
        return self
    
    def _rename_columns(self) -> 'ProgramCategoryTable':
        name = {
            'PROGRAM_CODE':'상품정보',
            'PROGRAM_NAME':'상품명',
            'CATE_SECOND':'제품군',
            'PROMOTION_YN':'유무상'
        }
        self.data.rename(columns=name, inplace=True)
        self._logger.write_info('column names changed into Korean')
        return self
    
    def _create_columns(self) -> 'ProgramCategoryTable':
        self.data['제품군_2'] = None
        self.data['제품시리즈'] = None
        self.data['제품시리즈_2'] = None
        self.data['보장타입'] = None
        self.data['케이스구독형'] = False
        self._logger.write_info('6 of empty columns created ["제품군_2", "제품시리즈", "제품시리즈_2", "보장타입", "케이스구독형"]')
        return self
    
    def _select_records(self) -> 'ProgramCategoryTable':
        # 파라미터로 넣은 PID에 해당하는 레코드만 선별
        self.data = self.data[self.data['상품정보'].isin(list(self.pid.keys()))]
        self._logger.write_info('the records has been selected by pid you input as parameter')
        return self
    
    def _read_program_category(self) -> 'ProgramCategoryTable':
        self._category = pd.read_parquet(DATA_PATH['program_category'])
        self._logger.write_info('the file, program_category read successfully')
        return self
    
    def _concatenate_data(self) -> 'ProgramCategoryTable':
        self.data = pd.concat([
            self._category,
            self.data
        ])
        self._logger.write_info('two of data, program_info, and program_category concatenated successfully')
        return self
    
    def _set_product_series2(self) -> 'ProgramCategoryTable':
        for key, value in self.pid.items():
            self.data.loc[self.data['상품정보'] == key, '제품시리즈_2'] = value
        
        self._logger.write_info('the value of the column, 제품시리즈_2 saved successfully')
        return self
    
    def _change_promotion_value(self) -> 'ProgramCategoryTable':
        choice = [
            self.data['유무상'] == 'Y',
            self.data['유무상'] == 'N'
        ]
        values = [
            '무상',
            '유상'
        ]
        self.data['유무상'] = np.select(choice, values, 'error')
        self._logger.write_info('the values of the column, 유무상 set successfully')
        return self
    
    def _set_warranty_type(self) -> 'ProgramCategoryTable':
        cond1 = (self.data['BATTERY_COUNT'] != -1)
        self.data['보장타입'] = np.where(cond1, '종합형', '파손보장형')
        
        cond2 = (self.data['제품군'] != '스마트폰')
        self.data['보장타입'] = np.where(cond2, '기타', self.data['보장타입'])
        self._logger.write_info('the value of the column, 보장타입 set successfully')
        return self
    
    def _drop_column(self) -> 'ProgramCategoryTable':
        self.data.drop(columns='BATTERY_COUNT', inplace=True)
        self._logger.write_info('battery_count column dropped')
        return self
    
    def _order_index(self) -> 'ProgramCategoryTable':
        self.data.reset_index(drop=True, inplace=True)
        return self
    
    def _save_data(self) -> None:
        self.data.to_parquet(DATA_PATH['program_category'])
        self._logger.write_info('program category data saved successfully')


class PIDUpdater(ProgramCategoryTable):
    
    cols = [
        'PROGRAM_CODE',
        'PROGRAM_NAME',
        'CATE_FIRST',
        'CATE_SECOND',
        'CATE_THIRD',
        'MONTHLY_PREMIUM',
        'LOST_COUNT',
        'REPAIR_COUNT',
        'BATTERY_COUNT',
        'ONSITE_COUNT',
        'LOST_DEDUCTIBLE',
        'REPAIR_DEDUCTIBLE',
        'BATTERY_DEDUCTIBLE',
        'ONSITE_DEDUCTIBLE',
        'PROMOTION_YN',
        'SHARE_SS',
        'SHARE_KB',
        'SHARE_HW',
        'SHARE_DB',
        'SHARE_CS',
        'PROMOTION_MONTH',
        'WARRANTY_MONTH',
        'START_DATE',
        'END_DATE',
        'EW_COUNT',
        'KAKAO_YN',
        'CLOSE_YEAR',
        'PROGRAM_DESC',
        'PROGRAM_FULL_NAME',
        'STG_PROGRAM_CODE',
        'PROMOTION_NAME',
    ]
    
    def __init__(self) -> None:
        super().__init__()
        self._info_query = QuerySet.program_info()
        self.info_data = self._read_info()
    
    def _read_info(self) -> DataFrame:
        return self.execute_query(self._info_query)[self.cols]
    
    def _drop_test_raws(self) -> None:
        index = [
            'KORSTG00000000000001',
            'KORSTG00000000000002',
            'KORSTG00000000000003'
        ]
        self.info_data = self.info_data[~self.info_data['PROGRAM_CODE'].isin(index)]
    
    def get_new_pid(self) -> str:
        self._drop_test_raws()
        col = '상품정보'
        self.info_data.rename(columns={'PROGRAM_CODE':col}, inplace=True)
        df = pd.concat([self.info_data[col], self.data[col]]).reset_index()
        df = df[~df[col].duplicated(keep=False)]
        self.info_data.rename(columns={col:'PROGRAM_CODE'}, inplace=True)
        
        if len(df) == 0:
            msg = 'There is no pid newly added'
            self._logger.write_info(msg)
            print(msg)
            return None
        
        pid = list(df[col].values)
        self._logger.write_info(f'new data found. PID : {pid}')
        return pid
    
    def update_category(
            self,
            pid_dict: Dict[str, str]=None,
            save: bool=None
        ) -> DataFrame:
        '''
        Parameter
        ---
        >>> pid_dict = {'KORSTG00000000000003':'S24'}
        '''
        self.insert(pid_dict, save)
        return self.data