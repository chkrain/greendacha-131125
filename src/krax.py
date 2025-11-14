from pyplc.platform import plc
from gear import GearROT, GearFQ, Feeder
from sys import platform
from misc import Factory
from mbfqconverters import FQConv
from pyplc.utils.trig import RTRIG
from pyplc.utils.misc import TP
from pyplc.utils.misc import TON
from collections import namedtuple


if platform=='vscode':
    PLC = namedtuple('PLC', ('CONV_ON_1', 'CONV_ON_2', 'RCONV_ON_1', 'RCONV_ON_2', 'SIGNAL', 'GATE', 'BELT_1', 'BELT_2', 'BELT_3', 'EMERGENCY'))
    plc = PLC()

factory_1 = Factory(emergency=plc.EMERGENCY)

fq_1 = FQConv(addr=1)
fq_2 = FQConv(addr=2)
fq_3 = FQConv(addr=3)

conv_1 = Feeder(q=plc.CONV_ON_1, fault=fq_1.fault, lock=plc.EMERGENCY, rot=plc.BELT_1, fq=fq_1.set_fq)
conv_2 = Feeder(q=plc.CONV_ON_2, fault=fq_2.fault, lock=plc.EMERGENCY, rot=plc.BELT_2, fq=fq_2.set_fq)
conv_3_r = Feeder(q=plc.RCONV_ON_1, fault=fq_3.fault, lock=plc.EMERGENCY, rot=plc.BELT_3, fq=fq_3.set_fq)
conv_3_l = Feeder(q=plc.RCONV_ON_2, fault=fq_3.fault, lock=plc.EMERGENCY, rot=plc.BELT_3, fq=-(fq_3.set_fq))

emergency_stoppable = (conv_1, conv_2, conv_3_r, conv_3_l)
factory_1.on_emergency = [ g.emergency for g in emergency_stoppable ]

def run(on: bool):
    conv_1.on = on

def notRun(off: bool):
    conv_1.off = off

def run_2(on: bool):
    conv_2.on = on

def notRun_2(off: bool):
    conv_2.off = off

instances = (factory_1, conv_1, conv_2, conv_3_l, conv_3_r, fq_1, fq_2, fq_3,
             RTRIG(clk=lambda: plc.SIGNAL==False, q=run),
             RTRIG(clk=lambda: plc.SIGNAL==True, q=notRun),
             RTRIG(clk=lambda: plc.GATE==False, q=notRun_2),
             RTRIG(clk=lambda: plc.GATE==True, q=run_2))

if platform=='linux':
    from imitation import IMotor,IRotation
    ibelt_1 = IRotation( q = plc.CONV_ON_1, rot = plc.BELT_1 )
    ibelt_2 = IRotation( q = plc.CONV_ON_2, rot = plc.BELT_2 )
    ibelt_3 = IRotation( q = plc.CONV_ON_3, rot = plc.BELT_3 )

    plc.force(EMERGENCY = True)
    
plc.run( instances=instances, ctx=globals() )
