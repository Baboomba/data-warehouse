from config import DATA_DIR, DATA_PATH
from data.columns import insurance_schema
from datetime import datetime
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os
import shutil


def backup(func, path, save_name):
    def wrapper(*args, **kwargs):
        try:
            dst_path = os.path.join(DATA_DIR['backup'], save_name)
            shutil.copy(path, dst_path)
        except FileNotFoundError as e:
            print(e)
        func(*args, **kwargs)
    return wrapper


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
            
        def read_files(self):
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
                pass
            
            condition = self.dataframe['이름'].isin(['테스트'])
            index = self.dataframe[condition].index
            self.dataframe.drop(index=index, inplace=True)
            self.diff = len(index)
            return self
        
        def verify_sum(self):
            if (sum(self.size) - self.diff) != int(self.dataframe.shape[0]):
                raise ValueError('The size after processing has been different.')
            return self
        
        def save(self):
            if self.close:
                self.dataframe.to_parquet(DATA_PATH['member_close'])
            else:
                self.dataframe.to_parquet(DATA_PATH['member_list'])
        
        def produce_result(self):
            self.read_files().concat().alter_type().delete_test_user().verify_sum().save()
 
    def count_folable5(self) -> None:
        df = pd.read_excel(r'data\raw_data\etc\폴더블5가입자.xlsx')
        df.to_parquet(r'data\table\folable_join.parquet')


class ExternalRawData:
    def __init__(self):
        self.ts_table_path = DATA_PATH['toss_raw']
        self.ss_table_path = DATA_PATH['samsung_raw']
        self.ss_dir = DATA_DIR['samsung']
        self.ts_dir = DATA_DIR['toss']
        self.ins_dir = DATA_DIR['insurance']
        
    class SamsungClose:
        def __init__(self, to_excel: bool=False, add_to_pre: bool=False):
            self.files = self.read_files()
            self.dataframe = []
            self.result(to_excel, add_to_pre)
        
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
                result = pd.concat([pre, self.dataframe])
                result.drop_duplicates(inplace=True)
                result.reset_index(drop=True, inplace=True)
            
        def result(self, to_excel: bool, add_to_pre: bool):
            self.to_dataframe().concat().to_excel(to_excel).add_to_previous(add_to_pre)
    
    
       
    def samsung_close(self):
        '''
        삼성 데이터의 시트를 합침
        '''
        
        files = os.listdir(self.ss_dir)
        
        try:
            result = []
            
            for num, file in enumerate(files):
                file_path = fr'{self.ss_dir}\{file}'
                with pd.ExcelFile(file_path) as xl:
                    sheet_names = xl.sheet_names
                    print(f'삼성 {num}번 파일 로드')
                    
                    for name in sheet_names:
                        df = xl.parse(sheet_name=name, skiprows=1)
                        result.append(df)
                    print(f'삼성 {num}번 파일 데이터프레임 생성')
        except Exception as e:
            print(e)
        
        result = pd.concat(result)
        result.reset_index(inplace=True, drop=True)
        
        now = datetime.now().strftime('%Y%m%d')
        result.to_excel(fr'result\SC+ 무선데이터_{now}.xlsx')
        print('삼성 데이터 엑셀 저장 완료')
        
        pre = pd.read_parquet(self.ss_table_path, engine='pyarrow')
        result = pd.concat([pre, result])
        result.drop_duplicates(inplace=True)
        result.reset_index(drop=True, inplace=True)
        result.to_parquet(self.ss_table_path, engine='pyarrow')
        print('삼성 데이터 파일 변환 및 테이블 저장 완료')
        

    def toss_close(self):
        '''
        토스 데이터 결합
        '''
        files = os.listdir(self.ts_dir)
        df = pd.read_excel(fr'{self.ts_dir}\{files[0]}')
        
        pre = pd.read_parquet(self.ts_table_path, engine='pyarrow')
        print('토스 데이터 로드')
        
        df = pd.concat([pre, df])
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)

        df.to_parquet(self.ts_table_path, engine='pyarrow')
        print('토스 데이터 변환 및 저장 완료')


    def payment_merged(self):
        '''
        토스 결제 테이블 추가
        
        삼성/토스 데이터 모두 수집되었을 경우 실행
        '''
        col = [
            '매출일',
            '결제상태',
            '주문번호',
            'PRODUCT_ID',
            'POLICY_ID'
        ]
        print('삼성 데이터 불러오는 중...')
        ss = pd.read_parquet(DATA_PATH['samsung_raw'], engine='pyarrow')
        ss = ss[['POLICY_ID', 'PAYMENT_ID', 'PRODUCT_ID']]
        print('토스 데이터 불러오는 중...')
        ts = pd.read_parquet(DATA_PATH['toss_raw'], engine='pyarrow')
        ts = ts[['매출일', '주문번호', '결제상태']]
        
        print('삼성 / 토스 데이터 병합 중...')
        df = pd.merge(ts, ss, left_on='주문번호', right_on='PAYMENT_ID', how='left')
        df.drop(columns='PAYMENT_ID', inplace=True)
        df.drop_duplicates(inplace=True)
        df = df[col]
        return df
    
    
    class Insurance:
        '''
        보험금공지 데이터 처리
        
        Parameter
        ---
        execute : True 설정 시, 실행과 저장 동시 수행
        '''
        def __init__(self, run: bool):
            self.path = DATA_PATH['insurance']
            self.dir = DATA_DIR['insurance']
            self.insurance_notice(run)
        
        def read_insurance(self):
            return pq.read_table(self.path)
        
        def process_insurance_data(self):
            files = os.listdir(self.dir)
            df = None
            
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
            return pa.concat_tables([table, table_pre])
        
        def save_concat(self) -> None:
            table = self.concat_ins_files()
            pq.write_table(table, self.path)
            print('보험금 공지 데이터 저장 완료')
            
        def insurance_notice(self, run: bool):
            if run:
                self.save_concat()
        