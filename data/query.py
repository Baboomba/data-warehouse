from datetime import datetime, timedelta



class QuerySet:
    '''
    데이터베이스에서 자주 사용하는 SQL 모음
    '''
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def sales_performance(start_date: str=None):
        '''
        Parameter
        ---
        start_date : 해당 날짜 이후의 모든 데이터
        '''
        sentence = f'''
        SELECT
            c.policy_id
            , c.program_code product_id
            , p.program_full_name product_name
            , TO_CHAR(c.start_date, 'YYYYMMDD') registration_date
            , m.model_pet_name device_model_name
            , c.shop_code store_code
            , c.sales_pro employee_name
        FROM sc_tpa.tb_contract c
        LEFT JOIN sc_tpa.tb_program_info p
        ON c.program_code = p.program_code
        LEFT JOIN sc_tpa.tb_model m
        ON c.enrolled_model = m.model_name
        WHERE 1=1
        AND c.start_date >= TO_DATE('{start_date} 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
        AND (c.shop_code IS NOT NULL
        OR c.sales_pro IS NOT NULL)
        ORDER BY c.start_date ASC
        '''
        return sentence
    
    @staticmethod
    def technomart_performance(start_date: str=None) -> str:
        sentence = f'''
         SELECT
            TO_CHAR(c.start_date, 'YYYYMMDD') registration_date
            , m.model_pet_name model
            , c.program_code product_id
            , p.program_full_name product_name
            , c.cid CID
            , c.shop_code store_id
            , c.sales_pro agent
            , c.policy_id
            , SUBSTR(SC_TPA.CRYPT.DECRYPT(c.full_name, 'FAME_TPA'), 1, 1) || '*' || SUBSTR(SC_TPA.CRYPT.DECRYPT(c.full_name, 'FAME_TPA'), 3, 3) name
            , SUBSTR(SC_TPA.CRYPT.DECRYPT(c.phone_number, 'FAME_TPA'), 1, 3) || '****' || SUBSTR(SC_TPA.CRYPT.DECRYPT(c.phone_number, 'FAME_TPA'), 8, 11) phone_number
        FROM sc_tpa.tb_contract c
        LEFT JOIN sc_tpa.tb_program_info p
        ON c.program_code = p.program_code
        LEFT JOIN sc_tpa.tb_model m
        ON c.enrolled_model = m.model_name
        WHERE 1=1
        AND c.start_date >= TO_DATE('{start_date} 00:00:00', 'YYYY-MM-DD HH24:MI:SS')
        AND c.cid in ('Technomart_SDR', 'Technomart_GB')
        ORDER BY c.start_date ASC
        '''
        return sentence
    
    @staticmethod
    def member_list(end_date: str=None) -> str:
        '''
        Parameter
        ---
        end_date : 해당 날짜까지의 데이터. 마감일 기준으로 입력
        '''
        sentence = f'''
        SELECT
            TP.PROGRAM_CODE AS "상품정보"
            , TP.PROGRAM_NAME AS "프로그램명"
            , TP.MONTHLY_PREMIUM AS "월요금"
            , TC.POLICY_ID
            , TC.ENROLLED_MODEL AS "가입모델명"
            , SC_TPA.CRYPT.DECRYPT(TC.FULL_NAME, 'FAME_TPA') AS "이름"
            , SC_TPA.CRYPT.DECRYPT(TC.PHONE_NUMBER, 'FAME_TPA') AS "연락처"
            , TC.IDENTIFICATION_NUMBER AS "생년월일"
            , JSON_VALUE(SC_TPA.CRYPT.DECRYPT(TC.SERIAL_NUMBER_JSON, 'FAME_TPA'), '$.device') AS "시리얼번호"
            , DECODE(TC.IMEI, NULL, '', DECODE(SC_TPA.CRYPT.DECRYPT(TC.IMEI, 'FAME_TPA'), '', '', SC_TPA.CRYPT.DECRYPT(TC.IMEI, 'FAME_TPA'))) AS "IMEI"
            , TO_CHAR(TC.EULA_DATE, 'YYYY-MM-DD') AS "최초통화일"
            , TO_CHAR(TC.START_DATE, 'YYYY-MM-DD') AS "보험가입일"
            , TO_CHAR(TC.END_DATE, 'YYYY-MM-DD') AS "보험해지일"
            , TC.INSURER_CODE AS "보험사"
            , DECODE(TC.STATUS_CODE, 'ACTV', '가입', 'SUSPEND', '미납', 'TRMNREQTD', '해지예약', 'TRMNTD', '해지') AS "보험상태"
            , TC.TAG_CODE AS "비대면솔루션값"
            , TP.PROMOTION_YN AS 프로모션유무
            , TC.START_DATE
        FROM SC_TPA.TB_CONTRACT TC
        INNER JOIN SC_TPA.TB_PROGRAM_INFO TP
        ON TC.PROGRAM_CODE = TP.PROGRAM_CODE
        WHERE 1=1
        AND TC.START_DATE <= TO_DATE('{end_date} 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
        AND TP.PROGRAM_CODE NOT LIKE 'KORSTG%' -- 테스트 데이터 삭제
        ORDER BY TC.START_DATE
        '''
        return sentence
    
    @staticmethod
    def member_close(end_date: str=None, promotion_only: bool=None) -> str:
        '''
        Parameter
        ---
        end_date : 해당 날짜까지의 데이터. 마감일 기준으로 입력
        '''
        if promotion_only:
            sentence = f'''
            SELECT
                A.PROGRAM_CODE AS "상품정보"
                , B.PROGRAM_NAME AS "프로그램명"
                , B.MONTHLY_PREMIUM AS "월요금"
                , A.POLICY_ID
                , A.ENROLLED_MODEL AS "가입모델명"
                , NVL(SC_TPA.F_CRYPT_DEC(A.IMEI),'') AS "IMEI"
                , TO_CHAR(A.START_DATE, 'YYYY-MM-DD') AS "보험가입일"
                , TO_CHAR(A.END_DATE, 'YYYY-MM-DD') AS "보험해지일"
                , A.INSURER_CODE AS "보험사"
                , DECODE(A.STATUS_CODE, 'ACTV', '가입', 'SUSPEND', '미납', 'TRMNREQTD', '해지예약', 'TRMNTD', '해지') AS "보험상태"
                , A.TAG_CODE AS "비대면솔루션값"
                , TO_CHAR(ADD_MONTHS(A.START_DATE, B.PROMOTION_MONTH),'YYYY-MM-DD') AS "무상 종료일"
                , CASE B.CATE_FIRST
                        WHEN '유상상품' THEN '유상'
                        WHEN '프로모션' THEN
                            CASE WHEN TO_CHAR(ADD_MONTHS(A.START_DATE, B.PROMOTION_MONTH), 'YYYYMMDD') < TO_CHAR(SYSDATE, 'YYYYMMDD')  THEN '전환'
                            ELSE '무상'
                            END
                        ELSE '오류' || '-' ||B.CATE_FIRST
                    END AS "유무상 구분"
                    ,B.PROMOTION_MONTH AS "무상 기간"
                    ,B.CLOSE_YEAR AS "정산년도"
            FROM SC_TPA.TB_CONTRACT A
            INNER JOIN SC_TPA.TB_PROGRAM_INFO B
            ON A.PROGRAM_CODE = B.PROGRAM_CODE
            WHERE 1=1
            AND A.START_DATE <= TO_DATE('{end_date} 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
            AND A.POLICY_ID NOT LIKE 'TES%' 
            AND A.POLICY_ID NOT LIKE 'KOR99%'
            AND A.POLICY_ID NOT LIKE 'KORTEST%'
            AND B.PROGRAM_CODE NOT LIKE 'KORSTG%'
            AND B.PROMOTION_YN = 'Y'
            ORDER BY A.START_DATE ASC
        '''            
        else:
            sentence = f'''
            SELECT
                A.PROGRAM_CODE AS "상품정보"
                , B.PROGRAM_NAME AS "프로그램명"
                , B.MONTHLY_PREMIUM AS "월요금"
                , A.POLICY_ID
                , A.ENROLLED_MODEL AS "가입모델명"
                , NVL(SC_TPA.F_CRYPT_DEC(A.IMEI),'') AS "IMEI"
                , TO_CHAR(A.START_DATE, 'YYYY-MM-DD') AS "보험가입일"
                , TO_CHAR(A.END_DATE, 'YYYY-MM-DD') AS "보험해지일"
                , A.INSURER_CODE AS "보험사"
                , DECODE(A.STATUS_CODE, 'ACTV', '가입', 'SUSPEND', '미납', 'TRMNREQTD', '해지예약', 'TRMNTD', '해지') AS "보험상태"
                , A.TAG_CODE AS "비대면솔루션값"
                , TO_CHAR(ADD_MONTHS(A.START_DATE, B.PROMOTION_MONTH),'YYYY-MM-DD') AS "무상 종료일"
                , CASE B.CATE_FIRST
                        WHEN '유상상품' THEN '유상'
                        WHEN '프로모션' THEN
                            CASE WHEN TO_CHAR(ADD_MONTHS(A.START_DATE, B.PROMOTION_MONTH), 'YYYYMMDD') < TO_CHAR(SYSDATE, 'YYYYMMDD')  THEN '전환'
                            ELSE '무상'
                            END
                        ELSE '오류' || '-' ||B.CATE_FIRST
                    END AS "유무상 구분"
                    ,B.PROMOTION_MONTH AS "무상 기간"
                    ,B.CLOSE_YEAR AS "정산년도"
            FROM SC_TPA.TB_CONTRACT A
            INNER JOIN SC_TPA.TB_PROGRAM_INFO B
            ON A.PROGRAM_CODE = B.PROGRAM_CODE
            WHERE 1=1
            AND A.START_DATE <= TO_DATE('{end_date} 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
            AND A.POLICY_ID NOT LIKE 'TES%' 
            AND A.POLICY_ID NOT LIKE 'KOR99%'
            AND A.POLICY_ID NOT LIKE 'KORTEST%'
            AND B.PROGRAM_CODE NOT LIKE 'KORSTG%'
            ORDER BY A.START_DATE ASC
        '''
        return sentence
    
    @staticmethod
    def claim(end_date: str=None) -> str:
        '''
        Parameter
        ---
        end_date : 해당 날짜까지의 데이터. 마감일 기준으로 입력
        '''
        start_date = datetime.strptime(end_date, '%Y-%m-%d')
        start_date = datetime.strftime(
            start_date - timedelta(days=100),
            '%Y-%m-%d'
        )
        sentence = f'''
        SELECT
            TCL.POLICY_ID,
            TC.PROGRAM_CODE,
            TC.INSURER_CODE,
            TO_CHAR(TCR.REG_DTM,'YYYY-MM-DD') AS END_DATE
        FROM SC_TPA.TB_CLAIM TCL
        INNER JOIN SC_TPA.TB_CONTRACT TC
        ON TCL.POLICY_ID = TC.POLICY_ID
        INNER JOIN SC_TPA.TB_CLAIM_REPAIR TCR
        ON TCL.CLAIM_ID = TCR.CLAIM_ID
        WHERE EVENT_TYPE='RepairDetail'
        AND TCL.START_DATE BETWEEN TO_DATE('{start_date} 00:00:00', 'YYYY-MM-DD HH24:MI:SS) AND TO_DATE('{end_date} 23:59:59', 'YYYY-MM-DD HH24:MI:SS)
        ORDER BY TCL.MOD_DTM
        '''
        return sentence
    
    @staticmethod
    def program_info() -> str:
        '''
        프로그램 인포 테이블.
        
        파라미터 없음.
        '''
        sentence = '''
        SELECT
            *
        FROM SC_TPA.TB_PROGRAM_INFO
        '''
        return sentence