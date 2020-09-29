import subprocess
import time

def findAddress():
    df = subprocess.check_output("lsusb")
    lines = df.split(b'\n')
    for line in lines:
        strLine = str(line)
        if 'National' in strLine:
            busNum = int(strLine[6:9])
            devNum = int(strLine[17:20])
            print('Found GPIB device at bus ', busNum, ' Device: ', devNum)
            return busNum, devNum
    print('GPIB USB device not found')
    return False
                

def uploadFirmware(busNum, devNum):
    comm1 = 'sudo fxload -D /dev/bus/usb/' + str(busNum).zfill(3) + '/' + str(devNum).zfill(3)
    comm2 = ' -I /home/pi/linux-gpib/ni_usb_b_firmware/niusbb_firmware.hex -s /home/pi/linux-gpib/ni_usb_b_firmware/niusbb_loader.hex'
    command = comm1 + comm2
    subprocess.run(command, shell=True)

def theRest():
    subprocess.run('sudo modprobe gpib_common', shell=True)
    time.sleep(.1)
    subprocess.run('sudo modprobe ni_usb_gpib', shell=True)
    time.sleep(.1)
    subprocess.run('sudo gpib_config', shell=True)
    time.sleep(.1)
    #give access to the gpib device
    subprocess.run('sudo chmod 666 /dev/gpib0', shell=True)

    #Now update the code
    #subprocess.run(
    #outp = subprocess.check_output('/home/pi/updateProber.sh')
    #print(outp)

    #Finally, start the program
    subprocess.run('python3 /home/pi/Desktop/proberCode/prober.pyw', shell=True)
    return

def main():
    #find address
    busNum, devNum = findAddress()
    #upload firmware
    uploadFirmware(busNum, devNum)
    print('uploading firmware, first time')
    time.sleep(3)
    #find address
    busNum, devNum = findAddress()
    #upload firmware
    uploadFirmware(busNum, devNum)
    print('uploading firmware, second time')
    time.sleep(3)

    #do the rest: modprobe and gpib_config
    theRest()
    #sudo gpib_config

if __name__ == '__main__':
    main()
