#James Bottoms
#jbottoms3@gatech.edu

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import xml.etree.ElementTree as etree


class GUI:

    # Creates GUI 
    def __init__(self):
        self.rootWin = Tk()
        self.rootWin.title("XML Processing")
        Button(self.rootWin,text="Choose File",command=self.clicked,width=14).pack()
        self.pitcherDict = {}
        
        self.rootWin.mainloop()

    # Action when "Choose File" Button is clicked
    def clicked(self):
        try:
            file = filedialog.askopenfilename()
            if file[-4:] != ".xml":
                raise Exception
            self.parseGames(file)
            self.writePitchers()
            
            
        except:
            messagebox.showwarning("ERROR","Please pick a valid .xml file!")
            return None
        

    # Parses each baseball game in the xml input file 
    def parseGames(self,file):
        tree = etree.parse(file)
        root = tree.getroot()
        aList = []

        for game in root:
            innings = game.findall("inning")
            for inning in innings:
                tops = inning.findall("top")
                bottoms = inning.findall("bottom")
                for top in tops:
                    atbats = top.findall("atbat")
                    for batter in atbats:
                        self.parseAtbat(batter)
                for bottom in bottoms:
                    atbats = bottom.findall("atbat")
                    for batter in atbats:
                        self.parseAtbat(batter)
                        
        messagebox.showinfo("Data Parse Successful","Press OK to save your output file.")

    # Parses each at bat to update necessary information for the output file
    def parseAtbat(self,atbat):
        currentpitcher = atbat.attrib['pitcher']
        if currentpitcher not in self.pitcherDict:
            self.pitcherDict[currentpitcher] = []
                
        for pitch in atbat:
            pitchType = pitch.attrib["pitch_type"]
            pitchResult = pitch.attrib["type"]
            if pitchResult != "B":
                pitchResult = "S"
            pitchSpeed = pitch.attrib["start_speed"]
            try:
                pitchSpeed = float(pitchSpeed)
            except:
                continue
            self.pitcherDict[currentpitcher].append([pitchType,pitchResult,pitchSpeed])
            

    # Writes pitcher data to output file   
    def writePitchers(self):
        newroot = etree.Element("Pitchers")

        aList = []
        for key in self.pitcherDict:
            aList.append(key)
        aList.sort()

        
        for pitcher in aList:
            newDict = self.processPitches(self.pitcherDict[pitcher])
            pitcherElement = etree.SubElement(newroot,'Pitcher',name=pitcher)
            for key in newDict:
                pitchdataElement = etree.SubElement(pitcherElement,'PitchData',pitchType=key)
                numpitched = etree.SubElement(pitchdataElement,"NumPitched")
                numpitched.text=str(newDict[key][0])
                avgspeed = etree.SubElement(pitchdataElement,"AvgSpeed")
                avgspeed.text=str(newDict[key][1])
                sbratio = etree.SubElement(pitchdataElement,"StrikeToBallRatio")
                sbratio.text=str(newDict[key][2])
            
        answer = messagebox.askyesno("Save File","Do you want to save as XML?")
        
        tree = etree.ElementTree(newroot)
        if answer == True:
            name = filedialog.asksaveasfilename(defaultextension=".xml")
            tree.write(name,"UTF-8")
            Label(self.rootWin,text="File successfully saved!").pack()
        else:
            return None
            


    # Reads through pitching data for all pitchers and updates information
    def processPitches(self,pitcheslist):
        aDict = {}
        
        for pitch in pitcheslist:
                if pitch[0] not in aDict:
                    aDict[pitch[0]] = [1,[0,0],[pitch[2]]]
                    if pitch[1] == "B":
                        aDict[pitch[0]][1][0] += 1
                    else:
                        aDict[pitch[0]][1][1] += 1
                else:
                    aDict[pitch[0]][0] += 1
                    if pitch[1] == "B":
                        aDict[pitch[0]][1][0] += 1
                    else:
                        aDict[pitch[0]][1][1] += 1
                    aDict[pitch[0]][2].append(pitch[2])
        
                    
        for pitchtype in aDict:
            numThrown = aDict[pitchtype][0]
            avgspeed = (sum(aDict[pitchtype][2])/len(aDict[pitchtype][2]))
            numB = aDict[pitchtype][1][0]
            numS = aDict[pitchtype][1][1]
            if numB == 0:
                numB = 1
            ratio = numS/numB
            aDict[pitchtype] = [numThrown,avgspeed,ratio]
        return aDict
                
            
GUI()
