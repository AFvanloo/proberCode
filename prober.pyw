#documentation


#from Tkinter import * for python 2.7
#import tkFileDialog for python 2.7
from tkinter import *
from tkinter import filedialog #or just type filedialog I guess?
from tkinter import font
import numpy as np
import csv
import os
import time

#This is where the measuring code goes:
import probeMeas as pm
import proberConfig #can probably be deleted

import connectGPIB as cg
import updateProber as up

#TODO adapt message window size


#TODO averages!

#TODO dynamic status updates


#TODO manual buttons: output+, output-, measure

#TODO fix not being able to delete the first measurement value

#TODO comment field entry in data frame and export

#TODO error when going beyond the dataframe

class Interface(Frame):

    def __init__(self, parent):
        '''
        Initialize the window
        '''

        Frame.__init__(self, parent)
        self.parent = parent
        self.grid()

        #default params
        self.config = proberConfig.config()

        #def IVData

        self.bWidth = 15
        self.cWdith = 10

        #latest data holders
        self.measNum = 0
        self.Ip=0
        self.Im=0
        self.Vp=0
        self.Vm=0
        self.R=0
        self.data = []
        
        #default values
        self.uvA = 100
        self.gain = 100
        self.avs = 10

        self.reconnectGPIB=False #remove during debugging


        #paths
        self.instPath = os.getcwd()
        #self.savePath = 
        self.saveName = self.timeName()
        #self.cfgpath = self.instpath+'/proberConfig.txt'

        self.verbose = False
        if self.verbose:
            print('Verbose mode')

        #create the buttons etc
        self.initUI()
        self.connectInstruments()

        if self.reconnectGPIB == True:
            cg.main()



    def initUI(self):
        '''
        create all buttons, tabs, windows etc
        '''

        if self.verbose:
            print('Initializing the GUI')


#-----------Left buttons---------------------------------------------------------------


        #prober button
        self.probeButton = Button(self, text='Probe!', width=self.bWidth, 
                height=2, bg = 'red', fg='white', 
                activebackground='white', activeforeground='red',
                command=self.probe, font='helvetica 14 bold')
        self.probeButton.grid(row=0, column=0, rowspan=2, columnspan=1, sticky='W')

        #IV-meas button
        #Not yet implemented!
        #self.IVButton = Button(self, text='IV curve', width=self.bWidth,
        #        command=self.IVpopupWindow)
        #self.IVButton.grid(row=2, column=0, sticky='W')


        #plot histogram
        self.histButton = Button(self, text='Show Histogram', width=self.bWidth,
                command=self.showHistogram)
        self.histButton.grid(row=2, column=0, sticky='W')

        #delete last data
        self.delButton = Button(self, text='Delete last data', width=self.bWidth,
                command=self.delLastData)
        self.delButton.grid(row=3, column=0, sticky='W')

        #reconnect instruments button
        #self.reconnectButton = Button(self, text='Reconnect \n instruments', width=self.bWidth, command=self.connectInstruments)
        #self.reconnectButton.grid(row=4, column=0, sticky='W')





#-----------Instrument connection frame-----------------------------------------------------


        self.instFrame = LabelFrame(self, text='Instruments', labelanchor='n')
        self.instFrame.grid(row=0, rowspan=2, column=1, columnspan=10)

        lIWidth=14

        #source
        #self.sourceLabel = Label(self.instFrame, text='Yokogawa GS200 \n voltage source', fg='red', width=lIWidth)
        #self.sourceLabel.grid(row=0, column=0, columnspan=2)
        self.sourceAddrLabel = Label(self.instFrame, text='Yoko \n GPIB: --', fg='red', width=lIWidth)
        self.sourceAddrLabel.grid(row=0, column=0, columnspan=2)
        
        #Keithley for measuring V
        #self.KeithleyVLabel = Label(self.instFrame, text='Keithley multimeter V', fg='red', width=lIWidth)
        #self.KeithleyVLabel.grid(row=0, column=2, columnspan=2)
        self.KeithleyVAddrLabel = Label(self.instFrame, text='Keithley V \n  GPIB: --', fg='red', width=lIWidth)
        self.KeithleyVAddrLabel.grid(row=0, column=2, columnspan=2)

        #Keithley for measuring I
        #self.KeithleyILabel = Label(self.instFrame, text='Keithley multimeter I', fg='red', width=lIWidth)
        #self.KeithleyILabel.grid(row=0, column=4, columnspan=2)
        self.KeithleyIAddrLabel = Label(self.instFrame, text='Keithley I \n GPIB: --', fg='red', width=lIWidth)
        self.KeithleyIAddrLabel.grid(row=0, column=4, columnspan=2)

        #SRS pre-amp
        #self.SRSPLabel = Label(self.instFrame, text='SRS preamp', fg='red', width=lIWidth)
        #self.SRSPLabel.grid(row=0, column=6, columnspan=2)
        self.SRSPAddrLabel = Label(self.instFrame, text='SRS pre-amp \n GPIB: --', fg='red', width=lIWidth)
        self.SRSPAddrLabel.grid(row=0, column=6, columnspan=2)
        
        #SRS diff amp
        #self.SRSDLabel = Label(self.instFrame, text='SRS diff amp', fg='red', width=lIWidth)
        #self.SRSDLabel.grid(row=0, column=8, columnspan=2)
        self.SRSDAddrLabel = Label(self.instFrame, text='SRS diff \n GPIB: --', fg='red', width=lIWidth)
        self.SRSDAddrLabel.grid(row=0, column=8, columnspan=2)





