import bluetooth
import time
class pourBluz:
    bd_addr = "98:D3:21:FC:82:A8"
    port = 1
    def __init__(self):
        pass
    def BluetoothAddressChange(self,BluetoothAddress):
        self.bd_addr=BluetoothAddress
    def BluetoothPortChange(self,port):
        self.port=port
    def connect(self):
        while True:
            try:
                self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                self.sock.connect((self.bd_addr, self.port))
                break
            except OSError:
                print('Connection failed, try again...')
                time.sleep(0.1)
    def naivesReceiveString(self):
        return self.sock.recv(1024).decode('utf-8','ignore')
    def naivesReceive(self):
        return self.sock.recv(65536)
    def naivesReceiveHex(self):
        return self.sock.recv(1024).hex()#The type of return value is STR
    def Hex55kai(self):
        count=0
        receivedHex=''
        while True:
            aLine=self.naivesReceiveHex()
            if aLine == '55':
                print(receivedHex)
                print(count)
                count+=1
                receivedHex=aLine
            else:
                receivedHex=receivedHex+aLine
    def received_string(self):
        return str(self.receive(),'utf-8')
    def close(self):
        self.sock.close()


if __name__=='__main__':
    Jazz=pourBluz()
    Jazz.connect()
    while True:
        print(Jazz.naivesReceiveHex())
