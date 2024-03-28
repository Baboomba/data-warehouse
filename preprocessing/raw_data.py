from config import DATA_DIR, DATA_PATH
from data.columns import insurance_schema
from datetime import datetime
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pyxlsb import open_workbook
import os


class MemberData:
    def __init__(self, close: bool=False):
        MemberData.MergeFiles(close)
    
    class MergeFiles:
        def __init__(self, close: bool=False):
            self.close = close
            self.files = self.list_files()
            self.dataframe = []
            self.size = []
            self.diff = 0
            self.produce_result()
        
        def list_files(self):
            if self.close:
                return os.listdir(DATA_DIR['member_close'])
            else:
                return os.listdir(DATA_DIR['member_list'])
        
        def read_xlsb(self):
            if self.close:
                dir = DATA_DIR['member_close']
            else:
                dir = DATA_DIR['member_list']
            
            for _, file in enumerate(self.files):
                path = fr'{dir}\{file}'
                
                with open_workbook(path) as wb:
                    for sht in wb.sheets:
                        data = []
                        with wb.get_sheet(sht) as sheet:
                            for row in sheet.rows():
                                row_data = [cell.v for cell in row]
                                data.append(row_data)
                                
                            columns = data[0]
                            data = data[1:]
                            temp = pd.DataFrame(data=data, columns=columns)
                            self.dataframe.append(temp)
                            self.size.append(int(temp.shape[0]))
            return self
        
        def read_csv(self):
            if self.close:
                dir = DATA_DIR['member_close']
            else:
                dir = DATA_DIR['member_list']
            
            for num, file in enumerate(self.files):
                df = pd.read_csv(fr'{dir}\{file}')
                self.dataframe.append(df)
                self.size.append(int(df.shape[0]))
                print(f'가입자 파일 {num}번 생성')
                print(f'가입자 파일 {num}번 파일 크기 : {df.shape[0]}')
            return self
        
        def concat(self):
            self.dataframe = pd.concat(self.dataframe).reset_index(drop=True)
            return self
        
        def alter_type(self):
            self.dataframe['IMEI'] = self.dataframe['IMEI'].astype(str)
            return self
        
        def delete_test_user(self):
            if self.close:
                return self
            
            condition = self.dataframe['이름'].isin(['테스트'])
            index = self.dataframe[condition].index
            self.dataframe.drop(index=index, inplace=True)
            self.diff = len(index)
            return self
        
        def verify_sum(self):
            if (sum(self.size) - self.diff) != int(self.dataframe.shape[0]):
                raise ValueError('The size after processing has been different.')
            return self
        
        def adjust_date_format(self):
            if self.close:
                self.dataframe['보험가입일'] = pd.to_datetime(self.dataframe['보험가입일'], origin='1899-12-30', unit='D')
                self.dataframe['보험해지일'] = pd.to_datetime(self.dataframe['보험해지일'], origin='1899-12-30', unit='D')
                self.dataframe['무상 종료일'] = pd.to_datetime(self.dataframe['무상 종료일'], origin='1899-12-30', unit='D')
            elif ~self.close:
                self.dataframe['START_DATE'] = pd.to_datetime(self.dataframe['START_DATE'], origin='1899-12-30', unit='D').dt.strftime('%Y-%m-%d')
            return self
        
        def save(self):
            if self.close:
                self.dataframe.to_parquet(DATA_PATH['member_close'])
            else:
                self.dataframe.to_parquet(DATA_PATH['member_list'])
        
        def produce_result(self):
            self.read_xlsb().\
                concat().\
                alter_type().\
                delete_test_user().\
                verify_sum().\
                adjust_date_format().\
                save()
 
    def count_folable5(self) -> None:
        df = pd.read_excel(r'data\raw_data\etc\폴더블5가입자.xlsx')
        df.to_parquet(r'data\table\folable_join.parquet')