#-------------Measurement settings frame-------------------------------------------------

        esWidth=12 
        
        self.settingsFrame = LabelFrame(self, text='Measurement settings', labelanchor='n')
        self.settingsFrame.grid(row=2, rowspan=3, column=1, columnspan=8)
        

        #source voltage setting
        sourceLabel2 = Label(self.settingsFrame, text='source Voltage (mV):')
        sourceLabel2.grid(row=0, column=0, columnspan=2)
        #self.sourceStr = StringVar()
        self.sourceEntry = Entry(self.settingsFrame, width=esWidth)
        self.sourceEntry.grid(row=1, column=0, columnspan=2)
        self.sourceEntry.insert(0, '.001')
        #self.sourceButton = Button(self.settingsFrame, text='Set source', command=self.setSource)
        #self.sourceButton.grid(row=2, column=0)

        #uV/A dropdown list and label
        self.uvALabel= Label(self.settingsFrame, text='uV/A setting:', anchor='c')
        self.uvALabel.grid(row=0, column=2, columnspan=1)
        self.uvAInt = IntVar()
        self.uvAInt.set(self.config['uV/A'])
        uvAList = ('1', '2', '5', '10', '20', '50', '100', '200', '500', '1000', '2000', '5000')
        self.uvAMenu = OptionMenu(self.settingsFrame, self.uvAInt, *uvAList, command=self.setuVA)
        self.uvAMenu.configure(width=esWidth)
        self.uvAMenu.grid(row=1, column=2, columnspan=1)

        #gain dropdown list
        self.gainLabel= Label(self.settingsFrame, text='amp gain setting:', anchor='c')
        self.gainLabel.grid(row=0, column=3, columnspan=1)
        gainList = ('1', '10', '100', '1000', '10000')
        self.gainInt = IntVar()
        self.gainInt.set(self.config['gain'])
        self.gainMenu = OptionMenu(self.settingsFrame, self.gainInt, *gainList, command=self.setGain)
        self.gainMenu.configure(width=esWidth)
        self.gainMenu.grid(row=1, column=3, columnspan=1)

        #wait entry
        self.waitLabel = Label(self.settingsFrame, text='wait between ON \n and measure (s)')
        self.waitLabel.grid(row=0, column=4, columnspan=2)
        #self.waitString = StringVar()
        self.waitEntry = Entry(self.settingsFrame, width=esWidth)#, textvariable=self.waitString, width=15)
        self.waitEntry.grid(row=1, column=4, columnspan=2)
        self.waitEntry.insert(0,'.5')


        #Averages
        self.avsLabel = Label(self.settingsFrame, text='#averages')
        self.avsLabel.grid(row=0, column=6, columnspan=1)
        #Entry
        self.avsEntry = Entry(self.settingsFrame, width=esWidth-2)
        self.avsEntry.grid(row=1, column=6, columnspan=1)
        self.avsEntry.insert(0,'10')

