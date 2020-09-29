import numpy as np
import pyvisa
import time

rm = pyvisa.ResourceManager('@py')



#If instruments are sufficiently static, we can use:
import proberConfig as pc #can probably be removed


#We could hardcode this here instead of in config
config = pc.config()
yokoAdr = config['sourceAddress']
KIAdr = config['iMeasAddress']
KVAdr = config['vMeasAddress']
#SRSDadr = config['srsDAddress']
#SRSPadr = config['srsDAddress']

print('yokoAdr is ', yokoAdr)




def connectInstruments():
    #find GPIB addresses
    rm = pyvisa.ResourceManager('@py')
    #GPIB instruments -- do they exist?
    connections = []
    for adr in [yokoAdr, KIAdr, KVAdr]:
        try:
            instName = visaRead(adr, mesg='*IDN?')
            print('instrument ', instName, ' is connected at ', adr)
            connections.append(True)
        except:
            print('No instrument at address', adr)
    #RS232
    #TODO
    #self.resourceList = rm.list_resources()
    #which is which?
    #return address is order: yoko source, Keithly V, Keithley I, SRS preamp, SRS diff amp
    #return None if not found

    initSource()
    return connections

def initSource(Vrange=1.):
    #set as voltage source
    visaWrite(yokoAdr, ':SOUR:FUNC VOLT')
    #set range
    visaWrite(yokoAdr, ':SOUR:RANGE 1')
    #set output off
    setSourceOutput(0)
    #set voltage to zero
    setSourceVoltage(0)


    


def measV():
    #visaGet(msg)
    V = visaRead(KVAdr, mesg='FETCH?')
    return float(V)


def measI():
    #visaGet(msg)
    I = visaRead(KIAdr, mesg='FETCH?')
    return float(I)


def setSourceVoltage(V):

    if abs(V) > 1:
        print('Trying to set source outside its range')
        return
    mesg = ':SOUR:LEV '+str(V)
    ans = visaWrite(yokoAdr, mesg)
    #return True if so
    return ans


def setSourceOutput(status):
    '''
    sets the output state. 

    INPUT: 0 for off, 1 for on
    '''
    if status in ['on', 'On', 'ON']:
        status = 1
    if status in ['off', 'Off', 'OFF']:
        status = 0

    #set output on or off
    mesg = ':OUTP ' + str(int(status))
    ans = visaWrite(yokoAdr, mesg)
    return ans

#====================Communication utilities==================


def visaWrite(adr, mesg, get_after_set=True):
    pass
    #implement get_after_set
    #send visa message
    #sleep 10ms
    #construct string
    gpibAdr = 'GPIB0::'+str(int(adr))+'::INSTR'
    inst = rm.open_resource(gpibAdr)

    #set
    inst.write(mesg)
    time.sleep(.01)
    #formulate question variant of mesg
    
    mesgParts = mesg.split(' ')
    question = mesgParts[0]
    inst.write((question+'?'))
    ans = inst.read()
    
    if ord(mesgParts[1][0]) < 58:
        #we have a number
        if float(ans) == float(mesgParts[1]):
            return True
        else:
            return False
    else:
        #assume the string is letters
        if ans[:-1] in mesgParts[1]:
            return True



    #if get_after_set:
    #    time.sleep(.01)
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


def visaRead(adr, mesg='READ?'):
    
    gpibAdr = 'GPIB0::'+str(int(adr))+'::INSTR'
    inst = rm.open_resource(gpibAdr)

    #send visa message
    inst.write(mesg)
    ans  = inst.read()[:-1]
    return ans


def reversePolarity():
    pass







def probe(voltage, wait=.5, uvA=100, gain=100, avs=10):
    
    print('probing')
    #set voltage
    setSourceVoltage(voltage)
    #switch output on
    setSourceOutput('ON')

    
    time.sleep(wait)

    #measure
    Vps, Ips = [], []
    for i in range(avs):
        Vps.append(measV())
        Ips.append(measI())
        time.sleep(.01)
    Vp = np.mean(Vps)
    Ip = np.mean(Ips)

    #toggle polarity
    setSourceVoltage(-1*voltage)
    time.sleep(wait)

    Vms, Ims = [], []
    for i in range(avs):
        Vms.append(measV())
        Ims.append(measI())
        time.sleep(.01)
    Vm = np.mean(Vms)
    Im = np.mean(Ims)

    #switch output off
    setSourceOutput('OFF')
    
    R = calcR(Vp, Vm, Ip, Im, uvA, gain)
    return Vp, Vm, Ip, Im, R

def calcR(Vp, Vm, Ip, Im, uvA=1, gain=100):
    '''
    Calculates R. Assumes SI values (ie, Volts and Volts)
    '''
    Vpp = Vp/gain
    Ipp = Ip*uvA*1e-6
    Vmm = Vm/gain
    Imm = Im*uvA*1e-6
    R = (Vpp-Vmm)/(Ipp-Imm)
    print('Measured resistance to be ', R)
    return R

def IV(uvA=100, gain=100):
    pass
    #


#================dummy measurement functions=====================

