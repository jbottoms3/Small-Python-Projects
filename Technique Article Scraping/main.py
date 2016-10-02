#James Bottoms
#jbottoms3@gatech.edu

import urllib.request
from re import findall
from tkinter import *

class WebScraper:
    # Creates GUI
    def __init__(self):
        self.rootWin = Tk()
        self.rootWin.title("Georgia Tech News From The TechNique")

        Label(self.rootWin, text = "Find the Latest News Headlines Around Georgia Tech!").grid(row=0,columnspan=2,column=0)
        Button(self.rootWin, text = "Get Info!" , command = self.getInfo).grid(row=1,column=0,columnspan=2,sticky=E+W)

        Label(self.rootWin, text= "Top Story: ").grid(row=2,column=0,sticky=E)
        self.firstStoryVar = StringVar()
        self.firstStoryVar.set('')
        Entry(self.rootWin, textvariable = self.firstStoryVar,width=55).grid(row=2, column=1)

        Label(self.rootWin, text= "Another Story: ").grid(row=3,column=0)
        self.secondStoryVar = StringVar()
        self.secondStoryVar.set('')
        Entry(self.rootWin, textvariable = self.secondStoryVar,width=55).grid(row=3,column=1)

        Label(self.rootWin, text= "Another Story: ").grid(row=4,column=0)
        self.thirdStoryVar = StringVar()
        self.thirdStoryVar.set('')
        Entry(self.rootWin, textvariable= self.thirdStoryVar,width=55).grid(row=4,column=1)
        
        self.rootWin.mainloop()

    # Scrapes news articles from the Technique and returns the titles of the most recent three
    def getInfo(self):
        response = urllib.request.urlopen("http://nique.net/")
        html = response.read()
        text = str(html)

        self.dataList = findall('rel="bookmark">[^<]+</a>', text)
        self.firstStory = self.dataList[0][15:-4]
        self.secondStory = self.dataList[1][15:-4]
        self.thirdStory = self.dataList[2][15:-4]
        if "\\xe2\\x80\\x9d" in self.firstStory or "\\xe2\\x80\\x9c" in self.firstStory or "\\xe2\\x80\\x99" in self.firstStory:
            self.secondStory = self.firstStory.replace("\\xe2\\x80\\x9d",'"')
            self.secondStory = self.firstStory.replace("\\xe2\\x80\\x9c",'"')
            self.secondStory = self.firstStory.replace("\\xe2\\x80\\x99","'")
        if "\\xe2\\x80\\x9d" in self.secondStory or "\\xe2\\x80\\x9c" in self.secondStory or "\\xe2\\x80\\x99" in self.secondStory:
            self.secondStory = self.secondStory.replace("\\xe2\\x80\\x9d",'"')
            self.secondStory = self.secondStory.replace("\\xe2\\x80\\x9c",'"')
            self.secondStory = self.secondStory.replace("\\xe2\\x80\\x99","'")
        if "\\xe2\\x80\\x9d" in self.thirdStory or "\\xe2\\x80\\x9c" in self.thirdStory or "\\xe2\\x80\\x99" in self.thirdStory:
            self.secondStory = self.thirdStory.replace("\\xe2\\x80\\x9d",'"')
            self.secondStory = self.thirdStory.replace("\\xe2\\x80\\x9c",'"')
            self.secondStory = self.thirdStory.replace("\\xe2\\x80\\x99","'")
        self.firstStoryVar.set(self.firstStory)
        self.secondStoryVar.set(self.secondStory)
        self.thirdStoryVar.set(self.thirdStory)

        return [self.firstStory,self.secondStory,self.thirdStory]



WebScraper()

