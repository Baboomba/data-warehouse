from config import DATA_DIR, DATA_PATH
from data.columns import insurance_schema
from datetime import datetime
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os


def transform_data(dir, file_type: str='csv'):
    '''
    디렉토리에 있는 파일을 읽어 하나의 데이터프레임 변환하여 합침
    
    file_type : xlsx, csv
    '''
    files = os.listdir(dir)
    result = []
    
    for file in files:
        if file_type == 'csv':
            df = pd.read_csv(fr'{dir}\{file}')
        else:
            df = pd.read_excel(fr'{dir}\{file}')
        result.append(df)
    
    result = pd.concat(result)
    return result
        


class MemberData:
    def __init__(self):
        self.member_dir = DATA_DIR['member_list']
        self.member_path = DATA_PATH['member_list']
        self.member_close_dir = DATA_DIR['member_close']
        self.member_close_path = DATA_PATH['member_close']
    
    def concat_files(self, type_check: bool, close_file: bool):
        '''
        csv 파일을 하나로 합침
        
        Parameter
        ---
        type_check : 파일의 타입 일치 여부 확인
        
        close_file : 가입자 파일 혹은 마감 파일 여부 확인
        '''
        result = []
        row_size = []
        
        dir = self.member_dir
        path = self.member_path
        
        # 병합 파일 결정
        if close_file:
            dir = self.member_close_dir
            path = self.member_close_path
        
        files = os.listdir(dir)
        
        # 데이터 추출        
        for num, file in enumerate(files):
            df = pd.read_csv(fr'{dir}\{file}')
            df['IMEI'] = df['IMEI'].astype(str)
            result.append(df)
            row_size.append(df.shape[0])
            print(f'가입자 파일 {num}번 생성')
            print(f'가입자 파일 {num}번 파일 크기 : {df.shape[0]}')
        
        # 타입 체크
        if type_check:
            self.check_type_member_list(result)
        
        # 파일 병합
        print(f'병합 전 총 회원수 : {sum(row_size)}명')
        result = pd.concat(result)
        result.reset_index(drop=True, inplace=True)
        print(f'병합 후 총 회원수 : {result.shape[0]}명')
        
        # 테스트 유저 삭제
        if not close_file:
            index = result[result['이름'].isin(['테스트'])].index
            result.drop(index=index, inplace=True)
            print('테스트 유저 삭제')
        
        if close_file:
            if (sum(row_size)) == int(result.shape[0]):
                print('병합 후 가입자 수 이상 없음')
                result.to_parquet(path)
                print('가입자 파일 저장 완료')
            else:
                print('가입자 파일 병합 오류')
        else:
            if (sum(row_size) - 4) == int(result.shape[0]):
                print('병합 후 가입자 수 이상 없음')
                result.to_parquet(path)
                print('가입자 파일 저장 완료')
            else:
                print('가입자 파일 병합 오류')

    
    def check_type_member_list(self, df_list: list):
        '''
        가입자 파일 타입 검사
        
        데이터프레임으로 타입 검사 실행
        '''
        df_type = df_list[0].dtypes
        
        for num in range(1, len(df_list)):
            if df_type.equals(df_list[num].dtypes):
                print(f'가입자 {num}번 파일 타입 일치')
            else:
                print(f'ERROR!!! 가입자 {num}번 파일 타입 불일치!!!')

    def folable5_count(self) -> None:
        df = pd.read_excel(r'data\raw_data\etc\폴더블5가입자.xlsx')
        df.to_parquet(r'data\table\folable_join.parquet')


class ExternalRawData:
    def __init__(self):
        self.ts_table_path = DATA_PATH['toss_raw']
        self.ss_table_path = DATA_PATH['samsung_raw']
        self.ss_dir = DATA_DIR['samsung']
        self.ts_dir = DATA_DIR['toss']
        self.ins_dir = DATA_DIR['insurance']
        
       
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
                        df = pd.read_excel(xl, sheet_name=name, skiprows=1)
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
        ss = pd.read_parquet(r'data\table\samsung_raw.parquet', engine='pyarrow')
        ss = ss[['POLICY_ID', 'PAYMENT_ID', 'PRODUCT_ID']]
        print('토스 데이터 불러오는 중...')
        ts = pd.read_parquet(r'data\table\toss_raw.parquet', engine='pyarrow')
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
        