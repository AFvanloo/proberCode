import numpy as np
import pyvisa
import time


#If instruments are sufficiently static, we can use:
import proberConfig as pc #can probably be removed


#We could hardcode this here instead of in config
config = pc.config()
vSourceadr = config['sourceAddress']
KeithelyIadr = config['iMeasAddress']
KeithelyVadr = config['vMeasAddress']
SRSDadr = config['srsDAddress']
SRSPadr = config['srsDAddress']


def connectInstruments():
    #find GPIB addresses
    #rm = pyvisa.ResourceManager()
    #self.resourceList = rm.list_resources()
    #which is which?
    #return address is order: yoko source, Keithly V, Keithley I, SRS preamp, SRS diff amp
    #return None if not found


    #dummy return
    return [3,5,8,None,7897]


def measVp():
    #visaGet(msg)
    #parse return message
    #return result
    return np.random.rand()*100

def measVm():
    #visaGet(msg)
    #parse return message
    #return result
    return np.random.rand()*-100

def measIp():
    #visaGet(msg)
    #parse return message
    #return result
    return np.random.rand()*100

def measIm():
    #visaGet(msg)
    #parse return message
    #return result
    return np.random.rand()*-100

def setSource(mV):
    #Do a get after set
    #check that the gotten value is the sent value
    #return True if so
    return True


def sourceOutput(status):
    #set output on or off
    #visaWrite()
    #check if on
    time.sleep(.01)
    #visaRead(on?)
    #parse, check if asked status is status

    #use get after set
    return True

#====================Communication utilities==================


def visaWrite(adr, mesg, get_after_set=True):
    pass
    #implement get_after_set
    #send visa message
    #sleep 10ms
    if get_after_set:
        time.sleep(.01)
        #if parsed output == input:
            #return True
        #else:
            #return False
    #ask instrument value
    #iVal = visa.ask() 
    #check if not ival == val
        #return False
    #else:
    #    return True


def visaRead(adr, mesg):
    pass
    #send visa message
    #output = visa....(mesg)
    #parse output

    #return output

def reversePolarity():
    pass







def probe(voltage, wait=.5, uvA=100, gain=100):
    #set voltage
    
    #switch output on
    sourceOutput('ON')

    time.sleep(wait)
    Vp = measVp()
    Ip = measIp()

    #toggle polarity
    time.sleep(wait)
    Vm = measVm()
    Im = measIm()

    #switch output off
    
    R = calcR(Vp, Vm, Ip, Im, uvA, gain)
    print('probing')
    return Vp, Vm, Ip, Im, R

def calcR(Vp, Vm, Ip, Im, uvA=100, gain=100):
    '''
    Calculates R. Assumes SI values (ie, Volts and Volts)
    '''
    Rp = Vp*uvA*1e-6/(Ip/gain)
    Rm = Im*uvA*1e-6/(Im/gain)
    return (Rp+Rm)/2

def IV(uvA=100, gain=100):
    pass
    #


#================dummy measurement functions=====================