#-------------Current values------------------------------------------------------
        '''
        Currently removed to save space

        self.measuredFrame = LabelFrame(self, text='Most recently measured values (maybe to be removed)', labelanchor='n')
        self.measuredFrame.grid(row=5, rowspan=1, column=2, columnspan=10)

        lWidth=13

        #V+ window
        self.VpFrame = LabelFrame(self.measuredFrame, text='V+:',  fg='white', bg='black', labelanchor='n')
        self.VpFrame.grid(row=0, rowspan=1, column=0, columnspan=2)
        self.VpLabel = Label(self.VpFrame, text='-', width=lWidth)
        self.VpLabel.grid(row=0, column=0, columnspan=2)

        #V- window
        self.VmFrame = LabelFrame(self.measuredFrame, text='V-:',  fg='white', bg='black', labelanchor='n')
        self.VmFrame.grid(row=0, rowspan=1, column=2, columnspan=2)
        self.VmLabel = Label(self.VmFrame, text='-', width=lWidth)
        self.VmLabel.grid(row=0, column=0, columnspan=2)

        #I+ window
        self.IpFrame = LabelFrame(self.measuredFrame, text='I+:',  fg='white', bg='black', labelanchor='n')
        self.IpFrame.grid(row=0, rowspan=1, column=4, columnspan=2)
        self.IpLabel = Label(self.IpFrame, text='-', width=lWidth)
        self.IpLabel.grid(row=0, column=0, columnspan=2)

        #I- window
        self.ImFrame = LabelFrame(self.measuredFrame, text='I-:',  fg='white', bg='black', labelanchor='n')
        self.ImFrame.grid(row=0, rowspan=1, column=6, columnspan=2)
        self.ImLabel = Label(self.ImFrame, text='-', width=lWidth)
        self.ImLabel.grid(row=0, column=0, columnspan=2)

        #R window
        self.RFrame = LabelFrame(self.measuredFrame, text='R:',  fg='white', bg='black', labelanchor='n')
        self.RFrame.grid(row=0, rowspan=1, column=8, columnspan=2)
        self.RLabel = Label(self.RFrame, text='-', width=lWidth)
        self.RLabel.grid(row=0, column=0, columnspan=2)

        '''


#--------------Data Frame--------------------------------------

#labels: V+, V-, I+, I-, R
#data

#statistics

#plotHistogram
        dWidths=[10, 12] + [7]*4 + [10] + 2*[5]+[12] 

        self.dataFrameWidth = 10
        self.dataFrameLength = 8

        self.dataFrame = LabelFrame(self, text='last few results', labelanchor='n')
        self.dataFrame.grid(row=6, rowspan=self.dataFrameLength,column=0, columnspan=self.dataFrameWidth)

        self.dataFrameLabels = ['measNum', 'Vsource (mV)', 'V+ (mV)', 'V- (mV)', 'I+ (mV)', 'I- (mV)', 'R (Ohm)', 'uV/A', 'gain', 'Comments']

        #pre-allocate list of lists
        self.labelList = [[0 for i in range(self.dataFrameWidth)] for j in range(self.dataFrameLength)]

        #Add 
        for i in range(self.dataFrameWidth):
            #set labels
            la = Label(self.dataFrame, text=self.dataFrameLabels[i], width=dWidths[i])
            la.grid(row=0, column=i)
            self.labelList[0][i]=la
            for j in range(1, self.dataFrameLength):
                #data labels
                if i < self.dataFrameWidth-1:
                    lb = Label(self.dataFrame, text='0', width=dWidths[i])
                    lb.grid(row=j, column=i)
                    self.labelList[j][i] = lb 
                elif i == self.dataFrameWidth-1:
                    #comment entries
                    en = Entry(self.dataFrame, width=20)
                    #en.insert(0, '')
                    en.grid(row=j, column=self.dataFrameWidth-1)
                    self.labelList[j][self.dataFrameWidth-1] = en


        


#----------------Statistics subframe-----------------------------------------
       
        sWidth = 12
        self.statFrame = LabelFrame(self, text='Resistance statistics', labelanchor='n', relief='sunken')
        self.statFrame.grid(row=16, rowspan=2, column=0, columnspan=3)

        #Average resistance
        self.RavFrame = LabelFrame(self.statFrame, text='Average Restistance',  fg='white', bg='black', labelanchor='n')
        self.RavFrame.grid(row=0, rowspan=1, column=0, columnspan=1)
        self.RavLabel = Label(self.RavFrame, text='-', width=sWidth)
        self.RavLabel.grid(row=0, column=0)

        #Standard deviation window
        self.RstdFrame = LabelFrame(self.statFrame, text='Standard deviation:',  fg='white', bg='black', labelanchor='n')
        self.RstdFrame.grid(row=0, rowspan=1, column=2, columnspan=1)
        self.RstdLabel = Label(self.RstdFrame, text='-', width=sWidth)
        self.RstdLabel.grid(row=0, column=0)


