import configparser
from typing import Callable, Tuple


def ini_reader(func: Callable[[str], Tuple[str, str]]=None) -> Callable[..., str]:

    def wrapper(*args, **kwargs) -> str:
        config_path = 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_path)
        section, key = func(*args, **kwargs)
        value = config.get(section, key)
        return value

    return wrapper

@ini_reader
def DATA_PATH(key: str=None) -> Tuple[str, str]:
    return 'DATA_PATH', key

@ini_reader
def DATA_DIR(key: str=None) -> Tuple[str, str]:
    return 'DATA_DIR', key

@ini_reader
def ORACLE_ACCOUNT(key: str=None) -> Tuple[str, str]:
    return 'ORACLE_ACCOUNT', key

@ini_reader
def BACK_UP(key: str=None) -> Tuple[str, str]:
    return 'BACK_UP', key

@ini_reader
def LOG_DIR(key: str=None) -> Tuple[str, str]:
    return 'LOG_DIR', key

@ini_reader
def LOG_SETTINGS(key: str=None) -> Tuple[str, str]:
    return 'LOG_SETTINGS', key