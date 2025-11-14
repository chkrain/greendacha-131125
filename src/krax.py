"""
Main application module

Ниже идёт ваша программа
"""

from pyplc.platform import plc
from sys import platform
from collections import namedtuple

if platform=='vscode':
    PLC = namedtuple('PLC', (''))
    plc = PLC()

instances = ()

if platform=='linux':
    instances += ()
    
plc.run( instances=instances, ctx=globals() )
