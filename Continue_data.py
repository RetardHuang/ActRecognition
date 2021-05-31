#This Program is aimed to collect data with of JY901 of 3 seconds.
from HexProcessing import BlueZHexUnit
from forBlueToothConnect import pourBluz
import threading
import joblib
from Process import Calculate
import numpy as np
#from scipy.fftpack import fft,ifft


def output_store(result):
    global type_counter, store_counter, temp
    temp[0,store_counter] = result
    store_counter = store_counter+1

def output_select():
    global store_counter, result, temp
    store_counter = 2
    # output = 0
    if np.sum(temp) == 0:
        result = 0
    elif temp[0] == 1 and temp[1] == 1 and temp[2] == 1:
        result = 1
    elif temp[0] == 2 and temp[1] == 2 and temp[2] == 2:
        result = 2
    elif temp[0] == 3 and temp[1] == 3 and temp[2] == 3:
        result = 3
    elif temp[0] == 4 and temp[1] == 4 and temp[2] == 4:
        result = 4

    temp = temp[[1,2,0]]

temp = np.zeros((1,3))
store_counter = 0




global Data, Bluemodule
class BHRecog(BlueZHexUnit,Calculate):
    def __init__(self):#Init Step must contain the length of window
        BlueZHexUnit.__init__(self)
        Calculate.__init__(self)
        self.leftedge=0
        self.stepLength=50
    ######################################
    ######################################
    def recognize(self):#此函数会不断循环进行，如果提前调用并只调用一次model，就在 _init_里面调用
        #print('Data pool is full, start a recognition')
        self.proAWin(self.FullValueList[0:self.windowLength])
        self.featureRecognize()
        # output_store(self.Labelstate)
        # if store_counter == 3:
        #     output_select()  # final output
        #     print(result)
        #这里就是开始识别代码的地方：
        #直接使用self.Feature[0]类似的调用特征
        print('The state is:',self.Labelstate)
        if self.Labelstate==0:
            print("保持不动")
        elif self.Labelstate==1:
            print("正在走路或者小型动作")
        elif self.Labelstate==2:
            print("正在走路或者小型动作")
            #print("正在进行坐下的动作")
        elif self.Labelstate==3:
            print("请注意，可能正在摔倒！")
        elif self.Labelstate==4:
            print("可能正在捡东西")
    ######################################
    ######################################
    def setWindowLength(self,wlength):
        self.windowLength=wlength
    def lopClimb(self):#To Reconize the action
        while True:
            if len(self.FullValueList) > (self.windowLength+self.stepLength):
                del self.FullValueList[0:self.stepLength]
                #print('Pool length is',len(self.FullValueList))
                self.recognize()####################################
                print(self.Feature)


    def lopcoupData(self):#To get the data, which need to be assgined into another thread
        global Bluemodule
        while True:
            #print('Receiving a new data train')
            self.coupData(Bluemodule.naivesReceiveHex())

if __name__=='__main__':
    Data= BHRecog()
    Data.loadModel()
    Data.setWindowLength(400)
    Bluemodule=pourBluz()
    Bluemodule.connect()#Connect to bluetooth module
    Read = threading.Thread(target=Data.lopcoupData, name='ReadTheData')
    Clim = threading.Thread(target=Data.lopClimb, name='ClimbTheData')
    Read.start()
    Clim.start()
    Read.join()
    Clim.join()




