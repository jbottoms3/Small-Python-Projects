#James Bottoms
#jbottoms3@gatech.edu

from tkinter import *
import csv



class WordSearch:

    # Creates GUI and prompts user to select word search and word bank files
    def __init__ (self):
        self.rootWin = Tk()
        self.rootWin.title('Word Search Generator!')
        Label(self.rootWin, text="Word Search File:").grid(row=0,column=0)
        Label(self.rootWin, text="Word Bank File:").grid(row=1,column=0)

        self.searchFileName = StringVar()
        self.searchFileName.set("...")
        searchFile = Entry(self.rootWin, textvariable=self.searchFileName, state="readonly", width=100)
        searchFile.grid(row=0,column=1)
        self.bankFileName = StringVar()
        self.bankFileName.set("...")
        bankFile = Entry(self.rootWin, textvariable=self.bankFileName, state="readonly", width=100)
        bankFile.grid(row=1,column=1)

        self.selectFileWS = Button(self.rootWin, text="Select File",command=self.openWSClicked)
        self.selectFileWS.grid(row=0,column=2)
        self.selectFileWB = Button(self.rootWin, text="Select File",command=self.openWBClicked)
        self.selectFileWB.grid(row=1,column=2)

        Button(self.rootWin,text="Generate Word Search",command=self.generate).grid(row=2,column=0)

        self.rootWin.mainloop()

    # Actions to select the csv files associated with the word search and the word bank
    def openWSClicked(self):
        self.fileNameWS = filedialog.askopenfilename()
        self.searchFileName.set(self.fileNameWS)
    def openWBClicked(self):
        self.fileNameWB = filedialog.askopenfilename()
        self.bankFileName.set(self.fileNameWB)

    # Reads both csv files prepares the word search data to be generated while preparing word bank data to be displayed as well
    def readFiles(self):
        try:
            f1 = open(self.fileNameWS)
            self.wordSearchLines = []
            for row in csv.reader(f1):
                for i in range(len(row)):
                    row[i] = row[i].strip()
                    row[i] = row[i].upper()
                    if not row[i].isalpha():
                        raise exception
                if row != []:
                    self.wordSearchLines.append(row)

            f2 = open(self.fileNameWB)
            self.wordBankLines = []
            for row in csv.reader(f2):
                for i in range(len(row)):
                    row[i] = row[i].strip()
                    row[i] = row[i].upper()
                    if not row[i].isalpha():
                        raise exception    
                if row[0] != []:
                    self.wordBankLines.append(row[0])

        except:
            messagebox.showwarning("Excuse Me!","Invalid file!")


    # Generates the empty word search from the data processed from the csv file
    def generate(self):
        self.readFiles()
        self.wsFrame = Frame(self.rootWin)
        Label(self.rootWin,text="Find the CS Vocab!").grid(row=3,column=1)
        self.letters = []
        
        for i in range(len(self.wordSearchLines)):
            tempList = []
            for j in range(len(self.wordSearchLines[0])):
                a = Label(self.wsFrame, text=self.wordSearchLines[i][j]+'   ')
                a.grid(row=i,column=j)
                tempList.append(a)
            self.letters.append(tempList)
        self.wsFrame.grid(row=4,column=1)

        self.wbFrame = Frame(self.rootWin)
        Label(self.wbFrame,text="Word Bank:").grid(row=0,column=0)
        self.words=[]
        
        for i in range(len(self.wordBankLines)):
            a = Label(self.wbFrame,text=self.wordBankLines[i])
            a.grid(row=1+i,column=0)
            self.words.append(a)
        self.wbFrame.grid(row=4,column=2)

        self.searchFrame = Frame(self.rootWin)
        self.wordEntry = Entry(self.searchFrame)
        self.wordEntry.grid(row=0,column=0)
        Button(self.searchFrame,text = "Find",command = self.updateGUI).grid(row=0,column=1)
        self.searchFrame.grid(row=5,column=1)

    # Finds all starting coordinates of the first letter in the word to be found
    def findStartingCoords(self):
        firstLetter = self.word[0]
        aList = []
        for i in range(len(self.wordSearchLines)):
            firstIndex = 0
            secondIndex = 0
            if firstLetter in self.wordSearchLines[i]:
                firstIndex = i
                for j in range(len(self.wordSearchLines[i])):
                    if self.wordSearchLines[i][j] == firstLetter:
                        secondIndex = j
                        aTuple = (firstIndex,secondIndex)
                        aList.append(aTuple)
        return aList
                
    # Takes word from user input, finds possible starting coordinates for the word, and then checks for a match with all possible words created from each starting coordinate
    def find(self):
        self.word = self.wordEntry.get().upper()
        if self.word not in self.wordBankLines:
            messagebox.showwarning("ERROR","Sorry... There are no matches for that word in the word bank. Please input a new word.")
            return None
        
        startingPts = self.findStartingCoords()
        for pt in startingPts:
            self.coordList = []
            ###Left to Right
            try:
                for i in range(len(self.word)):
                    if self.word[i] == self.wordSearchLines[pt[0]][pt[1]+i]:
                        self.coordList.append((pt[0],pt[1]+i))
                    else:
                        self.coordList = []
                        raise ValueError
                return self.coordList
            except:
                pass

            ###Right to Left
            try:
                for i in range(len(self.word)):
                    if self.word[i] == self.wordSearchLines[pt[0]][pt[1]-i]:
                        self.coordList.append((pt[0],pt[1]-i))
                    else:
                        self.coordList = []
                        raise ValueError
                return self.coordList
            except:
                pass

            ###Down Right
            try:
                for i in range(len(self.word)):
                    if self.word[i] == self.wordSearchLines[pt[0]+i][pt[1]+i]:
                        self.coordList.append((pt[0]+i,pt[1]+i))
                    else:
                        self.coordList = []
                        raise ValueError
                return self.coordList
            except:
                pass

            ###Down Left
            try:
                for i in range(len(self.word)):
                    if self.word[i] == self.wordSearchLines[pt[0]+i][pt[1]-i]:
                        self.coordList.append((pt[0]+i,pt[1]-i))
                    else:
                        self.coordList = []
                        raise ValueError
                return self.coordList
            except:
                pass

            ###Up Right
            try:
                for i in range(len(self.word)):
                    if self.word[i] == self.wordSearchLines[pt[0]-i][pt[1]+i]:
                        self.coordList.append((pt[0]-i,pt[1]+i))
                    else:
                        self.coordList = []
                        raise ValueError
                return self.coordList
            except:
                pass

            ###Up Left
            try:
                for i in range(len(self.word)):
                    if self.word[i] == self.wordSearchLines[pt[0]-i][pt[1]-i]:
                        self.coordList.append((pt[0]-i,pt[1]-i))
                    else:
                        self.coordList = []
                        raise ValueError
                return self.coordList
            except:
                pass

            ###Up
            try:
                for i in range(len(self.word)):
                    if self.word[i] == self.wordSearchLines[pt[0]-i][pt[1]]:
                        self.coordList.append((pt[0]-i,pt[1]))
                    else:
                        self.coordList = []
                        raise ValueError
                return self.coordList
            except:
                pass
        
            ###Down
            try:
                for i in range(len(self.word)):
                    if self.word[i] == self.wordSearchLines[pt[0]+i][pt[1]]:
                        self.coordList.append((pt[0]+i,pt[1]))
                    else:
                        self.coordList = []
                        raise ValueError
                return self.coordList
            except:
                pass
        
    # Updates GUI by highlighting the word in the search if the word is found
    def updateGUI (self):
        wordCoordList = self.find()
        if wordCoordList == None:
            return None
        for tup in wordCoordList:
            a = self.letters[tup[0]][tup[1]]
            a.config(bg = 'yellow')
            
        for i in range(len(self.wordBankLines)):
            if self.wordBankLines[i] == self.word:
                index = i
        b = self.words[index]
        b.config(fg ='grey')
        

WordSearch()     
       
