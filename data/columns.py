## 자주 사용하는 컬럼의 압축 내용 및 타입
##



def member_main_column(original: bool=False):
    '''
    회원정보 컬럼
    '''
    col = {
        '상품정보': str,
        '가입모델명': str,
        '보험가입일': str,
        '보험해지일': str,
        '보험상태': str,
        '프로모션유무': str,
        '보장타입': str,
        '제품군': str,
        '가입모델명_1': str,
        '가입기간': str
    }
    
    if original:
        return col
    else:
        col = list(col)
        return col[:6]

def program_info_column(original: bool=False):
    '''
    프로그램인포 컬럼
    '''
    col = {
        'PROGRAM_CODE': {'PID': str},
        'PROGRAM_NAME': {'상품명': str},
        'CATE_FIRST': {'유무상구분': str},
        'CATE_SECOND': {'제품군': str},
        'CATE_THIRD': {'제품시리즈': str},
        'MONTHLY_PREMIUM': {'월 보험료': int},
        'LOST_COUNT': {'보장횟수 분실': int},
        'REPAIR_COUNT': {'보장횟수 수리': int},
        'BATTERY_COUNT': {'보장횟수 배터리': int},
        'ONSITE_COUNT': {'보장횟수 방문': int},
        'LOST_DEDUCTIBLE': {'자부금 분실': int},
        'REPAIR_DEDUCTIBLE': {'자부금 수리': int},
        'BATTERY_DEDUCTIBLE': {'자부금 배터리교체': int},
        'ONSITE_DEDUCTIBLE': {'자부금 방문': int},
        'PROMOTION_YN': {'프로모션 여부': str},
        'SHARE_SS': {'지분율 삼성': float},
        'SHARE_KB': {'지분율 국민': float},
        'SHARE_HW': {'지분율 한화': float},
        'SHARE_DB': {'지분율 동부': float},
        'SHARE_CS': {'지분율 CS': float},
        'PROMOTION_MONTH': {'프로모션 기간': int},
        'WARRANTY_MONTH': {'보장기간': int},
        'START_DATE': {'상품출시일': str},
        'END_DATE': {'상풍종료일': str},
        'EW_COUNT': {'보증연장 횟수': int},
        'KAKAO_YN': {'카카오 발송여부': str},
        'CLOSE_YEAR': {'정산 기준년도': int},
        'PROGRAM_DESC': {'상품설명': str},
        'PROGRAM_FULL_NAME': {'상품 상세 코드': str},
        'STG_PROGRAM_CODE': {'개발 상품코드': str},
        'PROMOTION_NAME': {'상품 프로모션 이름': str},
        'MOBILE_INSURE_PRICE': {'모바일 보험료': int},
        'FEE_PGLL': {'PGLL보험(EW, 배터리)': int},
        'FEE_ONSITE': {'기업비용보상보험(방문수리)': int}
    }
    
    selected_col = ['PROGRAM_CODE', 'CATE_SECOND', 'CATE_THIRD']
    
    if original:
        return col
    else:
        _col = {key: col[key] for key in selected_col}
        return _col

def program_cate_column(original: bool=False):
    '''
    프로그램카테고리 컬럼
    '''
    col = [
        '상품정보',
        '상품명',
        '유무상',
        '제품군',
        '제품군_2',
        '제품시리즈',
        '제품시리즈_2',
        '가입채널',
        '보장타입',
        '케이스구독형'
    ]
    selected_col = ['상품정보', '제품군_2', '제품시리즈', '제품시리즈_2', '보장타입']
    
    if original:
        return col
    else:
        return selected_col

    
## 케이스 구독 전환 시 변경되는 팩코드
## PID, product_name, price_before, pac_code_before, price_after, pac_code_after
case_transition = {
    'pid': ['KORPRD20220207000503', 'KORPRD20220210000726', 'KORPRD20220210000150', 'KORPRD20220210000129', 'KORPRD20210813000042', 'KORPRD20210813000357'],
    'product_name': ['S22 케이스구독형', 'S8 케이스구독형', 'S8 케이스구독형', 'S8 케이스구독형', '폴드3 케이스 구독', '플립3 케이스 구독'],
    'price_before': [12900, 13900, 14900, 16900, 15900, 8900],
    'code_before': ['P-GT-NC1CS0MC', 'P-GT-NC1CT0HC', 'P-GT-NC2CT0HC', 'P-GT-NC3CT0HC', 'P-GT-NC1CS0PC', 'P-GT-NC1CS0HC'],
    'price_after': [3300, 4600, 4600, 4600, 6900, 4700],
    'code_after': ['P-GT-NCXCS0MC', 'P-GT-AC2CT0HC', 'P-GT-AC2CT0HC', 'P-GT-AC2CT0HC', 'P-GT-NCXCS0PC', 'P-GT-NCXCS0HC']
}


## 비대면솔루션 결과 테이블 컬럼
untact_column = {
    '상품정보': 'PROGRAM_CODE',
    '보험가입일': '보험가입일',
    'POLICY_ID': 'POLICY_ID',
    '보험사': '보험사',
    '가입모델명': '모델명',
    '비대면솔루션값': '비대면솔루션 값',
    '프로모션유무': '상품 구분',
    '가입 시점': '가입 시점',
    '가입월': '가입월',
    '해지월': '해지월',
    '정산대상여부': '정산대상여부'
}

import pyarrow as pa
insurance_schema = pa.schema([
            ('회원 넘버', pa.string()),
            ('보험사', pa.string()),
            ('상품ID', pa.string()),
            ('제품코드', pa.string()),
            ('기준월', pa.int32()),
            ('기준일', pa.int32()),
            ('GALAXY_ID', pa.string()),
            ('접수번호', pa.string()),
            ('모델', pa.string()),
            ('제조번호', pa.string()),
            ('처리형태', pa.string()),
            ('처리장소', pa.int32()),
            ('처리코드', pa.string()),
            ('불량여부', pa.int32()),
            ('특별처리코드', pa.string()),
            ('특별처리 2', pa.string()),
            ('VISIT_YN', pa.int32()),
            ('유상부품비', pa.int32()),
            ('수리비', pa.int32()),
            ('시장자재비', pa.int32()),
            ('받을금액', pa.int32()),
            ('입금금액', pa.int32()),
            ('자기부담금계', pa.int32()),
            ('총 할인금액', pa.int32()),
            ('자재할인금액', pa.int32()),
            ('수리비할인금액', pa.int32()),
            ('방문서비스비용', pa.int32()),
            ('참고)임직원할인자재비', pa.int32()),
            ('참고)임직원할인수리비', pa.int32()),
            ('임직원여부', pa.string()),
            ('DC_COM_CODE', pa.string()),
            ('총할인금액(VAT제외)', pa.int32()),
            ('자재할인금액(VAT제외)', pa.int32()),
            ('수리비할인금액(VAT제외)', pa.int32()),
            ('방문서비스비용(VAT제외)', pa.int32()),
            ('보험수리', pa.string()),
            ('배터리 교환', pa.string()),
            ('보증연장', pa.string()),
            ('방문 수리', pa.string()),
            ('파손수리', pa.string()),
            ('BILL_NO', pa.string()),
            ('SC_PLUS_YN', pa.string()),
            ('유무상 구분', pa.string()),
            ('기준', pa.date32()),
            ('접수 날짜', pa.date32()),
            ('무상 종료일', pa.date32()),
            ('무상종류 전/후', pa.string())
        ])