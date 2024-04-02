from config import ORACLE_ACCOUNT
from exception.log import Logger
import oracledb
import pandas as pd
from typing import List, Tuple


class DBConnection:
    _user = ORACLE_ACCOUNT['username']
    _password = ORACLE_ACCOUNT['password']
    _dsn = ORACLE_ACCOUNT['dsn']
    
    def __init__(self, log_level: str='error', log_path : str='db'):
        self.logger = Logger(log_level, log_path, False)
    
    def connect_to_db(self):
        try:
            con = oracledb.connect(
                dsn=self._dsn,
                user=self._user,
                password=self._password
            )
            self.logger.write_info('database connected successfully')
        except Exception as e:
            raise self.logger.write_log(e)
        
        return con
    
    def execute_query(self, query: str=None, **kwargs):
        try:
            con = self.connect_to_db()
            cur = con.cursor()
            cur.execute(query, **kwargs)
            results = cur.fetchall()
            columns = [col[0] for col in cur.description]
            self.logger.write_info(f'statement "{query}" executed and fetched the results')
        except Exception as e:
            raise self.logger.write_log(f'{e} : statement was "{query}"')
        finally:
            con.close()
            self.logger.write_info('database connection closed')
        
        df = pd.DataFrame(data=results, columns=columns)
        self.logger.write_info('A dataframe has been created from the results')
        return df
    
    def create_dataframe(self, fetch_result: List[Tuple], columns: list):
        return pd.DataFrame(fetch_result, columns=columns)