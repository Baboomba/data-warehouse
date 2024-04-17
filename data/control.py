from config import DATA_PATH, BACKUP
from data.database import DBConnection
from data.query import QuerySet
import numpy as np
import os
import pandas as pd
import shutil
from typing import Dict, Any, List


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
        return os.path.join(BACKUP[self.file_name], self.save_name)
    
    def copy(self):
        original_path = DATA_PATH[self.file_name]
        backup_path = self.create_destination()
        
        try:
            shutil.copy(original_path, backup_path)
        except FileNotFoundError as e:
            print(e)
            

class UpdateProgramCategory(DBConnection):
    '''
    program_info 테이블 신규 PID 추가될 경우, program_category를 업데이트 시킴
    
    Parameter
    ---
    pid_list : pid와 적용 제품군에 대한 딕셔너리
    
    >>> pid_dict = {'KOR123456': 'S24'}
    '''
    
    def __init__(self, pid_dict: Dict[str, str], save: bool=False) -> None:
        super().__init__()
        self.pid_list = pid_dict
        self._query = QuerySet.program_info()
        self._result(save)
    
    def set_value(
            self,
            pid: str | List[str]=None,
            column: str | List[str]=None,
            value: Any=None
        ) -> 'UpdateProgramCategory':
        '''
        특정 컬럼의 값을 지정함
        ---
        Parameter
        
        column : 값을 변경하고자 하는 컬럼명
        
        value : 변경하고자 하는 값(문자열, 수치 등)
        '''
        if isinstance(pid, List) and isinstance(column, List):
            for __pid, __column in zip(pid, column):
                if __column not in self.data.columns:
                    raise self.logger.exception(f'there is no such columns {column}')
                
                self.data.loc[self.data['상품정보'] == __pid, __column] = value
            return self
        
        if column not in self.data.columns:
            raise self.logger.exception(f'there is no such a column {column}')
        
        self.data.loc[self.data['상품정보'] == pid, column] = value
        return self
    
    def _execute_query(self) -> 'UpdateProgramCategory':
        self.data = self.execute_query(self._query)
        return self
    
    def _select_columns(self) -> 'UpdateProgramCategory':
        cols = [
           'PROGRAM_CODE',
           'PROGRAM_NAME',
           'CATE_SECOND',
           'BATTERY_COUNT',
           'PROMOTION_YN'
        ]
        self.data = self.data[cols]
        self.logger.write_info('the columns of the original data changed : ["PROGRAM_CODE", "PROGRAM_NAME", "CATE_SECOND", "BATTERY_COUNT", "PROMOTION_YN"]')
        return self
    
    def _rename_columns(self) -> 'UpdateProgramCategory':
        name = {
            'PROGRAM_CODE':'상품정보',
            'PROGRAM_NAME':'상품명',
            'CATE_SECOND':'제품군',
            'PROMOTION_YN':'유무상'
        }
        self.data.rename(columns=name, inplace=True)
        self.logger.write_info('column names changed into Korean')
        return self
    
    def _create_columns(self) -> 'UpdateProgramCategory':
        self.data['제품군_2'] = None
        self.data['제품시리즈'] = None
        self.data['제품시리즈_2'] = None
        self.data['보장타입'] = None
        self.data['케이스구독형'] = False
        self.logger.write_info('6 of empty columns created ["제품군_2", "제품시리즈", "제품시리즈_2", "보장타입", "케이스구독형"]')
        return self
    
    def _select_records(self) -> 'UpdateProgramCategory':
        # 파라미터로 넣은 PID에 해당하는 레코드만 선별
        self.data = self.data[self.data['상품정보'].isin(self.pid_list)]
        self.logger.write_info('the records has been selected by pid_list you input as parameter')
        return self
    
    def _read_program_category(self) -> 'UpdateProgramCategory':
        self._category = pd.read_parquet(DATA_PATH['program_category'])
        self.logger.write_info('the file, program_category read successfully')
        return self
    
    def _concatenate_data(self) -> 'UpdateProgramCategory':
        self.data = pd.concat([
            self._category,
            self.data
        ])
        self.logger.write_info('two of data, program_info, and program_category concatenated successfully')
        return self
    
    def _set_product_series2(self) -> 'UpdateProgramCategory':
        for key, value in self.pid_list.items():
            self.data.loc[self.data['상품정보'] == key, '제품시리즈_2'] = value
        
        self.logger.write_info('the value of the column, 제품시리즈_2 saved successfully')
        return self
    
    def _change_promotion_value(self) -> 'UpdateProgramCategory':
        choice = [
            self.data['유무상'] == 'Y',
            self.data['유무상'] == 'N'
        ]
        values = [
            '무상',
            '유상'
        ]
        self.data['유무상'] = np.select(choice, values, 'error')
        self.logger.write_info('the values of the column, 유무상 set successfully')
        return self
    
    def _set_warranty_type(self) -> 'UpdateProgramCategory':
        cond1 = (self.data['BATTERY_COUNT'] != -1)
        self.data['보장타입'] = np.where(cond1, '종합형', '파손보장형')
        
        cond2 = (self.data['제품군'] != '스마트폰')
        self.data['보장타입'] = np.where(cond2, '기타', self.data['보장타입'])
        self.logger.write_info('the value of the column, 보장타입 set successfully')
        return self
    
    def _save_data(self) -> None:
        self.data.to_parquet(DATA_PATH['program_category'])
        self.logger.write_info('program category data saved successfully')
    
    def _result(self, save: bool) -> None:
        self._execute_query().\
        _select_columns().\
        _rename_columns().\
        _create_columns().\
        _select_records().\
        _read_program_category().\
        _concatenate_data().\
        _set_product_series2().\
        _change_promotion_value().\
        _set_warranty_type()
        
        self.logger.write_info('operation ended completely')
        
        if save:
            self._save_data()
        else:
            self.logger.write_info('program info data has not been saved by the parameter option')