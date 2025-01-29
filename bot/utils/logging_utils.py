import logging

# Настройка логирования (если не настроено ранее)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="bot_log.log",
    filemode="a"
)

def log_function_call(func: object) -> object:
    """
    Декоратор для логирования вызовов функций.
    :rtype: object
    """
    def wrapper(*args, **kwargs):
        logging.info(u"Вызвана функция: {} с аргументами: args={}, kwargs={}".format(
            func.__name__, args, kwargs
        ))
        try:
            result = func(*args, **kwargs)
            logging.info(u"Функция {} завершилась успешно".format(func.__name__))
            return result
        except Exception as e:
            logging.error(u"Ошибка в функции {}: {}".format(func.__name__, str(e)))
            raise
    return wrapper
