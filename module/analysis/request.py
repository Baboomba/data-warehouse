from datetime import datetime
import pandas as pd
import os



def code_map():
    path = r'data\raw_data\code_map'
    file = os.listdir(path)
    code = pd.read_excel(fr'{path}\{file[0]}')
    member = pd.read_parquet(r'data\table\member_list.parquet')[['POLICY_ID', '보험사']]
    mg = pd.merge(code, member, left_on='회원 넘버', right_on='POLICY_ID')
    mg = mg.drop_duplicates()
    now = datetime.now().strftime('%Y%m%d')
    mg.to_excel(fr'result\코드_{now}.xlsx')
    return mg