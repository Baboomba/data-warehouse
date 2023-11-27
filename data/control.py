from config import DATA_PATH, BACKUP
import os
import shutil



class BackUp:
    '''
    Parameter
    ---
    
    file_name >>> refers the keys of DATA_PATH and BACKUP
    
    close_date >>> in the form like 20231030
    '''
    def __init__(self, file_name: str, close_date: str) -> None:
        self.file_name = file_name
        self.close_date = close_date
        self.save_name = self.destination_name()
        self.copy()
            
    def destination_name(self):
        return f'{self.file_name}_{self.close_date}.parquet'
    
    def create_destination(self):
        return os.path.join(BACKUP[self.file_name], self.save_name)
    
    def copy(self):
        original_path = DATA_PATH[self.file_name]
        backup_path = self.create_destination()
        
        try:
            shutil.copy(original_path, backup_path)
        except FileNotFoundError as e:
            print(e)