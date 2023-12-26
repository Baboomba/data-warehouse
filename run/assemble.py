from preprocessing.raw_data import ExternalRawData
from data.control import BackUp
from analysis.monthly_close import PaidProductCount

def paid_close(toss_raw: bool, samsung_raw: bool, backup_date: str):
    if toss_raw & samsung_raw:
        
        if backup_date:

            try:
                BackUp(file_name='toss_raw', close_date=backup_date)
                BackUp(file_name='samsung_raw', close_date=backup_date)
                BackUp(file_name='toss_payment', close_date=backup_date)
            except Exception as e:
                raise print(f'backup failed : {e}')
            
        try:
            ex = ExternalRawData()
            ex.SamsungClose(True, False, True)
            ex.TossClose(False, False, True)
            ex.MergedCloseData(True, True)
        except Exception as e:
            raise print(f'transforming files failed : {e}')
        
        close = PaidProductCount()
        close.ProcessAdditionalData(True) # to excel
        print('process completed')