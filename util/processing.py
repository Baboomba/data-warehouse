from config import DATA_PATH
import pandas as pd


class ConcatTossPaymentMerged:
    '''
    Parameter
    ---
    df : 입력할 데이터프레임
    
    cols : 날짜 형식으로 변환할 컬럼
    '''
    _path = DATA_PATH['toss_payment_merged']
    
    def __init__(self, df: pd.DataFrame, cols: list):
        self._input_df = df
        self._read_df = self._read_file()
        self._cols = cols
        self._main()
        
    def _read_file(self):
        return pd.read_parquet(self._path)

    def _alter_type_to_date(self):
        print(f'Target Columns : {self._cols}')
        for col in self.cols:
            self._input_df[col] = pd.to_datetime(self._input_df[col])
        return self
    
    def _concat_dataframe(self):
        df_list = [self._read_df, self._input_df]
        self._read_df = pd.concat(df_list)
        return self
    
    def _remove_duplicated_rows(self):
        self._read_df.drop_duplicates(inplace=True)
        return self
    
    def _write_to_parquet(self):
        self._read_df.to_parquet(self._path)
    
    def _main(self):
        self._alter_type_to_date()\
            ._concat_dataframe()\
            ._remove_duplicated_rows()\
            ._write_to_parquet()
        print('work completed!')