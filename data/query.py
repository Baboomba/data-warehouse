



class QuerySet:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def sales_performance(start: str=None):
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
        AND c.start_date >= TO_DATE('{start}', 'YYYY-MM-DD')
        AND (c.shop_code IS NOT NULL
        OR c.sales_pro IS NOT NULL)
        ORDER BY c.start_date ASC
        '''
        return sentence