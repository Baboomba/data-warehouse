from exception.log import Logger
import oracledb
import pandas as pd
from typing import List, Tuple
from util.config_reader import ORACLE_ACCOUNT


class DBConnection:
    _user = ORACLE_ACCOUNT('username')
    _password = ORACLE_ACCOUNT('password')
    _dsn = ORACLE_ACCOUNT('dsn')
    
    def __init__(self, log_level: str='error', log_path : str='db', console_log: bool=False):
        self._logger = Logger(log_level, log_path, console_log)
    
    def _connect_to_db(self):
        try:
            con = oracledb.connect(
                dsn=self._dsn,
                user=self._user,
                password=self._password
            )
            self._logger.write_info('database connected successfully')
        except Exception as e:
            raise self._logger.write_log(e)
        
        return con
    
    def execute_query(self, query: str=None, to_df: bool=True, **kwargs):
        con = None
        
        try:
            con = self._connect_to_db()
            cur = con.cursor()
            cur.execute(query, **kwargs)
            results = cur.fetchall()
            columns = [col[0] for col in cur.description]
            self._logger.write_info(f'SQL statement {query} executed and fetched the results')
        except Exception as e:
            raise self._logger.write_log(f'{e} : statement was wrong, {query}')
        finally:
            if con is not None:
                con.close()
                self._logger.write_info('database connection closed')
                
                if to_df:
                    df = self._create_dataframe(results, columns)
                    return df
                
        return results, columns
    
    def _create_dataframe(self, fetch_result: List[Tuple], columns: list):
        df = pd.DataFrame(fetch_result, columns=columns)
        self._logger.write_info('A dataframe has been created from the results')
        return df