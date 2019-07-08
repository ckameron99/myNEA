import sqlite3
class User:
    def __init__(self,id):
        self.id=id
        db=sqlite3.connect("user.db")
        stmt=f"SELECT * FROM User WHERE UserID={self.id}"
        results=db.execute(stmt)
        db.close()
        if len(results)==0:
            self.create()
        else:
            user=results[0]
            self.load(user)

    def load(self,user):
        self.forname=user[1]
        self.surname=user[2]
        self.DOB=user[3]
        self.Kudos=user[4]

    def create(self):
        db=sqlite3.connect("user.db")
        self.forname=input("please enter your forname: ")
        self.surname=input("please enter your surname: ")
        self.DOB=input("please enter your DOB: ")
        self.Kudos=0
        stmt='''INSERT INTO User (UserID,Forname,Surname,DOB,Kudos) VALUES ({self.id},{self.forname},{self.surname},{self.DOB},{self.Kudos})
        db.close()

    def save(self,id):
        db=sqlite3.connect("user.db")
        stmt="UPDATE User set Forname = {self.forname} WHERE UserID={self.id}"
        db.execute(stmt)
        stmt="UPDATE User set Surname = {self.forname} WHERE UserID={self.surname}"
        db.execute(stmt)
        stmt="UPDATE User set DOB = {self.forname} WHERE UserID={self.DOB}"
        db.execute(stmt)
        stmt="UPDATE User set Kudos = {self.forname} WHERE UserID={self.Kudos}"
        db.execute(stmt)
