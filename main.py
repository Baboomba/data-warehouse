from analysis.monthly_close import PaidProductClose, UntactSolution
from analysis.perfomance import MonthlyJoin, ConversionRate
from preprocessing.raw_data import MemberData
from datetime import datetime

def paid_close():
    # 유상 마감
    try:
        prom = PaidProductClose(
            process_data=False
        )
    except Exception as e:
        print(e)

def main_index():
    # 주요 지표
    try:
        main = MonthlyJoin()
    except Exception as e:
        print(e)

def untact_solution():
    start = '2023-09-01'   # 정산 시작일 기준
    end = '2023-09-15'
    untact = UntactSolution(start, end)

def conversion_rate():
    date = '2023-09'  # 마감월에 맞춰 입력
    conversion = ConversionRate(date)


if __name__ == '__main__':
    
    # 가입자 데이터 처리
    # member = MemberData()
        
    start = datetime.now()
    print(f'시작 시간 : {start}')
    
    paid_close()
    
    end = datetime.now()
    print(f'완료 시간 : {end}')
    print(f'작업 시간 : {end - start}')