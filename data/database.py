from typing import Any
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import MYSQL_ACCOUNT as acc
import os
import pandas as pd


class MySQLConnection:

    def __init__(self, url):
        __id = acc['id']
        __pw = acc['password']
        self.url = rf'mysql+pymysql://{__id}:{__pw}@localhost:3306/fame?charset=utf8'
        self.engine = create_engine(self.url)
    
    def session(self, func):
        
        def wrapper(self, *args, **kwargs):
            try:
                session = sessionmaker(bind=self.engine)
                session.begin()
                func(self, *args, **kwargs)
            except Exception as e:
                print(e)
            finally:
                session.close()
            
            
    
    def create_table(self):
        Base = declarative_base()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    
    # User 모델과 Post 모델 간의 관계 설정
    posts = relationship('Post', back_populates='author')

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    
    # 외래키 설정
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Post 모델과 User 모델 간의 관계 설정
    author = relationship('User', back_populates='posts')
    


## 파케이
class ParquetControll:
    def __init__(self):
        self.path = r'C:\Users\CS-2875\Documents\work\data\table\member'
        
    
    def tranform_files(self):
        '''
        csv 파일을 읽어서 데이터프레임 리스트로 반환
        '''
        files = os.listdir(self.path)
        df_list = []
        
        for file in files:
            df = pd.read_csv(fr'{self.path}\{file}')
            df_list.append(df)
        
        if len(self.check_type(self, df_list)) > 0:
            return print('타입 불일치')
        else:
            pass
        
        df_list = pd.concat(df_list)
        df_list.to_parquet(r'C:\Users\CS-2875\Documents\work\programming\fame\settlement\data\table\member_list.parquet', engine='pyarrow')
        
        return df_list
    
    def check_type(self, df_list):
        '''
        데이터프레임 리스트를 넣으면 타입 불일치 데이터프레임 추출
        '''
        unmatching = []
        for num, df in enumerate(df_list):
            if df.dtypes.equals(df_list[0].dtypes):
                pass
            else:
                unmatching.append(num)
        return unmatching
    
    def save_parquet(self, path):
        concat = pd.concat(empty)
        concat.to_parquet(path, engine='pyarrow')
    
    
    
    
    
# IMEI 값 float으로 변환
empty = []

df = pd.read_parquet(path=r'C:\Users\82102\Downloads\settlement\data\member_list\1.parquet', engine='pyarrow')

for num, val in enumerate(df['IMEI']):
    
    if not val == None:
        if not ((len(val) == 15) or (val == '')):
            empty.append(num)               


for num in empty:
    df.loc[num, 'IMEI'] = ''

df['IMEI'] = df['IMEI'].apply(lambda x: float(x) if x is not None and x != '' else None)