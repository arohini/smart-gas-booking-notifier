import serial
from time import sleep
from threading import Thread
import threading
import ConfigParser
import traceback

config = ConfigParser.ConfigParser()
config.readfp(open(r'config.cfg'))
phone_num = config.get('contacts', 'phonenum')
min_weight = config.get('contacts', 'min_weight')
gas_agency_num = config.get('contacts', 'gas_agency')

resume=threading.Event()

def weight_read():
    global config_arr
    global resume
    while True :
        try:
            ser=serial.Serial('/dev/ttyAMA0',9600,timeout=1)
            ser.flush()
            num=ser.inWaiting()
            if(num != 0):
                s=ser.read(num)
                print "weight",s
                weight= s.split(" Kg.")[0]
                if(float(weight) < 4):
                    resume.clear()
                    call_number(phone_num)
                    print "calling"
            ser.close()
        except:
            print traceback.format_exc()
            print "...."


def call_number(phnum):
   try: 
        global resume
        ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
        ser.flush()
        print "Calling ...",phnum
        cmd="ATD"+str(phnum)+";\r"
        ser.write(cmd)
        sleep(15)
        ser.write('ATH\r')
        ser.close()
   except:
        print "call_error"
        resume.set()
   

try:
    resume.set()
    wt_thread=Thread(target = weight_read)
    wt_thread.start()
    wt_thread.join()   
except:
    print traceback.format_exc()
    

    