#----------Saving etc------------------------------------------
        lastRow=16

        #save label
        self.saveLabel = Label(self, text='save at')
        self.saveLabel.grid(row=lastRow+2, column=0, sticky='E')

        #csv file path
        self.saveEntry = Entry(self, width=60)
        #TODO sanitize for windows: / -> \\
        #TODO B310 save folder
        #self.savePath = self.instPath + '/data/' + self.saveName
        #self.savePath = '/home/pi/Desktop/proberData/' + self.saveName
        self.savePath = '/media/B310/qubit_team/probeStation/data/' + self.saveName
        self.saveEntry.insert(0, self.savePath)
        self.saveEntry.grid(row=lastRow+2, column=1, columnspan=6)


        #save
        self.saveButton = Button(self, text='save', fg='blue', command=self.save)
        self.saveButton.grid(row=lastRow+2, column=7)

        #clear all / reset
        self.clearButton = Button(self, text='clear all / reset', width=self.bWidth, command=self.reset)
        self.clearButton.grid(row=lastRow+1, column=6, columnspan=2, sticky='E')

        #save as
        self.browseButton = Button(self, text='Browse ...', fg='blue', command=self.browseSave)
        self.browseButton.grid(row=lastRow+1, column=8)
        
        #quit
        self.quitButton = Button(self, text='Quit', fg='Red', \
                command=self.quit)
        self.quitButton.grid(row=lastRow+2, column=8, columnspan=1, sticky='E')

        #browse for save file path
        #filedialog?


