#James Bottoms
#jbottoms3@gatech.edu

from tkinter import *
import urllib.request
import base64
import pymysql


class GUI:

    # Creates Landing GUI
    def __init__(self):
        self.LoginPage()

    # Creates Login Page
    def LoginPage(self):
        self.rootWin = Tk()
        self.rootWin.title("Login")

        response = urllib.request.urlopen("http://www.cc.gatech.edu/classes/AY2015/cs2316_fall/codesamples/techlogo.gif")
        self.image = response.read()
        self.b64_data = base64.encodebytes(self.image)
        self.photo = PhotoImage(data=self.b64_data)

        self.pic = Label(self.rootWin, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=4)

        Label(self.rootWin, text="Username").grid(row=1,column=0,sticky=E)
        Label(self.rootWin, text="Password").grid(row=2,column=0,sticky=E)
        self.usernameLogin = Entry(self.rootWin,width=30)
        self.usernameLogin.grid(row=1,column=1,columnspan=2,sticky=E+W)
        self.passwordLogin = Entry(self.rootWin,width=30)
        self.passwordLogin.grid(row=2,column=1,columnspan=2,sticky=E+W)

        self.registerButton = Button(self.rootWin, text="Register", command=self.Register)
        self.registerButton.grid(row=3,column=1,sticky=E+W)
        self.loginButton = Button(self.rootWin, text="Login", command=self.LoginCheck)
        self.loginButton.grid(row=3,column=2,sticky=E+W)
        self.exitButton = Button(self.rootWin, text="Exit", command=self.ExitHelper)
        self.exitButton.grid(row=3,column=3,sticky=E)

        self.rootWin.mainloop()

    # Creates New User Registration Page
    def Register(self):
        self.rootWin.withdraw()
        self.regWin = Toplevel()
        self.regWin.title("Room Reservation New User Registration")

        response = urllib.request.urlopen("http://www.cc.gatech.edu/classes/AY2015/cs2316_fall/codesamples/techlogo.gif")
        self.image2 = response.read()
        self.b64_data2 = base64.encodebytes(self.image2)
        self.photo2 = PhotoImage(data=self.b64_data2)

        self.pic2 = Label(self.regWin, image = self.photo2)
        self.pic2.grid(row = 0, column = 0, columnspan=4)

        Label(self.regWin,text="Last Name").grid(row=1,column=0,sticky=W)
        Label(self.regWin,text="Username").grid(row=2,column=0,sticky=W)
        Label(self.regWin,text="Password").grid(row=3,column=0,sticky=W)
        Label(self.regWin,text="Confirm Password").grid(row=4,column=0,sticky=W)

        self.lastnameEntry = Entry(self.regWin,width=30,state="normal")
        self.lastnameEntry.grid(row=1,column=1)
        self.usernameEntry = Entry(self.regWin,width=30,state="normal")
        self.usernameEntry.grid(row=2,column=1)
        self.password1Entry = Entry(self.regWin,width=30,state="normal")
        self.password1Entry.grid(row=3,column=1)
        self.password2Entry = Entry(self.regWin,width=30,state="normal")
        self.password2Entry.grid(row=4,column=1)

        self.cancelButton = Button(self.regWin,text="Cancel",command=self.BackToLogin,width=15)
        self.cancelButton.grid(row=5,column=1,sticky=E)
        self.officialRegisterButton = Button(self.regWin,text="Register",command=self.RegisterNew)
        self.officialRegisterButton.grid(row=5,column=2)


    # Connects to database to be used for users and reservations
    def Connect(self):
        try:
            db = pymysql.connect(host="DB HOSTNAME",user="USERNAME",passwd = "PASSWORD",db="DB NAME")
            return db
        except:
            messagebox.showwarning("Warning","Please check your internet connection and try again!")

    # Exits window
    def ExitHelper(self):
        self.rootWin.destroy()

    # Returns to Login Screen
    def BackToLogin(self):
        self.regWin.withdraw()
        self.rootWin.deiconify()

    # Registers a new user and inserts their information into the ReservationUser Table
    def RegisterNew(self):
        self.registerLastName = self.lastnameEntry.get()
        self.registerUsername = self.usernameEntry.get()
        self.registerPass1 = self.password1Entry.get()
        self.registerPass2 = self.password2Entry.get()

        if self.registerPass1 == '':
            messagebox.showwarning("Warning","Password cannot be empty!")
            
        elif self.registerPass1 != self.registerPass2:
            messagebox.showwarning("Warning","Passwords must match!")
            
        elif any(i.isdigit() for i in self.registerPass1) == False:
            messagebox.showwarning("Warning","You must include at least one number in your password!")

        elif any(i.isupper() for i in self.registerPass1) == False:
            messagebox.showwarning("Warning","You must include at least one uppercase letter in your password!")

        else:
            db = self.Connect()
            c = db.cursor()
            if c.execute("""SELECT * FROM ReservationUser WHERE Username='"""+self.registerUsername+"""'""") != 0:
                messagebox.showwarning("Warning","Sorry! That username already exists!")
            else:
                if self.registerLastName == '':
                    c.execute("""INSERT INTO ReservationUser (Username,Password) VALUES ('"""+self.registerUsername+"""','"""+self.registerPass1+"""')""")
                    self.BackToLogin()
                    messagebox.showinfo("Congrats","You are now registered!")
                    c.close()
                    db.commit()
                else:
                    c.execute("""INSERT INTO ReservationUser (Username,Password,LastName) VALUES ('"""+self.registerUsername+"""','"""+self.registerPass1+"""','"""+self.registerLastName+"""')""")
                    self.BackToLogin()
                    messagebox.showinfo("Congrats","You are now registered!")
                    c.close()
                    db.commit()

    # Creates Home Page GUI
    def Homepage(self):
        self.homepageWin = Toplevel()
        self.homepageWin.title("Room Reservation Homepage")
        Label(self.homepageWin, text="Welcome To GT Room Reservation System!",relief=RAISED).grid(row=0,column=1,columnspan=3,sticky=E+W)
        self.currentReservesFrame = Frame(self.homepageWin)
        Label(self.currentReservesFrame, text = "Current Reservations").grid(row=0,column=0)

        db = self.Connect()
        c = db.cursor()
        c.execute("""SELECT * FROM RoomReservations WHERE ReservedBy='"""+self.usernameLogin.get()+"""'""")
        reservations = c.fetchall()
        if len(reservations)==0:
            a = StringVar()
            a.set("No Reservations")
            Entry(self.currentReservesFrame,textvariable=a,width=50,state="readonly").grid(row=0,column=1)
        else:
            for i in range(len(reservations)):
                a=StringVar()
                a.set("Room "+str(reservations[i][2])+" on "+reservations[i][0]+" floor "+str(reservations[i][1])+" is reserved for "+reservations[i][3]+" at "+reservations[i][4]+" hours.")
                Entry(self.currentReservesFrame,textvariable=a,width=50,state="readonly").grid(row=i,column=1)

        self.currentReservesFrame.grid(row=2,column=0,columnspan=5)
        Label(self.homepageWin,text="Make New Reservations:").grid(row=4,column=0)

        #Day Buttons
        self.frame1 = Frame(self.homepageWin,relief=SUNKEN,bd=1)
        Label(self.frame1,text="Day Choices").grid(row=0,column=0)
        self.v1 = StringVar()
        self.v1.set(" ")
        Radiobutton(self.frame1,text="Monday",variable=self.v1,value="Monday").grid(row=1,column=0)
        Radiobutton(self.frame1,text="Tuesday",variable=self.v1,value="Tuesday").grid(row=2,column=0)
        Radiobutton(self.frame1,text="Wednesday",variable=self.v1,value="Wednesday").grid(row=3,column=0)
        Radiobutton(self.frame1,text="Thursday",variable=self.v1,value="Thursday").grid(row=4,column=0)
        Radiobutton(self.frame1,text="Friday",variable=self.v1,value="Friday").grid(row=5,column=0)

        self.frame1.grid(row=5,column=0,sticky=E+W)
        self.day = self.v1.get()

        #Time Buttons
        self.frame2 = Frame(self.homepageWin,relief=SUNKEN,bd=1)
        Label(self.frame2,text="Time Choices").grid(row=0,column=0)
        self.v2 = StringVar()
        self.v2.set(" ")
        Radiobutton(self.frame2,text="Morning",variable=self.v2,value="Morning").grid(row=1,column=0)
        Radiobutton(self.frame2,text="Afternoon",variable=self.v2,value="Afternoon").grid(row=2,column=0)
        Radiobutton(self.frame2,text="Evening",variable=self.v2,value="Evening").grid(row=3,column=0)
        Radiobutton(self.frame2,text="Night",variable=self.v2,value="Night").grid(row=4,column=0)

        self.frame2.grid(row=5,column=1,sticky=E+W)
        self.time = self.v2.get()

        #Building Buttons
        self.frame3 = Frame(self.homepageWin,relief=SUNKEN,bd=1)
        Label(self.frame3,text="Building Choices").grid(row=0,column=0)
        self.v3 = StringVar()
        self.v3.set(" ")
        Radiobutton(self.frame3,text="CULC",variable=self.v3,value="CULC").grid(row=1,column=0)
        Radiobutton(self.frame3,text="Klaus",variable=self.v3,value="Klaus").grid(row=2,column=0)

        self.frame3.grid(row=5,column=2,sticky=E+W)
        self.building = self.v3.get()

        #Floor Buttons
        self.frame4 = Frame(self.homepageWin,relief=SUNKEN,bd=1)
        Label(self.frame4,text="Floor Choices").grid(row=0,column=0)
        self.v4 = IntVar()
        self.v4.set(0)
        Radiobutton(self.frame4,text="1",variable=self.v4,value=1).grid(row=1,column=0)
        Radiobutton(self.frame4,text="2",variable=self.v4,value=2).grid(row=2,column=0)
        Radiobutton(self.frame4,text="3",variable=self.v4,value=3).grid(row=3,column=0)
        Radiobutton(self.frame4,text="4",variable=self.v4,value=4).grid(row=4,column=0)

        self.frame4.grid(row=5,column=3,sticky=E+W)
        self.floor = self.v4.get()

        #Room Buttons
        self.frame5 = Frame(self.homepageWin,relief=SUNKEN,bd=1)
        Label(self.frame5,text="Room Choices").grid(row=0,column=0,columnspan=2)
        self.v5 = IntVar()
        self.v5.set(0)
        Radiobutton(self.frame5,text="1",variable=self.v5,value=1).grid(row=1,column=0)
        Radiobutton(self.frame5,text="2",variable=self.v5,value=2).grid(row=2,column=0)
        Radiobutton(self.frame5,text="3",variable=self.v5,value=3).grid(row=3,column=0)
        Radiobutton(self.frame5,text="4",variable=self.v5,value=4).grid(row=4,column=0)
        Radiobutton(self.frame5,text="5",variable=self.v5,value=5).grid(row=5,column=0)
        Radiobutton(self.frame5,text="6",variable=self.v5,value=6).grid(row=1,column=1)
        Radiobutton(self.frame5,text="7",variable=self.v5,value=7).grid(row=2,column=1)
        Radiobutton(self.frame5,text="8",variable=self.v5,value=8).grid(row=3,column=1)
        Radiobutton(self.frame5,text="9",variable=self.v5,value=9).grid(row=4,column=1)
        Radiobutton(self.frame5,text="10",variable=self.v5,value=10).grid(row=5,column=1)


        self.frame5.grid(row=5,column=4,sticky=E+W)
        self.room = self.v5.get()

        Button(self.homepageWin,text="Cancel All Reservations",command=self.cancelReservation).grid(row=6,column=0,sticky=E+W)
        Button(self.homepageWin,text="Check Available Options",command=self.availableReservations).grid(row=6,column=1,columnspan=2,sticky=E+W)
        Button(self.homepageWin,text="Stats",command=self.stats).grid(row=6,column=3,sticky=E+W)
        Button(self.homepageWin,text="Logout",command=self.logout).grid(row=6,column=4,sticky=E+W)


    # Cancels the Selected Reservation and removes it from the RoomReservations Table
    def cancelReservation(self):
        db = self.Connect()
        c = db.cursor()
        c.execute("""SELECT NumberOfReservations FROM ReservationUser WHERE Username='"""+self.usernameLogin.get()+"""'""")
        numRes = c.fetchall()[0][0]
        if numRes == 0:
            messagebox.showwarning("Error","You do not have any current reservations to cancel!")
            return None
        else:
            c.execute("""DELETE FROM RoomReservations WHERE ReservedBy='"""+self.usernameLogin.get()+"""'""")
            c.execute("""UPDATE ReservationUser SET NumberOfReservations=0 WHERE Username='"""+self.usernameLogin.get()+"""'""")
            messagebox.showinfo("Cancellation Completion","Congrats! You have cancelled your previous reservation(s).")
            self.homepageWin.withdraw()
            self.Homepage()

    # Fetches and Displays Available Reservations from the Database
    def availableReservations(self):
        self.day = self.v1.get()
        self.time = self.v2.get()
        self.building = self.v3.get()
        self.floor = self.v4.get()
        self.room = self.v5.get()
        if self.day == " " or self.time == " " or self.building == " " or self.floor == 0 or self.room == 0:
            messagebox.showwarning("Search Failure","Please choose a valid option from each category")
            return None

        db = self.Connect()
        c = db.cursor()

        if c.execute("""SELECT * FROM RoomReservations WHERE ReservedBy='"""+self.usernameLogin.get()+"""'""") >= 2:
            messagebox.showwarning("Error","You can only make 2 reservations per week. Try again next week.")
            return None

        if self.time == "Morning":
            a = c.execute("""SELECT * FROM RoomReservations WHERE Building='"""+self.building+"""' AND Floor="""+str(self.floor)+""" AND RoomNo="""+str(self.room)+""" AND Day='"""+self.day+"""' AND Time IN ('08:00','09:00','10:00','11:00')""")
            roomsReserved = c.fetchall()
            if a == 4:
                messagebox.showwarning("Search Failure","Sorry! But this room is unavailable for the selected day and time.")
                return None
            else:
                timesAvailable = ["08:00","09:00","10:00","11:00"]
                for i in range(len(roomsReserved)):
                    if roomsReserved[i][4] in timesAvailable:
                        del timesAvailable[timesAvailable.index(roomsReserved[i][4])]

                self.homepageWin.withdraw()

                self.reservationWin = Toplevel()
                self.reservationWin.title("Available Rooms")
                Label(self.reservationWin,text="Building",relief=RAISED).grid(row=0,column=0,sticky=E+W)
                Label(self.reservationWin,text="Floor",relief=RAISED).grid(row=0,column=1,sticky=E+W)
                Label(self.reservationWin,text="Room",relief=RAISED).grid(row=0,column=2,sticky=E+W)
                Label(self.reservationWin,text="Day",relief=RAISED).grid(row=0,column=3,sticky=E+W)
                Label(self.reservationWin,text="Time",relief=RAISED).grid(row=0,column=4,sticky=E+W)
                Label(self.reservationWin,text="Select",relief=RAISED).grid(row=0,column=5,sticky=E+W)

                self.selectvar = StringVar()
                self.selectvar.set(" ")
                for i in range(len(timesAvailable)):
                    Label(self.reservationWin,text=self.building).grid(row=i+1,column=0)
                    Label(self.reservationWin,text=str(self.floor)).grid(row=i+1,column=1)
                    Label(self.reservationWin,text=str(self.room)).grid(row=i+1,column=2)
                    Label(self.reservationWin,text=self.day).grid(row=i+1,column=3)
                    Label(self.reservationWin,text=timesAvailable[i]).grid(row=i+1,column=4)
                    Radiobutton(self.reservationWin,variable=self.selectvar,value=timesAvailable[i]).grid(row=i+1,column=5)

                Button(self.reservationWin,text="Submit Reservation",command=self.makeReservation).grid(row=6,column=3,columnspan=2,sticky=E+W)
                Button(self.reservationWin,text="Cancel",command=self.returnToHomepage).grid(row=6,column=5,sticky=E+W)

        elif self.time == "Afternoon":
            a = c.execute("""SELECT * FROM RoomReservations WHERE Building='"""+self.building+"""' AND Floor="""+str(self.floor)+""" AND RoomNo="""+str(self.room)+" AND Day='"""+self.day+"""' AND Time IN ('12:00','13:00','14:00','15:00')""")
            roomsReserved = c.fetchall()
            if a == 4:
                messagebox.showwarning("Search Failure","Sorry! But this room is unavailable for the selected day and time.")
                return None
            else:
                timesAvailable = ["12:00","13:00","14:00","15:00"]
                for i in range(len(roomsReserved)):
                    if roomsReserved[i][4] in timesAvailable:
                        del timesAvailable[timesAvailable.index(roomsReserved[i][4])]
                print(timesAvailable)

                self.homepageWin.withdraw()

                self.reservationWin = Toplevel()
                self.reservationWin.title("Available Rooms")
                Label(self.reservationWin,text="Building",relief=RAISED).grid(row=0,column=0,sticky=E+W)
                Label(self.reservationWin,text="Floor",relief=RAISED).grid(row=0,column=1,sticky=E+W)
                Label(self.reservationWin,text="Room",relief=RAISED).grid(row=0,column=2,sticky=E+W)
                Label(self.reservationWin,text="Day",relief=RAISED).grid(row=0,column=3,sticky=E+W)
                Label(self.reservationWin,text="Time",relief=RAISED).grid(row=0,column=4,sticky=E+W)
                Label(self.reservationWin,text="Select",relief=RAISED).grid(row=0,column=5,sticky=E+W)

                self.selectvar = StringVar()
                self.selectvar.set(" ")

                for i in range(len(timesAvailable)):
                    Label(self.reservationWin,text=self.building).grid(row=i+1,column=0)
                    Label(self.reservationWin,text=str(self.floor)).grid(row=i+1,column=1)
                    Label(self.reservationWin,text=str(self.room)).grid(row=i+1,column=2)
                    Label(self.reservationWin,text=self.day).grid(row=i+1,column=3)
                    Label(self.reservationWin,text=timesAvailable[i]).grid(row=i+1,column=4)
                    Radiobutton(self.reservationWin,variable=self.selectvar,value=timesAvailable[i]).grid(row=i+1,column=5)

                Button(self.reservationWin,text="Submit Reservation",command=self.makeReservation).grid(row=6,column=3,columnspan=2,sticky=E+W)
                Button(self.reservationWin,text="Cancel",command=self.returnToHomepage).grid(row=6,column=5,sticky=E+W)

        if self.time == "Evening":
            a = c.execute("""SELECT * FROM RoomReservations WHERE Building='"""+self.building+"""' AND Floor="""+str(self.floor)+""" AND RoomNo="""+str(self.room)+" AND Day='"""+self.day+"""' AND Time IN ('16:00','17:00','18:00','19:00')""")
            roomsReserved = c.fetchall()
            if a == 4:
                messagebox.showwarning("Search Failure","Sorry! But this room is unavailable for the selected day and time.")
                return None
            else:
                timesAvailable = ["16:00","17:00","18:00","19:00"]
                for i in range(len(roomsReserved)):
                    if roomsReserved[i][4] in timesAvailable:
                        del timesAvailable[timesAvailable.index(roomsReserved[i][4])]
                print(timesAvailable)

                self.homepageWin.withdraw()

                self.reservationWin = Toplevel()
                self.reservationWin.title("Available Rooms")
                Label(self.reservationWin,text="Building",relief=RAISED).grid(row=0,column=0,sticky=E+W)
                Label(self.reservationWin,text="Floor",relief=RAISED).grid(row=0,column=1,sticky=E+W)
                Label(self.reservationWin,text="Room",relief=RAISED).grid(row=0,column=2,sticky=E+W)
                Label(self.reservationWin,text="Day",relief=RAISED).grid(row=0,column=3,sticky=E+W)
                Label(self.reservationWin,text="Time",relief=RAISED).grid(row=0,column=4,sticky=E+W)
                Label(self.reservationWin,text="Select",relief=RAISED).grid(row=0,column=5,sticky=E+W)

                self.selectvar = StringVar()
                self.selectvar.set(" ")
                for i in range(len(timesAvailable)):
                    Label(self.reservationWin,text=self.building).grid(row=i+1,column=0)
                    Label(self.reservationWin,text=str(self.floor)).grid(row=i+1,column=1)
                    Label(self.reservationWin,text=str(self.room)).grid(row=i+1,column=2)
                    Label(self.reservationWin,text=self.day).grid(row=i+1,column=3)
                    Label(self.reservationWin,text=timesAvailable[i]).grid(row=i+1,column=4)
                    Radiobutton(self.reservationWin,variable=self.selectvar,value=timesAvailable[i]).grid(row=i+1,column=5)

                Button(self.reservationWin,text="Submit Reservation",command=self.makeReservation).grid(row=6,column=3,columnspan=2,sticky=E+W)
                Button(self.reservationWin,text="Cancel",command=self.returnToHomepage).grid(row=6,column=5,sticky=E+W)

        elif self.time == "Night":
            a = c.execute("""SELECT * FROM RoomReservations WHERE Building='"""+self.building+"""' AND Floor="""+str(self.floor)+""" AND RoomNo="""+str(self.room)+" AND Day='"""+self.day+"""' AND Time IN ('20:00','21:00','22:00','23:00')""")
            roomsReserved = c.fetchall()
            if a == 4:
                messagebox.showwarning("Search Failure","Sorry! But this room is unavailable for the selected day and time.")
                return None
            else:
                timesAvailable = ["20:00","21:00","22:00","23:00"]
                for i in range(len(roomsReserved)):
                    if roomsReserved[i][4] in timesAvailable:
                        del timesAvailable[timesAvailable.index(roomsReserved[i][4])]
                print(timesAvailable)

                self.homepageWin.withdraw()

                self.reservationWin = Toplevel()
                self.reservationWin.title("Available Rooms")
                Label(self.reservationWin,text="Building",relief=RAISED).grid(row=0,column=0,sticky=E+W)
                Label(self.reservationWin,text="Floor",relief=RAISED).grid(row=0,column=1,sticky=E+W)
                Label(self.reservationWin,text="Room",relief=RAISED).grid(row=0,column=2,sticky=E+W)
                Label(self.reservationWin,text="Day",relief=RAISED).grid(row=0,column=3,sticky=E+W)
                Label(self.reservationWin,text="Time",relief=RAISED).grid(row=0,column=4,sticky=E+W)
                Label(self.reservationWin,text="Select",relief=RAISED).grid(row=0,column=5,sticky=E+W)

                self.selectvar = StringVar()
                self.selectvar.set(" ")
                for i in range(len(timesAvailable)):
                    Label(self.reservationWin,text=self.building).grid(row=i+1,column=0)
                    Label(self.reservationWin,text=str(self.floor)).grid(row=i+1,column=1)
                    Label(self.reservationWin,text=str(self.room)).grid(row=i+1,column=2)
                    Label(self.reservationWin,text=self.day).grid(row=i+1,column=3)
                    Label(self.reservationWin,text=timesAvailable[i]).grid(row=i+1,column=4)
                    Radiobutton(self.reservationWin,variable=self.selectvar,value=timesAvailable[i]).grid(row=i+1,column=5)

                Button(self.reservationWin,text="Submit Reservation",command=self.makeReservation).grid(row=6,column=3,columnspan=2,sticky=E+W)
                Button(self.reservationWin,text="Cancel",command=self.returnToHomepage).grid(row=6,column=5,sticky=E+W)


    # Creates Selected Reservations for the User and Inserts Into the RoomReservations Table
    def makeReservation(self):
        if self.selectvar.get() == " ":
            messagebox.showwarning("Error","Please select a time slot to reserve or press 'Cancel'")
            return None
        self.realtime = self.selectvar.get()
        db = self.Connect()
        c = db.cursor()
        c.execute("""INSERT INTO RoomReservations (Building,Floor,RoomNo,Day,Time,ReservedBy) VALUES ('"""+self.building+"""',"""+str(self.floor)+""","""+str(self.room)+""",'"""+self.day+"""','"""+self.realtime+"""','"""+self.usernameLogin.get()+"""')""")

        numReservations = c.execute("""SELECT * FROM RoomReservations WHERE ReservedBy='"""+self.usernameLogin.get()+"""'""")

        c.execute("""UPDATE ReservationUser SET NumberOfReservations="""+str(numReservations)+""" WHERE Username='"""+self.usernameLogin.get()+"""'""")

        c.close()
        db.commit()

        messagebox.showinfo("Reservation Completion","Congrats! You have reserved your room. Click OK to go back to Homepage.")
        self.reservationWin.withdraw()
        self.Homepage()


    # Returns the user to the Home Page
    def returnToHomepage(self):
        self.reservationWin.withdraw()
        self.homepageWin.deiconify()

    # Calculates and Displays Reservation Statistics 
    def stats(self):
        db = self.Connect()
        c = db.cursor()
        numTotalRes = c.execute("""SELECT * FROM RoomReservations""")
        numTotalPpl = c.execute("""SELECT * FROM ReservationUser""")
        avg = numTotalRes/numTotalPpl

        numCulc = c.execute("""SELECT * FROM RoomReservations WHERE Building='CULC'""")
        numKlaus = c.execute("""SELECT * FROM RoomReservations WHERE Building='Klaus'""")

        if numCulc>numKlaus:
            statement = "CULC is more busy with "+str(numCulc)+" reservations so far."
        elif numKlaus>numCulc:
            statement = "Klaus is more busy with "+str(numKlaus)+" reservations so far."
        elif numCulc == numKlaus:
            statement = "Both are busy with "+str(numCulc)+" reservations so far."

        self.homepageWin.withdraw()
        self.statsWin = Toplevel()
        self.statsWin.title("Statistics")
        Label(self.statsWin, text="The average number of reservations per person is:").grid(row=0,column=0)
        a = StringVar()
        a.set(str(avg))
        Entry(self.statsWin, textvariable=a, state="readonly",width=50).grid(row=0,column=1)
        Label(self.statsWin, text="The busiest building:").grid(row=1,column=0,sticky=E)
        b = StringVar()
        b.set(statement)
        Entry(self.statsWin, textvariable=b, state="readonly",width=50).grid(row=1,column=1)
        Button(self.statsWin, text="Back",width=25,command=self.backclicked).grid(row=2,column=1,sticky=E)


    def logout(self):
        self.homepageWin.withdraw()
        self.rootWin.deiconify()

    # Action when back button is clicked
    def backclicked(self):
        self.statsWin.withdraw()
        self.Homepage()

    # Checks to Ensure That User Login Credentials are Authenticated
    def LoginCheck(self):
        self.userCheck = self.usernameLogin.get()
        self.passCheck = self.passwordLogin.get()

        db = self.Connect()
        c = db.cursor()
        if c.execute("""SELECT * FROM ReservationUser WHERE Username='"""+self.userCheck+"""' AND Password = '"""+self.passCheck+"""'""") == 0:
            messagebox.showwarning("Warning","Sorry, invalid Username/Password combination!")
        else:
            messagebox.showwarning("Congrats","You logged in succesfully!")
            self.rootWin.withdraw()
            self.Homepage()








GUI()

