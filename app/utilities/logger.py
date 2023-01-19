import logging

mylogger = logging.getLogger("myLogger")

assert mylogger.level == logging.NOTSET
assert mylogger.getEffectiveLevel() == logging.WARN

handlerConsola = logging.StreamHandler()
mylogger.addHandler(handlerConsola)
# mylogger.setLevel(logging.DEBUG)