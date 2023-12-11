import pandas as pd
import numpy as np
from datetime import datetime

from monthly import to_dataframe


# 녹스가드 삭제 대상 세기
class InactiveUser:
    def __init__(self, path, member_path):
        self.path = path
        self.member_path = member_path

    def process_member_list(self, path):
        df = to_dataframe(path)
        df = df[['POLICY_ID', '보험상태', '시리얼번호', '보험가입일']]
        df['temp_date'] = pd.to_datetime(df['보험가입일'])
        df['temp_date'] = df['temp_date'].astype('int64')
        df.rename(columns={'시리얼번호':'SN'}, inplace=True)
        df.reset_index(inplace=True)
        dfmax = df.loc[df.groupby('SN')['temp_date'].idxmax()]
        dfmax.reset_index(inplace=True)
        return dfmax
        
    def read_knox(self, save_path):
        knox = pd.read_csv(self.path)
        dfmax = self.process_member_list(self.member_path)
        knox = pd.merge(knox, dfmax, how='left', on='SN')
        knox.to_excel(save_path)
        



####################################################################################
####################################################################################



knox = pd.read_csv(r'C:\Users\CS-2875\Documents\work\결산\2023\09\녹스가드\녹스가드해지\Devices_20230917.csv')
member = pd.read_parquet(r'C:\Users\CS-2875\Documents\work\programming\fame\code\data\table\member_list.parquet', engine='pyarrow')

# 중복 시리얼 제거
member = member[~member['시리얼번호'].duplicated(keep=False)]

col_knox = [
    'IMEI1',
    'IMEI2',
    'SN',
    'APPROVAL ID',
    'STATUS',
    'UPLOADED'
]
knox = knox[col_knox]

col_mem = [
    'POLICY_ID',
    'IMEI',
    '시리얼번호',
    '보험가입일',
    '보험해지일',
    '보험상태'
]
member = member[col_mem]


merge = pd.merge(knox, member, left_on='SN', right_on='시리얼번호', how='inner')

# 중복 시리얼 제거
merge = merge.drop(merge[merge['SN'].duplicated(keep=False)].index)

# 잠금 제거
merge.drop(merge[(merge['STATUS'] == 'Locked | PIN') | (merge['STATUS'] == 'Locking')].index, inplace=True)

del knox
del member

# 가입자 제거
merge = merge.drop(merge[(merge['보험상태'] == '가입') | (merge['보험상태'] == '미납') | (merge['보험상태'] == '해지예약')].index)
merge.shape

merge.to_excel(r'C:\Users\CS-2875\Documents\work\결산\2023\09\녹스가드\녹스가드해지\2차검토\필터링_20230920.xlsx')

####################################################################################
####################################################################################

# 녹스가드 삭제
col_knox = [
    'IMEI1',
    'IMEI2',
    'SN',
    'STATUS',
    'APPROVAL ID'
]

col_member = [
    '상품정보',
    'POLICY_ID',
    '시리얼번호',
    '보험가입일',
    '보험해지일',
    '보험상태',
    '프로모션유무'
]
knox = pd.read_csv(r'C:\Users\CS-2875\Documents\work\결산\2023\09\녹스가드\녹스가드해지\Devices_20230927.csv')
knox = knox[col_knox]
knox.rename(columns={'SN': '시리얼번호'}, inplace=True)
member = pd.read_parquet(r'data\table\member_list.parquet')
member = member[col_member]

merge = pd.merge(knox, member, on='시리얼번호', how='left')
merge = merge[~merge['시리얼번호'].duplicated(keep=False)]
merge = merge[merge['보험상태'] == '해지']
merge = merge[merge['프로모션유무'] == 'N']
merge = merge[(merge['STATUS'] != 'Locking') | (merge['STATUS'] != 'Locked | PIN') | (merge['STATUS'] != 'Resetting')]

print(merge.shape)
merge.to_excel(r'result\녹스가드삭제대상.xlsx')

merge = pd.merge(knox, member, on='시리얼번호', how='left')
dupl = merge[merge['시리얼번호'].duplicated(keep=False)]
print(dupl.shape)
dupl['보험가입일'] = pd.to_datetime(dupl['보험가입일'], format='%Y-%m-%d')
max_join_date = dupl.groupby('시리얼번호')['보험가입일'].idxmax()
max_join_date.to_excel(r'result\녹스가드삭제대상(중복자).xlsx')