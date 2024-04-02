from config import LOG_DIR, LOG_SETTINGS
from datetime import datetime
import logging
import os


class Logger:
    '''
    로그를 기록하고 출력하는 클래스
    새로운 인스턴스를 생성할 때마다 새로운 파일을 만듦.
    하나의 인스턴스는 하나의 파일에 계속해서 기록을 덧붙여 나감.


    Parameter
    ---
    logger_name(str) : 로거 이름

    log_level(str) : 'debug', 'info', 'warning', 'error', 'critical' 중 하나의 값을 가짐

    path(str) : 로그 파일이 저장될 경로 >>> config.py의 LOG_DIR 변수 편집

    console_log(bool) : 로그 내용을 출력할 것인지 여부


    Example
    ---
    >>> logger = Logger('test', 'error', 'analysis')
    >>> logger.write_log('you entered the wrong number')
    >>> logger.set_level('info')
    >>> logger.write_log('result has just been saved.')

    '''
    def __init__(self, log_level: str=None, path: str=None, console_log: bool=True) -> None:
        logging.Logger.manager.loggerDict.clear()
        self._logger_name = None
        self._logger = logging.getLogger(self._logger_name)
        self._console_log = console_log
        self.log_level = log_level
        self._log_level = self.set_level(self.log_level)
        self._file_name = self._create_log_file(path)
        self._formatter = self._set_formatter()

    def _create_log_file(self, path):
        '''
        로그 파일의 이름과 경로를 결정하는 매서드
        '''
        self._make_diretory(path)
        time = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = fr'{path}_{time}.log'
        return fr'{LOG_DIR[path]}/{file_name}'
    
    def _make_diretory(self, path):
        '''
        LOG_DIR에 적힌 경로에 디렉터리가 없을 경우 생성하는 메서드
        '''
        if not os.path.exists(LOG_DIR[path]):
            os.makedirs(LOG_DIR[path])
        else:
            pass
        
    def set_level(self, log_level: str=None) -> None:
        '''
        로그 수준을 결정하는 매서드

        하나의 인스턴스에서도 로그 레벨은 계속해서 바꿀 수 있음
        '''
        self.log_level = log_level
        
        if log_level == "debug":
            self._logger.setLevel(logging.DEBUG)
        elif log_level == "info":
            self._logger.setLevel(logging.INFO)        
        elif log_level == "warning":
            self._logger.setLevel(logging.WARNING)        
        elif log_level == "error":
            self._logger.setLevel(logging.ERROR)
        elif log_level == "critical":
            self._logger.setLevel(logging.CRITICAL)
        else:
            print("[log level error] wrong parameter. select one of 'debug', 'waring', 'info', 'error', 'critical'")
    
    def write_log(self, msg: str=None) -> None:
        '''
        메시지를 기록하고 출력하는 메서드.
        '''
        if self.log_level == "debug":
            self._logger.debug(msg)
        elif self.log_level == "info":
            self._logger.info(msg)
        elif self.log_level == "warning":
            self._logger.warning(msg)
        elif self.log_level == "error":
            self._logger.error(msg)
        elif self.log_level == "critical":
            self._logger.critical(msg)
        else:
            print("[log massage error] wrong parameter. select one of 'debug', 'waring', 'info', 'error', 'critical'")
        
        if self._console_log:
            self.print_log(msg)
            
    def write_info(self, msg: str=None):
        self._logger.setLevel(logging.INFO)
        self._logger.info(msg)
        
    def write_error(self, msg: str=None):
        self._logger.setLevel(logging.ERROR)
        self._logger.error(msg)
    
    def print_log(self, msg: str=None):
        formatted_msg = self._formatter.format(logging.LogRecord(
            name=self._logger_name,
            level=self.log_level,
            pathname=self._file_name,
            lineno=1,
            msg=msg,
            args=None,
            exc_info=None
        ))
        print(formatted_msg)

    def set_handler(handler_func):
        '''
        로깅 핸들러를 추가하는 데코레이터
        '''

        def wrapper(self, *args, **kwargs):
            handler = handler_func(self, *args, **kwargs)
            self._logger.addHandler(handler)
            return handler
        
        return wrapper
    
    @set_handler
    def _file_handler(self):
        '''
        로그 파일을 생성하는 메서드
        '''
        return logging.FileHandler(
            filename=self._file_name,
            mode=LOG_SETTINGS['mode'],
            encoding=LOG_SETTINGS['encoding']
        )
    
    @set_handler
    def _stream_handler(self):
        '''
        로그 출력을 생성하는 메서드
        '''
        return logging.StreamHandler()
    
    def _set_formatter(self):
        '''
        핸들러의 포맷을 결정하는 메서드
        '''
        formatter = logging.Formatter('[%(levelname)s] %(asctime)s : %(message)s')
        handler = self._file_handler()
        handler.setFormatter(formatter)
        return formatter
    
    def exception(self, msg : str=None):
        '''
        예외 발생 로그 기록을 위한 메서드
        '''
        exc_msg = '(exception) ' + msg
        self.set_level('error')
        self.write_log(exc_msg)
        return Exception(exc_msg)