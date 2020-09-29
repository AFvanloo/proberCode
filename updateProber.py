import os
import subprocess
import time

def main():
    print('updating the probestation code from github')
    os.chdir('/home/pi/Desktop/proberCode')
    outp = subprocess.check_output('git pull origin master', shell=True)
    print(outp)
    time.sleep(2)

if __name__ == '__main__':
    main()
