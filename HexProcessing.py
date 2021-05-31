import forBlueToothConnect as BTC
import re
from copy import deepcopy as cp
class BlueZHexUnit:
    pattern = re.compile('.{2}')
    HexList=list([list(['']*6)]*4)
    ValueList=list([list([0]*3)]*4)
    ucRxBuffer=list(['']*15)
    FullValueList=[]
    def __init__(self):
        self.ucRxCnt = 0  # 0 at initial
    def HexSinProcess(self,j,i):
        Unsigned=(int((self.HexList[j][i+1]),16)<< 8) | (int(self.HexList[j][i],16))
        if Unsigned < 0x8000:
            return Unsigned
        else:
            return (Unsigned - 0x10000)
    def coupData(self,ReceivedHexString):
        HexPairs=self.pattern.findall(ReceivedHexString)#This two is use to split with interval two
        for aPair in HexPairs:
            self.ucRxBuffer[self.ucRxCnt] = aPair
            self.ucRxCnt += 1  # 0 at initial
            if self.ucRxBuffer[0]!='55':#If the first received is 55
                self.ucRxCnt = 0
                continue
            if self.ucRxCnt < 11:
                continue
            else:
                if self.ucRxBuffer[1] == '51':
                    self.HexList[0] = cp(self.ucRxBuffer[2:8])
                    smList=[]
                    for i in [0,2,4]:#因为存在校验位的缘故 所以会这样！
                        smList.append(self.HexSinProcess(0,i)/32768* 16)
                    self.ValueList[0]= cp(smList)
                elif self.ucRxBuffer[1] == '52':
                    self.HexList[1] = cp(self.ucRxBuffer[2:8])
                    smList=[]
                    for i in [0,2,4]:
                        smList.append(self.HexSinProcess(1,i) / 32768 * 2000 )
                    self.ValueList[1]= cp(smList)
                elif self.ucRxBuffer[1] == '53':
                    self.HexList[2] = cp(self.ucRxBuffer[2:8])
                    smList=[]
                    for i in [0,2,4]:
                        smList.append(self.HexSinProcess(2,i) / 32768 * 180 )
                    self.ValueList[2]= cp(smList)
                elif self.ucRxBuffer[1] == '54':
                    self.HexList[3] = cp(self.ucRxBuffer[2:8])
                    smList=[]
                    for i in [0,2,4]:
                        smList.append(self.HexSinProcess(3,i) )
                    self.ValueList[3]= cp(smList)
                    self.FullValueList.append(cp(self.ValueList))
                self.ucRxCnt =0
    def allclear(self):
        self.HexList=list([list(['']*6)]*4)
        self.ValueList=list([list([0]*3)]*4)
        self.FullValueList=[]


if __name__=='__main__':
    Jazz=BTC.pourBluz()
    Jazz.connect()
    Data=BlueZHexUnit()
    while True:
        aLine=Jazz.naivesReceiveHex()
        Data.coupData(aLine)
        print(Data.ValueList)