class ExternalRawData:
    def __init__(self):
        pass
        
    class SamsungClose:
        def __init__(self, to_excel: bool=False, add_to_pre: bool=False, save: bool=False):
            self.files = self.read_files()
            self.dataframe = []
            self.result(to_excel, add_to_pre, save)
        
        def read_files(self):
            return os.listdir(DATA_DIR['samsung'])
        
        def to_dataframe(self):
            try:
                for num, file in enumerate(self.files):
                    file_path = fr'{DATA_DIR["samsung"]}\{file}'
                    with pd.ExcelFile(file_path) as xl:
                        print(f'the {num}th file of the raw data of Samsung has just been read.')
                        sheet_names = xl.sheet_names
                        
                        for name in sheet_names:
                            df = xl.parse(sheet_name=name, skiprows=1)
                            self.dataframe.append(df)
                        print(f'The dataframe of the {num}th file created')
            except Exception as e:
                print(e)
            return self
        
        def concat(self):
            self.dataframe = pd.concat(self.dataframe)
            return self
        
        def to_excel(self, to_excel: bool):
            if to_excel:
                now = datetime.now().strftime('%Y%m%d')
                self.dataframe.to_excel(fr'result\SC+ 무선데이터_{now}.xlsx')
                print('삼성 데이터 엑셀 저장 완료')
            return self
        
        def add_to_previous(self, add_to_pre: bool):
            if add_to_pre:
                pre = pd.read_parquet(DATA_PATH['samsung_raw'], engine='pyarrow')
                self.dataframe = pd.concat([pre, self.dataframe])
                self.dataframe.drop_duplicates(inplace=True)
                self.dataframe.reset_index(drop=True, inplace=True)
            return self
        
        def save(self, save: bool):
            self.dataframe.to_parquet(DATA_PATH['samsung_raw'])
            
        def result(self, to_excel: bool, add_to_pre: bool, save: bool):
            self.to_dataframe().concat().to_excel(to_excel).add_to_previous(add_to_pre).save(save)

    class TossClose:
        def __init__(self, add_to_pre: bool=False, align: bool=False, save: bool=False):
            self.dataframe = self.read_data()
            self.result(add_to_pre, align, save)
        
        def read_data(self):
            file = os.listdir(DATA_DIR['toss'])
            return pd.read_excel(fr'{DATA_DIR["toss"]}\{file[0]}')
        
        def add_to_previous(self, add_to_previous):
            if add_to_previous:
                pre = pd.read_parquet(DATA_PATH['toss_raw'])
                self.dataframe = pd.concat([pre, self.dataframe])
            return self
        
        def align(self, align: bool=False):
            if align:
                self.dataframe.drop_duplicates(inplace=True)
                self.dataframe.reset_index(drop=True, inplace=True)
            return self
        
        def save(self, save: bool=False):
            if save:
                self.dataframe.to_parquet(DATA_PATH['toss_raw'])
        
        def result(self, add_to_previous, align, save):
            self.add_to_previous(add_to_previous).align(align).save(save)
    
    class MergedCloseData:
        __col = [
            '매출일',
            '결제상태',
            '주문번호',
            'PRODUCT_ID',
            'POLICY_ID'
        ]
        
        def __init__(self, save: bool=False, add_to_pre: bool=False):
            self.dataframe = self.merge()
            self.result(save, add_to_pre)
        
        def read_toss(self):
            return pd.read_parquet(DATA_PATH['toss_raw'], engine='pyarrow')[['매출일', '주문번호', '결제상태']]
        
        def read_samsung(self):
            return pd.read_parquet(DATA_PATH['samsung_raw'], engine='pyarrow')[['POLICY_ID', 'PAYMENT_ID', 'PRODUCT_ID']]
        
        def merge(self):
            ss = self.read_samsung()
            ts = self.read_toss()
            return pd.merge(ts, ss, left_on='주문번호', right_on='PAYMENT_ID', how='left')
        
        def adjust(self, drop: bool):
            if drop:
                self.dataframe.drop(columns='PAYMENT_ID', inplace=True)
            
            self.dataframe.drop_duplicates(inplace=True)
            self.dataframe.reset_index(drop=True, inplace=True)
            return self
        
        def format_date(self):
            self.dataframe['매출일'] = pd.to_datetime(self.dataframe['매출일'], format='%Y-%m-%d')
            return self
        
        def select_columns(self):
            self.dataframe = self.dataframe[self.__col]
            return self
        
        def add_to_previous(self, add_to_previous: bool):
            if add_to_previous:
                pre = pd.read_parquet(DATA_PATH['toss_payment'])
                self.dataframe = pd.concat([pre, self.dataframe])
            return self
        
        def save(self, save: bool):
            if save:
                self.dataframe.to_parquet(DATA_PATH['toss_payment'])
        
        def result(self, save, add_to_pre):
            self.adjust(True).format_date().select_columns().add_to_previous(add_to_pre).adjust(False).save(save)
       
    class Insurance:
        '''
        보험금공지 데이터 처리
        
        Parameter
        ---
        run : True 설정 시, 실행과 저장 동시 수행
        '''
        def __init__(self):
            self.path = DATA_PATH['insurance']
            self.dir = DATA_DIR['insurance']
            self.insurance_notice()
        
        def read_insurance(self):
            return pq.read_table(self.path)
        
        def process_insurance_data(self):
            files = os.listdir(self.dir)
            
            for file in files:
                if '.csv' in file:
                    df = pd.read_csv(fr'{self.dir}\{file}')
                    df['처리형태'] = df['처리형태'].astype(str)
                    df['기준'] = pd.to_datetime(df['기준'])
                    df['접수 날짜'] = pd.to_datetime(df['접수 날짜'])
                    df['무상 종료일'] = pd.to_datetime(df['무상 종료일'])
            return pa.Table.from_pandas(df, schema=insurance_schema)
        
        def concat_ins_files(self):
            table = self.process_insurance_data()
            table_pre = self.read_insurance()
            print('보험금 공지 데이터 병합 완료')
            return pa.concat_tables([table_pre, table])
        
        def save_concat(self) -> None:
            table = self.concat_ins_files()
            pq.write_table(table, self.path)
            print('보험금 공지 데이터 저장 완료')
            
        def insurance_notice(self):
            self.save_concat()
        