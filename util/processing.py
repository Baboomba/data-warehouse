import pandas as pd


def alter_type_to_date(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    '''
    Parameter
    ---
    df : 입력할 데이터프레임
    
    cols : 날짜 형식으로 변환할 컬럼
    '''
    for col in cols:
        df[col] = pd.to_datetime(df[col])
    return df