#========================================================================
#---------------------------Functions------------------------------------
#========================================================================

    def connectInstruments(self, GPIB=[1,2,3], RS323=[1,2]):
        #return address if connected:
        connections = pm.connectInstruments()
        adrLabels = ['vSourceAddrLabel', 'KeithleyVAddrLabel', 'KeithleyIAddrLabel', 'SRSPAddrLabel', 'SRSDAddrLabel']

        for i, adr in enumerate(connections):
            if adr != None:
                #set label colour to green
                setattr(self, adrLabels[i]+"['text']", adr)
                setattr(self, adrLabels[i]+"['fg']", 'green')


        #connect yoko source
        #pm.initSource()
        #connect 


    def setuVA(self, uVA):
        '''
        helper function for the dropdown list to select uVA setting
        '''
        print(uVA)
        self.uvA = int(uVA)


    def setGain(self, gain):
        '''
        helper function for the dropdown list to select gain
        '''
        self.uvA = int(gain)
        #set 

    def setSource(self):
        mV = self.sourceEntry.get()
        b = pm.setSource(mV)
        if not b:
            messageWindow('setting the source failed')


    def probe(self):
        #get wait and voltage from entry menus
        wait = float(self.waitEntry.get())
        voltage = float(self.sourceEntry.get())
        self.avs = int(self.avsEntry.get())


        #get uvA and gain from dropdown menus
        print(self.gainInt)
        self.uvA = self.uvAInt.get()
        self.gain = self.gainInt.get()
        
        #Probe it        
        self.Vp, self.Vm, self.Ip, self.Im, self.R = pm.probe(voltage, wait=wait, uvA=self.uvA, gain=self.gain, avs=self.avs)
        #set to current values
        #save values, put in data frame
        self.measNum += 1
        #On each line, we first append an empty comment, then read the comments from the field and insert them
        self.data.append([self.measNum, voltage, self.Vp, self.Vm, self.Ip, self.Im, self.R, self.gain, self.uvA, ''])
        self.getComments()
        self.updateResults()

    def IVpopupWindow(self):
        self.messageWindow('Automated IV curve measuring not yet implemented')
        return
        #ask from, to and step
        #Measure button
        #cancel button


    def updateResults(self):

        #Update the Vp, Vm, Ip, Im frames -- currently this frame does not exist
        #self.VpLabel.configure(text=round(self.Vp,4))
        #self.VmLabel.configure(text=round(self.Vm,4))
        #self.IpLabel.configure(text=round(self.Ip,4))
        #self.ImLabel.configure(text=round(self.Im,4))
        #self.RLabel.configure(text=round(self.R,4))

        #update list: rewrite the data
        for i in range(1, min(self.dataFrameLength-1, len(self.data))+1):
            for j in range(self.dataFrameWidth-1):
                if j == 6:
                    self.labelList[i][j]['text'] = str(round(self.data[-i][j],1))
                else:
                    self.labelList[i][j]['text'] = str(round(self.data[-i][j],4))
        
        #write zeros for things with no data.
        for i in range(len(self.data), self.dataFrameLength-1):
            for j in range(self.dataFrameWidth-1):
                self.labelList[i+1][j]['text'] = str(0)

        #rewrite entries according to self.data
        for i in range(1, min(self.dataFrameLength-1, len(self.data))+1):
            #empty all
            self.labelList[i][self.dataFrameWidth-1].delete(0, 'end')
            #rewrite
            self.labelList[i][self.dataFrameWidth-1].insert(0, self.data[-i][self.dataFrameWidth-1])

        #update average and std if its not an empty list
        av, std = self.calcStats()
        self.RavLabel.configure(text=round(av,5))
        self.RstdLabel.configure(text=round(std,5))

    def reset(self):

        #empty the comments:
        for i in range(1, min(self.dataFrameLength-1, len(self.data))+1):
            self.labelList[i][self.dataFrameWidth-1].delete(0, 'end')

        #empty the label list / remove data
        self.data = []
        self.measNum = 0

        #change the timestamp / saveName
        self.saveName = self.timeName()
        self.savePath = '/media/B310/qubit_team/probestation/data/' + self.saveName
        #remove existing entry
        self.saveEntry.delete(0, 'end')
        self.saveEntry.insert(0, self.savePath)

        #check all instrument connections and settings
        #finally, update everything
        self.updateResults()



    def getComments(self):
        '''
        Store the comments into the correct line of self.data
        This should be executed at least on 'probe' and 'delete data point' at the start of the function
        '''
        #Go through comments from 1 to dataFrameLength.
        for i in range(1, min(self.dataFrameLength-1, len(self.data))+1):
            #ignore if empty
            entryVal = self.labelList[i][self.dataFrameWidth-1].get()
            if entryVal == '':
                continue
            else:
                #store in self.data
                dataNum = int(self.labelList[i][0]['text'])
                self.data[dataNum-1][self.dataFrameWidth-1]=entryVal
            



    def delLastData(self):
        #first check for new comments
        self.getComments()
        if len(self.data) >= 1:
            self.data = self.data[:-1]
            self.measNum -= 1
            self.updateResults()


    def toCSV(self):
        pass

    def timeName(self):
        t = time.localtime()
        #string construction split over 2 lines
        tName = str(t[0]) + str(t[1]).zfill(2) + str(t[2]).zfill(2) + '_' + str(t[3]).zfill(2) 
        tName +=  '_' + str(t[4]).zfill(2) + '_' + str(t[5]).zfill(2) + '.csv'
        return tName
        


    def closeWindow(self):
        os.chdir(self.instPath)
        self.quit()
        self.master.destroy()

    def quitRet(self):
        self.quit()
        self.master.destroy()
        return self

    def calcStats(self):
        #if the list is empty, return zeros
        if self.data == []: return 0,0
        #otherwise, calculate the mean and std
        Rs = [data[6] for data in self.data]
        Rav = np.mean(Rs)
        Rstd = np.std(Rs)
        return Rav, Rstd

    def showHistogram(self):
        Rs = data[:][5]
        pass


    def messageWindow(self, msgtext, bgc='blue', actCol='red'):
        '''
        second popup message
        '''
        messageWin = Toplevel()
        typotext = Button(messageWin, text=msgtext,
                   bg=bgc, fg="yellow",
                   activebackground=actCol, activeforeground="white",
                   padx=messageWin.winfo_screenwidth()/6,
                   pady=messageWin.winfo_screenheight()/6,
                   command=messageWin.destroy)
        typotext.grid(row=0,column=0)

    def browseSave(self):
        self.savePath = filedialog.asksaveasfilename(defaultextension='.csv', title='Save as', initialdir='/media/B310/qubit_team/probestation/data')
        print(self.savePath)
        if self.savePath == None: #used cancel button
            return
        #put into entry
        self.saveEntry.delete(0, 'end')
        self.saveEntry.insert(0, self.savePath)
        self.save()


    def save(self):
        #get save path from entry
        self.savePath = self.saveEntry.get()

        #Are all comment entries added to self.data?


        #combine labels and data
        self.labeledData = [self.dataFrameLabels] + self.data
        print('before saving: self. labeledData is ', self.labeledData)

        #export to CSV file
        with open(self.savePath, 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.labeledData)

        saveMessage = 'File saved at ' + self.savePath + '\n (click to remove this message)'
        self.messageWindow(saveMessage, bgc='blue', actCol='green')



#==========================Actually run it==========================

def main():
    root = Tk()
    root.attributes('-zoomed', True)
    def_font = font.nametofont("TkDefaultFont")
    def_font.config(size=9)
    root.title('Junction Prober')
    root.geometry("800x400")
    interface = Interface(root)
    root.mainloop()

if __name__ == '__main__':
    main()
    


