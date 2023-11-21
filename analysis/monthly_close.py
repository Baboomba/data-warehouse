# import sys
# sys.path.append()

from config import DATA_PATH
from data.columns import case_transition, untact_column
from datetime import datetime
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
from preprocessing.raw_data import ExternalRawData



class PaidProductClose(ExternalRawData):
    '''
    유상 마감 연산 클래스로 ExternalRawData 상속
    
    PARAMETERS
    ---
    save : 병합 파일 저장 여부(불리언)
    
    load : 삼성/토스 병합 파일 변수 저장 여부(불리언)
    
    save : 병합 파일 저장 여부(불리언)
    
    ss : 삼성 raw 파일 전처리 여부
    
    ts : 토스 raw 파일 전처리 여부
    
    pay : 결제 건수 산출 여부    
    '''
    
    ## 필요 없는 컬럼 제거 위해 설정
    __ss_col = [
            'PAYMENT_ID',
            'PACK_CODE',
            'INSURANCE_COMPANY_CODE',
            'PRODUCT_ID',
            'POLICY_ID'
        ]
        
    __ts_col = [
        '상점아이디(MID)',
        '정산액 입금일',
        '매출일',
        '결제일',
        '주문번호',
        '결제상태',
        '결제·취소액 (A)',
        'PG수수료 (B)',
        '당일 정산액 (C) = (A-B)'
    ]
    
    __cate_col = [
        '상품정보',
        '제품군_2',
        '제품시리즈',
        '제품시리즈_2',
        '보장타입',
        '유무상'
    ]
    
    def __init__(self, save: bool):
        super().__init__()
        self.cate_table_path = DATA_PATH['program_category']
        self.dataframe = self.return_merged_table()
        self.save_dataframe(save)
        # self.pivot_dic = self.create_result(self.dataframe)  # 엑셀 피벗으로 대체
        # self.save_files(save)   # 엑셀 피벗으로 대체 self.create_result() 위한 저장 함수
        
    
    def return_merged_table(self):
        '''
        토스, 무선, 제품 병합 테이블 반환 함수
        '''
        ts = pd.read_parquet(self.ts_table_path)
        ts = ts[self.__ts_col]
        # ts = ts[ts['결제상태'] != '부분취소']
        print(f'병합 전 토스 데이터 건수 : {ts.shape[0]}건')
        ss = pd.read_parquet(self.ss_table_path)
        ss = ss[self.__ss_col]
        print(f'병합 전 삼성 데이터 건수 : {ss.shape[0]}건')
        cate = pd.read_parquet(self.cate_table_path)
        cate = cate[self.__cate_col]

        mg = pd.merge(ts, ss, left_on='주문번호', right_on='PAYMENT_ID', how='left')
        print('삼성/토스 데이터 1차 병합')
        print(f'병합 후 토스 데이터 건수 : {ts.shape[0]}건')
        
        mg = mg.drop_duplicates()
        print('병합 후 중복 항목 제거')
    
        if ts.shape[0] == mg.shape[0]:
            print('결재 데이터 병합 작업 이상 없음')
            mg = self.alter_pac_code(mg)
            mg = self.process_offset(mg)
            mg = self.pre_payment_merge(mg)
        else:
            print('size error ==> 결제 데이터 병합 오류')
            return None
                    
        mg = pd.merge(mg, cate, left_on='PRODUCT_ID', right_on='상품정보', how='left')
        print('제품 테이블 병합')
        mg = mg.drop_duplicates()
        print('병합 후 중복 항목 제거')
        
        mg.drop(columns='PAYMENT_ID', inplace=True)
        mg.drop(columns='상품정보', inplace=True)
        print('병합을 위해 사용된 컬럼 제거(중복 컬럼)')
        
        if ts.shape[0] == mg.shape[0]:
            return mg
        else:
            print('데이터 병합 오류')
            return None
    
    
    def alter_pac_code(self, df_join):    # 삼성과 토스 데이터가 조인된 데이터프레임을 인풋으로 넣음
        '''
        케이스 구독 만료된 고객의 팩코드를 변경
        '''
        code = pd.DataFrame(case_transition)
        size = len(code)

        for num in range(size):
            
            con1 = (df_join['PACK_CODE'] == code['code_before'][num]) 
            con2 = (df_join['결제·취소액 (A)'] != code['price_before'][num])
            condition = (con1 & con2)
            df_join.loc[condition, 'PACK_CODE'] = code['code_after'][num]
        
        print('케이스 구독자 팩코드 변경 완료')

        return df_join
        
                
    def process_offset(self, df_join):
        '''
        결제/취소 쌍 상계처리
        '''
        print('병합 데이터 결제/취소 상계 건 검색...')
        
        con1 = df_join['주문번호'].duplicated(keep=False)
        con2 = df_join['PAYMENT_ID'].isna()
        con3 = (df_join['결제상태'].nunique() == 2)
        
        dupl = df_join[con1 & con2 & con3].sort_values('주문번호')
        dupl = dupl.reset_index()

        _index = []

        for num in range(dupl.shape[0] - 1):
            if dupl.loc[num, '주문번호'] != dupl.loc[num + 1, '주문번호']:
                pass
            else:
                if (dupl.loc[num, '결제·취소액 (A)'] != 0) and (dupl.loc[num + 1, '결제·취소액 (A)'] != 0):
                    if (dupl.loc[num, '결제·취소액 (A)'] + dupl.loc[num + 1, '결제·취소액 (A)']) == 0:
                        _index.append(dupl.loc[num, 'index'])
                        _index.append(dupl.loc[num + 1, 'index'])
                    
        print(f'상계 건 : {len(_index)}건')

        for idx in _index:
            df_join.loc[idx, 'PACK_CODE'] = '`+-완료'
            print(f'인덱스 {idx}번 상계 처리')
        return df_join
    
 
    def pre_payment_merge(self, df_join):
        '''
        전월 토스 결제건 처리
        '''
        df = pd.read_parquet(DATA_PATH['toss_payment_merged'])
        df = df[['주문번호', 'packcode', 'ins', 'PRODUCT_ID']]
        df.rename(columns={
            'packcode': 'PACK_CODE_',
            'ins': 'INSURANCE_COMPANY_CODE_',
            'PRODUCT_ID': 'PRODUCT_ID_'
        }, inplace=True)
        mg = pd.merge(df_join, df, how='left', on='주문번호')
        condition = ((mg['PACK_CODE'].isna()) & ~(mg['PACK_CODE_'].isna()))
        mg.loc[mg[condition].index, 'PACK_CODE'] = mg.loc[mg[condition].index, 'PACK_CODE_']
        mg.loc[mg[condition].index, 'INSURANCE_COMPANY_CODE'] = mg.loc[mg[condition].index, 'INSURANCE_COMPANY_CODE_']
        mg.loc[mg[condition].index, 'PRODUCT_ID'] = mg.loc[mg[condition].index, 'PRODUCT_ID_']
        mg.drop(columns=['PACK_CODE_', 'INSURANCE_COMPANY_CODE_', 'PRODUCT_ID_'], inplace=True)
        print('전월 토스 결제 처리 완료')
        return mg
    
    
    def save_dataframe(self, save: bool) -> None:
        if save:
            now = datetime.now().strftime('%Y%m%d')
            self.dataframe.to_excel(fr'result\유상마감데이터_{now}.xlsx')
        
    
    ## 여기부터 cell_style 메서드까지 미사용 코드    
    def create_result(self, df_join):
        '''
        보험사별 그룹화 집계 및 피벗
        
        상품정보와 pac_code 피벗테이블 딕셔너리 반환
        '''
        index = ['PRODUCT_ID', 'PACK_CODE']
        columns = ['결제상태', 'INSURANCE_COMPANY_CODE']
        values = '주문번호'
        
        groups = []
        print('그룹화 집계 중...')
        
        for element in index:
            print(f'그룹화 대상 : {element}, INSURANCE_COMPANY_CODE, 결제상태')
            col_pid = [element, 'INSURANCE_COMPANY_CODE', '결제상태']
            group = df_join.groupby(col_pid)['주문번호'].count().reset_index()
            groups.append(group)
            print(f'{element} 테이블 그룹화 집계 완료')
        
        pivots = {}
        print(f'피벗 테이블 생성...')

        for num, element in enumerate(index):
            pivot = groups[num].pivot(index=element, columns=columns, values=values).fillna(0)
            print(f'{element} 피벗 테이블 생성 완료')
        
            # 합계 컬럼 추가
            pivot[('합계', 'HW')] = pivot[('완료', 'HW')] - pivot[('취소', 'HW')]
            pivot[('합계', 'KB')] = pivot[('완료', 'KB')] - pivot[('취소', 'KB')]
            pivot[('합계', 'SS')] = pivot[('완료', 'SS')] - pivot[('취소', 'SS')]
            print(f'{element} 피벗 테이블 합계 컬럼 추가')
            
            pivots[element] = pivot
            
        return pivots
    
    
    def save_files(self, save):
        '''
        추출된 데이터를 엑셀 파일로 저장
        
        3개 시트 : 피벗테이블(pid, pac_code), 결제 테이블
        '''
        if save:
            wb = Workbook()
            print('엑셀 워크북 생성')
            self.pivot_dic['raw_data'] = self.dataframe
            
            for key, value in self.pivot_dic.items():
                sheet = wb.create_sheet(title=key)
                print(f'{key} 시트 생성')
                
                print('데이터 입력 중 : [', end='')
                ratio = value.shape[0] * 0.01
                for num, row in enumerate(dataframe_to_rows(value, index=True, header=True)):
                    sheet.append(row)
                    
                    if num >= ratio:
                        print('#', end='')
                        ratio += value.shape[0] * 0.01
                print(f']\n{key} 시트 입력 완료')
            
            delete = wb['Sheet']
            wb.remove(delete)
            wb = self.cell_style(wb)
            
            print('데이터 저장 중...')
            now = datetime.now().strftime('%Y%m%d')
            dir = fr'result\유상데이터정산_{now}.xlsx'
            wb.save(dir)
            print('데이터 저장 완료')
        
    
    def cell_style(self, workbook):
        '''
        셀 병합 및 폰트 사이즈 조정
        '''
        sheets = workbook.sheetnames
        
        # 범위 변수
        ranges = [
            'A1:A2',
            'B1:D1',
            'E1:G1',
            'H1:J1'
        ]
        
        for sht in sheets:
            # 시트 활성화
            ws = workbook[sht]
            workbook.active = ws
            print(f'{sht} 시트의 셀과 폰트를 조정 중...')
            
            if sht == 'raw_data':
                continue
            else:
                ws['A1'] = sht
                # 셀 병합
                for rng in ranges:
                    ws.merge_cells(rng)

            # 모든 데이터를 한 칸씩 올리기
            for row in ws.iter_rows(min_row=3, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
                for cell in row:
                    cell.value = ws.cell(row=cell.row + 1, column=cell.column).value

            # 폰트 조정
            for row in ws.iter_rows():
                for cell in row:
                    cell.font = Font(size=9)
            
        return workbook


#####################################################################################################################
## 무상 마감
#####################################################################################################################


class ConversionClassification:
    '''
    보험금 유상 전환 구분
    
    인스턴스 생성 시 회원넘버, 접수번호 데이터프레임 입력
    '''
    def __init__(self, dataframe, save: bool):
        self.basic_data = dataframe
        self.member_path = DATA_PATH['member_close']
        self.save_data(save)
        
    def read_member(self):
        return pd.read_parquet(self.member_path)
    
    def adjust_columns(self):
        df = self.read_member()
        return df[['POLICY_ID', '유무상 구분', '보험가입일', '무상 종료일']]
    
    def alter_type(self):
        df = self.adjust_columns()
        df['무상 종료일'] = pd.to_datetime(df['무상 종료일'])
        return df
    
    # processing samsung data
    def extract_date(self):
        self.basic_data['접수날짜'] = self.basic_data['접수번호'].str[:8]
        self.basic_data['접수날짜'] = pd.to_datetime(self.basic_data['접수날짜'], format='%Y%m%d')
        self.basic_data.rename(columns={'회원 넘버':'POLICY_ID'}, inplace=True)
        return self
    
    def merge_dataframe(self):
        self.extract_date()
        df = self.alter_type()
        return pd.merge(self.basic_data, df, on='POLICY_ID', how='left')
    
    def classify_payment(self):
        con = self.merge_dataframe()
        con['무상 종료일'] = pd.to_datetime(np.where(con['유무상 구분'] == '유상', None, con['무상 종료일']))
        return con
    
    def classify_timing(self):
        con = self.classify_payment()
        con['무상종류 전/후'] = (con['접수날짜'] - con['무상 종료일']).dt.days
        # condition to classify the time of the benefit
        conditions = [
            con['무상종류 전/후'] > 0,
            con['무상종류 전/후'] <= 0
        ]
        values = ['후', '전']
        
        con['무상종류 전/후'] = np.select(conditions, values, None)
        return con
    
    def correct_conversion(self):
        con = self.classify_timing()
        condition = ((con['유무상 구분'] == '전환') & (con['무상종류 전/후'] == '전'))
        con['temp'] = np.where(condition, '무상', con['유무상 구분'])
        return con
    
    def save_data(self, save: bool):
        if save:
            df = self.correct_conversion()
            df.to_excel(r'result\보험금전환구분.xlsx')
    


class PromotionClose:
    '''
    보험사 증빙용 무상상품 정산 마감
    '''
    def __init__(self):
        self.member_close_table = DATA_PATH['member_close']
        self.promotion_info_table = DATA_PATH['promotion_info']
        self.columns = [
            '상품정보',
            '프로그램명',
            '월요금',
            'POLICY_ID',
            '보험가입일',
            '보험해지일',
            '보험사',
            '보험상태',
            '유무상 구분'
        ]
        self.data = pd.read_parquet(self.member_close_table)
        self.final_result()
    
    def date_type_transform(self):
        self.data['보험가입일'] = pd.to_datetime(self.data['보험가입일'], format='%Y-%m-%d')
        self.data['보험해지일'] = pd.to_datetime(self.data['보험해지일'], format='%Y-%m-%d')
        return self
    
    def select_promotion(self):
        self.data = self.data[self.data['유무상 구분'] == '무상']
        return self
    
    def select_active(self):
        self.data = self.data[self.data['보험상태'] != '해지']
        return self
    
    def add_close_month(self):
        '''
        정산월 조정(하루씩 더함)
        
        2023년 9월 조정은 특이 사항임
        '''
        self.data['정산월'] = (self.data['보험가입일'] + pd.DateOffset(days=1)).dt.to_period('M')
        cond1 = (self.data['보험가입일'] > '2023-09-26')   # 9월 마감이 26일 일어남
        cond2 = (self.data['보험가입일'] < '2023-10-31')
        self.data.loc[cond1 & cond2, '정산월'] = pd.to_datetime('2023-10').strftime('%Y-%m')
        return self
    
    def group_for_result(self):
        self.data = self.data.groupby(['정산월', '상품정보', '보험사'])['POLICY_ID'].count().reset_index()
        return self
    
    def extract_promotion_info(self):
        info = pd.read_parquet(self.promotion_info_table)
        info = info[['상품정보', '프로모션명_요약']]
        info = info[~info['상품정보'].duplicated()]
        return info
    
    def final_result(self):
        self.date_type_transform().select_promotion().select_active().add_close_month().group_for_result()
        promotion = self.extract_promotion_info()
        self.data = pd.merge(self.data, promotion, on='상품정보', how='left')
        self.data.rename(columns={'POLICY_ID':'수량', '상품정보':'프로그램명'}, inplace=True)
        now = datetime.now().strftime('%Y%m%d')
        self.data.to_excel(fr'result\무상상품마감_{now}.xlsx')
        return self
    
    






#####################################################################################################################
## 비대면솔루션
#####################################################################################################################

class UntactSolution:
    '''
    Parameter
    ---
    start : 정산 시작 기준일
    
    end : 정산 마감 기준일
    
    period_dic : 정산 기간 딕셔너리. {'2023-10':['2023-09-26', '2023-10-30']}
    
    
    '''
    def __init__(self, period_dic: dict):
        self.start = None
        self.end = None
        self.set_date(period_dic)
        self.assebled_function(period_dic)
    
    def assebled_function(self, period_dic):
        df = self.join_time()
        df = self.add_join_close_month(df, period_dic)
        df = self.payment_status(df)
        df = self.ordering_columns(df)
        df = self.classify_payment(df)
        
        now = datetime.now().strftime('%Y%m%d')
        df.to_excel(fr'result\유상 상품 비대면진단_{self.start}_{self.end}_{now}.xlsx')
        print('데이터 저장 완료')
        return df
    
    def set_date(self, period_dic: dict):
        i = 0
        for _, item in period_dic.items():
            if i == 0:
                self.start = item[0]
            if i == (len(period_dic) - 1):
                self.end = item[1]
            i += 1
    
    def join_time(self):
        '''
        가입 시점 계산
        
        보험가입일 - 최초통화일 <= 2  --> 3일 이내
        
        보험가입일 - 최초통화일 >= 3  --> 최초통화일+2일 이후
        
        join_date
        ---
        보험가입일(str)
        
        call_date
        ---
        최초통화일(str)
        '''
        print('회원정보 데이터 불러오는 중...')
        df = pd.read_parquet(DATA_PATH['member_list'])
        
        print('가입 시점 계산 중...')
        df['최초통화일'] = pd.to_datetime(df['최초통화일'], format='%Y-%m-%d')
        df['보험가입일'] = pd.to_datetime(df['보험가입일'], format='%Y-%m-%d')
        df['보험해지일'] = pd.to_datetime(df['보험해지일'], format='%Y-%m-%d')
        
        df = df[(df['보험가입일'] >= self.start) & (df['보험가입일'] <= self.end)]

        df['가입 시점'] = (df['보험가입일'] - df['최초통화일']).dt.days
        
        condition = (df['가입 시점'] <= 2)
        df['가입 시점'] = np.where(condition, '3일 이내', '최초통화일+2일 이후')
        
        df.reset_index(drop=True, inplace=True)
        df = df.drop('최초통화일', axis=1)
        return df
    
    def add_join_close_month(self, df, period_dic: dict):
        df['가입월'] = None
        df['해지월'] = None
        
        for key, item in period_dic.items():
            cond_start = (df['보험가입일'] >= item[0])
            cond_end = (df['보험가입일'] <= item[1])
            df.loc[df[(cond_start & cond_end)].index, '가입월'] = key
            
            cond_start = (df['보험해지일'] >= item[0])
            cond_end = (df['보험해지일'] <= item[1])
            df.loc[df[(cond_start & cond_end)].index, '해지월'] = key
            
        df['보험가입일'] = df['보험가입일'].dt.strftime('%Y-%m-%d')
        df['보험해지일'] = df['보험해지일'].dt.strftime('%Y-%m-%d')
        return df

        
    def payment_status(self, df):
        print('정산 대상 여부 계산 중...')
        cond1 = (df['가입월'] == df['해지월'])
        df['정산대상여부'] = np.where(cond1, '당월해지', '정산대상')
        return df
    
    def ordering_columns(self, df):
        '''
        결과 컬럼만 추출
        
        인덱스 삭제
        '''
        print('컬럼 조정 중...')
        df = df.rename(columns=untact_column)
        col = list(untact_column.values())
        # df = df[col]
        # df = df.set_index('PROGRAM_CODE', drop=True)
        return df
    
    def classify_payment(self, df):
        '''
        유무상 구분
        
        비대면솔루션 값만 추출
        '''
        print('유무상 구분 및 비대면솔루션 값 선별 중...')
                
        condition = (df['상품 구분'] == 'Y')
        df['상품 구분'] = np.where(condition, '무상', '유상')
                
        df = df[df['상품 구분'] == '유상']
        df = df[df['비대면솔루션 값'].notnull()]
        return df