#This Program is aimed to collect data with of JY901 of 3 seconds.
from HexProcessing import BlueZHexUnit
from forBlueToothConnect import pourBluz
from Process import Calculate

import time
import  numpy as np
global Data, Bluemodule, NumberOfTests, Label
Data=BlueZHexUnit()
Bluemodule=pourBluz()
NumberOfTests=5
TimeOfAWindow=3
Calculating=Calculate(Data.windowLength)

Bluemodule.connect()#Connect to bluetooth module
Starttime=time.time()#Record Start Time
for shit in range(1,NumberOfTests+1):
    Starttime=time.time()
    while True:
        Data.coupData(Bluemodule.naivesReceiveHex())#Read Every string come from HC05.Process it ,and save them in Data.FullValueList
        Endtime=time.time()#Record time
        SampleTime=Endtime-Starttime
        if SampleTime>=TimeOfAWindow:
            print ('This sampling time is: ',SampleTime,'s')
            Calculating.proAWin(Data.TruOut())
            Calculating.putin(shit-1)
            Data.allclear()
            #time.sleep(0.5)#This step can bed added to another thread
            print('Rest!')
            #time.sleep(2)#This step can bed added to another thread
            break
        else:
            continue
Bluemodule.close()
print(Calculating.FullFeature)
Calculating.SavewithLabel(0)

